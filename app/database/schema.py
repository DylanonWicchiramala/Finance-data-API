companyInfo = """companyInfo(
  cik INT(10) NOT NULL,
  ticker STRING PRIMARY KEY NOT NULL,
  name STRING,
  entity_type STRING,
  sic INT,
  industry STRING,
  exchanges STRING,
  description STRING,
  website STRING,
  category STRING,
  investor_website STRING,
  fiscal_year_end STRING,
  state_of_incorporation STRING
  ) 
"""

latestFormUpdate="""latestFormUpdate(
  cik INT(10) PRIMARY KEY NOT NULL,
  timestamp FLOAT
)"""

submissionForm = """submissionForm(
  accession_number INT(15) PRIMARY KEY NOT NULL,
  cik INT(10),
  filing_date DATE,
  report_date DATE,
  acceptance_date_time DATETIME,
  index_url STRING,
  primary_docment_url STRING,
  act STRING,
  form STRING,
  file_number STRING,
  film_number STRING,
  items INT,
  size INT,
  is_xbrl INT,
  is_inline_xbrl INT,
  primary_docment STRING,
  primary_doc_description STRING
)"""

# # from CONDENSED CONSOLIDATED STATEMENTS OF INCOME R2.htm
# financialStatement = """financialStatement(
#   accession_number INT(15) PRIMARY KEY NOT NULL,
#   revenue float,
#   gross_profit float,
#   operating_income float,
#   net_income float,
#   cost_of_revenue float,
#   operating_expenses float,
#   non_operating_income float,
#   shares_outstanding INT,
#   shares_outstanding_diluted INT,
#   money_scale STRING,
#   shares_outstanding_scale STRING
# )"""

# # from CONDENSED CONSOLIDATED BALANCE SHEETS R4.htm or R5.htm
# balanceSheets ="""balanceSheets(
#   accession_number INT(15) PRIMARY KEY NOT NULL,
#   total_assets float,
#   total_liabilities float,
#   shareholder_equity float,
#   cash_and_cash_equivalents float,
#   money_scale STRING
# )"""

# # from CONDENSED CONSOLIDATED STATEMENTS OF CASH FLOWS R7.htm
# cashFlows = """cashFlows(
#   accession_number INT(15) PRIMARY KEY NOT NULL,
#   cash_from_operating_activities float,
#   cash_from_financing_activities float,
#   cash_from_investing_activities float,
#   free_cash_flow float,
#   money_scale numberScale
# )"""

# # from CONDENSED CONSOLIDATED STATEMENTS OF INCOME R2.htm
# financialRatio = """financialRatio(
#   accession_number INT(15) PRIMARY KEY NOT NULL,
#   earnings_per_share float,
#   earnings_per_share_diluted float,
#   sales_per_share float,
#   sales_per_share_diluted float,
#   price_to_earnings float,
#   price_to_sales float,
#   return_on_assets float,
#   return_on_equity float,
#   gross_margin float,
#   operating_margin float,
#   net_margin float
# )"""