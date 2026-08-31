"""Behavioural tests for the build_staging_base_models skill rules.

Tests the deterministic, rule-based components Claude must follow when executing
the skill. Each test group corresponds to a specific rule defined in SKILL.md,
phase_inputs.md, or phase_build.md.

Rule areas covered:
- source_folder derivation (schema name → folder name)
- macro type detection (macro call pattern → macro_type label)
- table alias derivation (table name → table_lower alias)
- column classification (Airbyte metadata / CDC metadata / business columns)
- standard column rename map
- file naming conventions (staging and base)
"""

import pytest

# ─── source_folder derivation ──────────────────────────────────────────────────
# phase_inputs.md Step 2: strip trailing _SOURCE_CDC or _SOURCE suffix, lowercase.


def derive_source_folder(schema_name: str) -> str:
    """Derive the source_folder from a Snowflake schema name.

    Rules (phase_inputs.md Step 2):
    - Strip trailing ``_SOURCE_CDC`` suffix first, then ``_SOURCE``.
    - Lowercase the result.

    :param schema_name: Snowflake schema name in UPPER_CASE.
    :type schema_name: str
    :return: Source folder name in lowercase.
    :rtype: str
    """
    name = schema_name
    if name.endswith("_SOURCE_CDC"):
        name = name[: -len("_SOURCE_CDC")]
    elif name.endswith("_SOURCE"):
        name = name[: -len("_SOURCE")]
    return name.lower()


@pytest.mark.parametrize("schema_name,expected", [
    ("SALESFORCE_SOURCE", "salesforce"),
    ("RMS_SOURCE_CDC", "rms"),
    ("AMS_SOURCE", "ams"),
    ("NETSUITE_SOURCE", "netsuite"),
    ("HUBSPOT_SOURCE_CDC", "hubspot"),
    ("MYSCHEMA", "myschema"),                     # no suffix — lowercase as-is
    ("MULTI_WORD_SOURCE_CDC", "multi_word"),
])
def test_derive_source_folder(schema_name: str, expected: str) -> None:
    """source_folder must be derived by stripping the correct suffix and lowercasing.

    :param schema_name: Input schema name.
    :type schema_name: str
    :param expected: Expected source_folder value.
    :type expected: str
    """
    assert derive_source_folder(schema_name) == expected


# ─── macro type detection ──────────────────────────────────────────────────────
# phase_inputs.md Step 2: match macro call in existing .sql files to macro_type.

MACRO_TYPE_MAP: dict[str, str] = {
    "incremental_airbyte_merge_pk_join_hash": "incremental-hash",
    "incremental_airbyte_cdc_merge_pk_join": "cdc",
    "full_load_airbyte_merge": "full-load",
    "incremental_airbyte_cdc_dynamic": "dynamic-cdc",
    "dynamic_airbyte_merge_non_cdc": "dynamic-non-cdc",
    "incremental_airbyte_merge_pk_join": "incremental",
}


def detect_macro_type(sql_content: str) -> str | None:
    """Detect the macro_type from the macro call found in a staging SQL file.

    :param sql_content: Content of an existing staging .sql file.
    :type sql_content: str
    :return: macro_type string, or None if no known macro call is found.
    :rtype: str | None
    """
    for macro_call, macro_type in MACRO_TYPE_MAP.items():
        if macro_call in sql_content:
            return macro_type
    return None


@pytest.mark.parametrize("macro_call,expected_type", [
    ("incremental_airbyte_merge_pk_join_hash", "incremental-hash"),
    ("incremental_airbyte_cdc_merge_pk_join", "cdc"),
    ("full_load_airbyte_merge", "full-load"),
    ("incremental_airbyte_cdc_dynamic", "dynamic-cdc"),
    ("dynamic_airbyte_merge_non_cdc", "dynamic-non-cdc"),
    ("incremental_airbyte_merge_pk_join", "incremental"),
])
def test_macro_type_detection(macro_call: str, expected_type: str) -> None:
    """detect_macro_type must map each known macro call to the correct macro_type label.

    :param macro_call: Macro function name found in SQL content.
    :type macro_call: str
    :param expected_type: Expected macro_type label.
    :type expected_type: str
    """
    sql = f"{{{{ {macro_call}(arg1, arg2) }}}}"
    assert detect_macro_type(sql) == expected_type


def test_macro_type_detection_unknown_returns_none() -> None:
    """detect_macro_type must return None when no known macro call is present."""
    assert detect_macro_type("SELECT 1") is None


