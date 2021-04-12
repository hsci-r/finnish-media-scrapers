from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import argparse
import os
import logging
import glob
from pathlib import Path

class HtmlToText(ABC):

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-o","--output-directory",help="output directory",required=True)
        parser.add_argument("input",help="input file or directory",nargs="+")
        return(parser.parse_args())

    @abstractmethod
    def extract(self,soup: BeautifulSoup) -> str:
        pass

    def main(self) -> None:
        logging.basicConfig(level=logging.INFO)
        args = self.parse_arguments()
        os.makedirs(args.output_directory,exist_ok=True)
        for ig in args.input:
            if os.path.isdir(ig):
                iglob = os.path.join(ig,"*.html")
            else:
                iglob = ig 
            for ifile in glob.glob(iglob):
                ofile = os.path.join(args.output_directory,Path(ifile).name).replace(".html",".txt")
                with open(ifile) as inf:
                    s = BeautifulSoup(inf,'lxml')
                    content = self.extract(s)
                    with open(ofile,"w") as of:
                        of.write(content)
                    logging.info(f"Extracted text from {ifile} into {ofile}.")

