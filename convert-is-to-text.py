from bs4 import BeautifulSoup, NavigableString
import argparse
import os
import logging
import glob
import re
from pathlib import Path

logging.basicConfig(level=logging.INFO)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--input-directory",help="input directory",required=True)
    parser.add_argument("-o","--output-directory",help="output directory",required=True)
    return(parser.parse_args())

def main() -> None:
    args = parse_arguments()
    os.makedirs(args.output_directory,exist_ok=True)
    iglob = os.path.join(args.input_directory,"*.html")
    for ifile in glob.glob(iglob):
        ofile = os.path.join(args.output_directory,Path(ifile).name).replace(".html",".txt")
        with open(ifile) as inf:
            s = BeautifulSoup(inf,'lxml')
            output = ""
            elements = s.select('p.article-body,.article--m-headline,.article-title-40')
            if elements is not None:
                for e in elements:
                    output += e.get_text() + "\n"
            

            with open(ofile,"w") as of:
                of.write(output)
            logging.info(f"Extracted text from {ifile} into {ofile}.")

if __name__ == '__main__':
    main()