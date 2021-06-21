---
title: 'Finnish Media Scrapers'
tags:
  - Web scraping
  - Media research
  - Python
authors:
  - name: Eetu Mäkelä^[corresponding author]
    affiliation: 1
  - name: Pihla Toivanen^[co-first author]
    orcid: 0000-0003-0872-7098
    affiliation: 1 # (Multiple affiliations must be quoted)
affiliations:
 - name: University of Helsinki
   index: 1
date: 25 May 2021
bibliography: paper.bib

---

# Summary

Finnish Media Scrapers is a package for extracting articles from Finnish journalistic media websites by the [University of Helsinki](https://www.helsinki.fi/) [Human Sciences – Computing Interaction research group](https://heldig.fi/hsci/).
Included are scrapers for four big Finnish media: newspapers [YLE](https://www.yle.fi/uutiset/) & [Helsingin Sanomat](https://www.hs.fi/), and tabloids [Iltalehti](https://www.iltalehti.fi/) & [Iltasanomat](https://www.is.fi/).

# Statement of need

There is an increasing need for user-friendly computational tools in the humanities and social sciences. For example, a common workflow in media research is to collect a large amount of data and combine quantitative and qualitative methods in the analysis phase (@Koivunen, @Weber2011). This package responds to the research needs by providing easy-to-use tools for scraping Finnish media articles and extracting the texts from the scraped HTML files.

The scripts have been already used in a Finnish data journalism article analyzing how Finnish members of parliament were represented in the four media the scrapers include. The article was published in the Finnish weekly news magazine Suomen Kuvalehti in May 2021 (@SKarticle), and after publishing the Finnish Media Scrapers package has gained interest from Finnish computational social science community.

# General workflow

The general workflow for using the scrapers is as follows:
1. The scrapers support specifying a keyword as well as a timespan for extraction, and output a CSV of all matching articles with links.
2. A second set of scripts then allows downloading the matched articles in HTML format.
3. Third, there are further scripts for extracting plain text versions of the article texts out of the HTML.
4. Finally, a script exists to post-filter the resulting plain texts again with keywords.

Important to know when applying the workflow is that due to the fact that all the sources use some kind of stemming for their search, they can often return also spurious hits. Further, if searching for multiple words, the engines often perform a search for either word instead of the complete phrase. The post-filtering script above exists to counteract this by allowing the refiltering of the results more rigorously and uniformly locally.

At the same time and equally importantly, the stemming for a particular media may not cover e.g. all inflectional forms of words. Thus, it often makes sense to query for at least all common inflected variants and merge the results. For a complete worked up example of this kind of use, see the [members_of_parliament](https://github.com/hsci-r/finnish-media-scraper/tree/master/members_of_parliament) folder, which demonstrates how one can collect and count how many articles in each media mention the members of the Finnish Parliament.

# Acknowledgements

We acknowledge contributions from Suomen Kuvalehti team (Samuel Nyroos, Salla Vuorikoski and Leena Sharma) during the testing phase of the scrapers.

# References
