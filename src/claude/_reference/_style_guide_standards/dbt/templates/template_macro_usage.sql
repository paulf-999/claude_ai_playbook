-- Surrogate key
{{ create_surrogate_key(['MERCHANT_ID', 'SOURCE_SYSTEM']) }} AS "KEY"

-- Numeric cleaning
{{ clean_and_cast_numeric('M."Gross Volume"', precision=38, scale=4, default_value=0) }} AS gross_volume

-- Row limiting (append to every major CTE and final SELECT)
SELECT *
FROM FINAL
{{ limit_rows() }}