def test_incremental_hash_takes_priority_over_incremental() -> None:
    """incremental_airbyte_merge_pk_join_hash must not be misidentified as incremental.

    The longer macro name contains the shorter one as a substring, so order of
    matching matters.
    """
    sql = "{{ incremental_airbyte_merge_pk_join_hash(arg) }}"
    assert detect_macro_type(sql) == "incremental-hash"


# ─── table alias derivation ───────────────────────────────────────────────────
# phase_build.md Step 4: lowercase table name, strip SF_ prefix for Salesforce.


def derive_table_lower(table_name: str) -> str:
    """Derive the table_lower alias from an UPPER_CASE table name.

    Rules (phase_build.md Step 4):
    - Lowercase the table name.
    - Strip a leading ``SF_`` prefix if present (Salesforce convention).

    :param table_name: Source table name in UPPER_CASE.
    :type table_name: str
    :return: Lowercased alias with SF_ prefix removed where applicable.
    :rtype: str
    """
    lower = table_name.lower()
    if lower.startswith("sf_"):
        lower = lower[3:]
    return lower


@pytest.mark.parametrize("table_name,expected", [
    ("SF_INTEGRATION_CONTACT__C", "integration_contact__c"),
    ("SF_ACCOUNT", "account"),
    ("OPPORTUNITY", "opportunity"),
    ("RMS_ORDER_HEADER", "rms_order_header"),
    ("SF_LEAD__C", "lead__c"),
    ("TRANSACTION", "transaction"),
])
def test_derive_table_lower(table_name: str, expected: str) -> None:
    """table_lower must be derived by lowercasing and stripping the SF_ prefix.

    :param table_name: Input table name in UPPER_CASE.
    :type table_name: str
    :param expected: Expected table_lower alias.
    :type expected: str
    """
    assert derive_table_lower(table_name) == expected


# ─── column classification ────────────────────────────────────────────────────
# phase_build.md Step 3: classify columns into three groups.

AIRBYTE_METADATA_COLS: frozenset[str] = frozenset({
    "_AIRBYTE_RAW_ID",
    "_AIRBYTE_EXTRACTED_AT",
    "_AIRBYTE_META",
})


def classify_column(col: str) -> str:
    """Classify a column name into one of three groups.

    Rules (phase_build.md Step 3):
    - ``airbyte_metadata`` — ``_AIRBYTE_RAW_ID``, ``_AIRBYTE_EXTRACTED_AT``, ``_AIRBYTE_META``
    - ``cdc_metadata`` — any column starting with ``_AB_CDC_``
    - ``business`` — everything else

    :param col: Column name in UPPER_CASE.
    :type col: str
    :return: One of ``'airbyte_metadata'``, ``'cdc_metadata'``, or ``'business'``.
    :rtype: str
    """
    if col in AIRBYTE_METADATA_COLS:
        return "airbyte_metadata"
    if col.startswith("_AB_CDC_"):
        return "cdc_metadata"
    return "business"


@pytest.mark.parametrize("col,expected_class", [
    ("_AIRBYTE_RAW_ID", "airbyte_metadata"),
    ("_AIRBYTE_EXTRACTED_AT", "airbyte_metadata"),
    ("_AIRBYTE_META", "airbyte_metadata"),
    ("_AB_CDC_UPDATED_AT", "cdc_metadata"),
    ("_AB_CDC_DELETED_AT", "cdc_metadata"),
    ("_AB_CDC_LOG_FILE", "cdc_metadata"),
    ("ID", "business"),
    ("ISDELETED", "business"),
    ("CREATEDDATE", "business"),
    ("AMOUNT", "business"),
    ("_AIRBYTE_RAW_ID_EXTRA", "business"),  # not in the exact set
])
def test_column_classification(col: str, expected_class: str) -> None:
    """Each column must be classified into the correct group.

    :param col: Column name.
    :type col: str
    :param expected_class: Expected classification string.
    :type expected_class: str
    """
    assert classify_column(col) == expected_class


# ─── standard column rename map ───────────────────────────────────────────────
# phase_build.md Step 5: apply standard renames in the base model.

COLUMN_RENAME_MAP: dict[str, str] = {
    "OWNERID": "OWNER_ID",
    "ISDELETED": "IS_DELETED",
    "CREATEDDATE": "CREATED_DATE",
    "CREATEDBYID": "CREATED_BY_ID",
    "SYSTEMMODSTAMP": "SYSTEM_MOD_STAMP",
    "LASTACTIVITYDATE": "LAST_ACTIVITY_DATE",
    "LASTMODIFIEDBYID": "LAST_MODIFIED_BY_ID",
    "LASTMODIFIEDDATE": "LAST_MODIFIED_DATE",
    "LASTVIEWEDDATE": "LAST_VIEWED_DATE",
    "LASTREFERENCEDDATE": "LAST_REFERENCED_DATE",
}


