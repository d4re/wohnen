import logging
from lxml import etree
import hashlib

logger = logging.getLogger(__name__)

xmlforms_ns = {
  'x': 'http://www.openpromos.com/OPPC/XMLForms',
  'meta': 'http://www.openpromos.com/OPPC/XMLFormsMetaData'
}

object_url = 'https://portal1s.easysquare.com/meinehowoge/#/form/%252Fsheet%252Fsection/%FLATID%/%252Fsection%252F0%252Fbox%252F0%252Fhead%252F0'
base_url = 'https://portal1s.easysquare.com/meinehowoge/'

def parse(xml_input):
    # parse results
    if isinstance(xml_input, str):
        xml_input = xml_input.encode('utf-8')
    tree = etree.XML(xml_input)
    all_flats = tree.xpath("//x:box[contains(@boxid,'ESQ_VM_REOBJ_ALL')]/x:head", namespaces=xmlforms_ns)

    logger.info(f"Will parse {len(all_flats)} flats")

    for flat in all_flats:
        flat_dict = {}

        title_tree = flat.xpath("./x:title", namespaces=xmlforms_ns)[0].text
        flat_dict['title'] = title_tree.strip() if title_tree else '(kein Titel)'

        pos = flat.xpath("./x:address", namespaces=xmlforms_ns)[0]
        flat_dict['pos'] = {
          'long' : pos.attrib['lon'],
          'lat' : pos.attrib['lat']
        }

        flat_dict['addr'] = flat.xpath('./x:subtitle', namespaces=xmlforms_ns)[0].text.replace('(Beispielobjekt)','').strip()
        flat_dict['kiez'] = ''

        # id will somehow change every 30min, so instead we need to derive something from title and address
        #flat_dict['id'] = flat.xpath("./x:id", namespaces=xmlforms_ns)[0].text.strip()
        flat_dict['id'] = hashlib.sha512(f"{flat_dict['title']} - {flat_dict['addr']}".encode('utf-8')).hexdigest()

        flat_dict['properties'] = {}
        properties = flat.xpath('./x:details/x:row', namespaces=xmlforms_ns)
        for property in properties:
            if property.attrib['title'] == 'District':
                flat_dict['kiez'] = property.text.strip()
                continue

            flat_dict['properties'][property.attrib['title']] = property.text.strip()

        flat_dict['link'] = base_url

        yield flat_dict