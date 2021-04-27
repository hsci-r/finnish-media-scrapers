import pandas as pd
import os
import argparse

df = pd.read_csv("kedustajat-expanded.csv")

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username',help="email to use for article fetching")
parser.add_argument('-p','--password',help="password to use for article fetching")
args = parser.parse_args()

names = []
firstnames = list(df['First name'])
lastnames = list(df['Expanded last name'])
lastnames_original = list(df['Last name'])

names_original = []

for i in range(0, len(firstnames)):
    names.append(firstnames[i] + " " + lastnames[i])
    names_original.append(firstnames[i] + " " + lastnames_original[i])


for i in range(0, len(names)):
    print("Fetching " + names[i])
    name_without_spaces = names[i].replace(" ", "")
    original_name_without_spaces = names_original[i].replace(" ", "")
    
    #IL
   
    filename = 'kansanedustaja_data/queries/il-inflections-'+ name_without_spaces + ".csv"
    os.system('python fetch-open.py -i ' + filename + ' -o kansanedustaja_data/articles/il-' + original_name_without_spaces)
    
    # IS
    filename = 'kansanedustaja_data/queries/is-inflections-'+ name_without_spaces + ".csv"
    os.system('python fetch-open.py -i ' + filename + ' -o kansanedustaja_data/articles/is-' + original_name_without_spaces)
    
    # YLE
    filename = 'kansanedustaja_data/queries/yle-inflections-'+ name_without_spaces + ".csv"
    os.system('python fetch-open.py -i ' + filename + ' -o kansanedustaja_data/articles/yle-' + original_name_without_spaces)
    
     # HS
    filename = 'kansanedustaja_data/queries/hs-inflections-'+ name_without_spaces + ".csv"
    os.system('python fetch-hs.py -i ' + filename + ' -o kansanedustaja_data/articles/hs-' + original_name_without_spaces + " -u " + args.username + " -p " + args.password)
    
    
    