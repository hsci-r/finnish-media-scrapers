#!/usr/bin/env python3
from bs4 import BeautifulSoup
from utils.HtmlToText import HtmlToText

class YleHtmlToText(HtmlToText):
    def extract(self, s: BeautifulSoup) -> str:
        output = ""
        elements = s.select('.yle__article')
        if elements is not None:
            for e in elements:
                output += e.get_text() + "\n"
        return output

if __name__ == '__main__':
    c = YleHtmlToText()
    c.main()

