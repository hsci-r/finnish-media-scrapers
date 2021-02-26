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
  parser.add_argument('-t','--to-date',help="to date (inclusive, YYYY-MM-DD, defaults to today)", required=True)
  parser.add_argument('-q','--query',help="query string to search for",required=True)
  parser.add_argument('-o','--output',help="output CSV file",required=True)
  parser.add_argument('-a','--articles',help="directory to fetch articles into (optional)")
  parser.add_argument('-l','--limit',help="number of articles to fetch per query (max==50)",default=50,type=int)
  parser.add_argument('-d','--delay',help="number of seconds to wait between consecutive requests",default=1.0,type=float)
  parser.add_argument('--quiet', default=False, action='store_true', help="Log only errors")
  return(parser.parse_args())

api: str = "https://yle-fi-search.api.yle.fi/v1/search?app_id=hakuylefi_v2_prod"
app_key: str = "4c1422b466ee676e03c4ba9866c0921f"

def build_url(query: str, offset: int, limit: int, date_start: int, date_end: int) -> str:
    url = f"{api}&app_key={app_key}&language=fi&limit={limit}&offset={offset}&query={query}&service=uutiset&time=custom&timeFrom={date_start}&timeTo={date_end}&type=article&uiLanguage=fi"
    return url

def main():
    args = parse_arguments()
    # for testing: args = {'delay': 1.0, 'from_date':'2020-02-16', 'limit': 10, 'output':'output.csv', 'query':'SDP', 'to_date':'2020-02-18', 'articles': 'articles/'}
    
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)

    date_start = args.from_date
    date_end = args.to_date
    response = requests.get(build_url(args.query,0,0,date_start,date_end))
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
    try:
        if args.articles is not None:
            os.makedirs(args.articles,exist_ok=True)
        with open(args.output,"w") as of:
            co = csv.writer(of)
            co.writerow(['url','title','date_modified'])
            offset = 0
            response = requests.get(build_url(args.query,offset,args.limit,date_start,date_end))
            total_count = 0
            while True:
                if response.status_code != 200:
                    logging.error(f"Got unexpected response code {response.status_code} for {response.url}.")
                    break
                r = response.json()
                if r is None:
                    logging.error(f"Got empty response for {response.url}")
                    break
                logging.info(f"Processing {len(r['data'])} articles from {response.url}")
                total_count += len(r['data'])
                for a in r['data']:
                    url = a['url']['full']
                    title = a['headline']
                    date_modified = a['datePublished']
                    co.writerow([url,title,date_modified])
                    if args.articles is not None:
                        sleep(random.randrange(args.delay*2))
                        file = os.path.join(args.articles,"art-"+str(a['id'])+".html")
                        with open(file,"wb") as af:
                            article_request = requests.get(url)
                            af.write(article_request.content)
                        logging.info(f"wrote article into {file}")
                if len(r['data'])!=args.limit:
                    logging.info(f"Processed {len(r['data'])} results which is less than the limit, assuming we're done.")
                    break
                else:
                    offset += args.limit
                    sleep(random.randrange(args.delay*2))
                    response = requests.get(build_url(args.query,offset,args.limit,date_start,date_end))
    finally:
         logging.info(f"Processed totally {total_count} articles")

if __name__ == '__main__':
    main()