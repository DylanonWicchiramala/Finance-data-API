import pandas as pd
import os

PATH = os.environ.get("DATA_PATH")

PATH = './data'


class dataset():
    df:pd.DataFrame = None
    path:str = None
    def __init__(self, path, df=None):
        self.path = path
        if self.df is not None:
            self.df = df
        else:
            try:
                self.df = pd.read_csv(self.path)
            except FileNotFoundError:
                self.save()
        
    def save(self):
        if self.df is not None:
            self.df.to_csv(self.path)
        else:
            pd.DataFrame(list()).to_csv()
        print("Data saved at " + self.path)
        
        
        
company_info = dataset( os.path.join(PATH, "finance_data/company_info.csv") )
