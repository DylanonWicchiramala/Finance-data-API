import sys
sys.path.append('.')
sys.path.append('./database')
# sys.path.append('./app')

from tqdm import tqdm
import schema
from get_data import scrape_companies_info, scrape_submission_form
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

def __tablefilter(connection, table_name:str, filter:dict, columns:list=None, c="AND"):
    """
    Search data in table  by filter and return the result as sql3 cursor.
    
    :param:
        connection: SQL3 connection object
        table_name: name of table to search
        filter: The filter (in dict) to search for
        columns: List of columns to return (default is all columns)
        c: condition AND, OR
    :return: Dictionary containing company info (return list if have many result) if found, otherwise None
    """
    cursor = connection.cursor()
    
    filter = list(filter.items())
    condition = []
    for q, v in filter:
        if hasattr(v, '__iter__') and not isinstance(v, str):
            condition.append(f"{q} IN {str(tuple(v))}")
        else:
            condition.append("{} = '{}'".format(q, v))
            
    condition = " WHERE " + f" {c} ".join(condition)    

    if columns is None:
        res = cursor.execute(
            f"""
            SELECT *
            FROM {table_name} 
            """ + condition
            )
    else:
        res = cursor.execute(
            f"""
            SELECT {','.join(columns)} 
            FROM {table_name} 
            """ + condition
            )
    return res


def company_info_load(connection, force=False):
    ciks = scrape_companies_info.get_ciks()

    keys = list(ciks[0].keys())
    values = [ list(d.values()) for d in ciks]

    cursor = connection.cursor()

    if force: cursor.execute("DROP TABLE IF EXISTS companyInfo")
    cursor.execute("CREATE TABLE IF NOT EXISTS " + schema.companyInfo)
    cursor.executemany(
        f"""
        INSERT OR REPLACE INTO companyInfo ({",".join(keys)})
        VALUES ({",".join("?"*len(keys))})
        """, 
        values
        )

    logger.info("companyInfo database loaded")
    connection.commit()
    

def company_info_get(connection, filter:dict, columns:list=None, get_first:bool=True):
    """
    Search for company info by filter and return the result as a dictionary.
    
    :param:
        session: SQLAlchemy session object
        filter: The filter (in dict) to search for
        columns: List of columns to return (default is all columns)
        get_first: If True, return only first object
    :return: Dictionary containing company info (return list if have many result) if found, otherwise None
    """
    res = __tablefilter(connection, "companyInfo", filter, columns)
    res = res.fetchone() if get_first else res.fetchall()
    
    if get_first: 
        if res is not None:
            return dict(zip(columns, res))
        else:
            return None

    else: return [ dict(zip(columns, r)) for r in res ]
    

def submissions_form_load(connection, cik:int|str, max_days_old:int=0, commit_database:bool=True):
    # data will not update when the number of the days since data was update less than max_day_old.
    def perform_load(connection, cik:int|str):
        submissions_form = scrape_submission_form.get_submissions_form(cik)
        
        # if not have submission form.
        if len(submissions_form)==0:
            logger.info("No submissions from of CIK{}".format(cik))
            return

        keys = list(submissions_form[0].keys())
        values = [ list(d.values()) for d in submissions_form]

        cursor = connection.cursor()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS " + schema.latestFormUpdate)
        cursor.execute("CREATE TABLE IF NOT EXISTS " + schema.submissionForm)
        cursor.executemany(
            f"""
            INSERT OR REPLACE INTO submissionForm ({",".join(keys)})
            VALUES ({",".join("?"*len(keys))})
            """, 
            values
            )
        cursor.execute(f"""
            INSERT OR REPLACE INTO latestFormUpdate (cik, timestamp)
            VALUES ({cik},{datetime.today().timestamp()})
            """)

        logger.info("Submissions from of CIK{} was loaded into a database.".format(cik))
        if commit_database: connection.commit()
    
    if max_days_old != 0:
        cursor = connection.cursor()
        
        latest_form_update = cursor.execute(f"""
            SELECT timestamp FROM latestFormUpdate 
            WHERE cik={int(cik)}
            """).fetchone()
        
        latest_form_update = latest_form_update[0] if latest_form_update is not None else 0.0

        delta_days = (datetime.today().timestamp() - latest_form_update)/86400

    if delta_days > max_days_old:
        perform_load(connection=connection, cik=cik)
    
    
def submissions_form_load_all(connection, max_days_old:int=0):
    cursor = connection.cursor()
    ciks = cursor.execute("""
    SELECT cik FROM companyInfo
    """).fetchall()
    ciks = [cik[0] for cik in ciks]
    ciks = set(ciks)
    
    for cik in tqdm(ciks, desc="getting submission form."):
        submissions_form_load(connection=connection, cik=cik, max_days_old=max_days_old, commit_database=False)
        
    connection.commit()
        

def submissions_form_drop(connection):
    cursor = connection.cursor()
    cursor.execute("""
        DROP TABLE submissionForm, latestFormUpdate
        """)
    
    connection.commit()
    