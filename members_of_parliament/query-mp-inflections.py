import os

import pandas as pd

df = pd.read_csv("mp-expanded-orpo.csv")

names = []
firstnames = list(df['first_name'])
lastnames = list(df['expanded_last_name'])

for i in range(0, len(firstnames)):
    names.append(firstnames[i] + " " + lastnames[i])


for name in names:
    name_replaced = name.replace(" ", "")

    if not os.path.isfile('../queries/il-inflections-' + name_replaced + ".csv"):
        os.system('fms-query-il -f 2020-01-01 -t 2020-01-07 -o ../queries/il-inflections-' +
                  name_replaced + '.csv' + '  -q ' + '"' + name + '"')

    if not os.path.isfile('../queries/is-inflections-' + name_replaced + ".csv"):
        os.system('fms-query-is -f 2020-01-01 -t 2020-01-07 -o ../queries/is-inflections-' +
                  name_replaced + '.csv' + '  -q ' + '"' + name + '"')

    if not os.path.isfile('../queries/yle-inflections-' + name_replaced + ".csv"):
        os.system('fms-query-yle -f 2020-01-01 -t 2020-01-07 -o ../queries/yle-inflections-' +
                  name_replaced + '.csv' + '  -q ' + '"' + name + '"')

    if not os.path.isfile('../queries/hs-inflections-' + name_replaced + ".csv"):
        os.system('fms-query-hs -f 2020-01-01 -t 2020-01-07 -o ../queries/hs-inflections-' +
                  name_replaced + '.csv' + '  -q ' + '"' + name + '"')
