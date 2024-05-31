from Database import crud, database, query
from sqlalchemy.orm import Session

def prepare():
    session = database.SessionLocal()

    crud.create_tables(force_recreate=False)

    crud.company_info_update(session, force=False)

    session.close()
