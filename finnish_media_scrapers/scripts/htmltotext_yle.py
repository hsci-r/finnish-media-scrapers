#!/usr/bin/env python3
"""Command-line script for converting YLE HTML into plain text
"""

import argparse
import glob
import logging
import os
from pathlib import Path

from ..htmltotext import extract_text_from_yle_html

logging.basicConfig(level=logging.INFO)


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output-directory",
                        help="output directory", required=True)
    parser.add_argument("input", help="input file or directory", nargs="+")
    return parser.parse_args()


def main():
    args = _parse_arguments()
    os.makedirs(args.output_directory, exist_ok=True)
    for input_spec in args.input:
        if os.path.isdir(input_spec):
            input_files_glob = os.path.join(input_spec, "*.html")
        else:
            input_files_glob = input_spec
        for input_file_name in glob.glob(input_files_glob):
            output_file_name = os.path.join(args.output_directory, Path(
                input_file_name).name).replace(".html", ".txt")
            with open(input_file_name) as input_file:
                try:
                    content = extract_text_from_yle_html(input_file)
                    with open(output_file_name, "w") as output_file:
                        output_file.write(content)
                    logging.info("Extracted text from %s into %s.",
                                 input_file_name, output_file_name)
                except ValueError:
                    logging.error("Couldn't extract text from %s.", input_file_name)


if __name__ == '__main__':
    main()
