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

    try:
        if args.articles is not None:
            driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.CHROME)
            os.makedirs(args.articles,exist_ok=True)
        with open(args.output,"w") as of:
            co = csv.writer(of)
            co.writerow(['url','title','date_modified'])
            #date_start = int(datetime.timestamp(datetime.fromisoformat(args['from_date'])) * 1000)
            #date_end = int(datetime.timestamp((datetime.fromisoformat(args['to_date']) if args['to_date'] is not None else datetime.now()) + timedelta(days=1)) * 1000)
            date_start = args.from_date
            date_end = args.to_date
            offset = 0
            response = requests.get(build_url(args.query,offset,args.limit,date_start,date_end))
            r = response.json()
            while True:
                if r is None:
                    logging.info("Got empty repsonse for {response.url}")
                    break
                logging.info(f"Processing {len(r)} articles from {response.url}")
                for a in r['data']:
                    url = a['url']['full']
                    title = a['headline']
                    date_modified = a['datePublished']
                    co.writerow([url,title,date_modified])
                    if args.articles is not None:
                        sleep(random.randrange(args.delay*2))
                        file = os.path.join(args.articles,"art-"+str(a['id'])+".html")
                        with open(file,"w") as af:
                            driver.get(url)
                            article = WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "yle__article__content", " " ))]')).get_attribute('innerHTML')
                            af.write(article)
                        logging.info(f"wrote article into {file}")
                if len(r['data'])!=args.limit:
                    logging.info(f"Processed {len(r)} results which is less than the limit, assuming we're done.")
                    break
                else:
                    offset += args.limit
                    sleep(random.randrange(args.delay*2))
                    response = requests.get(build_url(args.query,offset,args.limit,date_start,date_end))
                    r = response.json()
    finally:
        if driver is not None:
            driver.close()

if __name__ == '__main__':
    main()