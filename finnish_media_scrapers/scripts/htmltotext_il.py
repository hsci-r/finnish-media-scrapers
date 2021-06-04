#!/usr/bin/env python3

from ..htmltotext import extract_text_from_il_html
import argparse
import os
import logging
import glob
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--output-directory",help="output directory",required=True)
    parser.add_argument("input",help="input file or directory",nargs="+")
    return(parser.parse_args())

def main():
    args = parse_arguments()
    os.makedirs(args.output_directory,exist_ok=True)
    for ig in args.input:
        if os.path.isdir(ig):
            iglob = os.path.join(ig,"*.html")
        else:
            iglob = ig 
        for ifile in glob.glob(iglob):
            ofile = os.path.join(args.output_directory,Path(ifile).name).replace(".html",".txt")
            with open(ifile) as inf:
                try:
                    content = extract_text_from_il_html(inf)
                    with open(ofile,"w") as of:
                        of.write(content)
                    logging.info(f"Extracted text from {ifile} into {ofile}.")
                except ValueError:
                    logging.error(f"Couldn't extract text from {ifile}.")

if __name__ == '__main__':
    main()


