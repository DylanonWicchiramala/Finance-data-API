import os
# import sqlite3

PATH = os.environ.get("DATA_PATH")

# PATH = './data'

DATABASE_PATH = os.path.join(PATH, 'financedata.db')

# connection = sqlite3.connect(DATABASE_PATH)