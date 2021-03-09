#!/usr/bin/env python3

# %%

import requests
import logging
import csv
import random
from datetime import datetime, timedelta
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
  parser.add_argument('-l','--limit',help="number of articles to fetch per query (50/100)",default=100,type=int)
  parser.add_argument('-d','--delay',help="number of seconds to wait between consecutive requests",default=1.0,type=float)
  parser.add_argument('--quiet', default=False, action='store_true', help="Log only errors")
  return(parser.parse_args())

api: str = "https://www.hs.fi/api/search"

def build_url(query: str, offset: int, limit: int, date_start: int, date_end: int) -> str:
    return f"{api}/{query}/kaikki/custom/new/{offset}/{limit}/{date_start}/{date_end}"

def main():
    args = parse_arguments()
    date_start = int(datetime.timestamp(datetime.fromisoformat(args.from_date)) * 1000)
    date_end = int(datetime.timestamp((datetime.fromisoformat(args.to_date) if args.to_date is not None else datetime.now()) + timedelta(days=1)) * 1000)
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    response = requests.get(build_url(args.query,9950,50,date_start,date_end))
    if response.status_code != 200:
        logging.error(f"Got unexpected response code {response.status_code} for {response.url}.")
        return
    r = response.json()
    if len(r)!=0:
        logging.error("Query results in more than 9950 results. The HS API refuses to return more than 10000 results, so refusing to continue. You can work around this limitation by doing multiple queries on smaller timespans.")
        return
    with open(args.output,"w") as of:
        co = csv.writer(of)
        co.writerow(['id','url','title''date_modified','lead'])
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
            if len(r)==0:
                logging.info(f"Got 0 results, assuming we're done.")
                break
            total_count += len(r)
            logging.info(f"Processing {len(r)} articles from {response.url}")
            for a in r:
                url = 'https://www.hs.fi'+a['href']
                title = a['title']
                date_modified = a['displayDate']
                lead = a['ingress'] if 'ingress' in a else ''
                id = a['id']
                co.writerow([id,url,title,date_modified,lead])
            offset += args.limit
            sleep(random.randrange(args.delay*2))
            response = requests.get(build_url(args.query,offset,args.limit,date_start,date_end))
        logging.info(f"Processed {total_count} articles in total.")            

if __name__ == '__main__':
    main()
