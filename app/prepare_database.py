from database import crud, data
import logging
logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)

exceptions = []

# try:
    
crud.company_info_load(data.connection, from_cache_file=True, force=False)

crud.submissions_form_load_all(data.connection, n_batch_commits=8, max_days_old=7)
crud.submissions_form_load_random(data.connection, n_rand=500, n_batch_commits=8, max_days_old=2)

# ciks = [
#     789019,
# ]
# crud.submissions_form_load_many(data.connection, ciks=ciks, max_days_old=0)
    
# except Exception as e:
#     exceptions.append(e)
    
# print("exceptions:{}".format(exceptions))

