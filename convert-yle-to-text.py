#!/usr/bin/env python3
from bs4 import BeautifulSoup,NavigableString
from utils.HtmlToText import HtmlToText
import logging

class YleHtmlToText(HtmlToText):
    def extract(self, s: BeautifulSoup) -> str:
        e = s.select_one('.yle__article')
        if e is None:
            e = s.select_one('#yle__section--article')
        if e is None:
            e = s.select_one('article.content')
        if e is not None:
            for tag in ['h1','h2','h3','h4','h5','h6','h7','p','div']:
                for p in e.find_all(tag):
                    p.insert_after(NavigableString('\n\n'))
            return e.get_text()
        else:
            return "" 

if __name__ == '__main__':
    c = YleHtmlToText()
    c.main()

