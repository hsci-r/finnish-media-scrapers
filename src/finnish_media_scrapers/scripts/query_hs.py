#!/usr/bin/env python3

from ..query import query_hs
import logging
from datetime import datetime,timedelta
import argparse
import csv
from time import sleep
import random

logging.basicConfig(level=logging.INFO)

def parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('-f','--from-date',help="from date (inclusive, YYYY-MM-DD)",required=True)
  parser.add_argument('-t','--to-date',help="to date (inclusive, YYYY-MM-DD, defaults to today)",default=datetime.today().strftime('%Y-%m-%d'))
  parser.add_argument('-q','--query',help="query string to search for",required=True)
  parser.add_argument('-o','--output',help="output CSV file",required=True)
  parser.add_argument('-l','--limit',help="number of articles to fetch per query (50/100)",default=100,type=int)
  parser.add_argument('-d','--delay',help="number of seconds to wait between consecutive requests",default=1.0,type=float)
  parser.add_argument('--quiet', default=False, action='store_true', help="Log only errors")
  return(parser.parse_args())

def main():
    args = parse_arguments()
    
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    with open(args.output,"w") as of:
        co = csv.writer(of)
        co.writerow(['id','url','title','date_modified'])
        total_count = 0
        for response in query_is(args.query,args.from_date,args.to_date,args.limit):
            total_count += len(response.articles)
            logging.info(f"Processing {len(response.articles)} articles from {response.url}. In total fetched {total_count} articles.")
            for article in response.articles:
                co.writerow([article.id,article.url,article.title,article.date_modified])
            sleep(random.randrange(args.delay*2))
        logging.info(f"Processed {total_count} articles in total.")

if __name__ == '__main__':
    main()
    
