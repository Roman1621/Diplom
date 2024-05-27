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
                if current_section is not None and current_list:
                    attribute_dict[current_section] = ast.literal_eval(''.join(current_list))
                current_section = line.replace(section_marker, '').strip()
                current_list = []
            else:
                if current_section is not None:
                    current_list.append(line.strip())
        if current_section is not None and current_list:
            attribute_dict[current_section] = ast.literal_eval(''.join(current_list))
        return attribute_dict