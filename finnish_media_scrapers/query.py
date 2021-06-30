"""Functions related to querying articles from the apis of YLE, Helsingin Sanomat (HS), Ilta-Sanomat (IS) and Iltalehti (IL)
"""
from datetime import datetime, timedelta
from typing import AsyncIterable

import attr
from aiohttp import ClientSession


@attr.s
class Article:
    """An article

    Attributes:
        id (str): the unique id for the article
        url (str): the url from which the article may be found
        title (str): the title or headline of the article
        date_modified (str): the date of last modification for the article
    """
    id: str = attr.ib()
    url: str = attr.ib()
    title: str = attr.ib()
    date_modified: str = attr.ib()


@attr.s
class Result:
    """A result from a single API call

    Attributes:
        articles (list[Article]): a list of the article objects returned
        url (str): the URL of the API query
        total (int): the total number of articles for the query. -1 if not available.
    """
    articles: 'list[Article]' = attr.ib()
    url: str = attr.ib()
    total: int = attr.ib(default=-1)


yle_api: str = "https://yle-fi-search.api.yle.fi/v1/search"


async def query_yle(session: ClientSession, query: str, language: str, from_date: str, to_date: str, batch_size: int = 10000) -> AsyncIterable[Result]:
    """Query the YLE API for articles matching a query

    Args:
        session (ClientSession): the aiohttp session to use
        query (str): the query string to search for
        language (str): language to search (either 'fi' or 'sv')
        from_date (str): date to search from (inclusive, YYYY-MM-DD)
        to_date (str): date to search to (inclusive, YYYY-MM-DD)
        batch_size (int, optional): How many entries to query for in a single API call. Maximum and default for the YLE API is 10000.

    Raises:
        ValueError: when something goes wrong in the API call

    Yields:
        AsyncIterable[Result]: each Result contains the results from a single API call
    """
    params = {
        'app_id': 'hakuylefi_v2_prod',
        'app_key': '4c1422b466ee676e03c4ba9866c0921f',
        'service': 'uutiset',
        'language': language,
        'uiLanguage': language,
        'type': 'article',
        'time': 'custom',
        'timeFrom': from_date,
        'timeTo': to_date,
        'query': query,
        'offset': 0,
        'limit': batch_size
    }
    async with session.get(yle_api, params=params) as response:
        if response.status != 200:
            raise ValueError(
                f"Got unexpected response code {response.status} for {response.url}.")
        response_json = await response.json()
        if response_json is None:
            raise ValueError(f"Got empty response for {response.url}")
        if response_json['meta']['count'] > 10000:
            raise ValueError(
                f"Query results in {response_json['meta']['count']} results. The YLE API refuses to return more than 10000 results, so refusing to continue. You can work around this limitation by doing multiple queries on smaller timespans.")
    while True:
        async with session.get(yle_api, params=params) as response:
            if response.status != 200:
                raise ValueError(
                    f"Got unexpected response code {response.status} for {response.url}.")
            response_json = await response.json()
            if response_json is None:
                raise ValueError(f"Got empty response for {response.url}")
            if len(response_json['data']) == 0:  # Got 0 results, assuming we're done.
                break
            articles = [Article(id=a['id'], url=a['url']['full'], title=a['headline'],
                                date_modified=a['datePublished']) for a in response_json['data']]
            yield Result(articles, str(response.url), response_json['meta']['count'])
            params['offset'] += batch_size
            if params['offset'] > response_json['meta']['count']:  # Got all results from the API.")
                break


is_api: str = "https://www.is.fi/api/search"


async def query_is(session: ClientSession, query: str, from_date: str, to_date: str, batch_size: int = 100) -> AsyncIterable[Result]:
    """Query the IS API for articles matching a query

    Args:
        session (ClientSession): the aiohttp session to use
        query (str): the query string to search for
        from_date (str): date to search from (inclusive, YYYY-MM-DD)
        to_date (str): date to search to (inclusive, YYYY-MM-DD)
        batch_size (int, optional): How many entries to query for in a single API call. Values supported by the IS API are 50 and 100 (which is the default).

    Raises:
        ValueError: when something goes wrong in the API call

    Yields:
        AsyncIterable[Result]: each Result contains the results from a single API call
    """
    def _build_is_url(query: str, offset: int, limit: int, date_start: int, date_end: int) -> str:
        return f"{is_api}/{query}/kaikki/custom/new/{offset}/{limit}/{date_start}/{date_end}"
    date_start = int(datetime.timestamp(
        datetime.fromisoformat(from_date)) * 1000)
    date_end = int(datetime.timestamp(
        datetime.fromisoformat(to_date) + timedelta(days=1)) * 1000)
    async with session.get(_build_is_url(
            query, 9950, 50, date_start, date_end)) as response:
        if response.status != 200:
            raise ValueError(
                f"Got unexpected response code {response.status} for {response.url}.")
        response_json = await response.json()
        if len(response_json) != 0:
            raise ValueError("Query results in more than 9950 results. The IS API refuses to return more than 10000 results, so refusing to continue. You can work around this limitation by doing multiple queries on smaller timespans.")
    offset = 0
    while True:
        async with session.get(_build_is_url(query, offset, batch_size, date_start, date_end)) as response:
            if response.status != 200:
                raise ValueError(
                    f"Got unexpected response code {response.status} for {response.url}.")
            response_json = await response.json()
            if response_json is None:
                raise ValueError(f"Got empty response for {response.url}")
            if len(response_json) == 0:  # Got 0 results, assuming we're done.
                break
            articles = [Article(id=a['id'], url='https://www.is.fi'+a['href'],
                                title=a['title'], date_modified=a['displayDate']) for a in response_json]
            yield Result(articles, str(response.url), -1)
            offset += batch_size


