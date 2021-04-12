import os

folder = "kansanedustaja_data/articles/"

folders = [name for name in os.listdir(folder)]

import pandas as pd
import os

df = pd.read_csv("kedustajat-expanded.csv")
names = []
firstnames = list(df['First name'])
lastnames = list(df['Expanded last name'])
lastnames_original = list(df['Last name'])
names_original = []

for i in range(0, len(firstnames)):
    names.append(firstnames[i] + " " + lastnames[i])
    names_original.append(firstnames[i] + " " + lastnames_original[i])
    
names_original = list(set(names_original))

for f in names_original:
    foldername = "il-" + f.replace(" ", "")
    os.system('python convert-il-to-text.py -i ' + folder+foldername + ' -o kansanedustaja_data/article_texts/' + foldername)
    
    foldername = "is-" + f.replace(" ", "")
    os.system('python convert-is-to-text.py -i ' + folder+foldername + ' -o kansanedustaja_data/article_texts/' + foldername)

    foldername = "yle-" + f.replace(" ", "")
    os.system('python convert-yle-to-text.py -i ' + folder+foldername + ' -o kansanedustaja_data/article_texts/' + foldername)

    foldername = "hs-" + f.replace(" ", "")
    os.system('python convert-hs-to-text.py -i ' + folder+foldername + ' -o kansanedustaja_data/article_texts/' + foldername)

