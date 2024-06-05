from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from typing import Annotated
# from Database import crud, database, query
# from sqlalchemy.orm import Session

# from prepare_database import prepare 
# from pydantic import BaseModel

# session = database.SessionLocal()
app = FastAPI(
    title= "Finance API",
    version= "0.01 beta"
)

# prepare()

# class PostBase(BaseModel):
#     title: str
#     content: str
#     user_id: int
    
# class UserBase(BaseModel):
    # username: str

    
# def get_db():
#     session = database.SessionLocal()
#     try:
#         yield session 
#     finally:
#         session.close()
        
        
# db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
def read_root():
    return RedirectResponse(url='/docs')


## company_info
# @app.get("/company-info/", status_code=status.HTTP_200_OK)
# async def read_post(ticker: str=None, cik: str=None, session: db_dependency=None):
#     if ticker is not None:
#         ticker = ticker.upper()
#         post = crud.company_info_get(session=session, filter={'ticker':ticker}, get_first=True)
#     elif cik is not None:
#         cik = int(cik)
#         post = crud.company_info_get(session=session, filter={'cik':cik}, get_first=False)
#     else:
#         return None
#     if post is None:
#         raise HTTPException(status_code=404, detail="ticker or cik is not found.")
#     return post


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