# wohnen

There's nothing to be written about the housing sitation in Berlin that hasn't been said before.

The program is built with a sort-of modular design so it can be extended to work for more sites.

Currently implemented are scraper and parser for
  * inberlinwohnen.de, where the city of Berlin advertises it's flats
  * deutsche-wohnen.com
  * ebay-kleinanzeigen.de (it's a mess)

## Usage

The config uses a mix of command line arguments and the file `config.py`.

```shell
» ./wohnen.py --help
usage: wohnen.py [-h] [--scrape] [--email EMAIL] sites [sites ...]

positional arguments:
  sites                 list of sites to check

optional arguments:
  -h, --help            show this help message and exit
  --scrape              actually scrape
  --email EMAIL         email addresses to send notify about new flats (single email address per option)

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

## Authors
- Benedikt Kristinsson <benedikt@inventati.org>
- Peter Große <pegro@friiks.de>