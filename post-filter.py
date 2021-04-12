#!/usr/bin/env python3

# %%

import logging
import csv
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)
# %%

import argparse
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input',help="input CSV file containing articles to post-filter (from query-il.py, query-is.py or query-yle.py)",required=True)
    parser.add_argument('-t','--txt',help="directory containing the plain texts extracted from the articles",required=True)
    parser.add_argument('-o','--output',help="output CSV the contents of which will be the input CSV with a column added for the post-filtering result",required=True)
    parser.add_argument('-q','--query-strings',help="query strings to search for",nargs="+")
    parser.add_argument('-ci','--case-insensitive',default=False,action='store_true',help="compare without regard to upper or lower case")
    parser.add_argument('--quiet', default=False, action='store_true', help="Log only errors")    
    return parser.parse_args()

def main():
    args = parse_arguments()
    query_strings = args.query_strings
    if args.case_insensitive:
        query_strings = map(query_strings,lambda l: l.lower())
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    with open(args.input) as inf, open(args.output,'w') as outf:
        cr = csv.DictReader(inf)
        cw = csv.DictWriter(outf,[*cr.fieldnames,'matches'])
        for a in cr:
            txt = Path(os.path.join(args.txt,a['id']+'.txt')).read_text()
            if args.case_insensitive:
                txt = txt.lower()
            matches = 0
            for qs in query_strings:
                matches = matches + txt.count(qs)
            cw.writerow({**a,'matches':matches})


if __name__ == '__main__':
    main()
