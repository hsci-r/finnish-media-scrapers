#!/usr/bin/env python3

# %%

import os
from ..fetch import prepare_session_hs,fetch_article_hs
import logging
import csv
import random
from time import sleep

from selenium import webdriver

logging.basicConfig(level=logging.INFO)
# %%

import argparse
def parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i','--input',help="input CSV file containing articles to fetch (from query-hs.py)",required=True)
  parser.add_argument('-o','--output',help="directory to fetch articles into",required=True)
  parser.add_argument('-u','--username',help="email to use for article fetching",required=True)
  parser.add_argument('-p','--password',help="password to use for article fetching",required=True)
  parser.add_argument('-mw','--max-web-driver-wait',help="maximum time in seconds to wait for the webdriver to render a page before failing (default 30)",default=30,type=int)
  parser.add_argument('-w','--web-driver',help="the Selenium web driver to use (out of remote [default],chrome,firefox)",default="remote")
  parser.add_argument('-d','--delay',help="number of seconds to wait between consecutive requests (default 1.0)",default=1.0,type=float)
  parser.add_argument('--quiet', default=False, action='store_true', help="Log only errors")
  return(parser.parse_args())

def main():
    args = parse_arguments()
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    try:
        if args.web_driver == 'remote':
            try:
                driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.CHROME)
            except:
                logging.error("Cannot download articles if Selenium is not running on localhost. (e.g. docker run -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:4.0.0-beta-1-20210215)")
                return
        elif args.web_driver == 'chrome':
            driver = webdriver.Chrome()
        elif args.web_driver == 'firefox':
            driver = webdriver.Firefox()
        else:
            logging.error("Unknown web driver specified. Must be one of remote/chrome/firefox.")
            return
    except:
        logging.error("Couldn't initialize selected Selenium webdriver.")
        return
    try:
        logging.info("Connecting to Selenium.")
        logging.info("Logging into HS.")
        prepare_session_hs(driver,args.username,args.password,args.max_web_driver_wait)
        logging.info("Logged in.")
        sleep(3)
        os.makedirs(args.output,exist_ok=True)
        with open(args.input) as inf:
            cr = csv.DictReader(inf)
            for a in cr:
                url = a['url']
                file = os.path.join(args.output,str(a['id'])+".html")
                if not os.path.exists(file):
                    article = fetch_article_hs(driver,url,args.max_web_driver_wait)
                    with open(file,"w") as af:
                        af.write("<!DOCTYPE html><head><meta charset='utf-8'></head>" + article + "</html>")
                    logging.info(f"Wrote article {url} into {file}")
                    sleep(random.randrange(args.delay*2))
                else:
                    logging.info(f"Skipping {url} as {file} already exists.")
    finally:
        driver.close()
            
if __name__ == '__main__':
    main()
