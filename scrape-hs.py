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
  parser.add_argument('-l','--limit',help="number of articles to fetch per query (50/100)",default=100,type=int)
  parser.add_argument('-d','--delay',help="number of seconds to wait between consecutive requests",default=1.0,type=float)
  parser.add_argument('--quiet', default=False, action='store_true', help="Log only errors")
  return(parser.parse_args())

api: str = "https://www.hs.fi/api/search"

def build_url(query: str, offset: int, limit: int, date_start: int, date_end: int) -> str:
    return f"{api}/{query}/kaikki/custom/new/{offset}/{limit}/{date_start}/{date_end}"

def main():
    args = parse_arguments()
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    try:
        driver = None
        if args.articles is not None:
            driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.CHROME)
            driver.get("https://www.hs.fi")
            login = driver.find_element_by_xpath("//*[contains(text(), 'Kirjaudu')]")
            driver.execute_script("arguments[0].click();", login)
            user = driver.find_element_by_id("username")
            user.send_keys(args.username)
            pas = driver.find_element_by_id("password")
            pas.send_keys(args.password),
            pas.submit()
            os.makedirs(args.articles,exist_ok=True)
        with open(args.output,"w") as of:
            co = csv.writer(of)
            co.writerow(['url','title''date_modified','lead'])
            date_start = int(datetime.timestamp(datetime.fromisoformat(args.from_date)) * 1000)
            date_end = int(datetime.timestamp((datetime.fromisoformat(args.to_date) if args.to_date is not None else datetime.now()) + timedelta(days=1)) * 1000)
            offset = 0
            response = requests.get(build_url(args.query,offset,args.limit,date_start,date_end))
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
                logging.info(f"Processing {len(r)} articles from {response.url}")
                for a in r:
                    url = 'https://www.hs.fi'+a['href']
                    title = a['title']
                    date_modified = a['displayDate']
                    lead = a['ingress'] if 'ingress' in a else ''
                    co.writerow([url,title,date_modified,lead])
                    if args.articles is not None:
                        sleep(random.randrange(args.delay*2))
                        file = os.path.join(args.articles,"art-"+str(a['id'])+".html")
                        with open(file,"w") as af:
                            driver.get(url)
                            article = WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//div[@id='page-main-content']/following-sibling::*")).get_attribute('innerHTML')
                            af.write(article)
                        logging.info(f"wrote article into {file}")
                offset += args.limit
                if offset >= 10000:
                    logging.error("HS API refuses to return more than 10000 results, which we've now crawled. You can work around this limitation by doing multiple queries on smaller timespans.")
                    break
                sleep(random.randrange(args.delay*2))
                response = requests.get(build_url(args.query,offset,args.limit,date_start,date_end))
    finally:
        if driver is not None:
            driver.close()

if __name__ == '__main__':
    main()