il_api: str = "https://api.il.fi/v1/articles/search"


async def query_il(session: ClientSession, query: str, from_date: str, to_date: str, batch_size: int = 200) -> AsyncIterable[Result]:
    """Query the IL API for articles matching a query

    Args:
        session (ClientSession): the aiohttp session to use
        query (str): the query string to search for
        from_date (str): date to search from (inclusive, YYYY-MM-DD)
        to_date (str): date to search to (inclusive, YYYY-MM-DD)
        batch_size (int, optional): How many entries to query for in a single API call.  Maximum and default for the IL API is 200.

    Raises:
        ValueError: when something goes wrong in the API call

    Yields:
        AsyncIterable[Result]: each Result contains the results from a single API call
    """
    params = {
        'date_start': from_date,
        'date_end': to_date,
        'q': query,
        'offset': 0,
        'limit': batch_size
    }
    while True:
        async with session.get(il_api, params=params) as response:
            if response.status != 200:
                raise ValueError(
                    f"Got unexpected response code {response.status} for {response.url}.")
            response_json = (await response.json())['response']
            if response_json is None:
                raise ValueError(f"Got empty response for {response.url}")
            if len(response_json) == 0:  # Got 0 results, assuming we're done.
                break
            articles = [Article(
                id=a['article_id'],
                url='http://iltalehti.fi/' +
                    a['category']['category_name']+"/a/"+a['article_id'],
                title=a['title'],
                date_modified=a['updated_at'] if a['updated_at'] is not None else a['published_at']
            ) for a in response_json]
            yield Result(articles, str(response.url), -1)
            params['offset'] += batch_size

hs_api: str = "https://www.hs.fi/api/search"


async def query_hs(session: ClientSession, query: str, from_date: str, to_date: str, batch_size: int = 100) -> AsyncIterable[Result]:
    """Query the HS API for articles matching a query

    Args:
        session (ClientSession): the aiohttp session to use
        query (str): the query string to search for
        from_date (str): date to search from (inclusive, YYYY-MM-DD)
        to_date (str): date to search to (inclusive, YYYY-MM-DD)
        batch_size (int, optional): How many entries to query for in a single API call. Values supported by the HS API are 50 and 100 (which is the default).

    Raises:
        ValueError: when something goes wrong in the API call

    Yields:
        AsyncIterable[Result]: each Result contains the results from a single API call
    """
    def _build_hs_url(query: str, offset: int, limit: int, date_start: int, date_end: int) -> str:
        return f"{hs_api}/{query}/kaikki/custom/new/{offset}/{limit}/{date_start}/{date_end}"
    date_start = int(datetime.timestamp(
        datetime.fromisoformat(from_date)) * 1000)
    date_end = int(datetime.timestamp(
        datetime.fromisoformat(to_date) + timedelta(days=1)) * 1000)
    async with session.get(_build_hs_url(
            query, 9950, 50, date_start, date_end)) as response:
        if response.status != 200:
            raise ValueError(
                f"Got unexpected response code {response.status} for {response.url}.")
        response_json = await response.json()
        if len(response_json) != 0:
            raise ValueError("Query results in more than 9950 results. The HS API refuses to return more than 10000 results, so refusing to continue. You can work around this limitation by doing multiple queries on smaller timespans.")
    offset = 0
    while True:
        async with session.get(_build_hs_url(query, offset, batch_size, date_start, date_end)) as response:
            if response.status != 200:
                raise ValueError(
                    f"Got unexpected response code {response.status} for {response.url}.")
            response_json = await response.json()
            if response_json is None:
                raise ValueError(f"Got empty response for {response.url}")
            if len(response_json) == 0:  # Got 0 results, assuming we're done.
                break
            articles = [Article(id=a['id'], url='https://www.hs.fi'+a['href'],
                                title=a['title'], date_modified=a['displayDate']) for a in response_json]
            yield Result(articles, str(response.url), -1)
            offset += batch_size
