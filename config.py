from logging import DEBUG, INFO, WARNING, ERROR

jsonfile = "/home/benedikt/wohnen.json"
loglevel = DEBUG

name_from = "Wohnungsschnüffler"
email_from = "wo-schnueffi@example.com"

smtp_server = "localhost"


## Set searches
## This only has an effect when run with --scrape
min_rooms = 2
max_rooms = 4
max_rent = 1000
# 0 = No wbs
# 1 = only wbs
# 2 = doesnt matter
wbs = 0

