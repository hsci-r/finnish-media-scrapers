# Example: Petteri Orpo (or all members of parliament)

These example scripts collect articles about Petteri Orpo, chairperson of National Coalition Party (mp-expanded-orpo.csv) during a specific timeframe (from 2020-01-01 to 2020-01-07).

If you want to collect articles about every member of parliament in Finland during 2020, change mp-expanded-orpo.csv to mp-expanded.csv in files fetch-mp-inflections.py and query-mp-inflections.py

`mkdir ../queries`

`python3 query-mp-inflections.py`

`python3 fetch-mp-inflections.py -u <insert your user> -p  <insert your password>`
