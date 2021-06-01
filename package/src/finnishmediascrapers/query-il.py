#!/usr/bin/env python3

# %%

import requests
import logging
import csv
import random
from time import sleep

logging.basicConfig(level=logging.INFO)
# %%

import argparse
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--from-date',help="from date (inclusive, YYYY-MM-DD)",required=True)
    parser.add_argument('-t','--to-date',help="to date (inclusive, YYYY-MM-DD, defaults to today)")
    parser.add_argument('-q','--query',help="query string to search for",required=True)
    parser.add_argument('-o','--output',help="output CSV file",required=True)
    parser.add_argument('-l','--limit',help="number of articles to fetch per query (max==200)",default=200,type=int)
    parser.add_argument('-d','--delay',help="number of seconds to wait between consecutive requests",default=1.0,type=float)
    parser.add_argument('--quiet', default=False, action='store_true', help="Log only errors")    
    return parser.parse_args()

api: str = "https://api.il.fi/v1/articles/search"

def main():
    args = parse_arguments()
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    with open(args.output,"w") as of:
        co = csv.writer(of)
        co.writerow(['id','url','title','date_created','date_modified','lead'])
        params = {
            'date_start':args.from_date,
            'date_end':args.to_date,
            'q':args.query,
            'offset':0,
            'limit':args.limit
            }
        response = requests.get(api,params)
        total_count = 0
        while True:
            if response.status_code != 200:
                logging.error(f"Got unexpected response code {response.status_code} for {response.url}.")
                break
            r = response.json()['response'] 
            if r is None:
                logging.error(f"Got empty response for {response.url}")
                break
            if len(r)==0:
                logging.info(f"Got 0 results, assuming we're done.")
                break
            logging.info(f"Processing {len(r)} articles from {response.url}")
            total_count += len(r)
            for a in r:
                url = 'http://iltalehti.fi/'+a['category']['category_name']+"/a/"+a['article_id']
                title = a['title']
                date_created = a['published_at']
                date_modified = a['updated_at'] if a['updated_at'] is not None else date_created
                lead = a['lead']
                id = a['article_id']
                co.writerow([id,url,title,date_created,date_modified,lead])
            params['offset']+=args.limit
            sleep(random.randrange(args.delay*2))
            response = requests.get(api,params)
        logging.info(f"Processed {total_count} articles in total.")


if __name__ == '__main__':
    main()