def apply_rename(col: str) -> str:
    """Return the renamed column if a standard rename exists, else the column as-is.

    :param col: Column name in UPPER_CASE.
    :type col: str
    :return: Renamed column, or the original if no rename is defined.
    :rtype: str
    """
    return COLUMN_RENAME_MAP.get(col, col)


@pytest.mark.parametrize("source_col,expected_renamed", [
    ("OWNERID", "OWNER_ID"),
    ("ISDELETED", "IS_DELETED"),
    ("CREATEDDATE", "CREATED_DATE"),
    ("CREATEDBYID", "CREATED_BY_ID"),
    ("SYSTEMMODSTAMP", "SYSTEM_MOD_STAMP"),
    ("LASTACTIVITYDATE", "LAST_ACTIVITY_DATE"),
    ("LASTMODIFIEDBYID", "LAST_MODIFIED_BY_ID"),
    ("LASTMODIFIEDDATE", "LAST_MODIFIED_DATE"),
    ("LASTVIEWEDDATE", "LAST_VIEWED_DATE"),
    ("LASTREFERENCEDDATE", "LAST_REFERENCED_DATE"),
])
def test_standard_renames_applied(source_col: str, expected_renamed: str) -> None:
    """All ten standard column renames must map to the correct output name.

    :param source_col: Source column name.
    :type source_col: str
    :param expected_renamed: Expected output name after rename.
    :type expected_renamed: str
    """
    assert apply_rename(source_col) == expected_renamed


@pytest.mark.parametrize("col", [
    "ID",
    "AMOUNT",
    "NAME",
    "CURRENCY_ISO_CODE",
    "STAGE_NAME",
])
def test_non_renamed_columns_pass_through(col: str) -> None:
    """Columns not in the rename map must be output as-is.

    :param col: Column name that has no standard rename.
    :type col: str
    """
    assert apply_rename(col) == col


def test_rename_map_has_exactly_ten_entries() -> None:
    """The standard rename map must contain exactly the ten entries defined in phase_build.md."""
    assert len(COLUMN_RENAME_MAP) == 10


# ─── file naming conventions ──────────────────────────────────────────────────
# phase_build.md Steps 4 and 5: derive file names for staging and base models.


def staging_file_name(source_folder: str, table_lower: str) -> str:
    """Derive the staging model file name.

    Convention (phase_build.md Step 4):
    ``staging_<source_folder>_<table_lower>.sql``

    :param source_folder: Derived source folder name (lowercase).
    :type source_folder: str
    :param table_lower: Derived table alias (lowercase, SF_ stripped).
    :type table_lower: str
    :return: Staging SQL file name.
    :rtype: str
    """
    return f"staging_{source_folder}_{table_lower}.sql"


def base_file_name(source_folder: str, table_lower: str) -> str:
    """Derive the base model file name.

    Convention (phase_build.md Step 5):
    ``<source_folder>_<table_lower>.sql``

    :param source_folder: Derived source folder name (lowercase).
    :type source_folder: str
    :param table_lower: Derived table alias (lowercase, SF_ stripped).
    :type table_lower: str
    :return: Base SQL file name.
    :rtype: str
    """
    return f"{source_folder}_{table_lower}.sql"


@pytest.mark.parametrize("source_folder,table_lower,expected_staging,expected_base", [
    (
        "salesforce",
        "integration_contact__c",
        "staging_salesforce_integration_contact__c.sql",
        "salesforce_integration_contact__c.sql",
    ),
    (
        "rms",
        "rms_order_header",
        "staging_rms_rms_order_header.sql",
        "rms_rms_order_header.sql",
    ),
    (
        "ams",
        "transaction",
        "staging_ams_transaction.sql",
        "ams_transaction.sql",
    ),
])
def test_file_naming_conventions(
    source_folder: str,
    table_lower: str,
    expected_staging: str,
    expected_base: str,
) -> None:
    """Staging and base file names must follow the conventions in phase_build.md.

    :param source_folder: Source folder name.
    :type source_folder: str
    :param table_lower: Table alias.
    :type table_lower: str
    :param expected_staging: Expected staging SQL file name.
    :type expected_staging: str
    :param expected_base: Expected base SQL file name.
    :type expected_base: str
    """
    assert staging_file_name(source_folder, table_lower) == expected_staging
    assert base_file_name(source_folder, table_lower) == expected_base
