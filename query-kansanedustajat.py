ked = open("kansanedustajat.txt").read().split("\n")

names = []
party_dict = {}

for row in ked:
    name = row.split(",")[0].replace("*", "")
    names.append(name)
    party_dict[name] = row.split(",")[1]
    

import os


for name in names:
    os.system('python query-yle.py -f 2020-07-01 -t 2020-12-31 -o kansanedustaja_data/queries/yle-'+ name.replace(" ", "") + '.csv' + '  -q ' + '"' + name + '"')
    os.system('python query-is.py -f 2020-07-01 -t 2020-12-31 -o kansanedustaja_data/queries/is-'+ name.replace(" ", "") + '.csv' + '  -q ' + '"' + name + '"')
    os.system('python query-il.py -f 2020-07-01 -t 2020-12-31 -o kansanedustaja_data/queries/il-'+ name.replace(" ", "") + '.csv' + '  -q ' + '"' + name + '"')
    os.system('python query-hs.py -f 2020-07-01 -t 2020-12-31 -o kansanedustaja_data/queries/hs-'+ name.replace(" ", "") + '.csv' + '  -q ' + '"' + name + '"')
    