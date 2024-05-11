import pandas as pd
import ast

def parsDStoDict(path):
    d = dict()
    cur = pd.read_csv(path, usecols=['Name', 'Attribute Vector'])
    for index, row in cur.iterrows():
        attList = ast.literal_eval(row['Attribute Vector'])
        d[row['Name']] = attList
    return d