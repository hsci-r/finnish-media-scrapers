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

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

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
  parser.add_argument('-u','--username',help="email to use for article fetching")
  parser.add_argument('-p','--password',help="password to use for article fetching")
  parser.add_argument('-l','--limit',help="number of articles to fetch per query (max==50)",default=50,type=int)
  parser.add_argument('-d','--delay',help="number of seconds to wait between consecutive requests",default=1.0,type=float)
  parser.add_argument('--quiet', default=False, action='store_true', help="Log only errors")
  return(parser.parse_args())


#https://www.is.fi/api/search/SDP/kaikki/custom/new/0/50/1593561600000/1609372800000
api: str = "https://www.is.fi/api/search"

def build_url(query: str, offset: int, limit: int, date_start: int, date_end: int) -> str:
    return f"{api}/{query}/kaikki/custom/new/{offset}/{limit}/{date_start}/{date_end}"

def main():
    args = parse_arguments()
    print(args)
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    try:
        driver = None
        if args.articles is not None:
            os.makedirs(args.articles,exist_ok=True)
        with open(args.output,"w") as of:
            co = csv.writer(of)
            co.writerow(['url','title''date_modified','lead'])
            date_start = int(datetime.timestamp(datetime.fromisoformat(args.from_date)) * 1000)
            date_end = int(datetime.timestamp((datetime.fromisoformat(args.to_date) if args.to_date is not None else datetime.now()) + timedelta(days=1)) * 1000)
            
            offset = 0
            response = requests.get(build_url(args.query,offset,args.limit,date_start,date_end))
            r = response.json()
            total_count = 0
            while True:
                if r is None:
                    logging.info("Got empty repsonse for {response.url}")
                    break
                logging.info(f"Processing {len(r)} articles from {response.url}")
                total_count += len(r)
                for a in r:
                    url = 'https://www.is.fi'+a['href']
                    title = a['title']
                    date_modified = a['displayDate']
                    lead = a['ingress'] if 'ingress' in a else ''
                    co.writerow([url,title,date_modified,lead])
                    if args.articles is not None:
                        sleep(random.randrange(args.delay*2))
                        file = os.path.join(args.articles,"art-"+str(a['id'])+".html")
                        with open(file,"w") as af:
                            article_request = requests.get(url)
                            content = article_request.content.decode("utf-8")
                            af.write("<!DOCTYPE html> <head><meta charset='utf-8'></head>" + content + "</html>")
                        logging.info(f"wrote article into {file}")
                if len(r)!=args.limit:
                    logging.info(f"Processed {len(r)} results which is less than the limit, assuming we're done {offset}.")
                    break
                else:
                    offset += args.limit
                    sleep(random.randrange(args.delay*2))
                    response = requests.get(build_url(args.query,offset,args.limit,date_start,date_end))
                    r = response.json()
    finally:
        logging.info(f"Processed totally {total_count} articles")

if __name__ == '__main__':
    main()
