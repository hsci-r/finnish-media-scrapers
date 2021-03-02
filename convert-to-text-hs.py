#!/usr/bin/env python3

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
            e = s.find('main')
            if e is not None:
                s = e
            e = s.select_one('div#page-main-content + article')
            if e is not None:
                s = e
            for e in s.find_all('aside'):
                e.extract()
            for e in s.select('section.article-body + div'):
                e.extract()
            for r in s.select('div.article-info'):
                r.extract()
            for r in s.select('div.related-articles'):
                r.extract()
            for r in s.select('div.article-actions'):
                r.extract()
            for tag in ['h1','h2','h3','h4','h5','h6','h7','p','div']:
                for p in s.find_all(tag):
                    p.insert_after(NavigableString('\n\n'))
            txt = s.get_text()
            txt = txt.replace("\xad", "")
            txt = re.sub("\n\n+","\n\n",txt)
            with open(ofile,"w") as of:
                of.write(txt)
            logging.info(f"Extracted text from {ifile} into {ofile}.")

if __name__ == '__main__':
    main()
