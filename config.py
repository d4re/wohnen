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
    'rent_total_max': 770,
    'wbs': 0
}

filter = {
    'allow': {
    },
    'block' : {
        'title' : [
            'untermiete',
            'zwischenmiete',
            'zwischemiete',
            'suche wohnung',
            'suche 1',
            'suche 2',
            'suche eine ',
            'suche ein zimmer',
            'zum teilen',
            'nur tauch',
            'tausch',
            'tauch wohnung',
            'tauchwohnung',
            'swap',
            'sublet',
            'auf zeit',
            'kurzzeit',
            ' tage ',
            ' week',
            ' month',
            ' wochen',
            ' monate',
            ' wg ',
            ' wg-',
            'wg zimmer',
            'wg-zimmer',
            'er wg',
            'er-wg',
            'wohngemeinschaft',
            'shared apartment',
            '*wbs*',
            'mit wbs',
            'wbs mit',
            '+ wbs',
            'wbs-wohn',
            'wbs-berechtigte',
            'ferienwohnung',
            'ferien wohnung',
            'monteur',
            'montage ',
            'studentenwohnheim',
            'studenten-appartement',
            'anfragestop',
            'suche stellplatz',
            'münchen',
            'eberswalde'
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
            'das zweite bild',
            'vielzahl an nachrichten',
            'vielzahl von nachrichten',
            'untermieten',
            'untervermieten',
            'untermieter',
            'untermiete',
            'zwischenmiete',
            'auf zeit',
            ' tage ',
            'monatsweise',
            'nur tausch',
            'ich tausche',
            'zum tausch',
            'tauschen',
            'wohnungstausch',
            'ich suche eine ',
            'belohnung',
            'lundberg',
            'monteur',
            'Büroplatz'
        ]
    }
}
