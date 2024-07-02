import os
import sqlite3
import logging
from sys import platform
logger = logging.getLogger(__name__)

if platform == "linux" or platform == "linux2":
    PATH = os.environ.get("DATA_PATH", "/var/lib/data")
    DATABASE_PATH = "/var/lib/data/"+"financedata.db"
else:
    PATH = os.environ.get("DATA_PATH", "./data")

    DATABASE_PATH = os.path.join(os.path.abspath(PATH), 'financedata.db')


logger.warning("Data path location: {}".format(PATH))
connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)