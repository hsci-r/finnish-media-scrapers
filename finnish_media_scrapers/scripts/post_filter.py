#!/usr/bin/env python3
"""Command-line script for post-filtering results from search API queries
"""
import argparse
import csv
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.INFO)


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', required=True,
        help="input CSV file containing articles to post-filter (from query-il.py, query-is.py or query-yle.py)")
    parser.add_argument(
        '-t', '--txt',
        required=True,
        help="directory containing the plain texts extracted from the articles")
    parser.add_argument(
        '-o', '--output', required=True,
        help="output CSV the contents of which will be the input CSV with a column added for the post-filtering result")
    parser.add_argument('-q', '--query-strings',
                        help="query strings to search for", nargs="+")
    parser.add_argument('-ci', '--case-insensitive', default=False,
                        action='store_true', help="compare without regard to upper or lower case")
    parser.add_argument('--quiet', default=False,
                        action='store_true', help="Log only errors")
    return parser.parse_args()


def main():
    args = _parse_arguments()
    query_strings = args.query_strings
    if args.case_insensitive:
        query_strings = map(query_strings, lambda l: l.lower())
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    with open(args.input) as inf, open(args.output, 'w') as outf:
        csv_input = csv.DictReader(inf)
        csv_output = csv.DictWriter(outf, [*csv_input.fieldnames, 'matches'])
        csv_output.writeheader()
        for article in csv_input:
            txt = Path(os.path.join(args.txt, article['id']+'.txt')).read_text()
            if args.case_insensitive:
                txt = txt.lower()
            matches = 0
            for query_string in query_strings:
                matches = matches + txt.count(query_string)
            csv_output.writerow({**article, 'matches': matches})


if __name__ == '__main__':
    main()
