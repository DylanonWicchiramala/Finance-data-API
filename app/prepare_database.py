from database import crud, data
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

exceptions = []

try:
    
    crud.company_info_load(data.connection)
    crud.submissions_form_load_all(data.connection)
    
except Exception as e:
    exceptions.append(e)
    
print(exceptions)

