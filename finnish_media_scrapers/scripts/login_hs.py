#!/usr/bin/env python3
"""Command-line script for logging in to Helsingin Sanomat
"""
# %%

import argparse
import asyncio
import csv
import logging
import os
import random
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



from ..fetch import fetch_article_hs, prepare_session_hs

logging.basicConfig(level=logging.INFO)
# %%


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', '--username', help="email to use for article fetching", required=True)
    parser.add_argument(
        '-p', '--password', help="password to use for article fetching", required=True)
    parser.add_argument('-mw', '--max-web-driver-wait',
                        help="maximum time in seconds to wait for the webdriver to render a page before failing (default 30)", default=30, type=int)
    parser.add_argument(
        '-d', '--delay', help="number of seconds to wait between consecutive requests (default 1.0)", default=1.0, type=float)
    parser.add_argument('--quiet', default=False,
                        action='store_true', help="Log only errors")
    return parser.parse_args()


async def _amain():
    args = _parse_arguments()
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        #driver = webdriver.Chrome(options=chrome_options, 
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.implicitly_wait(10)
        try:
            driver.get("https://www.hs.fi/")
            cookies_frame = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//iframe[@title='SP Consent Message']")))
            driver.switch_to.frame(cookies_frame)
            ok_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='OK']")))
            ok_button.click()
            driver.switch_to.default_content()
            login = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Kirjaudu')]")))
            login.click()

            user = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "username")))
            user.send_keys(args.username)

            passw = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "password")))
            passw.send_keys(args.password)

            submit = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type=submit]")))
            submit.click()

            cookies = driver.get_cookies()
            print(cookies)

            
        finally:
            print("closed")
    finally:
        print("finished")


def main():
    asyncio.run(_amain())


if __name__ == '__main__':
    main()