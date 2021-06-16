import requests
from datetime import datetime,timedelta
from typing import Iterator

class Article:
    """An article

    Attributes:
        id (str): the unique id for the article
        url (str): the url from which the article may be found
        title (str): the title or headline of the article
        date_modified (str): the date of last modification for the article
    """
    def __init__(self, id: str, url: str, title: str, date_modified: str):
        self.id = id
        self.url = url
        self.title = title
        self.date_modified = date_modified

class Result:
    """A result from a single API call

    Attributes:
        articles (list[Article]): a list of the article objects returned
        url (str): the URL of the API query
        total (int): the total number of articles for the query. -1 if not available.
    """
    def __init__(self, articles: 'list[Article]', url: str, total: int = -1):
        self.articles = articles
        self.url = url
        self.total = total

yle_api: str = "https://yle-fi-search.api.yle.fi/v1/search"

def query_yle(query:str, language: str, from_date: str, to_date: str, batch_size: int = 10000) -> Iterator[Result]:
    """Query the YLE API for articles matching a query

    Args:
        query (str): the query string to search for
        language (str): language to search (either 'fi' or 'sv')
        from_date (str): date to search from (inclusive, YYYY-MM-DD)
        to_date (str): date to search to (inclusive, YYYY-MM-DD)
        batch_size (int, optional): How many entries to query for in a single API call. Maximum and default for the YLE API is 10000.

    Raises:
        ValueError: when something goes wrong in the API call

    Yields:
        Iterator[Result]: each Result contains the results from a single API call
    """
    params = {
        'app_id':'hakuylefi_v2_prod',
        'app_key':'4c1422b466ee676e03c4ba9866c0921f',
        'service':'uutiset',
        'language': language,
        'uiLanguage': language,
        'type':'article',
        'time':'custom',
        'timeFrom':from_date,
        'timeTo':to_date,
        'query':query,
        'offset':0,
        'limit':batch_size
    }
    response = requests.get(yle_api,params)
    if response.status_code != 200:
        raise ValueError(f"Got unexpected response code {response.status_code} for {response.url}.")
    r = response.json()
    if r is None:
        raise ValueError(f"Got empty response for {response.url}")
    if r['meta']['count']>10000:
        raise ValueError(f"Query results in {r['meta']['count']} results. The YLE API refuses to return more than 10000 results, so refusing to continue. You can work around this limitation by doing multiple queries on smaller timespans.")
    response = requests.get(yle_api,params)
    while True:
        if response.status_code != 200:
            raise ValueError(f"Got unexpected response code {response.status_code} for {response.url}.")
        r = response.json()
        if r is None:
            raise ValueError(f"Got empty response for {response.url}")
        if len(r['data'])==0: # Got 0 results, assuming we're done.
            break
        articles = [ Article(id=a['id'],url=a['url']['full'],title=a['headline'],date_modified=a['datePublished']) for a in r['data'] ]
        yield Result(articles,response.url,r['meta']['count'])
        params['offset']+=batch_size
        if params['offset']>r['meta']['count']: # Got all results from the API.")
            break
        response = requests.get(yle_api,params)

is_api: str = "https://www.is.fi/api/search"

def query_is(query: str, from_date: str, to_date: str, batch_size: int = 100) -> Iterator[Result]:
    """Query the IS API for articles matching a query

    Args:
        query (str): the query string to search for
        from_date (str): date to search from (inclusive, YYYY-MM-DD)
        to_date (str): date to search to (inclusive, YYYY-MM-DD)
        batch_size (int, optional): How many entries to query for in a single API call. Values supported by the IS API are 50 and 100 (which is the default).

    Raises:
        ValueError: when something goes wrong in the API call

    Yields:
        Iterator[Result]: each Result contains the results from a single API call    
    """
    def _build_is_url(query: str, offset: int, limit: int, date_start: int, date_end: int) -> str:
        return f"{is_api}/{query}/kaikki/custom/new/{offset}/{limit}/{date_start}/{date_end}"
    date_start = int(datetime.timestamp(datetime.fromisoformat(from_date)) * 1000)
    date_end = int(datetime.timestamp(datetime.fromisoformat(to_date) + timedelta(days=1)) * 1000)
    response = requests.get(_build_is_url(query,9950,50,date_start,date_end))
    if response.status_code != 200:
        raise ValueError(f"Got unexpected response code {response.status_code} for {response.url}.")
    r = response.json()
    if len(r)!=0:
        raise ValueError("Query results in more than 9950 results. The IS API refuses to return more than 10000 results, so refusing to continue. You can work around this limitation by doing multiple queries on smaller timespans.")
    offset = 0
    response = requests.get(_build_is_url(query,offset,batch_size,date_start,date_end))
    while True:
        if response.status_code != 200:
            raise ValueError(f"Got unexpected response code {response.status_code} for {response.url}.")
        r = response.json()
        if r is None:
            raise ValueError(f"Got empty response for {response.url}")
        if len(r)==0: # Got 0 results, assuming we're done.
            break
        articles = [ Article(id=a['id'],url='https://www.is.fi'+a['href'],title=a['title'],date_modified=a['displayDate']) for a in r ]
        yield Result(articles,response.url,-1)
        offset += batch_size
        response = requests.get(_build_is_url(query,offset,batch_size,date_start,date_end))

