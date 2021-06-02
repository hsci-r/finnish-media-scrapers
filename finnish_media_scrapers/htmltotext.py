from bs4 import BeautifulSoup,NavigableString
import re
from typing import Union, TextIO

def extract_text_from_hs_html(html: Union[str,TextIO]) -> str:
    """extract article text from Helsingin Sanomat article HTML

    Args:
        html (Union[str,TextIO]): a string or a file-like object containing the article HTML

    Raises:
        ValueError: The layout of the article was not recognized, or the article parsed as empty

    Returns:
        str: article text
    """
    s = BeautifulSoup(html)
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
                raise ValueError("Article layout not recognized")
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
    txt = txt.strip()
    if txt == "":
        raise ValueError("Parsing results in an empty article")
    return txt