import logging
from mechanize import Browser
from config import Applicant

logger = logging.getLogger(__name__)


br = Browser()
# Ignore robots.txt
br.set_handle_robots( False )
# Google demands a user-agent that isn't a robot
br.addheaders = [('User-agent', '"Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)"')]

form_mapping = {
    "tx_powermail_pi1[field][name]": "surname",
    "tx_powermail_pi1[field][vorname]" : "forename",
    "tx_powermail_pi1[field][strasse]" : "street",
    "tx_powermail_pi1[field][plz]" : "plz",
    "tx_powermail_pi1[field][ort]" : "city",
    "tx_powermail_pi1[field][e_mail]" : "email",
    "tx_powermail_pi1[field][telefon]" : "phone",
    }

def apply(flat: dict, applicant: Applicant):

    br.open(flat["link"])

    br.select_form(data_parsley_validate="data-parsley-validate")

    applicant_dict = applicant.dict()

    for form_field, field  in form_mapping.items():
        br[form_field] = applicant_dict[field]
    br.find_control(id="powermail_field_datenschutzhinweis_1").items[0].selected=True

    request = br.click()
    res = br.submit()

    logger.info(f"response url: {res.geturl()}, response code: {res.getcode()}")
    
    if "/wohnungen-berlin/angebote/vielen-dank/" in br.geturl():
        logger.info(f"auto-submitting worked")
        return True
    else:
        logger.error(f"Error while autosubmitting")
        logger.info(request)
        logger.info(request.get_data())
    


