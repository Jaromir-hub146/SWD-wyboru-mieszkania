""" ....... """


import pandas as pd
import os


class DataBase:
    def __init__(self, filename='default'):
        self.filename = filename
        self.dict = {}
        self.load_txt(self.filename)
        self.ranking = []

    def save(self, file='default'):
        f = open(f"data/{file}.txt", 'w')
        for k, v in self.dict.items():
            data = k
            for val in v:
                data += f";{val}"
            data += '\n'
            f.write(data)
        f.close()

    def load_txt(self, file_name):
        self.filename = file_name
        f = open(("data/" + self.filename + ".txt"), 'r')
        for line in f:
            lst = line.strip().split(';')
            key = lst.pop(0)
            temp = []
            for i in lst:
                if i == 'False':
                    temp.append(False)
                elif i == 'True':
                    temp.append(True)
                else:
                    temp.append(float(i))
            self.dict[key] = temp

    def load_excel(self, filen):
        path = os.path.abspath("data")
        df = pd.read_excel(f"{path}\\{filen}.xlsx", index_col=0, header=0)
        data = df.T.to_dict('list')
        self.dict.update(data)
