{% snapshot dim_merchant_history %}
    {{
        config(
          target_schema='WAREHOUSE',
          strategy='check',
          unique_key='KEY',
          check_cols=['SOURCE_SYSTEM_ID', 'MID', 'DBA_NAME', ...]
        )
    }}

    SELECT *
    FROM {{ ref('dim_merchant') }}
    {{ limit_rows() }}

{% endsnapshot %}
