from fastapi import FastAPI, HTTPException, Depends, status, Query
from typing import List
from fastapi.responses import RedirectResponse
from typing import Annotated
from database import crud, data
from sqlite3 import Connection

# from prepare_database import prepare 

app = FastAPI(
    title= "Finance API",
    version= "0.01 beta"
)

# prepare()

def get_db():
    yield data.connection 
        
db_dependency = Annotated[Connection, Depends(get_db)]


@app.get("/")
def read_root():
    return RedirectResponse(url='/docs')


## company_info
@app.get("/company-info/{cik_or_ticker}", status_code=status.HTTP_200_OK)
async def company_info_get_by_cik(cik_or_ticker:int|str, connection: db_dependency=None):
    item_limit = 100
    
    if cik_or_ticker.isnumeric():
        cik = int(cik_or_ticker)
        post = crud.company_info_get(connection=connection, filter={'cik':cik}, columns=None, item_limit=item_limit)
    else:
        ticker = cik_or_ticker.upper()
        post = crud.company_info_get(connection=connection, filter={'ticker':ticker}, columns=None, item_limit=item_limit)    
    
    if post is None or len(post) == 0:
        raise HTTPException(status_code=404, detail="ticker or cik is not found.")
    return post


## submission form
@app.get("/filing/", status_code=status.HTTP_200_OK)
async def submissions_form_get(
    ticker:str|List[str]=Query(None),
    cik:str|List[str]=Query(None),
    accession_number:str|List[str]=Query(None),
    act:str|List[str]=Query(None),
    form:str|List[str]=Query(None),
    date_form:str=None, 
    date_to:str=None, 
    limit:int=100, 
    connection:db_dependency=None
    ):
    if isinstance(ticker, str):
        ticker = ticker.upper()
    elif isinstance(ticker, list):
        ticker = [ t.upper() for t in ticker ]
    if isinstance(cik, int) or isinstance(cik, str):
        cik = int(cik)
    elif isinstance(cik, list):
        cik = [int(c) for c in cik]
    if isinstance(form, str):
        form = form.upper()
    elif isinstance(form, list):
        form = [ f.upper() for f in form ]
    post = crud.submissions_form_get(
        connection, 
        filter={
            "ticker": ticker,
            "cik": cik,
            "accession_number": accession_number,
            "act": act,
            "form": form,   
        }, 
        columns=None, 
        date_from=date_form, 
        date_to=date_to, 
        item_limit=limit
        )
    if post is None or len(post) == 0:
        raise HTTPException(status_code=404, detail="data is not found.")
    return post


@app.get("/super-secret-easter-egg/", status_code=status.HTTP_200_OK)
async def super_secret_easter_egg():
    return RedirectResponse("https://youtu.be/dQw4w9WgXcQ?si=NOCkG90opbxpYCyZ")


@app.get("/ping/", tags=["healthcheck"], summary="Perform a Health Check", 
         response_description="Return HTTP Status Code 200 (OK)", status_code=status.HTTP_200_OK)
async def ping():
    return "OK"



