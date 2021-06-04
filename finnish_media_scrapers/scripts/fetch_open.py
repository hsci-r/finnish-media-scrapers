#!/usr/bin/env python3

import os
import requests
import logging
import csv
import random
from time import sleep

logging.basicConfig(level=logging.INFO)

import argparse
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input',help="input CSV file containing articles to fetch (from query-il, query-is or query-yle)",required=True)
    parser.add_argument('-o','--output',help="directory to fetch articles into",required=True)
    parser.add_argument('-d','--delay',help="number of seconds to wait between consecutive requests",default=1.0,type=float)
    parser.add_argument('--quiet', default=False, action='store_true', help="Log only errors")    
    return parser.parse_args()

def main():
    args = parse_arguments()
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    os.makedirs(args.output,exist_ok=True)
    with open(args.input) as inf:
        cr = csv.DictReader(inf)
        for a in cr:
            file = os.path.join(args.output,a['id']+".html")
            if not os.path.exists(file):
                with open(file,"wb") as af:
                    af.write(requests.get(a['url']).content)
                logging.info(f"wrote {a['url']} into {file}")
                sleep(random.randrange(args.delay*2))


if __name__ == '__main__':
    main()