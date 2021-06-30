#!/usr/bin/env python3
"""Command-line script for querying Helsingin Sanomat
"""


import argparse
import asyncio
import csv
import logging
import random
from datetime import datetime
from time import sleep

import aiohttp

from ..query import query_hs

logging.basicConfig(level=logging.INFO)


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--from-date',
                        help="from date (inclusive, YYYY-MM-DD)", required=True)
    parser.add_argument('-t', '--to-date', help="to date (inclusive, YYYY-MM-DD, defaults to today)",
                        default=datetime.today().strftime('%Y-%m-%d'))
    parser.add_argument(
        '-q', '--query', help="query string to search for", required=True)
    parser.add_argument(
        '-o', '--output', help="output CSV file", required=True)
    parser.add_argument(
        '-l', '--limit', help="number of articles to fetch per query (50/100)", default=100, type=int)
    parser.add_argument(
        '-d', '--delay', help="number of seconds to wait between consecutive requests", default=1.0, type=float)
    parser.add_argument('--quiet', default=False,
                        action='store_true', help="Log only errors")
    return parser.parse_args()


async def _amain():
    args = _parse_arguments()

    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    with open(args.output, "w") as output_file:
        csv_output = csv.writer(output_file)
        csv_output.writerow(['id', 'url', 'title', 'date_modified'])
        total_count = 0
        async with aiohttp.ClientSession() as session:
            async for response in query_hs(session, args.query, args.from_date, args.to_date, args.limit):
                total_count += len(response.articles)
                logging.info(
                    "Processing %d articles from %s. In total fetched %d articles.",
                    len(response.articles), response.url, total_count)
                for article in response.articles:
                    csv_output.writerow([article.id, article.url,
                                        article.title, article.date_modified])
                sleep(random.randrange(args.delay*2))
            logging.info("Processed %s articles in total.", total_count)


def main():
    asyncio.run(_amain())


if __name__ == '__main__':
    main()
