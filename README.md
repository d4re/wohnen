# wohnen

There's nothing to be written about the housing sitation in Berlin that hasn't been said before.

The program is built with a sort-of modular design so it can be extended to work for more sites.

Currently implemented are scraper and parser for
  * inberlinwohnen.de, where the city of Berlin advertises it's flats
  * deutsche-wohnen.com
  * ebay-kleinanzeigen.de (it's a mess what people post)
  * howoge.de (SAP + Easysquare/PROMOS madness)
  * wbm.de
  * immowelt.de
  * wg-gesucht.de

## Usage

The config uses a mix of command line arguments and the file `config.py`.

```shell
» ./wohnen.py --help
usage: wohnen.py [-h] [--scrape] [--quiet] [--email EMAIL] [--formattest] sites [sites ...]

positional arguments:
  sites          list of sites to check

optional arguments:
  -h, --help     show this help message and exit
  --scrape       actually scrape
  --quiet        hide log output
  --email EMAIL  email addresses to send notify about new flats
  --formattest   test email formatting
```

Set the search parameters in config.py:

```python
query_parameters = {
    'area_min': 42,
    'rooms_min': 2,
    'rooms_max': 5,
    'rent_base_max': 600,
    'rent_total_max': 700,
    # 0 = no wbs, 1 = only wbs, 2 = doesnt matter
    'wbs': 0
}
```

## TODO
  * not all filter settings are propagated in all site modules (at least rent works everywhere)
  * document parsertest.py

## Authors
- Benedikt Kristinsson <benedikt@inventati.org>
- Peter Große <pegro@friiks.de>
