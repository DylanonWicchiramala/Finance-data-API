from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# URL_DATABASE = 'mysql+pymysql://root:cwn,CD0sql@localhost:3306/financedata'

URL_DATABASE = os.environ.get("DATABASE_URL")
engine = create_engine(URL_DATABASE)

# engine = create_engine("mysql+pymysql://root:aODIJfe3@db:3306/financedata")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()