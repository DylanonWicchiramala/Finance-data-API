import sys
sys.path.append('.')
sys.path.append('./database')
# sys.path.append('./app')

from typing import Any
from tqdm import tqdm
import schema
from get_data import scrape_companies_info, scrape_submission_form
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

def __tablefilter(cursor, table_name:str, filter:dict, columns:list=None, c="AND"):
    """
    Search data in table  by filter and return the result as sql3 cursor.
    
    :param:
        cursor: SQL3 cursor object
        table_name: name of table to search
        filter: The filter (in dict) to search for
        columns: List of columns to return (default is all columns)
        c: condition AND, OR
    :return: Dictionary containing company info (return list if have many result) if found, otherwise None
    """
    
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


def __tableinsertmany(cursor, items:list[dict[str, Any]], schema:str, primary_key_column:str=None, update_on_conflit=False, force:bool=False):
    keys = list(items[0].keys())
    items = [ list(d.values()) for d in items]
    
    table_name = schema.split("(")[0]

    if force:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    cursor.execute("CREATE TABLE IF NOT EXISTS " + schema)
    
    if update_on_conflit:
        # Constructing the update clause for conflict resolution
        update_clause = ", ".join([f"{key} = excluded.{key}" for key in keys if key != primary_key_column])
        
        cursor.executemany(
            f"""
            INSERT INTO {table_name} ({','.join(keys)})
            VALUES ({",".join("?"*len(keys))})
            ON CONFLICT({primary_key_column}) DO UPDATE SET {update_clause}
            """, 
            items
        )
    else:
        # insert submission form information.
        cursor.executemany(
            f"""
            INSERT OR REPLACE INTO {table_name} ({",".join(keys)})
            VALUES ({",".join("?"*len(keys))})
            """, 
            items
            )
    

def __tableinsert(cursor, item:dict[str, Any], schema:str, primary_key_column:str=None, update_on_conflit=False, force:bool=False):
    keys = list(item.keys())
    values = list(item.values())
    
    table_name = schema.split("(")[0]

    if force: cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    cursor.execute("CREATE TABLE IF NOT EXISTS " + schema)
    
    if update_on_conflit:
        # Constructing the update clause for conflict resolution
        update_clause = ", ".join([f"{key} = excluded.{key}" for key in keys if key != primary_key_column])
        
        cursor.execute(f"""
            INSERT INTO {table_name} ({','.join(keys)})
            VALUES ({",".join("?"*len(keys))})
            ON CONFLICT({primary_key_column}) DO UPDATE SET {update_clause}
            """,
            values)
    else:
        cursor.execute(f"""
            INSERT OR REPLACE INTO {table_name} ({','.join(keys)})
            VALUES ({",".join("?"*len(keys))})
            """,
            values)
    
    
def __tableupdate(cursor, item: dict[str, Any], schema: str, key_column: str):
    keys = list(item.keys())
    values = list(item.values())
    
    table_name = schema.split("(")[0]
    
    cursor.execute("CREATE TABLE IF NOT EXISTS " + schema)
    
    set_clause = ", ".join([f"{key}=?" for key in keys if key != key_column])
    update_values = [item[key] for key in keys if key != key_column]
    key_value = item[key_column]

    cursor.execute(f"""
        UPDATE {table_name}
        SET {set_clause}
        WHERE {key_column} = ?
        """, update_values + [key_value])
    

def company_info_load(connection, force=False):
    ciks = scrape_companies_info.get_ciks()

    cursor = connection.cursor()

    __tableinsertmany(cursor=cursor, items=ciks, schema=schema.companyInfo, primary_key_column='ticker', update_on_conflit=True, force=force)

    connection.commit()
    logger.info("companyInfo database loaded")
    

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
    cursor = connection.cursor()
    res = __tablefilter(cursor, "companyInfo", filter, columns)
    res = res.fetchone() if get_first else res.fetchall()
    
    if get_first: 
        if res is not None:
            return dict(zip(columns, res))
        else:
            return None

    else: return [ dict(zip(columns, r)) for r in res ]
    

def submissions_form_load(connection, cik:int|str, max_days_old:int=0, do_commit:bool=True):
    # data will not update when the number of the days since data was update less than max_day_old.
    def perform_load(connection, cik:int|str):
        submissions_form, company_info = scrape_submission_form.get_submissions_form(cik)
        
        cursor = connection.cursor()
        
        # if not have submission form.
        if len(submissions_form)==0:
            logger.info("No submissions from of CIK{}".format(cik))
        else:       
            # insert submission form into the database table
            __tableinsertmany(cursor=cursor, items=submissions_form, schema=schema.submissionForm, force=False)
            logger.info("Submissions from of CIK{} was loaded into a database.".format(cik))
        
        # update company information to company_info table
        __tableupdate(cursor=cursor, item=company_info, schema=schema.companyInfo, key_column='cik')
        
        # record submit form update date.
        __tableinsert(cursor=cursor, item={"cik":cik, "timestamp":datetime.today().timestamp()}, schema=schema.latestFormUpdate, force=False)

        if do_commit: connection.commit()
    
    cursor = connection.cursor()
    # create relevant table.
    cursor.execute("CREATE TABLE IF NOT EXISTS " + schema.latestFormUpdate)
    cursor.execute("CREATE TABLE IF NOT EXISTS " + schema.submissionForm)
    
    if max_days_old == 0:
        perform_load(connection=connection, cik=cik)
        return
    
    latest_form_update = __tablefilter(cursor=cursor, table_name='latestFormUpdate', filter={'cik':int(cik)}, columns=['timestamp'], c="AND")
    latest_form_update = latest_form_update.fetchone()
    latest_form_update = latest_form_update[0] if latest_form_update is not None else 0.0

    delta_days = (datetime.today().timestamp() - latest_form_update)/86400

    if delta_days > max_days_old:
        perform_load(connection=connection, cik=cik)
    else:
        logger.info(f"Submission form information of {cik} was already loaded {delta_days} days ago.")
    
    
def submissions_form_load_many(connection, ciks:list[int|str], max_days_old:int=0):
    ciks = set(ciks)
    
    for cik in tqdm(ciks, desc="getting submission form."):
        submissions_form_load(connection=connection, cik=cik, max_days_old=max_days_old, do_commit=False)
        
    connection.commit()
    
    
def submissions_form_load_all(connection, max_days_old:int=0):
    cursor = connection.cursor()
    # getting cik from company info
    ciks = cursor.execute("""
    SELECT cik FROM companyInfo
    WHERE entity_type = "operating" OR entity_type = "" OR entity_type IS NULL
    """).fetchall()
    ciks = [cik[0] for cik in ciks]
    ciks = set(ciks)
    
    if len(ciks)==0:
        logger.warning("Submissions form not load any, due to no data in companyInfo")
        return 
    
    for cik in tqdm(ciks, desc="getting submission form."):
        submissions_form_load(connection=connection, cik=cik, max_days_old=max_days_old, do_commit=True)
        
    connection.commit()
        

def submissions_form_drop(connection):
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE submissionForm""")
    cursor.execute("""DROP TABLE latestFormUpdate""")
    
    connection.commit()
    

#TODO: submissions_form_get
def submissions_form_get(connection, cik, filing_date_from, filing_date_to):
    pass
    