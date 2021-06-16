import pandas as pd
import os
import argparse

df = pd.read_csv("mp-expanded.csv")

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username',help="email to use for article fetching")
parser.add_argument('-p','--password',help="password to use for article fetching")
args = parser.parse_args()

names = []
firstnames = list(df['first_name'])
lastnames = list(df['expanded_last_name'])
lastnames_original = list(df['last_name'])

names_original = []

for i in range(0, len(firstnames)):
    names.append(firstnames[i] + " " + lastnames[i])
    names_original.append(firstnames[i] + " " + lastnames_original[i])


for i in range(0, len(names)):
    print("Fetching " + names[i])
    name_without_spaces = names[i].replace(" ", "")
    original_name_without_spaces = names_original[i].replace(" ", "")
    
    #IL
   
    filename = '../queries/il-inflections-'+ name_without_spaces + ".csv"
    os.system('fms-fetch-open -i ' + filename + ' -o ../articles/il-' + original_name_without_spaces)
    
    # IS
    filename = '../queries/is-inflections-'+ name_without_spaces + ".csv"
    os.system('fms-fetch-open -i ' + filename + ' -o ../articles/is-' + original_name_without_spaces)
    
    # YLE
    filename = '../queries/yle-inflections-'+ name_without_spaces + ".csv"
    os.system('fms-fetch-open -i ' + filename + ' -o ../articles/yle-' + original_name_without_spaces)
    
     # HS
    filename = '../queries/hs-inflections-'+ name_without_spaces + ".csv"
    os.system('fms-fetch-hs -i ' + filename + ' -o ../articles/hs-' + original_name_without_spaces + " -u " + args.username + " -p " + args.password)
    
    
    
