#!/usr/bin/env python3
from bs4 import BeautifulSoup
from utils.HtmlToText import HtmlToText

class IsHtmlToText(HtmlToText):
    def extract(self, s: BeautifulSoup) -> str:
        output = ""
        elements = s.select('p.article-body,article.single-article,.article--m-headline,.article-title-40')
        if elements is not None:
            for e in elements:
                output += e.get_text() + "\n"
        return output

if __name__ == '__main__':
    c = IsHtmlToText()
    c.main()
