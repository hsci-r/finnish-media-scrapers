#!/usr/bin/env python3
"""Command-line script for fetching article HTML from Helsingin Sanomat
"""
# %%

import argparse
import asyncio
import csv
import logging
import os
import random
from time import sleep

from pyppeteer import launch

from ..fetch import fetch_article_hs, prepare_session_hs

logging.basicConfig(level=logging.INFO)
# %%


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="input CSV file containing articles to fetch (from query-hs.py)", required=True)
    parser.add_argument(
        '-o', '--output', help="directory to fetch articles into", required=True)
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
    browser = await launch()
    try:
        session = await browser.newPage()
        try:
            logging.info("Logging into HS.")
            await prepare_session_hs(session, args.username,
                                     args.password, args.max_web_driver_wait)
            logging.info("Logged in.")
            os.makedirs(args.output, exist_ok=True)
            with open(args.input) as input_file:
                csv_input = csv.DictReader(input_file)
                for article in csv_input:
                    url = article['url']
                    file = os.path.join(args.output, str(article['id'])+".html")
                    if not os.path.exists(file):
                        article = await fetch_article_hs(
                            session, url, args.max_web_driver_wait)
                        with open(file, "w") as article_file:
                            article_file.write(
                                "<!DOCTYPE html><head><meta charset='utf-8'></head>" + article + "</html>")
                        logging.info("Wrote article %s into %s", url, file)
                        sleep(random.randrange(args.delay*2))
                    else:
                        logging.info("Skipping %s as %s already exists.", url, file)
        finally:
            await session.close()
    finally:
        await browser.close()


def main():
    asyncio.run(_amain())


if __name__ == '__main__':
    main()
