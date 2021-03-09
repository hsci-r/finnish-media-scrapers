#!/usr/bin/env python3

# %%

import os
import requests
import logging
import csv
import random
from datetime import datetime, timedelta
from time import sleep
import time
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
# %%

import argparse
def parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('-f','--from-date',help="from date (inclusive, YYYY-MM-DD)",required=True)
  parser.add_argument('-t','--to-date',help="to date (inclusive, YYYY-MM-DD, defaults to today)")
  parser.add_argument('-q','--query',help="query string to search for",required=True)
  parser.add_argument('-o','--output',help="output CSV file",required=True)
  parser.add_argument('-a','--articles',help="directory to fetch articles into (optional)")
  parser.add_argument('-l','--limit',help="number of articles to fetch per query (max==10000)",default=10000,type=int)
  parser.add_argument('-d','--delay',help="number of seconds to wait between consecutive requests",default=1.0,type=float)
  parser.add_argument('--quiet', default=False, action='store_true', help="Log only errors")
  return(parser.parse_args())

api: str = "https://yle-fi-search.api.yle.fi/v1/search"

def main():
    args = parse_arguments()
    # for testing: args = {'delay': 1.0, 'from_date':'2020-02-16', 'limit': 10, 'output':'output.csv', 'query':'SDP', 'to_date':'2020-02-18', 'articles': 'articles/'}
    
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)

    params = {
        'app_id':'hakuylefi_v2_prod',
        'app_key':'4c1422b466ee676e03c4ba9866c0921f',
        'service':'uutiset',
        'language':'fi',
        'uiLanguage':'fi',
        'type':'article',
        'time':'custom',
        'timeFrom':args.from_date,
        'timeTo':args.to_date if args.to_date is not None else datetime.today().strftime('%Y-%m-%d'),
        'query':args.query,
        'offset':0,
        'limit':args.limit
    }

    response = requests.get(api,params)
    if response.status_code != 200:
        logging.error(f"Got unexpected response code {response.status_code} for {response.url}.")
        return
    r = response.json()
    if r is None:
        logging.error(f"Got empty response for {response.url}")
        return
    if r['meta']['count']>10000:
        logging.error(f"Query results in {r['meta']['count']} results. The YLE API refuses to return more than 10000 results, so refusing to continue. You can work around this limitation by doing multiple queries on smaller timespans.")
        return
    with open(args.output,"w") as of:
        co = csv.writer(of)
        co.writerow(['id','url','title','date_modified'])
        response = requests.get(api,params)
        total_count = 0
        while True:
            if response.status_code != 200:
                logging.error(f"Got unexpected response code {response.status_code} for {response.url}.")
                break
            r = response.json()
            if r is None:
                logging.error(f"Got empty response for {response.url}")
                break
            if len(r['data'])==0:
                logging.info(f"Got 0 results, assuming we're done.")
                break
            logging.info(f"Processing {len(r['data'])} articles from {response.url}")
            total_count += len(r['data'])
            for a in r['data']:
                url = a['url']['full']
                title = a['headline']
                date_modified = a['datePublished']
                id = a['id']
                co.writerow([id,url,title,date_modified])
            params['offset']+=args.limit
            if params['offset']>r['meta']['count']:
                logging.info(f"Got all {r['meta']['count']} results from the API.")
                break
            sleep(random.randrange(args.delay*2))
            response = requests.get(api,params)
        logging.info(f"Processed {total_count} articles in total.")

if __name__ == '__main__':
    main()