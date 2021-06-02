#!/usr/bin/env python3
from bs4 import BeautifulSoup,NavigableString
from utils.HtmlToText import HtmlToText

class IsHtmlToText(HtmlToText):
    def _extract(self, s: BeautifulSoup) -> str:
        output = ""
        e = s.select_one('article.single-article,article.article--m,article.article--l,article.article--xl-picture-top,article.article--xl-title-top')
        if e is not None:
            for tag in ['h1','h2','h3','h4','h5','h6','h7','p','div']:
                for p in e.find_all(tag):
                    p.insert_after(NavigableString('\n\n'))
            return e.get_text()
        else:
            return ""

if __name__ == '__main__':
    c = IsHtmlToText()
    c.main()
