#!/usr/bin/env python3
from bs4 import BeautifulSoup
from utils.HtmlToText import HtmlToText

class IlHtmlToText(HtmlToText):
    def extract(self, s: BeautifulSoup) -> str:
        output = ""
        elements = s.select('.article-description-pov-text,.article-description,.article-headline,.paragraph,h3,h1,h2')
        if elements is not None:
            for e in elements:
                output += e.get_text() + "\n"
        return output

if __name__ == '__main__':
    c = IlHtmlToText()
    c.main()