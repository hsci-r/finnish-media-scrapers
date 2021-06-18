"""Functions to extract article plain texts from the YLE/HS/IL/IS HTML articles
"""
import re
from typing import TextIO, Union

from bs4 import BeautifulSoup, NavigableString


def extract_text_from_svyle_html(html: Union[str, TextIO]) -> str:
    """Extract article text from Svenska YLE article HTML

    Args:
        html (Union[str,TextIO]): a string or a file-like object containing the article HTML

    Raises:
        ValueError: The layout of the article was not recognized, or the article parsed as empty

    Returns:
        str: article text
    """
    soup = BeautifulSoup(html, 'lxml')
    elem = soup.select_one('article#main-content')
    if elem is None:
        raise ValueError("Article layout not recognized")
    for elem_to_remove in soup.select('aside#id-article__tags'):
        elem_to_remove.extract()
    for elem_to_remove in soup.select('#comments'):
        elem_to_remove.extract()
    for elem_to_remove in soup.select('.ydd-share-buttons'):
        elem_to_remove.extract()

    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p', 'div']:
        for block_elem in elem.find_all(tag):
            block_elem.insert_after(NavigableString('\n\n'))
    txt = elem.get_text().strip()
    if txt == "":
        raise ValueError("Parsing results in an empty article")
    return txt


def extract_text_from_yle_html(html: Union[str, TextIO]) -> str:
    """Extract article text from YLE article HTML

    Args:
        html (Union[str,TextIO]): a string or a file-like object containing the article HTML

    Raises:
        ValueError: The layout of the article was not recognized, or the article parsed as empty

    Returns:
        str: article text
    """
    soup = BeautifulSoup(html, 'lxml')
    elem = soup.select_one('.yle__article')
    if elem is None:
        elem = soup.select_one('#yle__section--article')
    if elem is None:
        elem = soup.select_one('article.content')
    if elem is None:
        raise ValueError("Article layout not recognized")
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p', 'div']:
        for block_elem in elem.find_all(tag):
            block_elem.insert_after(NavigableString('\n\n'))
    txt = elem.get_text().strip()
    if txt == "":
        raise ValueError("Parsing results in an empty article")
    return txt


def extract_text_from_is_html(html: Union[str, TextIO]) -> str:
    """Extract article text from Ilta-Sanomat article HTML

    Args:
        html (Union[str,TextIO]): a string or a file-like object containing the article HTML

    Raises:
        ValueError: The layout of the article was not recognized, or the article parsed as empty

    Returns:
        str: article text
    """
    soup = BeautifulSoup(html, 'lxml')
    elem = soup.select_one(
        'article.single-article,article.article--m,article.article--l,article.article--xl-picture-top,article.article--xl-title-top')
    if elem is None:
        raise ValueError("Article layout not recognized")
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p', 'div']:
        for block_elem in elem.find_all(tag):
            block_elem.insert_after(NavigableString('\n\n'))
    txt = elem.get_text().strip()
    if txt == "":
        raise ValueError("Parsing results in an empty article")
    return txt


def extract_text_from_il_html(html: Union[str, TextIO]) -> str:
    """Extract article text from Iltalehti article HTML

    Args:
        html (Union[str,TextIO]): a string or a file-like object containing the article HTML

    Raises:
        ValueError: The layout of the article was not recognized, or the article parsed as empty

    Returns:
        str: article text
    """
    soup = BeautifulSoup(html, 'lxml')
    soup = soup.select_one('.article-content')
    if soup is None:
        raise ValueError("Article layout not recognized")
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p', 'div']:
        for block_elem in soup.find_all(tag):
            block_elem.insert_after(NavigableString('\n\n'))
    txt = soup.get_text().strip()
    if txt == "":
        raise ValueError("Parsing results in an empty article")
    return txt


def extract_text_from_hs_html(html: Union[str, TextIO]) -> str:
    """Extract article text from Helsingin Sanomat article HTML

    Args:
        html (Union[str,TextIO]): a string or a file-like object containing the article HTML

    Raises:
        ValueError: The layout of the article was not recognized, or the article parsed as empty

    Returns:
        str: article text
    """
    soup = BeautifulSoup(html, 'lxml')
    elem = soup.select_one('#__nuxt,article.article--xxl')
    if elem is not None:
        soup = elem
    else:
        elem = soup.find('main')
        if elem is not None:
            soup = elem
        elem = soup.select_one('div#page-main-content + article')
        if elem is not None:
            soup = elem
        else:
            elem = soup.select_one('div#page-main-content,#paid-content')
            if elem is not None:
                soup = elem
            else:
                raise ValueError("Article layout not recognized")
    for elem in soup.find_all('aside'):
        elem.extract()
    for elem in soup.select('section.article-body + div'):
        elem.extract()
    for elem_to_remove in soup.select('div.article-info'):
        elem_to_remove.extract()
    for elem_to_remove in soup.select('div.related-articles'):
        elem_to_remove.extract()
    for elem_to_remove in soup.select('div.article-actions'):
        elem_to_remove.extract()
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'p', 'div']:
        for block_elem in soup.find_all(tag):
            block_elem.insert_after(NavigableString('\n\n'))
    txt = soup.get_text()
    txt = txt.replace("\xad", "")
    txt = re.sub("\n\n+", "\n\n", txt)
    txt = txt.strip()
    if txt == "":
        raise ValueError("Parsing results in an empty article")
    return txt
