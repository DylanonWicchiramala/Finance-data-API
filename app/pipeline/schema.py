companyInfo = """companyInfo(
  cik INT(10) NOT NULL,
  cik_str STRING(10) NOT NULL,
  ticker STRING PRIMARY KEY NOT NULL,
  name STRING ,
  secter STRING ,
  industry STRING
)"""

submissionForm = """submissionForm(
  accession_number INT(15) PRIMARY KEY NOT NULL,
  cik INT(10),
  filing_date DATE,
  report_date DATE,
  acceptance_date_time DATETIME,
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

# enum numberScale {
#   million
#   billion
#   trillion
# }

# enum currency{
#   usd
#   thb
# }

# Table financialStatement{
#   accession_number INT(15) [pk]
#   ticker STRING(10)

#   revenue float
#   gross_profit float
#   operating_income float
#   net_income float
#   cost_of_revenue float
#   operating_expenses float
#   non_operating_expenses float

#   shares_outstanding INT
#   shares_outstanding_diluted INT
#   money_scale numberScale
#   shares_outstanding_scale numberScale
# }

# Table balanceSheets{
#   accession_number INT(15) [pk]
#   ticker STRING(10)

#   total_assets float
#   total_liabilities float
#   shareholder_equity float
#   cash_and_cash_equivalents float
#   money_scale numberScale
# }

# Table cashFlows{
#   accession_number INT(15) [pk]
#   ticker STRING(10)

#   cash_from_operating_activities float
#   cash_from_financing_activities float
#   cash_from_investing_activities float
#   free_cash_flow float
#   money_scale numberScale
# }

# Table financialRatio{
#   accession_number INT(15) [pk]
#   ticker STRING(10)

#   EPS float
#   EPS_diluted float
#   sales_per_share float
#   sales_per_share_diluted float
#   ROA float
#   ROE float
#   gross_margin float
#   operating_margin float
#   net_margin float
# }