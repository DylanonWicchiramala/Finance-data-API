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

def __tablefilter(cursor, table_name:str, filter:dict, columns:list=None, condition="AND"):
    """
    Search data in table  by filter and return the result as sql3 cursor.
    
    :param:
        cursor: SQL3 cursor object
        table_name: name of table to search
        filter: The filter (in dict) to search for
        columns: List of columns to return (default is all columns)
        condition: condition AND, OR
    :return: Dictionary containing company info (return list if have many result) if found, otherwise None
    """
    
    filter = list(filter.items())
    condition = []
    if filter is not None or len(filter) != 0:
        for q, v in filter:
            if v is not None:
                if hasattr(v, '__iter__') and not isinstance(v, str) and len(v) > 1:
                    condition.append(f"{q} IN {str(tuple(v))}")
                else:
                    v = v[0] if isinstance(v, list) else v
                    condition.append("{} = \"{}\"".format(q, v))
            
    condition = " WHERE " + f" {condition} ".join(condition)    

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
    columns = [ col[0] for col in res.description]
    return res, columns


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
    

def company_info_load(connection, from_cache_file=True, force=False):
    ciks = scrape_companies_info.get_ciks(use_cache_file=from_cache_file)

    cursor = connection.cursor()

    __tableinsertmany(cursor=cursor, items=ciks, schema=schema.companyInfo, primary_key_column='ticker', update_on_conflit=True, force=force)

    connection.commit()
    logger.info("companyInfo database loaded")
    

def company_info_get(connection, filter:dict, columns:list=None, item_limit:int=1000) -> list[dict]:
    """
    Search for company info by filter and return the result as a dictionary.
    
    :param:
        connection: sqlite connection object
        filter: The filter (in dict) to search for
        columns: List of columns to return (default is all columns)
        items_limit: The maximum number of output items to return.
    :return: Dictionary containing company info (return list if have many result) if found, otherwise None
    """
    cursor = connection.cursor()
    res, columns = __tablefilter(cursor, "companyInfo", filter, columns)
    res = res.fetchmany(item_limit)
    
    return [ dict(zip(columns, r)) for r in res ]
    

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
    
    latest_form_update, _ = __tablefilter(cursor=cursor, table_name='latestFormUpdate', filter={'cik':int(cik)}, columns=['timestamp'], condition="AND")
    latest_form_update = latest_form_update.fetchone()
    latest_form_update = latest_form_update[0] if latest_form_update is not None else 0.0

    delta_days = (datetime.today().timestamp() - latest_form_update)/86400

    if delta_days > max_days_old:
        perform_load(connection=connection, cik=cik)
    else:
        logger.info(f"Submission form information of {cik} was already loaded {delta_days} days ago.")
    
    
def submissions_form_load_many(connection, ciks:list[int|str], n_batch_commits:int=1, max_days_old:int=0):
    def __get_outdated_cik(connection, ciks:list=None, max_days_old:int=0):
        now_timestamp = datetime.now().timestamp()
        diff_seconds = max_days_old * 24 * 60 * 60

        diff_timestamp = now_timestamp - diff_seconds

        ciks_str = ', '.join(map(str, ciks))

        # Execute the SQL query
        query = f"""
            SELECT companyInfo.cik 
            FROM companyInfo LEFT JOIN LatestFormUpdate 
            ON companyInfo.cik = latestFormUpdate.cik 
            WHERE latestFormUpdate.timestamp < {str(diff_timestamp)} OR latestFormUpdate.cik IS NULL
        """
        if ciks is not None:
            query = query + f" AND companyInfo.cik IN ({ciks_str})"
        cursor = connection.cursor()
        ciks = cursor.execute(query).fetchall()
        connection.commit()
        return [cik[0] for cik in ciks]
    
    # remove duplicates of values
    ciks = list(dict.fromkeys(ciks))
    
    ciks = __get_outdated_cik(connection=connection, ciks=ciks, max_days_old=max_days_old)
    
    for i in tqdm(range(len(ciks)), desc="getting submission form."):
        submissions_form_load(connection=connection, cik=ciks[i], max_days_old=0, do_commit=False)
        if i % n_batch_commits == n_batch_commits-1:
            connection.commit()
        
    connection.commit()
    
    
