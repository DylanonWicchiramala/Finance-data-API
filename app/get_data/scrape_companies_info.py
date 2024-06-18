import sys
sys.path.append('./get_data')

from typing import Any
from util import request_get
import logging
logger = logging.getLogger(__name__)

def ciks_transform(dictionary:list[dict[str: Any]]) -> list[dict[str: Any]]:
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
    logger.info("Getting cik data")

    cik_data = request_get("https://www.sec.gov/files/company_tickers.json").json()
    
    cik_t = ciks_transform(cik_data)   
    
    cik_t = list(cik_t.values())
    
    return cik_t
