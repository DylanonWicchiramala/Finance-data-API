from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType


company_info = StructType([
    StructField("cik", IntegerType(), nullable=False),
    StructField("cik_str", StringType(), nullable=False),
    StructField("ticker", StringType(), nullable=False),
    StructField("name", StringType()),
    StructField("sector", StringType()),
    StructField("industry", StringType())
])

# financial_statement_schema = StructType([
#     StructField("accession_number", IntegerType(), nullable=False),
#     StructField("ticker", StringType(), nullable=False),
#     StructField("revenue", FloatType()),
#     StructField("gross_profit", FloatType()),
#     StructField("operating_income", FloatType()),
#     StructField("net_income", FloatType()),
#     StructField("cost_of_revenue", FloatType()),
#     StructField("operating_expenses", FloatType()),
#     StructField("non_operating_expenses", FloatType()),
#     StructField("shares_outstanding", IntegerType()),
#     StructField("shares_outstanding_diluted", IntegerType()),
#     StructField("money_scale", StringType()),  # Assuming NumberScale is defined as StringType
#     StructField("shares_outstanding_scale", StringType())  # Assuming NumberScale is defined as StringType
# ])
