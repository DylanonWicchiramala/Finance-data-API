from typing import Any
import requests
import json
from os import path
from ratelimit import limits, sleep_and_retry


# @sleep_and_retry
@limits(calls=10, period=1.05)
def __request_get(url, *args,**kwargs):
    headers = {'User-agent': 'Mozilla/5.0'}
    return requests.get(url, headers = headers, *args, **kwargs)


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


def get_ciks() -> dict[int, dict[str, Any]]:
    """ download the cik data contain ticker , company name and cik number.
        save into a csv if local_path is not None.
    """
    x = __request_get("https://www.sec.gov/files/company_tickers.json")
    try:
        x=x.json()
    except:
        print(x)
    cik_data = x
    
    return ciks_transform(cik_data)   