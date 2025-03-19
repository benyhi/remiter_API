import pandas as pd 

class ImportExcel:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_excel(self):
        df = pd.read_excel(self.file_path)
        dict = df.to_dict(orient='records')
        return dict

    def read_csv(self):
        df = pd.read_csv(self.file_path)
        dict = df.to_dict(orient='records')
        return dict