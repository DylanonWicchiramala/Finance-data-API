from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from typing import Annotated
from pipeline import crud, data
from sqlite3 import Connection, connect

# from prepare_database import prepare 

app = FastAPI(
    title= "Finance API",
    version= "0.01 beta"
)

# prepare()

def get_db():
    connection = connect(data.DATABASE_PATH, check_same_thread=False    )
    try:
        yield connection 
    finally:
        connection.close()
        
db_dependency = Annotated[Connection, Depends(get_db)]


@app.get("/")
def read_root():
    return RedirectResponse(url='/docs')


## company_info
@app.get("/company-info/", status_code=status.HTTP_200_OK)
async def read_post(ticker: str=None, cik: str=None, connection: db_dependency=None):
    if ticker is not None:
        ticker = ticker.upper()
        post = crud.company_info_get(connection=connection, filter={'ticker':ticker}, columns=['cik', 'ticker', 'name'], get_first=True)
    elif cik is not None:
        cik = int(cik)
        post = crud.company_info_get(connection=connection, filter={'cik':cik}, columns=['cik', 'ticker', 'name'    ], get_first=False)
    else:
        return None
    if post is None or len(post) == 0:
        raise HTTPException(status_code=404, detail="ticker or cik is not found.")
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