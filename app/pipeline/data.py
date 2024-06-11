import pandas as pd
import os
import sqlite3

PATH = os.environ.get("DATA_PATH")

# PATH = './data'

connection = sqlite3.connect(os.path.join(PATH, 'financedata.db'))
cursor = connection.cursor()