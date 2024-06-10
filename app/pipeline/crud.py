import sys
sys.path.append('.')
sys.path.append('./pipeline')
sys.path.append('./app')


import pandas as pd
from get_data import scrape_companies_info



def company_info_load(dataset):
    ciks = scrape_companies_info.get_ciks()
    
    dataset.df = pd.DataFrame(ciks).T
    
    dataset.save()
    

def company_info_get(dataset, filter:dict, columns:list=None, get_first:bool=True):
    """
    Search for company info by filter and return the result as a dictionary.
    
    :param:
        session: SQLAlchemy session object
        filter: The filter (in dict) to search for
        columns: List of columns to return (default is all columns)
        get_first: If True, return only first object
    :return: Dictionary containing company info (return list if have many result) if found, otherwise None
    """
    df = dataset.df
    res = pd.DataFrame([])
    
    for k, v in filter.items():
        res._append(df[df[k]==v])
        
    print(res)
    
    
from data import  company_info


company_info_get(company_info, {"cik":1652044})