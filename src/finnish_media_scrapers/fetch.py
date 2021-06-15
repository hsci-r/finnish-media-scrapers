from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from typing import Union

#  Scraping of the other sources can be done just using requests, but HS needs a user to be logged in, as well as renders their articles using dynamic javascript, thus requiring a Selenium session to enable fetching the articles.

def prepare_session_hs(driver: Union[webdriver.Remote,webdriver.Firefox,webdriver.Chrome,webdriver.Opera], username: str, password: str):
    """Prepare a Selenium session for scraping articles from Helsingin Sanomat by logging in using the provided user id and password.

    Args:
        driver (Union[webdriver.Remote,webdriver.Firefox,webdriver.Chrome,webdriver.Opera]): the Selenium session to use
        username (str): the username to log in as
        password (str): the password to use for logging in
    """
    driver.get("https://www.hs.fi")
    cookies_frame = WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//iframe[@title='SP Consent Message']"))
    driver.switch_to.frame(cookies_frame)
    ok_button = WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//button[@title='OK']"))
    ok_button.click()
    driver.switch_to.default_content()
    login = WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//*[contains(text(), 'Kirjaudu')]"))
    driver.execute_script("arguments[0].click();", login)
    user = WebDriverWait(driver,30).until(lambda d: d.find_element_by_id("username"))
    user.send_keys(username)
    pas = driver.find_element_by_id("password")
    pas.send_keys(password),
    pas.submit()

def fetch_article_hs(driver: Union[webdriver.Remote,webdriver.Firefox,webdriver.Chrome,webdriver.Opera],url:str) -> str:
    """Fetch the HTML of a single article using a Selenium session where prepare_session_hs has been called before.

    Args:
        driver (Union[webdriver.Remote,webdriver.Firefox,webdriver.Chrome,webdriver.Opera]): the Selenium session to use.
        url (str): the HS article URL to fetch article content from

    Raises:
        ValueError: If parsing the article fails, probably due to encountering a prevously unknown layout

    Returns:
        str: the HTML of the article
    """
    driver.get(url)
    try:
        dynamic_content = WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//div[@id='page-main-content']/following-sibling::*"))
        if dynamic_content.tag_name == 'iframe':
            driver.switch_to.frame(dynamic_content)
            WebDriverWait(driver,30).until(lambda d: d.find_element_by_xpath("//div[@class='paywall-content']|//div[@id='paid-content']"))
    except TimeoutException:
        raise ValueError(f"Couldn't find the dynamic content I was looking for in {url}. There may be a class of HS articles we're not yet handling.")
    article = driver.find_element_by_xpath('/*').get_attribute('innerHTML')
    return(article)
