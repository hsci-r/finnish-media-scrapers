#!/usr/bin/env python3
"""Command-line script for fetching article HTML from openly available sources
"""

import argparse
import asyncio
import csv
import logging
import os
import random
from time import sleep

import aiohttp

logging.basicConfig(level=logging.INFO)


def _parse_arguments():
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


async def _amain():
    args = _parse_arguments()
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    os.makedirs(args.output, exist_ok=True)
    with open(args.input) as input_file:
        async with aiohttp.ClientSession() as session:
            csv_input = csv.DictReader(input_file)
            for article in csv_input:
                article_file_name = os.path.join(args.output, article['id']+".html")
                if not os.path.exists(article_file_name):
                    async with session.get(article['url']) as response:
                        content = await response.text()
                        with open(article_file_name, "w") as article_file:
                            article_file.write(content)
                    logging.info("wrote %s into %s", article['url'], article_file_name)
                    sleep(random.randrange(args.delay*2))


def main():
    asyncio.run(_amain())


if __name__ == '__main__':
    main()
