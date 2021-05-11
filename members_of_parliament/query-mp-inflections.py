import pandas as pd

df = pd.read_csv("mp-expanded.csv")

names = []
firstnames = list(df['first_name'])
lastnames = list(df['expanded_last_name'])

for i in range(0, len(firstnames)):
    names.append(firstnames[i] + " " + lastnames[i])
    
import os.path

for name in names:
    name_replaced = name.replace(" ", "")
    
    if not os.path.isfile('../queries/il-inflections-' + name_replaced + ".csv"):
        os.system('python ../query-il.py -f 2020-01-01 -t 2020-12-31 -o ../queries/il-inflections-'+ name_replaced + '.csv' + '  -q ' + '"' + name + '"')
    
    if not os.path.isfile('../queries/is-inflections-' + name_replaced + ".csv"):
        os.system('python ../query-is.py -f 2020-01-01 -t 2020-12-31 -o ../queries/is-inflections-'+ name_replaced + '.csv' + '  -q ' + '"' + name + '"')
    
    if not os.path.isfile('../queries/yle-inflections-' + name_replaced + ".csv"):
        os.system('python ../query-yle.py -f 2020-01-01 -t 2020-12-31 -o ../queries/yle-inflections-'+ name_replaced + '.csv' + '  -q ' + '"' + name + '"')
    
    if not os.path.isfile('../queries/hs-inflections-' + name_replaced + ".csv"):
        os.system('python ../query-hs.py -f 2020-01-01 -t 2020-12-31 -o ../queries/hs-inflections-'+ name_replaced + '.csv' + '  -q ' + '"' + name + '"')
