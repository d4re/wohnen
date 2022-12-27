from logging import DEBUG, INFO, WARNING, ERROR
from pathlib import Path
import os
import yaml
from pydantic import BaseModel

class EmailAccount(BaseModel):
    name_from: str
    email_from: str
    host: str
    port: int
    username: str
    password: str

class TelegramAccount(BaseModel):
    name: str
    api_key: str

accounts_file = os.path.dirname(__file__) + "/local/accounts.yaml"

def get_mail_account() -> EmailAccount:
    with open(accounts_file, "r") as file:
        accounts = yaml.safe_load(file)
    return EmailAccount.parse_obj(accounts["email"])

def get_telegram_account() -> TelegramAccount:
    with open(accounts_file, "r") as file:
        accounts = yaml.safe_load(file)
    return TelegramAccount.parse_obj(accounts["telegram_bot"])


data_path = f"{Path.home()}/wohnen/data"

loglevel = DEBUG
logfile = f"{data_path}/scrape.log"

## Set searches
## This only has an effect when run with --scrape
query_parameters = {
    'area_min': 50,
    'rooms_min': 1,
    'rooms_max': 4,
    'rent_base_max': 1600,
    'rent_total_max': 1600,
    'wbs': 0
}

filter = {
    'allow': {
    },
    'block' : {
        'title' : [
            'flatmate',
            'untermiete',
            'zwischenmiete',
            'zwischemiete',
            'zwischenvermiet',
            'suche wohnung',
            'suche 1',
            'suche 2',
            'suche 3',
            'suche eine ',
            'suche ein zimmer',
            'suche mietwohnung',
            'zum teilen',
            'nur tauch',
            'tausch',
            'tauch wohnung',
            'tauchwohnung',
            'tauchen',
            'zimmer gegen',
            'swap',
            'sublet',
            'subrent',
            'auf zeit',
            'kurzzeit',
            ' befristet',
            'temporary',
            'für monat ',
            ' tage ',
            ' week',
            ' month',
            ' wochen',
            ' monate',
            '1 monat',
            ' wg ',
            ' wg-',
            '-wg',
            'wg zimmer',
            'wg-zimmer',
            'er wg',
            'er-wg',
            'wohngemeinschaft',
            'mitbewohner',
            'shared apartment',
            'shared room',
            '*wbs*',
            'mit wbs',
            'wbs mit',
            '+ wbs',
            '!wbs',
            'wbs-wohn',
            'wbs-berechtigte',
            'wbs-pflichtig',
            'bedingung wbs',
            'wbs wohnung',
            'ferienwohnung',
            'ferien wohnung',
            'monteur',
            'montage ',
            'montagewohnung',
            'studentenwohnheim',
            'studenten-appartement',
            'studenten wohnanlage',
            'nur für studenten',
            'students only',
            'anfragestop',
            'suche stellplatz',
            'fensterputzer',
            'münchen',
            'eberswalde',
            'ukraine',
            'belohnung',
            'prämie',
            'ohne anmeldung',
            ' möblierte ',
            'voll möbliert',
            'einkommen zwischen',
            'einkommensorientiert'
        ],
        'kiez': [
            'steglitz',
            'zehlendorf',
            'wannsee',
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
            'mahlsdorf',
            'kaulsdorf',
            'hellersdorf',
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
            'siemensstadt',
            'waidmannslust',
            'altglienicke'
        ],
        'Beschreibung': [ # ebay kleinanzeigen field
            'das zweite foto',
            'das zweite bild',
            'vielzahl an nachrichten',
            'vielzahl von nachrichten',
            'nur auf instagram',
            'untervermieten',
            'untermiet',
            'zwischenmiete',
            'zwischen miete',
            'on vacation for',
            'flat share',
            'auf zeit',
            'short-term',
            'temporary',
            'für die zeit',
            'from now until',
            ' tage ',
            'monatsweise',
            'nur tausch',
            'ich tausche',
            'zum tausch',
            'im tausch',
            'tauschen',
            'wohnungstausch',
            'tauschwohnung',
            'swap only',
            'ich suche eine ',
            'wir suchen eine ',
            'belohnung',
            'lundberg',
            'lofgren',
            'monteur',
            'büroplatz',
            'pendler',
            'vermietende',
            'ohne anmeldung',
            'keine anmeldung',
            'wg zimmer',
            'lorem ipsum'
        ]
    }
}
