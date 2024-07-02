import os
import sqlite3
import logging
logger = logging.getLogger(__name__)

PATH = os.environ.get("DATA_PATH", "var/lib/data")
# PATH = os.environ.get("DATA_PATH", "./data")
logger.warning("Data path location: {}".format(PATH))

DATABASE_PATH = os.path.join(os.path.abspath(PATH), 'financedata.db')

connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)