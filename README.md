# Finnish Media Scrapers

[![DOI](https://zenodo.org/badge/335605978.svg)](https://zenodo.org/badge/latestdoi/335605978)

Scrapers for extracting articles from Finnish journalistic media websites by the [University of Helsinki](https://www.helsinki.fi/) [Human Sciences – Computing Interaction research group](https://heldig.fi/hsci/).

Included are scrapers for [YLE](https://www.yle.fi/uutiset/), [Helsingin Sanomat](https://www.hs.fi/), [Iltalehti](https://www.iltalehti.fi/) and [Iltasanomat](https://www.is.fi/). See below for limitations relating to individual sources.

## Installation

There are two ways to get the scripts to work.

The first one is to install the scrapers as a package with pip (`python3 setup.py install` in the cloned repository folder). If installed this way, the scripts should appear as executables in your `bin`, e.g. as `fms-query-yle`.

The other is to download the repository, set up a development environment for it and run the scripts within it. The easiest way to do this is through Conda. This can be done by running e.g. `conda env create -f environment.yml --prefix venv` and then `conda activate ./venv`. If running the scripts this way without installing them, you need to call them directly by their package names, e.g. `python -m finnish_media_scrapers.scripts.query_yle`.

Apart from using the scripts, the functionality of the package is also provided as a python module that you may use programmatically from within Python. For the functionalities thus provided, see under [finnish_media_scrapers](finnish_media_scrapers/).

## General workflow

![Data collection workflow with using pip-packet](https://github.com/hsci-r/finnish_media_scrapers/raw/master/images/fms_datacollection_50border.png)

The general workflow for using the scrapers is as follows:

1.  The scrapers support specifying a keyword as well as a timespan for extraction, and output a CSV of all matching articles with links.
2.  A second set of scripts then allows downloading the matched articles in HTML format.
3.  Third, there are further scripts for extracting plain text versions of the article texts out of the HTML.
4.  Finally, a script exists to post-filter the resulting plain texts again with keywords.

Important to know when applying the workflow is that due to the fact that all the sources use some kind of stemming for their search, they can often return also spurious hits. Further, if searching for multiple words, the engines often perform a search for either word instead of the complete phrase. The post-filtering script above exists to counteract this by allowing the refiltering of the results more rigorously and uniformly locally.

At the same time and equally importantly, the stemming for a particular media may not cover e.g. all inflectional forms of words. Thus, it often makes sense to query for at least all common inflected variants and merge the results. For a complete worked up example of this kind of use, see the [members_of_parliament](https://github.com/hsci-r/finnish-media-scraper/tree/master/members_of_parliament) folder, which demonstrates how one can collect and count how many articles in each media mention the members of the Finnish Parliament.

## Helsingin Sanomat

First, query the articles you want using `fms-query-hs`. For example, `fms-query-hs -f 2020-02-16 -t 2020-02-18 -o hs-sdp.csv -q SDP`.

For downloading articles, this scraper requires 1) a user id and password for Helsingin Sanomat and 2) a Selenium Docker container to be running. After installing Docker, run `docker run -p 4444:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome:4.0.0-beta-1-20210215` in another console before invoking the script. After these prequisites are fulfilled, you can fetch the articles using `fms-fetch-hs`. For example `fms-fetch-hs -i hs-sdp.csv -o hs-sdp -u username -p password`. After fetching the articles, extract texts with `fms-html-to-text-hs -o hs-sdp-output hs-sdp`.

Known special considerations:

- The search engine used seems to be employing some sort of stemming/lemmatization, so e.g. the query string `kok` seems to match `kokki`, `koko` and `koki`.
- A single query can return at most 9,950 hits. This can be sidestepped by invoking the script multiple times with smaller query time spans.

## Yle

Known special considerations:

- A single query can return at most 10,000 hits. This can be sidestepped by invoking the script multiple times with smaller query time spans.

example: `fms-query-yle -f 2020-02-16 -t 2020-02-18 -o yle-sdp.csv -q SDP` + `fms-fetch-open -i yle-sdp.csv -o yle-sdp` + `fms-html-to-text-yle -o yle-sdp-output yle-sdp` (or `fms-html-to-text-svyle -o svyle-sdp-output svyle-sdp` if articles come from Svenska YLE)

## Iltalehti

example: `fms-query-il -f 2020-02-16 -t 2020-02-18 -o il-sdp.csv -q SDP` + `fms-fetch-open -i il-sdp.csv -o il-sdp` + `fms-html-to-text-il -o il-sdp-output il-sdp`

## Iltasanomat

example: `fms-query-is -f 2020-02-16 -t 2020-02-18 -o is-sdp.csv -q SDP` + `fms-fetch-open -i is-sdp.csv -o is-sdp` + `fms-html-to-text-is -o is-sdp-output is-sdp`

## Using fms-post-filter script

For example, after collecting texts from Helsingin Sanomat with the exampla above, run:
`fms-post-filter -i hs-sdp.csv -t hs-sdp-output/ -o hs-sdp-filtered.csv -q SDP`

where `-i` parameter specifies the query output file, `-t` the folder name to search extracted texts, `-o` the output filename and `-q` search word to filter. 

There is also an option `-ci` for configuring the case-insensitiveness (default false). 

## Contact

For more information on the scrapers, please contact associate professor [Eetu Mäkelä](http://iki.fi/eetu.makela).
