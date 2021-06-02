#!/usr/bin/env python3
from bs4 import BeautifulSoup,NavigableString
from utils.HtmlToText import HtmlToText

class IlHtmlToText(HtmlToText):
    def _extract(self, s: BeautifulSoup) -> str:
        s = s.select_one('.article-content')
        if s is not None:
            for tag in ['h1','h2','h3','h4','h5','h6','h7','p','div']:
                for p in s.find_all(tag):
                    p.insert_after(NavigableString('\n\n'))
            return s.get_text()
        else:
            return ""

if __name__ == '__main__':
    c = IlHtmlToText()
    c.main()
