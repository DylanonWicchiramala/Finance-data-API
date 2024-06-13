from typing import Any
import json
from util import request_get

def ciks_transform(dictionary):
    for i in dictionary:
        cik = int(dictionary[i]['cik_str'])
        cik_str = str(cik).zfill(10)
        ticker = dictionary[i]['ticker']      
        name = dictionary[i]['title']
        
        dictionary[i] = {}
        dictionary[i]['cik'] = cik
        dictionary[i]['cik_str'] = cik_str
        dictionary[i]['ticker'] = ticker
        dictionary[i]['name'] = name
        
    return dictionary


def get_ciks() -> list[dict[str, Any]]:
    """ download the cik data contain ticker , company name and cik number.
        save into a csv if local_path is not None.
    """

    cik_data = request_get("https://www.sec.gov/files/company_tickers.json").json()
    
    cik_t = ciks_transform(cik_data)   
    
    cik_t = list(cik_t.values())
    
    return cik_t
