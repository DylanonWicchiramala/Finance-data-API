import sys
sys.path.append('.')

sys.path.append('./Database')

from models import CompanyInfo, Base
from get_data import scrape_companies_info
from sqlalchemy import create_engine
from sqlalchemy.orm import load_only
from Database import database

session = database.SessionLocal()

def create_tables(force_recreate=False):
    """
    Function to create the company_info table in the database.
    """
    if force_recreate:
        # Drop all tables
        try:
            Base.metadata.drop_all(database.engine) 
            print("Dropped all tables")
        except:
            pass
        
    # Create the company_info table
    Base.metadata.create_all(database.engine)

    print("tables created successfully")
    

def company_info_update(session, force=False):
    ciks = scrape_companies_info.get_ciks()
    
    if force: session.query(CompanyInfo).delete()
    
    for info in ciks.values():
        # Check if the company already exists in the database
        existing_company = session.query(CompanyInfo).filter_by(cik=int(info['cik'])).first()
        if existing_company:
            # If the company with the same CIK already exists, skip adding it
            continue
        
        # Similarly, check if a company with the same ticker already exists
        existing_company = session.query(CompanyInfo).filter_by(ticker=info['ticker']).first()
        if existing_company:
            # If the company with the same ticker already exists, skip adding it
            continue
        
        # If the company doesn't exist in the database, add it
        company = CompanyInfo(
            cik=int(info['cik']),
            cik_str=info['cik_str'],
            ticker=info['ticker'],
            name=info['name'],
        )
        session.add(company)

    # Commit the session to save the changes
    session.commit()

    # Close the session
    session.close()

    

def company_info_get(session, filter:dict, columns:list=None, get_first:bool=True):
    """
    Search for company info by filter and return the result as a dictionary.
    
    :param:
        session: SQLAlchemy session object
        filter: The filter (in dict) to search for
        columns: List of columns to return (default is all columns)
        get_first: If True, return only first object
    :return: Dictionary containing company info (return list if have many result) if found, otherwise None
    """
    query = session.query(CompanyInfo).filter_by(**filter)
    
    if columns:
        orm_columns = [getattr(CompanyInfo, column) for column in columns]
        query = query.options(load_only(*orm_columns))
        
    companies = query.all()
    
    # Close the session
    session.close()
    
    if len(companies)==1:
        return companies[0].__dict__
    elif companies:
        if get_first:
            return companies[0].__dict__
        return [ company.__dict__ for company in companies ]
    else:
        return None