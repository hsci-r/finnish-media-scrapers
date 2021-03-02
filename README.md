# MediaScraper

Scrapers for extracting articles from Finnish journalistic media websites. The scrapers support specifying a keyword as well as a timespan for extraction, and support either getting a CSV of all matching articles with links, or of also downloading the articles in HTML format.

Included are scrapers for [YLE](https://www.yle.fi/uutiset/), [Helsingin Sanomat](https://www.hs.fi/), [Iltalehti](https://www.iltalehti.fi/) and [Iltasanomat](https://www.is.fi/). See below for limitations relating to individual sources.

## Installation

The easiest way to install the required dependencies for these scripts is through Conda. This can be done by running e.g. `conda env create -f environment.yml --prefix venv` and then `conda activate ./venv`.

# Helsingin Sanomat

For downloading articles (instead of just listing them), this scraper requires 1) a user id and password for Helsingin Sanomat and 2) a Selenium Docker container to be running. After installing Docker, run `docker run -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:4.0.0-beta-1-20210215` in another console before invoking the script.

Known special considerations:

- The search engine used seems to be employing some sort of stemming/lemmatization, so e.g. the query string `kok` seems to match `kokki`, `koko` and `koki`.
- A single query can return at most 9,950 hits. This can be sidestepped by invoking the script multiple times with smaller query time spans.

## Yle

Known special considerations:

- A single query can return at most 9,950 hits. This can be sidestepped by invoking the script multiple times with smaller query time spans.

example: `python scrape-yle.py -f 2020-02-16 -t 2020-02-18 -o output.csv -q SDP `
