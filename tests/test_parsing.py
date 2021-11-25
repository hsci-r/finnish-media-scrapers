"""Regression and defensive programming tests for finnish-media-scrapers
"""

import pytest

from finnish_media_scrapers.htmltotext import (extract_text_from_hs_html,
                                               extract_text_from_il_html,
                                               extract_text_from_is_html,
                                               extract_text_from_svyle_html,
                                               extract_text_from_yle_html)

# %%


def remove_content(input_file, output_file):
    """Utility function to remove all content from HTML articles so that no IPR problems remain when using them in tests"""
    from bs4 import BeautifulSoup
    with open(input_file) as inf, open(output_file, 'w') as outf:
        soup = BeautifulSoup(inf, 'lxml')
        for text_node in soup.find_all(text=True):
            text_node.replace_with("TEXT")
        outf.write(str(soup))

# %%


def test_hs_parser():
    """Test parsing of various HS article formats"""

    # common page-main-content variant
    with open("tests/example_articles/hs/2000006466966-sanitized.html", encoding="utf-8") as htmlf, \
            open("tests/example_articles/hs/2000006466966-sanitized.txt", encoding="utf-8") as txtf:
        expected = txtf.read()
        assert expected == extract_text_from_hs_html(htmlf)

    # paid-content variant
    with open("tests/example_articles/hs/2000006560604-sanitized.html", encoding="utf-8") as htmlf, \
            open("tests/example_articles/hs/2000006560604-sanitized.txt", encoding="utf-8") as txtf:
        expected = txtf.read()
        assert expected == extract_text_from_hs_html(htmlf)

    # nuxt variant
    with open("tests/example_articles/hs/2000006585357-sanitized.html", encoding="utf-8") as htmlf, \
            open("tests/example_articles/hs/2000006585357-sanitized.txt", encoding="utf-8") as txtf:
        expected = txtf.read()
        assert expected == extract_text_from_hs_html(htmlf)


def test_yle_parser():
    """Test parsing of various YLE article formats"""

    # common .yle__article variant
    with open("tests/example_articles/yle/3-11222287-sanitized.html", encoding="utf-8") as htmlf, \
            open("tests/example_articles/yle/3-11222287-sanitized.txt", encoding="utf-8") as txtf:
        expected = txtf.read()
        assert expected == extract_text_from_yle_html(htmlf)

    # .yle__section--article variant
    with open("tests/example_articles/yle/3-11609882-sanitized.html", encoding="utf-8") as htmlf, \
            open("tests/example_articles/yle/3-11609882-sanitized.txt", encoding="utf-8") as txtf:
        expected = txtf.read()
        assert expected == extract_text_from_yle_html(htmlf)

    # article.content variant
    with open("tests/example_articles/yle/3-11173365-sanitized.html", encoding="utf-8") as htmlf, \
            open("tests/example_articles/yle/3-11173365-sanitized.txt", encoding="utf-8") as txtf:
        expected = txtf.read()
        assert expected == extract_text_from_yle_html(htmlf)


def test_svyle_parser():
    """Test parsing of various Svenska YLE article formats"""

    # common page-main-content variant
    with open("tests/example_articles/svyle/7-1456870-sanitized.html", encoding="utf-8") as htmlf, \
            open("tests/example_articles/svyle/7-1456870-sanitized.txt", encoding="utf-8") as txtf:
        expected = txtf.read()
        assert expected == extract_text_from_svyle_html(htmlf)


def test_il_parser():
    """Test parsing of various IL article formats"""

    # .article-content variant
    with open("tests/example_articles/il/52ae7095-adf3-4430-a603-3bebff5f79f2-sanitized.html", encoding="utf-8") as htmlf, \
            open("tests/example_articles/il/52ae7095-adf3-4430-a603-3bebff5f79f2-sanitized.txt", encoding="utf-8") as txtf:
        expected = txtf.read()
        assert expected == extract_text_from_il_html(htmlf)


def test_is_parser():
    """Test parsing of various IS article formats"""

    # .single-article variant
    with open("tests/example_articles/is/2000006436350-sanitized.html", encoding="utf-8") as htmlf, \
            open("tests/example_articles/is/2000006436350-sanitized.txt", encoding="utf-8") as txtf:
        expected = txtf.read()
        assert expected == extract_text_from_is_html(htmlf)

    # .article--m variant
    with open("tests/example_articles/is/2000006456837-sanitized.html", encoding="utf-8") as htmlf, \
            open("tests/example_articles/is/2000006456837-sanitized.txt", encoding="utf-8") as txtf:
        expected = txtf.read()
        assert expected == extract_text_from_is_html(htmlf)

    # .article--l variant
    with open("tests/example_articles/is/2000007693397-sanitized.html", encoding="utf-8") as htmlf, \
            open("tests/example_articles/is/2000007693397-sanitized.txt", encoding="utf-8") as txtf:
        expected = txtf.read()
        assert expected == extract_text_from_is_html(htmlf)

    # .article--xl-picture-top variant
    with open("tests/example_articles/is/2000006365914-sanitized.html", encoding="utf-8") as htmlf, \
            open("tests/example_articles/is/2000006365914-sanitized.txt", encoding="utf-8") as txtf:
        expected = txtf.read()
        assert expected == extract_text_from_is_html(htmlf)

    # .article--xl-title-top variant
    with open("tests/example_articles/is/2000006562357-sanitized.html", encoding="utf-8") as htmlf, \
            open("tests/example_articles/is/2000006562357-sanitized.txt", encoding="utf-8") as txtf:
        expected = txtf.read()
        assert expected == extract_text_from_is_html(htmlf)


def test_defensive_parsing():
    with open("tests/example_articles/is/2000006436350-sanitized.html", encoding="utf-8") as htmlf:
        article = htmlf.read()
        with pytest.raises(ValueError):
            extract_text_from_il_html(article)
        with pytest.raises(ValueError):
            extract_text_from_yle_html(article)
        with pytest.raises(ValueError):
            extract_text_from_svyle_html(article)
    with open("tests/example_articles/svyle/7-1456870-sanitized.html", encoding="utf-8") as htmlf:
        article = htmlf.read()
        with pytest.raises(ValueError):
            extract_text_from_hs_html(article)
        with pytest.raises(ValueError):
            extract_text_from_is_html(article)
