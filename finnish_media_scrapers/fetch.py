"""Utilities for fetching articles.
Currently only affects Helsingin Sanomat. Scraping of the other sources can be done just using requests,
but HS needs a user to be logged in, as well as renders their articles using dynamic javascript,
thus requiring a Selenium session to enable fetching the articles.
"""

from pyppeteer.browser import Page


async def prepare_session_hs(
        session: Page,
        username: str, password: str, max_web_driver_wait: int = 30):
    """Prepare a pyppeteer session for scraping articles from Helsingin Sanomat
    by logging in using the provided user id and password.

    Raises:
        TimeoutError: if the web driver is unable to find the elements it is looking for in 30 seconds.
                      May indicate changes to the loging page structure.

    Args:
        session (Page): the pyppeteer session to use
        username (str): the username to log in as
        password (str): the password to use for logging in
        max_web_driver_wait (int): the maximum number of seconds to wait for the webdriver to
                                   render a page before failing (default: 30)

    """
    max_web_driver_wait = 1000 * max_web_driver_wait
    await session.goto("https://www.hs.fi", timeout=max_web_driver_wait)
    cookies_frame = await session.waitForXPath("//iframe[@title='SP Consent Message']", timeout=max_web_driver_wait)
    frame = await cookies_frame.contentFrame()
    ok_button = await frame.waitForXPath("//button[@title='OK']", timeout=max_web_driver_wait)
    await ok_button.click()
    login = await session.waitForXPath("//*[contains(text(), 'Kirjaudu')]", timeout=max_web_driver_wait)
    await login.click()
    user = await session.waitForSelector("#username", timeout=max_web_driver_wait)
    await user.type(username)
    passw = await session.waitForSelector("#password", timeout=max_web_driver_wait)
    await passw.type(password)
    submit = await session.waitForSelector("button[type=submit]", timeout=max_web_driver_wait)
    await submit.click()
    await session.waitForNavigation()


async def fetch_article_hs(
        session: Page,
        url: str, max_web_driver_wait: int = 30) -> str:
    """Fetch the HTML of a single article using a pyppeteer session where
    prepare_session_hs has been called before.

    Args:
        session (Page): the pyppeteer session to use
        url (str): the HS article URL to fetch article content from
        max_web_driver_wait (int): the maximum number of seconds to wait for the webdriver to
                                   render a page before failing (default: 30)


    Raises:
        ValueError: If parsing the article fails, probably due to encountering a prevously unknown layout

    Returns:
        str: the HTML of the article
    """
    max_web_driver_wait = 1000 * max_web_driver_wait
    await session.goto(url, timeout=max_web_driver_wait)
    try:
        main_content = await session.waitForXPath("//div[@id='page-main-content']/following-sibling::*", timeout=max_web_driver_wait)
        tag_name = await (await main_content.getProperty('tagName')).jsonValue()
        if tag_name == 'IFRAME':
            content = await main_content.contentFrame()
            if len(await session.xpath("//div[@class='paywall-container']")) != 0:
                await session.waitForXPath("//div[@class='paywall-content']|//div[@id='paid-content']")
        else:
            content = session
    except TimeoutError as timeout_exception:
        raise ValueError(
            f"Couldn't find the dynamic content I was looking for in {url}. There may be a class of HS articles we're not yet handling."
        ) from timeout_exception
    article = await content.content()
    return article
