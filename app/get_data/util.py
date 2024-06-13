from typing import Any
import requests
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=10, period=1.05)
def request_get(url, *args,**kwargs):
    headers = {'User-agent': 'Mozilla/5.0'}
    return requests.get(url, headers = headers, *args, **kwargs)


def convert_to_list_dict(dict_of_lists:dict[str: list[Any]]) -> list[dict[str: Any]]:
    # Get all the keys from the dictionary
    keys = list(dict_of_lists.keys())
    
    # Use zip to combine corresponding elements from all lists
    zipped_values = zip(*[dict_of_lists[key] for key in keys])
    
    # Convert the zipped values to a list of dictionaries
    result = [dict(zip(keys, values)) for values in zipped_values]
    
    return result