il_api: str = "https://api.il.fi/v1/articles/search"

def query_il(query: str, from_date: str, to_date: str, batch_size: int = 200) -> Iterator[Result]:
    """Query the IL API for articles matching a query

    Args:
        query (str): the query string to search for
        from_date (str): date to search from (inclusive, YYYY-MM-DD)
        to_date (str): date to search to (inclusive, YYYY-MM-DD)
        batch_size (int, optional): How many entries to query for in a single API call.  Maximum and default for the IL API is 200.

    Raises:
        ValueError: when something goes wrong in the API call

    Yields:
        Iterator[Result]: each Result contains the results from a single API call    
    """
    params = {
            'date_start':from_date,
            'date_end':to_date,
            'q':query,
            'offset':0,
            'limit':batch_size
    }
    response = requests.get(il_api,params)
    while True:
        if response.status_code != 200:
            raise ValueError(f"Got unexpected response code {response.status_code} for {response.url}.")
        r = response.json()['response'] 
        if r is None:
            raise ValueError(f"Got empty response for {response.url}")
        if len(r)==0: # Got 0 results, assuming we're done.
            break
        articles = [ Article(
            id=a['article_id'],
            url='http://iltalehti.fi/'+a['category']['category_name']+"/a/"+a['article_id'],
            title=a['title'],
            date_modified=a['updated_at'] if a['updated_at'] is not None else a['published_at']
            ) for a in r ]
        yield Result(articles,response.url,-1)
        params['offset']+=batch_size
        response = requests.get(il_api,params)

hs_api: str = "https://www.hs.fi/api/search"

def query_hs(query: str, from_date: str, to_date: str, batch_size: int = 100):
    def _build_hs_url(query: str, offset: int, limit: int, date_start: int, date_end: int) -> str:
        return f"{hs_api}/{query}/kaikki/custom/new/{offset}/{limit}/{date_start}/{date_end}"
    date_start = int(datetime.timestamp(datetime.fromisoformat(from_date)) * 1000)
    date_end = int(datetime.timestamp(datetime.fromisoformat(to_date) + timedelta(days=1)) * 1000)
    response = requests.get(_build_hs_url(query,9950,50,date_start,date_end))
    if response.status_code != 200:
        raise ValueError(f"Got unexpected response code {response.status_code} for {response.url}.")
    r = response.json()
    if len(r)!=0:
        raise ValueError("Query results in more than 9950 results. The HS API refuses to return more than 10000 results, so refusing to continue. You can work around this limitation by doing multiple queries on smaller timespans.")
    offset = 0
    response = requests.get(_build_hs_url(query,offset,batch_size,date_start,date_end))
    while True:
        if response.status_code != 200:
            raise ValueError(f"Got unexpected response code {response.status_code} for {response.url}.")
        r = response.json()
        if r is None:
            raise ValueError(f"Got empty response for {response.url}")
        if len(r)==0: # Got 0 results, assuming we're done.
            break
        articles = [ Article(id=a['id'],url='https://www.hs.fi'+a['href'],title=a['title'],date_modified=a['displayDate']) for a in r ]
        yield Result(articles,response.url,-1)
        offset += batch_size
        response = requests.get(_build_hs_url(query,offset,batch_size,date_start,date_end))
    