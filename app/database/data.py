import os
import sqlite3


PATH = os.environ.get("DATA_PATH")
print("Data path location: {}".format(PATH))
PATH = "var/lib/data"

# PATH = './data'

DATABASE_PATH = os.path.join(os.path.abspath(PATH), 'financedata.db')

connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)