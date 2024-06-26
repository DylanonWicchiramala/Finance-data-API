from typing import Any
import requests
from ratelimit import limits, sleep_and_retry
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

@sleep_and_retry
@limits(calls=10, period=1.05)
def request_get(url, *args,**kwargs):
    headers = {'User-agent': 'Mozilla/5.0'}
    logger.debug("Getting data from outer URL: {}".format(url))
    return requests.get(url, headers = headers, *args, **kwargs)


def convert_to_list_dict(dict_of_lists:dict[str: list[Any]]) -> list[dict[str: Any]]:
    # Get all the keys from the dictionary
    keys = list(dict_of_lists.keys())
    
    # Use zip to combine corresponding elements from all lists
    zipped_values = zip(*[dict_of_lists[key] for key in keys])
    
    # Convert the zipped values to a list of dictionaries
    result = [dict(zip(keys, values)) for values in zipped_values]
    
    return result


def calculate_fiscal_period(report_date:str, fiscal_year_end:str) -> str:
    report_date = datetime.strptime(report_date, '%Y-%m-%d')
    fiscal_year_end = datetime.strptime(str(report_date.year)+"/"+fiscal_year_end, "%Y/%m%d")

    quarter = (((report_date - fiscal_year_end) / 92).days - 1) % 4 + 1
    if quarter == 4:
        fiscal_period_str = str(report_date.year) + "FY"
    else:
        fiscal_period_str = str(report_date.year) + "Q" + str(quarter)

    return fiscal_period_str