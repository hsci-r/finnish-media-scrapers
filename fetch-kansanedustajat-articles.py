import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-u','--username',help="email to use for article fetching")
parser.add_argument('-p','--password',help="password to use for article fetching")
args = parser.parse_args()

ked = open("kansanedustajat.txt").read().split("\n")

names = []
party_dict = {}

for row in ked:
    name = row.split(",")[0].replace("*", "")
    names.append(name)
    party_dict[name] = row.split(",")[1]
    


for name in names:
    print("Fetching " + name)
    #YLE
    name_without_spaces = name.replace(" ", "")
    filename = 'kansanedustaja_data/queries/yle-'+ name_without_spaces + ".csv"
    os.system('python fetch-open.py -i ' + filename + ' -o kansanedustaja_data/articles/yle-' + name_without_spaces)
    
    #IL
    filename = 'kansanedustaja_data/queries/il-'+ name_without_spaces + ".csv"
    os.system('python fetch-open.py -i ' + filename + ' -o kansanedustaja_data/articles/il-' + name_without_spaces)
    
    #IS
    filename = 'kansanedustaja_data/queries/is-'+ name_without_spaces + ".csv"
    os.system('python fetch-open.py -i ' + filename + ' -o kansanedustaja_data/articles/is-' + name_without_spaces)
    
    #HS
    filename = 'kansanedustaja_data/queries/hs-'+ name_without_spaces + ".csv"
    os.system('python fetch-hs.py -i ' + filename + ' -o kansanedustaja_data/articles/hs-' + name_without_spaces + " -u " + args.username + " -p " + args.password)