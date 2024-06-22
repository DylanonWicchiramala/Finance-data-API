import sys
sys.path.append('./get_data')

from typing import Any
from util import request_get
import logging
from requests.exceptions import JSONDecodeError
import json
logger = logging.getLogger(__name__)

def ciks_transform(dictionary:list[dict[str: Any]]) -> list[dict[str: Any]]:
    for i in dictionary:
        cik = int(dictionary[i]['cik_str'])
        ticker = dictionary[i]['ticker']      
        name = dictionary[i]['title']
        
        dictionary[i] = {}
        dictionary[i]['cik'] = cik
        dictionary[i]['ticker'] = ticker
        dictionary[i]['name'] = name
        
    return dictionary


def get_ciks(use_cache_file=True) -> list[dict[str, Any]]:
    """ download the cik data contain ticker , company name and cik number.
        save into a csv if local_path is not None.
    """
    def load_local_ciks():
        f = open('./data/finance_data/company_info.json')
        cik_data = json.load(f)
        return cik_data
    
    logger.info("Getting cik data")

    
    if use_cache_file:
        cik_data = load_local_ciks()
    
    else:
        cik_data_raw = request_get("https://www.sec.gov/files/company_tickers.json")
        try:
            cik_data = cik_data_raw.json()
        except JSONDecodeError as e:
            logger.warning(f"Error decoding json data. request got: {cik_data_raw.text}")
            try: 
                cik_data = load_local_ciks()
            except Exception as e:
                raise e
            
    cik_t = ciks_transform(cik_data)   
    
    cik_t = list(cik_t.values())
    
    return cik_t
