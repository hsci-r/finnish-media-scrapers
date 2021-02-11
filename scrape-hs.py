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

from typing import Any, Optional, Sequence, Dict, Callable
import _csv

logging.basicConfig(level=logging.INFO)
# %%
from tap import Tap
class ArgumentParser(Tap):
    from_date: str # from date (inclusive, YYYY-MM-DD)
    to_date: Optional[str] = None # to date (inclusive, YYYY-MM-DD, defaults to today)
    query: str # query string to search for
    limit: int = 50 # number of articles to fetch per query (max==50)
    output: str # output CSV file
    delay: float = 1.0 # number of seconds to wait between consecutive requests
    articles: Optional[str] = None # directory to fetch articles into (optional)
    quiet: bool = False # Log only errors
    username: Optional[str] = None # email to use for article fetching
    password: Optional[str] = None # password to use for article fetching

api: str = "https://www.hs.fi/api/search"

def build_url(query: str, offset: int, limit: int, date_start: int, date_end: int) -> str:
    return f"{api}/{query}/kaikki/custom/new/{offset}/{limit}/{date_start}/{date_end}"

def main():
    args = ArgumentParser().parse_args()
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
            r = response.json()
            while True:
                if r is None:
                    logging.info("Got empty repsonse for {response.url}")
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
                if len(r)!=args.limit:
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