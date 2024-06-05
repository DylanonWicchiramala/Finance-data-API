from sqlalchemy import Column, String, Integer, Float, ForeignKey, Enum, Date
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship
from database import Base
import enum

# class User(Base):
#     __tablename__ = 'users'
    
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(100), unique=True)

# class Post(Base):
#     __tablename__ = 'posts'
    
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(50))
#     content = Column(String(500))
#     user_id = Column(Integer)
    
# Enums
class NumberScale(enum.Enum):
    million = 'million'
    billion = 'billion'
    trillion = 'trillion'

class Currency(enum.Enum):
    usd = 'usd'
    thb = 'thb'
    
class FormType(enum.Enum):
    _10q = '10-Q'
    _10k = '10-K'
    

# Tables
class CompanyInfo(Base):
    __tablename__ = 'company_info'

    cik = Column(Integer, primary_key=True)
    cik_str = Column(String(10), primary_key=True)
    ticker = Column(String(10), primary_key=True, unique=True, nullable=False)
    name = Column(String(100))
    sector = Column(String(100))
    industry = Column(String(100))
    currency = Column(Enum(Currency))

class SubmissionForm(Base):
    __tablename__ = 'submission_form'

    accession_number = Column(Integer, primary_key=True, unique=True)
    cik = Column(Integer)#, ForeignKey('company_info.cik'))
    ticker = Column(String(10))#, ForeignKey('company_info.ticker'))
    report_quarter = Column(String(6))
    report_date = Column(Date)
    filing_date = Column(Date)
    form_type = Column(Enum(FormType))
    raw_doc_id = Column(Integer)

class RawDocument(Base):
    __tablename__ = 'raw_document'
    
    accession_number = Column(Integer, ForeignKey('submission_form.accession_number'), primary_key=True)
    page_number = Column(Integer, primary_key=True)
    document = Column(LONGTEXT)

class FinancialStatement(Base):
    __tablename__ = 'financial_statement'

    accession_number = Column(Integer, ForeignKey('submission_form.accession_number'), primary_key=True)
    ticker = Column(String(10), ForeignKey('company_info.ticker'))

    revenue = Column(Float)
    gross_profit = Column(Float)
    operating_income = Column(Float)
    net_income = Column(Float)
    cost_of_revenue = Column(Float)
    operating_expenses = Column(Float)
    non_operating_expenses = Column(Float)

    shares_outstanding = Column(Integer)
    shares_outstanding_diluted = Column(Integer)
    money_scale = Column(Enum(NumberScale))
    shares_outstanding_scale = Column(Enum(NumberScale))

class BalanceSheets(Base):
    __tablename__ = 'balance_sheets'

    accession_number = Column(Integer, ForeignKey('submission_form.accession_number'), primary_key=True)
    ticker = Column(String(10), ForeignKey('company_info.ticker'))

    total_assets = Column(Float)
    total_liabilities = Column(Float)
    shareholder_equity = Column(Float)
    cash_and_cash_equivalents = Column(Float)
    money_scale = Column(Enum(NumberScale))

class CashFlows(Base):
    __tablename__ = 'cash_flows'

    accession_number = Column(Integer, ForeignKey('submission_form.accession_number'), primary_key=True)
    ticker = Column(String(10), ForeignKey('company_info.ticker'))

    cash_from_operating_activities = Column(Float)
    cash_from_financing_activities = Column(Float)
    cash_from_investing_activities = Column(Float)
    free_cash_flow = Column(Float)
    money_scale = Column(Enum(NumberScale))

class FinancialRatio(Base):
    __tablename__ = 'financial_ratio'

    accession_number = Column(Integer, ForeignKey('submission_form.accession_number'), primary_key=True)
    ticker = Column(String(10), ForeignKey('company_info.ticker'))

    EPS = Column(Float)
    EPS_diluted = Column(Float)
    sales_per_share = Column(Float)
    sales_per_share_diluted = Column(Float)
    ROA = Column(Float)
    ROE = Column(Float)
    gross_margin = Column(Float)
    operating_margin = Column(Float)
    net_margin = Column(Float)