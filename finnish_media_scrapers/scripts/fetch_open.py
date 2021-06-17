#!/usr/bin/env python3
"""Command-line script for fetching article HTML from openly available sources
"""

import argparse
import csv
import logging
import os
import random
from time import sleep

import requests

logging.basicConfig(level=logging.INFO)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', help="input CSV file containing articles to fetch (from query-il, query-is or query-yle)", required=True)
    parser.add_argument(
        '-o', '--output', help="directory to fetch articles into", required=True)
    parser.add_argument(
        '-d', '--delay', help="number of seconds to wait between consecutive requests", default=1.0, type=float)
    parser.add_argument('--quiet', default=False,
                        action='store_true', help="Log only errors")
    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    os.makedirs(args.output, exist_ok=True)
    with open(args.input) as input_file:
        csv_input = csv.DictReader(input_file)
        for article in csv_input:
            article_file_name = os.path.join(args.output, article['id']+".html")
            if not os.path.exists(article_file_name):
                with open(article_file_name, "wb") as article_file:
                    article_file.write(requests.get(article['url']).content)
                logging.info("wrote %s into %s", article['url'], article_file_name)
                sleep(random.randrange(args.delay*2))


if __name__ == '__main__':
    main()
