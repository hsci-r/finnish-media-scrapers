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

            print("sent keys")

            submit = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type=submit]")))
            submit.click()

            print("submitted")

            sleep(2)
            
            #WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "#ddStyleCaptchaBody1647967644328")))
            #WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[z-index="2147483647"]')))
           # print(driver.find_element_by_css_selector('[z-index="2147483647"]'))

            #divs = driver.find_elements_by_tag_name('div')
            #for d in divs:
            #    print(d.get_attribute('innerHTML'))


            print("Captcha opened")
            while True:
                try:
                    res = driver.find_element_by_css_selector('div[style="height:100vh;width:100%;position:absolute;top:0;left:0;z-index:2147483647;background-color:#ffffff;"]')
                    html = res.get_attribute('innerHTML')
                    if "iframe" not in html:
                        break
                except:
                    break
                sleep(2)

            print("Captcha closed")

            user = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, "username")))
            user.send_keys(args.username)

            passw = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "password")))
            passw.send_keys(args.password)

            print("sent keys")

            submit = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type=submit]")))
            submit.click()

            cookies = driver.get_cookies()
            print(cookies)
            
            '''

            captcha = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID ,"recaptcha-anchor")))

  

            cookies = driver.get_cookies()
            print(cookies)

            elem = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "captcha__human__title")) 
            )

            second = driver.find_elements_by_tag_name('iframe')[1]
            driver.switch_to.frame(second)
            

            #captcha_frame = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//iframe[@title='reCAPTCHA']")))
            #driver.switch_to.frame(captcha_frame)
            captcha = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID ,"recaptcha-anchor")))
            captcha.click()
            '''

            
        finally:
            print("closed")
    finally:
        print("finished")


def main():
    asyncio.run(_amain())


if __name__ == '__main__':
    main()