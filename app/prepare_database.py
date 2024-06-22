from database import crud, data
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

exceptions = []

# try:
    
crud.company_info_load(data.connection, force=False)
crud.submissions_form_load_all(data.connection, max_days_old=60)

# ciks = [
#     320193,
#     1045810,
#     789019,
# ]
# crud.submissions_form_load_many(data.connection, ciks=ciks, max_days_old=1)
    
# except Exception as e:
#     exceptions.append(e)
    
print(exceptions)

