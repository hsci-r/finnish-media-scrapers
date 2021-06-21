---
title: 'Finnish Media Scrapers'
tags:
  - Web scraping
  - Media research
  - Python
authors:
  - name: Eetu Mäkelä^[corresponding author]
    orcid: 0000-0002-8366-8414
    affiliation: 1
  - name: Pihla Toivanen^[co-first author]
    orcid: 0000-0003-0872-7098
    affiliation: 1
affiliations:
 - name: University of Helsinki
   index: 1
date: 21 June 2021
bibliography: paper.bib

---

# Summary

Finnish Media Scrapers is a package for extracting articles from Finnish journalistic media websites by the [University of Helsinki](https://www.helsinki.fi/) [Human Sciences – Computing Interaction research group](https://heldig.fi/hsci/).
Included are scrapers for the four biggest Finnish journalistic media: [YLE](https://www.yle.fi/uutiset/), [Helsingin Sanomat](https://www.hs.fi/), [Iltalehti](https://www.iltalehti.fi/) and [Iltasanomat](https://www.is.fi/).

# Statement of need

There is an increasing need for user-friendly computational tools in the humanities and social sciences. For example, a common workflow in media research is to collect a large amount of data and combine quantitative and qualitative methods in the analysis phase (@Koivunen, @Weber2011). This package responds to the research needs by providing easy-to-use tools for scraping Finnish media articles and extracting the article texts from the scraped HTML files. At the same time, the functionality has also been packaged as a Python module for the benefit of more computationally-savvy users.

The scripts were originally developed for a data journalism article (@SKarticle) analyzing how Finnish members of parliament were represented in the media in 2020. Further developing and packaging the scripts into a reusable package was based on an expressed interest from the Finnish computational science community. Since initial beta release a couple of months ago, the package is now known to be already used in at least two research projects targeting Finnish media analysis.

# General workflow

The general workflow for using the scrapers is as follows:
1. The scrapers support specifying a keyword as well as a timespan for extraction, and output a CSV of all matching articles with links.
2. A second set of scripts then allows downloading the matched articles in HTML format.
3. Third, there are further scripts for extracting plain text versions of the article texts out of the HTML.
4. Finally, a script exists to post-filter the resulting plain texts again with keywords.

Important to know when applying the workflow is that due to the fact that all the sources use some kind of stemming for their search, they can often return also spurious hits. Further, if searching for multiple words, the engines often perform a search for either word instead of the complete phrase. The post-filtering script above exists to counteract this by allowing the refiltering of the results more rigorously and uniformly locally.

At the same time and equally importantly, the stemming for a particular media may not cover e.g. all inflectional forms of words. Thus, it often makes sense to query for at least all common inflected variants and merge the results. For a complete worked up example of this kind of use, see the [members_of_parliament](https://github.com/hsci-r/finnish-media-scraper/tree/master/members_of_parliament) folder, which demonstrates how one can collect and count how many articles in each media mention the members of the Finnish Parliament.

# Acknowledgements

We acknowledge contributions from the Suomen Kuvalehti team (Samuel Nyroos, Salla Vuorikoski and Leena Sharma) during the testing phase of the scrapers.

# References
