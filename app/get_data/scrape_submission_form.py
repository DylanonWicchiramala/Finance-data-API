from typing import Any
import json
import pandas as pd
import json
from util import request_get, convert_to_list_dict

def get_submissions_info(
        cik:str|int, 
        get_older_files:bool|int=False, 
        save_path:str=None) -> dict[str, list]:
    """ get document summissions for the ticker from https://data.sec.gov/submissions
    parameters:
        cik: str
        get_older_files: bool
            getting olders submissions that older than 5 years old.
    """    
    def __concat_submission(dict1, dict2):
        out_dict = {}
        
        #concat dict
        for key in dict2.keys():
            # Concatenate the lists if the key is present in both dictionaries
            out_dict[key] = dict1.get(key, []) + dict2.get(key, [])
            
        return out_dict
    
    def __get_submission_meta(cik:str|int) -> dict[str, list]:
        """ returns dictionary of submission metadata.
        """
        
        cik = str(cik).zfill(10)

        # get the metadata of the submissions.
        meta = request_get(base_url + f"CIK{cik}.json").json()
        
        return meta
    
    base_url = "https://data.sec.gov/submissions/"
    
    filings = __get_submission_meta(cik=cik)['filings']
    submissions = {}

    # get the recent submission files.
    submissions = filings['recent']

    # get the older submission files.
    if 'files' in filings.keys() and get_older_files:
        older_file_meta = filings['files']
        for i in range(len(older_file_meta)):
            sub = request_get(base_url + older_file_meta['name']).json()
            submissions = __concat_submission(submissions, sub)
            
    sub_df = pd.DataFrame(submissions)
    
    # filter the form submission.
    sub_df = dict(sub_df[sub_df['form'].isin(['10-Q', '10-K', '10-K/A', '10-Q/A'])])

    submissions = dict(sub_df)
    
    # casting panda series to list
    submissions = {k:list(v) for k,v in submissions.items()}
    
    # adding cik
    submissions['cik'] = [int(cik)]* len(sub_df)

    #save to cache json data
    if save_path is not None:
        with open(save_path, 'w') as json_file:
            json.dump(submissions, json_file, indent=4)
    
    # submissions = convert_to_list_dict(submissions)
    
    return submissions