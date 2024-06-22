from fastapi import FastAPI, HTTPException, Depends, status
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
@app.get("/company-info/", status_code=status.HTTP_200_OK)
async def read_post(ticker: str=None, cik: str=None, connection: db_dependency=None):
    if ticker is not None:
        ticker = ticker.upper()
        post = crud.company_info_get(connection=connection, filter={'ticker':ticker}, columns=None, get_first=True)
    elif cik is not None:
        cik = int(cik)
        post = crud.company_info_get(connection=connection, filter={'cik':cik}, columns=None, get_first=False)
    else:
        return None
    if post is None or len(post) == 0:
        raise HTTPException(status_code=404, detail="ticker or cik is not found.")
    # data.connection.close()
    return post


# @app.get("/company-info/convert-ticker/{ticker}", status_code=status.HTTP_200_OK)
# async def read_post(ticker: str, session: db_dependency=None):
#     ticker = ticker.upper()
#     post = crud.company_info_get(session=session, filter={'ticker':ticker}, columns=['cik','cik_str','ticker','name'], get_first=True)
#     if post is None:
#         raise HTTPException(status_code=404, detail="company ticker is not found.")
#     return post


# @app.get("/company-info/convert-cik/{cik}", status_code=status.HTTP_200_OK)
# async def read_post(cik: str, session: db_dependency=None):
#     cik = int(cik)
#     post = crud.company_info_get(session=session, filter={'cik':cik}, columns=['cik','cik_str','ticker','name'], get_first=False)
#     if post is None:
#         raise HTTPException(status_code=404, detail="company cik is not found.")
#     return post


@app.get("/super-secret-easter-egg/", status_code=status.HTTP_200_OK)
async def super_secret_easter_egg():
    return RedirectResponse("https://youtu.be/dQw4w9WgXcQ?si=NOCkG90opbxpYCyZ")


@app.get("/ping/", tags=["healthcheck"], summary="Perform a Health Check", 
         response_description="Return HTTP Status Code 200 (OK)", status_code=status.HTTP_200_OK)
async def ping():
    return "OK"



# @app.post("/posts/", status_code=status.HTTP_201_CREATED)
# async def create_post(post: PostBase, session: db_dependency):
#     db_post = models.Post(**post.model_dump())
#     session.add(db_post)
#     session.commit()


# @app.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
# async def delete_post(post_id: int, db: db_dependency):
#     db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
#     if db_post is None:
#         raise HTTPException(status_code=404, detail="post not found")
#     db.delete(db_post)
#     db.commit()
        

# @app.post("/users/", status_code=status.HTTP_201_CREATED)
# async def create_user(user: UserBase, db: db_dependency):
#     # db_user = models.User(**user.dict())
#     db_user = models.User(**user.model_dump())
#     db.add(db_user)
#     db.commit()
    

# @app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
# async def read_user(user_id: int, db: db_dependency):
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user