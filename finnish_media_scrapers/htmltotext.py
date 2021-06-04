from bs4 import BeautifulSoup,NavigableString
import re
from typing import Union, TextIO

def extract_text_from_svyle_html(html: Union[str,TextIO]) -> str:
    """Extract article text from Svenska YLE article HTML

    Args:
        html (Union[str,TextIO]): a string or a file-like object containing the article HTML

    Raises:
        ValueError: The layout of the article was not recognized, or the article parsed as empty

    Returns:
        str: article text
    """
    s = BeautifulSoup(html,'lxml')
    e = s.select_one('article#main-content')
    if e is None:
        raise ValueError("Article layout not recognized")
    for r in s.select('aside#id-article__tags'):
        r.extract()
    for r in s.select('#comments'):
        r.extract()
    for r in s.select('.ydd-share-buttons'):
        r.extract()

    for tag in ['h1','h2','h3','h4','h5','h6','h7','p','div']:
        for p in e.find_all(tag):
            p.insert_after(NavigableString('\n\n'))
    txt= e.get_text().strip()
    if txt == "":
        raise ValueError("Parsing results in an empty article")
    return(txt)

def extract_text_from_yle_html(html: Union[str,TextIO]) -> str:
    """Extract article text from YLE article HTML

    Args:
        html (Union[str,TextIO]): a string or a file-like object containing the article HTML

    Raises:
        ValueError: The layout of the article was not recognized, or the article parsed as empty

    Returns:
        str: article text
    """
    s = BeautifulSoup(html,'lxml')
    e = s.select_one('.yle__article')
    if e is None:
        e = s.select_one('#yle__section--article')
    if e is None:
        e = s.select_one('article.content')
    if e is None:
        raise ValueError("Article layout not recognized")
    for tag in ['h1','h2','h3','h4','h5','h6','h7','p','div']:
        for p in e.find_all(tag):
            p.insert_after(NavigableString('\n\n'))
    txt= e.get_text().strip()
    if txt == "":
        raise ValueError("Parsing results in an empty article")
    return(txt)

def extract_text_from_is_html(html: Union[str,TextIO]) -> str:
    """Extract article text from Ilta-Sanomat article HTML

    Args:
        html (Union[str,TextIO]): a string or a file-like object containing the article HTML

    Raises:
        ValueError: The layout of the article was not recognized, or the article parsed as empty

    Returns:
        str: article text
    """
    s = BeautifulSoup(html,'lxml')
    e = s.select_one('article.single-article,article.article--m,article.article--l,article.article--xl-picture-top,article.article--xl-title-top')
    if e is None:
        raise ValueError("Article layout not recognized")
    for tag in ['h1','h2','h3','h4','h5','h6','h7','p','div']:
        for p in e.find_all(tag):
            p.insert_after(NavigableString('\n\n'))
    txt= e.get_text().strip()
    if txt == "":
        raise ValueError("Parsing results in an empty article")
    return(txt)

def extract_text_from_il_html(html: Union[str,TextIO]) -> str:
    """Extract article text from Iltalehti article HTML

    Args:
        html (Union[str,TextIO]): a string or a file-like object containing the article HTML

    Raises:
        ValueError: The layout of the article was not recognized, or the article parsed as empty

    Returns:
        str: article text
    """
    s = BeautifulSoup(html,'lxml')
    s = s.select_one('.article-content')
    if s is None:
        raise ValueError("Article layout not recognized")
    for tag in ['h1','h2','h3','h4','h5','h6','h7','p','div']:
        for p in s.find_all(tag):
            p.insert_after(NavigableString('\n\n'))
    txt = s.get_text().strip()
    if txt == "":
        raise ValueError("Parsing results in an empty article")
    return(txt)

def extract_text_from_hs_html(html: Union[str,TextIO]) -> str:
    """Extract article text from Helsingin Sanomat article HTML

    Args:
        html (Union[str,TextIO]): a string or a file-like object containing the article HTML

    Raises:
        ValueError: The layout of the article was not recognized, or the article parsed as empty

    Returns:
        str: article text
    """
    s = BeautifulSoup(html,'lxml')
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
    return(txt)