#!/usr/bin/env python3

# %%

import os
import logging
import csv
import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

logging.basicConfig(level=logging.INFO)
# %%

import argparse
def parse_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument('-i','--input',help="input CSV file containing articles to fetch (from query-hs.py)",required=True)
  parser.add_argument('-o','--output',help="directory to fetch articles into",required=True)
  parser.add_argument('-u','--username',help="email to use for article fetching")
  parser.add_argument('-p','--password',help="password to use for article fetching")
  parser.add_argument('-d','--delay',help="number of seconds to wait between consecutive requests",default=1.0,type=float)
  parser.add_argument('--quiet', default=False, action='store_true', help="Log only errors")
  return(parser.parse_args())

def main():
    args = parse_arguments()
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    try:
        driver = None
        logging.info("Connecting to Selenium.")
        try:
            driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.CHROME)
        except:
            logging.error("Cannot download articles if Selenium is not running on localhost.")
            return
        logging.info("Logging into HS.")
        driver.get("https://www.hs.fi")
        login = driver.find_element_by_xpath("//*[contains(text(), 'Kirjaudu')]")
        driver.execute_script("arguments[0].click();", login)
        user = driver.find_element_by_id("username")
        user.send_keys(args.username)
        pas = driver.find_element_by_id("password")
        pas.send_keys(args.password),
        pas.submit()
        logging.info("Logged in.")
        os.makedirs(args.output,exist_ok=True)
        sleep(3)
        with open(args.input) as inf:
            cr = csv.DictReader(inf)
            for a in cr:
                file = os.path.join(args.output,"art-"+str(a['id'])+".html")
                if not os.path.exists(file):
                    url = a['url']
                    driver.get(url)
                    try:
                        dynamic_content = WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//div[@id='page-main-content']/following-sibling::*"))
                        if dynamic_content.tag_name == 'iframe':
                            driver.switch_to.frame(dynamic_content)
                            WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//div[@class='paywall-content']|//div[@id='paid-content']"))
                    except TimeoutException:
                        logging.warning(f"Couldn't find the dynamic content I was looking for in {url}. There may be a class of HS articles we're not yet handling.")
                    with open(file,"w") as af:
                        article = driver.find_element_by_xpath('/*').get_attribute('innerHTML')
                        af.write("<!DOCTYPE html><head><meta charset='utf-8'></head>" + article + "</html>")
                    logging.info(f"Wrote article {url} into {file}")
                else:
                    logging.info(f"Skipping {url} as {file} already exists.")
                sleep(random.randrange(args.delay*2))
    finally:
        if driver is not None:
            driver.close()
            

if __name__ == '__main__':
    main()
