from logging import DEBUG, INFO, WARNING, ERROR

data_path = "/home/pegro/wohnen/data/main"

loglevel = DEBUG
logfile = f"{data_path}/scrape.log"

name_from = "Wohnungsschnüffler"
email_from = "wo-schnueffi@example.com"

smtp_server = "localhost"

## Set searches
## This only has an effect when run with --scrape
query_parameters = {
    'area_min': 42,
    'rooms_min': 2,
    'rooms_max': 5,
    'rent_base_max': 600,
    'rent_total_max': 700,
    'wbs': 0
}

filter = {
    'allow': {
    },
    'block' : {
        'title' : [
            'untermiete',
            'zwischenmiete',
            'suche wohnung',
            'tausche',
            'tauschwohnung',
            'im tausch',
            'nur tausch',
            'wohnungstausch',
            'zum tausch',
            'tausch!',
            '*tausch*',
            'tausch:',
            'tausch wohnung',
            'tauch wohnung',
            'sublet',
            'auf zeit',
            ' wg ',
            ' wg-',
            'wg zimmer',
            ' suche eine ',
            '*wbs*',
            'mit wbs',
            'ferienwohnung',
            'ferien wohnung',
            'monteur'
        ],
        'kiez': [
            'steglitz',
            'zehlendorf',
            'wannsee',
            'mariendorf',
            'marienfelde',
            'buckow',
            'wilhelmsruh',
            'dahlem',
            'spandau',
            'wittenau',
            'tegel',
            'grunewald',
            'lichterfelde',
            'lankwitz',
            'lichtenrade',
            'gropiusstadt',
            'rudow',
            'adlershof',
            'köpenick',
            'grünau',
            'biesdorf',
            'mahlsdorf',
            'friedrichsfelde',
            'kaulsdorf',
            'hellersdorf',
            'marzahn',
            'hohenschönhausen',
            'heinersdorf',
            'buch',
            'märkisches viertel',
            'rosenthal',
            'blankenburg',
            'hermsdorf',
            'falkenhagener feld',
            'staaken',
            'friedenau',
            'westend',
            'lübars',
            'haselhorst',
            'siemensstadt'
        ],
        'Beschreibung': [ # ebay kleinanzeigen field
            'das zweite foto',
            'vielzahl an nachrichten',
            'untermieten',
            'untervermieten',
            'untermieter',
            'nur tausch',
            'zum tausch'
        ]
    }
}