def submissions_form_load_all(connection, n_batch_commits:int=1, max_days_old:int=0):
    cursor = connection.cursor()
    # getting cik from company info
    ciks = cursor.execute("""
    SELECT cik FROM companyInfo
    """).fetchall()
    ciks = [cik[0] for cik in ciks]
    
    if len(ciks)==0:
        logger.warning("Submissions form not load any, due to no data in companyInfo")
        return 
    
    submissions_form_load_many(connection=connection, ciks=ciks, n_batch_commits=n_batch_commits, max_days_old=max_days_old)
    
    connection.commit()
    

def submissions_form_load_random(connection, n_rand:int=500, n_batch_commits:int=1, max_days_old:int=0):
    cursor = connection.cursor()
    # getting cik from company info
    ciks = cursor.execute(f"""
    SELECT cik FROM companyInfo
    ORDER BY RANDOM() LIMIT {str(n_rand)}
    """).fetchmany(n_rand)
    ciks = [cik[0] for cik in ciks]
    
    if len(ciks)==0:
        logger.warning("Submissions form not load any, due to no data in companyInfo")
        return 

    submissions_form_load_many(connection=connection, ciks=ciks, n_batch_commits=n_batch_commits, max_days_old=max_days_old)
        
    connection.commit()
        

def submissions_form_drop(connection):
    cursor = connection.cursor()
    cursor.execute("""DROP TABLE submissionForm""")
    cursor.execute("""DROP TABLE latestFormUpdate""")
    
    connection.commit()
    

def submissions_form_get(connection, filter:dict, columns:list=None, date_from:str=None, date_to:str=None, item_limit:int=1000) -> list[dict]:
    """
    Search for company filing by filter and return the result as a list of dictionary.
    
    :param:
        connection: sqlite connection object
        filter: The filter (in dict) to search for
        columns: List of columns to return (default is all columns)
        date_from: filter date from 
        date_to: filterr date to
    :return: Dictionary containing company info (return list if have many result) if found, otherwise None
    """
    cursor = connection.cursor()
    
    filter = {} if filter is None else list(filter.items())
    
    condition = []
    if filter is not None or len(filter) != 0:
        for q, v in filter:
            if v is not None:
                if hasattr(v, '__iter__') and not isinstance(v, str) and len(v) > 1:
                    condition.append(f"{q} IN {str(tuple(v))}")
                else:
                    v = v[0] if isinstance(v, list) else v
                    condition.append("{} = \"{}\"".format(q, v))
                
        condition = f" AND ".join(condition)    
    
        
    date_from = datetime.strftime(datetime.strptime(date_from, "%Y-%m-%d"), "%Y-%m-%d") if date_from is not None else None
    date_to = datetime.strftime(datetime.strptime(date_to, "%Y-%m-%d"), "%Y-%m-%d") if date_to is not None else None
    
    if date_from is not None:
        datefrom_cont = f"date(filing_date) > date(\"{date_from}\")"
        condition = condition + f" AND {datefrom_cont}" if len(condition) > 0 else datefrom_cont
    if date_to is not None:
        dateto_cont = f"date(filing_date) < date(\"{date_to}\")"
        condition = condition + f" AND {dateto_cont}" if len(condition) > 0 else dateto_cont
        
    if len(condition) == 0:
        condition = "TRUE"

    column = """
        ticker, companyInfo.cik, primary_doc_description, primary_docment,
        accession_number, filing_date, report_date, acceptance_date_time, 
        index_url, primary_docment_url, act, form
        """ if columns is None else ','.join(columns)
    
    query = f"""
        SELECT {column}
        FROM submissionForm INNER JOIN companyInfo ON submissionForm.cik = companyInfo.cik
        WHERE {condition}
        """
    
    q_res = cursor.execute(query)
    data = q_res.fetchmany(item_limit)
    
    columns = [ col[0] for col in q_res.description]
    
    if len(data) == 0:
        return None
    
    datadict = [ dict(zip(columns, r)) for r in data ]
    return datadict