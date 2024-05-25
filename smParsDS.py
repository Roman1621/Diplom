import pandas as pd
import ast

def parsDStoDict(path):
    d = dict()
    cur = pd.read_csv(path)
    if 'Attribute Vector' not in cur.columns:
        return -1
    cur = cur[['Name', 'Attribute Vector']]
    for index, row in cur.iterrows():
        attList = ast.literal_eval(row['Attribute Vector'])
        d[row['Name']] = attList
    return d

def parsAtNames(path):
    with open(path) as file:
        data = file.read().strip().split('\n')
        attribute_dict = {}
        current_section = None
        section_marker = '#'
        for line in data:
            if line == '':
                continue
            if line.startswith(section_marker):
                current_section = line.replace(section_marker, '')
                attribute_dict[current_section] = []
            else:
                if current_section is not None:
                    line = line[1:-1]
                    attribute_dict[current_section].append(ast.literal_eval(line))
        return attribute_dict