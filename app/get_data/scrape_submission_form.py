from typing import Any
import json
import pandas as pd
import json
from util import request_get, convert_to_list_dict
import logging
logger = logging.getLogger(__name__)

def submissions_form_transform(submissions_form:list[dict[str: Any]], submission_meta:list[dict[str: Any]]) -> list[dict[str: Any]]:
    cik = submission_meta['cik']
    exchanges = submission_meta['exchanges']
    tickers = submission_meta['tickers']
    try:
        if isinstance(exchanges, list):
            t = [f"{exchange}:{ticker}" for exchange, ticker in list(zip(exchanges, tickers))]
            exchanges = ",".join(t)
        else:
            exchanges = f"{exchanges}:{tickers}"
    except TypeError:
        exchanges = ""
    company_info = {
        'cik': cik,
        'entity_type': submission_meta['entityType'],
        'sic': submission_meta['sic'],
        'industry': submission_meta['sicDescription'],
        'exchanges': exchanges,
        'description': submission_meta['description'],
        'website': submission_meta['website'],
        'category': submission_meta['category'],
        'investor_website': submission_meta['investorWebsite'],
        'fiscal_year_end': submission_meta['fiscalYearEnd'],
        'state_of_incorporation': submission_meta['stateOfIncorporation']
    }
    
    for i in range(len(submissions_form)):
        accession_number = submissions_form[i]['accessionNumber']
        primary_document = submissions_form[i]['primaryDocument']
        accession_number_nodash = accession_number.replace('-','')
        submissions_form[i] = {
            'accession_number': accession_number,
            'cik': submissions_form[i]['cik'],
            'filing_date': submissions_form[i]['filingDate'],
            'report_date': submissions_form[i]['reportDate'],
            'acceptance_date_time': submissions_form[i]['acceptanceDateTime'],
            'index_url' : f"https://www.sec.gov/Archives/edgar/data/{str(cik)}/{accession_number_nodash}/{accession_number}-index.htm",
            'primary_docment_url' : f"https://www.sec.gov/Archives/edgar/data/{str(cik)}/{accession_number_nodash}/{primary_document}",
            'act': submissions_form[i]['act'],
            'form': submissions_form[i]['form'],
            'file_number': submissions_form[i]['fileNumber'],
            'film_number': submissions_form[i]['filmNumber'],
            'items': submissions_form[i]['items'],
            'size': submissions_form[i]['size'],
            'is_xbrl': submissions_form[i]['isXBRL'],
            'is_inline_xbrl': submissions_form[i]['isInlineXBRL'],
            'primary_docment': primary_document,
            'primary_doc_description': submissions_form[i]['primaryDocDescription']
        }
    return submissions_form, company_info

def get_submissions_form(
        cik:str|int, 
        get_older_files:bool|int=False, 
        save_path:str=None) -> list[dict[str: Any]]:
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
    
    logger.info("Getting submission info of CIK{}".format(cik))
    
    metas = __get_submission_meta(cik=cik)
    filings = metas['filings']
    
    submissions = {}

    # get the recent submission files.
    submissions = filings['recent']

    # get the older submission files.
    if 'files' in filings.keys() and get_older_files:
        older_file_meta = filings['files']
        for i in range(len(older_file_meta)):
            sub = request_get(base_url + older_file_meta['name']).json()
            submissions = __concat_submission(submissions, sub)
            
    # sub_df = pd.DataFrame(submissions)
    
    # # filter the form submission.
    # # sub_df = dict(sub_df[sub_df['form'].isin(['10-Q', '10-K', '10-K/A', '10-Q/A'])])

    # submissions = dict(sub_df)
    
    
    # # casting panda series to list
    # submissions = {k:list(v) for k,v in submissions.items()}
    
    # adding cik
    submissions['cik'] = [int(cik)]* len(submissions['accessionNumber'])
    
    #save to cache json data
    if save_path is not None:
        with open(save_path, 'w') as json_file:
            json.dump(submissions, json_file, indent=4)
            logger.info("Submissions info of CIK{} saved at {}".format(cik, save_path))
    
    submissions = convert_to_list_dict(submissions)
    
    submissions, company_info = submissions_form_transform(submissions, metas)
    
    return submissions, company_info