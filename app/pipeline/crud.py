import sys
sys.path.append('.')
sys.path.append('./pipeline')
# sys.path.append('./app')

import schema
from get_data import scrape_companies_info


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
  ciks = list(ciks.values())

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