#!/usr/bin/env python3
from bs4 import BeautifulSoup,NavigableString
from utils.HtmlToText import HtmlToText
import re

class HsHtmlToText(HtmlToText):
    def _extract(self, s: BeautifulSoup) -> str:
        e = s.select_one('#__nuxt,article.article--xxl')
        if e is not None:
            s = e
        else:
            e = s.find('main')
            if e is not None:
                s = e
            e = s.select_one('div#page-main-content + article')
            if e is not None:
                s = e
            else:
                e = s.select_one('div#page-main-content,#paid-content')
                if e is not None:
                    s = e
                else:
                    return ""
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
        return txt

if __name__ == '__main__':
    c = HsHtmlToText()
    c.main()
