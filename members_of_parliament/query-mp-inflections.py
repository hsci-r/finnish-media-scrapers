import pandas as pd

df = pd.read_csv("kedustajat-expanded.csv")

names = []
firstnames = list(df['First name'])
lastnames = list(df['Expanded last name'])

for i in range(0, len(firstnames)):
    names.append(firstnames[i] + " " + lastnames[i])
    
import os.path

for name in names:
    name_replaced = name.replace(" ", "")
    
    
    if not os.path.isfile('kansanedustaja_data/queries/il-inflections-' + name_replaced + ".csv"):
        os.system('python query-il.py -f 2020-01-01 -t 2020-12-31 -o kansanedustaja_data/queries/il-inflections-'+ name_replaced + '.csv' + '  -q ' + '"' + name + '"')
    
    if not os.path.isfile('kansanedustaja_data/queries/is-inflections-' + name_replaced + ".csv"):
        os.system('python query-is.py -f 2020-01-01 -t 2020-12-31 -o kansanedustaja_data/queries/is-inflections-'+ name_replaced + '.csv' + '  -q ' + '"' + name + '"')
    
    if not os.path.isfile('kansanedustaja_data/queries/yle-inflections-' + name_replaced + ".csv"):
        os.system('python query-yle.py -f 2020-01-01 -t 2020-12-31 -o kansanedustaja_data/queries/yle-inflections-'+ name_replaced + '.csv' + '  -q ' + '"' + name + '"')
    
    if not os.path.isfile('kansanedustaja_data/queries/hs-inflections-' + name_replaced + ".csv"):
        os.system('python query-hs.py -f 2020-01-01 -t 2020-12-31 -o kansanedustaja_data/queries/hs-inflections-'+ name_replaced + '.csv' + '  -q ' + '"' + name + '"')
