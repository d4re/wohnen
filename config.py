from logging import DEBUG, INFO, WARNING, ERROR

data_path = "/home/pegro/wohnen/"

loglevel = DEBUG
logfile = "/home/pegro/wohnen/scrape.log"

name_from = "Wohnungsschnüffler"
email_from = "wo-schnueffi@example.com"

smtp_server = "localhost"


## Set searches
## This only has an effect when run with --scrape
min_area = 42
min_rooms = 2
max_rooms = 5
max_rent = 600
# 0 = No wbs
# 1 = only wbs
# 2 = doesnt matter
wbs = 0

filter = {
    'allow': {
    },
    'block' : {
        'title' : ['suche wohnung', 'tausche', 'tauschwohnung', 'zwischenmiete', 'untermiete', 'nur tausch', 'wohnungstausch', 'zum tausch', 'tausch!', '*tausch*', 'tausch:', 'tausch wohnung', 'tauch wohnung', 'sublet', 'auf zeit', ' wg ', ' wg-', 'wg zimmer', ' suche eine ', '*wbs*'],
        'kiez': ['steglitz', 'zehlendorf', 'wannsee', 'mariendorf', 'marienfelde', 'buckow', 'wilhelmsruh', 'dahlem', 'spandau', 'wittenau', 'tegel', 'grunewald', 'lichterfelde', 'lankwitz', 'lichtenrade', 'gropiusstadt', 'rudow', 'adlershof', 'köpenick', 'grünau', 'biesdorf', 'mahlsdorf', 'friedrichsfelde', 'kaulsdorf', 'hellersdorf', 'marzahn', 'hohenschönhausen', 'heinersdorf', 'buch', 'märkisches viertel', 'rosenthal', 'blankenburg', 'hermsdorf', 'falkenhagener feld', 'staaken', 'friedenau', 'westend', 'lübars', 'haselhorst', 'siemensstadt']
    }
}
