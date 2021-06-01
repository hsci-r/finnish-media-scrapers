
#!/usr/bin/env python3
from bs4 import BeautifulSoup,NavigableString
from utils.HtmlToText import HtmlToText
import logging

class SvenskaYleHtmlToText(HtmlToText):
    def extract(self, s: BeautifulSoup) -> str:
        e = s.select_one('article#main-content')
        if e is not None:
            for r in s.select('aside#id-article__tags'):
                r.extract()
            for r in s.select('#comments'):
                r.extract()
            for r in s.select('.ydd-share-buttons'):
                r.extract()

            for tag in ['h1','h2','h3','h4','h5','h6','h7','p','div']:
                for p in e.find_all(tag):
                    p.insert_after(NavigableString('\n\n'))
            return e.get_text()
        else:
            return "" 

if __name__ == '__main__':
    c = SvenskaYleHtmlToText()
    c.main()


