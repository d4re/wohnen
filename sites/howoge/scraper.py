import base64
from datetime import datetime
from lxml import etree
import requests
from urllib.parse import urlencode
import uuid

'''
Step 1:

POST https://portal1s.easysquare.com/meinehowoge/api5/authenticate?api=6.139&sap-language=de

User-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.105 Safari/537.36
Content-type: application/x-www-form-urlencoded; charset=UTF-8
Accept: text/html, */*; q=0.01
X-Requested-With: XMLHttpRequest
Origin: https://portal1s.easysquare.com
Referer: https://portal1s.easysquare.com/meinehowoge/
Cookie: esq-alias=%2fmeinehowoge; sap-usercontext=sap-client=451

Data:
sap-ffield_b64=dXNlcj1XT0E3NDI2MyZwYXNzd29yZD1BamQzejRRZDQ%3D
-> user=WOA74263&password=Ajd3z4Qd4
-> see https://portal1s.easysquare.com/meinehowoge/~20211124135010~/brands/howoge/brandconfig.json
 -> URL can be assembled via content from https://portal1s.easysquare.com/meinehowoge/index.html -> e.g. <link href="https://portal1s.easysquare.com/meinehowoge/~20211124134839~/brands/howoge/scss/main.css"...>

Interesting response headers:
expect-mysapsso2: b4nDcFP1t/VSqOTBGra7vh24uRk=
    (FIXME needed for anything?)
set-cookie: SAP_SESSIONID_PP0_451=YufoToaiihC28BLc16dh9NMOm9iXOBHsm1wKELG5Agg%3d; path=/; secure; HttpOnly
    (should be handled by requests session)


Step 2:
FIXME: unclear if needed (maybe service ID is fix)

POST https://portal1s.easysquare.com/meinehowoge/api5/services?api=6.139

Request headers:
sap-ffield_b64=dXNlcj1XT0E3NDI2Mw==
-> only user

Response: XML!
Immobiliensuche -> service ID: 04DDC5B6-67F2-814F-88E5-86A7E0391E2A


(
Step 3:

GET https://portal1s.easysquare.com/prorex/xmlforms?application=ESQ_IA_REOBJ&sap-client=451&command=action&name=boxlist&api=6.139&head-oppc-version=6.139.10&_=1645903079761
-> _ is probably a timestamp

-> same as services request, I guess
)

Step 3:

GET https://portal1s.easysquare.com/prorex/xmlforms?application=ESQ_IA_REOBJ&sap-client=451&command=action&name=get&id=400C82FA-7F52-8ACA-8F8F-6349A4A95BB1&api=6.139&head-oppc-version=6.139.10

Note: action=get and id=04DDC5B6-67F2-814F-88E5-86A7E0391E2A
FIXME: maybe we can skip to here after authenticating, maybe step 2

Response: XML!
Form to be modified!

<?xml version="1.0" encoding="utf-8"?>
<form xmlns="http://www.openpromos.com/OPPC/XMLForms" xmlns:meta="http://www.openpromos.com/OPPC/XMLFormsMetaData" xmlns:oppc="http://www.openpromos.com/OPPC/XMLForms" xmlns:prv="urn:mine" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="400C82FA-7F52-8ACA-8F8F-6349A4A95BB1" originalId="400C82FA-7F52-8ACA-8F8F-6349A4A95BB1" xsi:schemaLocation="http://www.openpromos.com/OPPC/XMLForms ..\FormSchema.xsd">
  <head>
    <originalId>400C82FA-7F52-8ACA-8F8F-6349A4A95BB1</originalId>
    <id/>
    <date/>
    <title/>
    <keywords/>
  </head>
  <actions>
    <action id="01search_re_obj" includeInMenu="false" includeInQuick="false" style="cancel" title="Suchen">
      <type>
        <server command="search_re_obj" locksForm="true" waitForResponse="true"/>
      </type>
      <preconditions valid="true"/>
    </action>
    <action id="02load_search" includeInMenu="false" includeInQuick="false" title="Suchvariante laden">
      <type>
        <server command="load_search" locksForm="true" waitForResponse="true"/>
      </type>
    </action>
    <action id="03delete_search" includeInMenu="false" includeInQuick="false" title="Suche löschen">
      <type>
        <server command="delete_search" locksForm="true" waitForResponse="true"/>
      </type>
      <confirmation>
        <title>Suche löschen</title>
        <message>Möchten Sie die Gespeicherte Suche endgültig löschen?</message>
        <acceptTitle>Ja</acceptTitle>
        <cancelTitle>Nein</cancelTitle>
      </confirmation>
    </action>
  </actions>
  <sheet refname="topmostSheet" title="Filter/Suche Objekt">
    <section id="ESQ_FORM_VALIDATION" visibility="hidden">
      <textfield defaultValue="true" editable="false" id="ESQ_CHANGED" text.expression="'true'" title="Technisch: Aktualisiert?" visibility="hidden">true</textfield>
      <textfield defaultValue="" id="ESQ_IS_IN_CONTEXT" visibility="hidden"/>
    </section>
    <section title="Was suchen Sie?" visibility.expression="$cf_search_variants.empty? true : false">
      <textfield defaultValue="X" editable="false" id="SO_#ISFILTERED#_I_EQ" title="Gefiltert" visibility="hidden">X</textfield>
      <choicefield id="SO_#USE_TYP#_I_EQ" refname="use_typ" required="false" span="6" span.s="12" title="Art">
        <choice id="0100" selected="true" title="Wohnung"/>
      </choicefield>
      <numberfield defaultValue="50" id="SO_#PAGINGTOP#_I_EQ" maxvalue="999999999" span="6" span.s="12" title="Maximale Trefferzahl">50</numberfield>
    </section>
    <section id="WBS_SECTION" subtitle="Mit einem Wohnberechtigungsschein (WBS) können Sie eine geförderte Wohnung beziehen. Den WBS beantragen Sie am besten bei Ihrem Wohnungsamt." title="Wohnberechtigungsschein" visibility.expression="$cf_search_variants.empty? true : false">
      <choicefield id="SO_#HAS_WBS#_I_EQ" multipleChoice="false" span="12" style="inline" title="Wohnberechtigungsschein" visibility="default">
        <choice id="X" meta:field_id_overwrite="SO_#HAS_WBS_NO_MATTER#_I_NE" selected="true" title="Alle Angebote"/>
        <choice id="X" title="WBS erforderlich"/>
        <choice id="X" meta:field_id_overwrite="SO_#HAS_WBS#_I_NE" title="WBS nicht erforderlich"/>
      </choicefield>
    </section>
    <section title="Lage" visibility.expression="$cf_search_variants.empty? true : false">
      <textfield id="SO_#STREET#_I_CP#MCX" maxlength="120" refname="street" span="6" span.s="12" title="Straße"/>
      <textfield id="SO_#HOUSE_NUM#_I_CP" maxlength="20" span="6" span.s="12" title="Hausnummer"/>
      <textfield id="SO_#POSTCODE#_I_CP" maxlength="20" span="6" span.s="12" title="Postleitzahl"/>
      <textfield id="SO_#CITY#_I_CP#MCX" maxlength="80" refname="city" span="6" span.s="12" title="Ort"/>
      <choicefield id="SO_#DISTR_ID#_I_EQ" multipleChoice="true" refname="district" span="6" span.s="12" title="Stadtteil">
        <choice id="DS4451" title="Alt-Hohenschönhausen"/>
        <choice id="DS4452" title="Alt-Lichtenberg"/>
        <choice id="DS4453" title="Buch"/>
        <choice id="DS4454" title="Charlottenburg-Wilmersdorf"/>
        <choice id="DS4455" title="Dahlwitz-Hoppegarten"/>
        <choice id="DS4456" title="Fennpfuhl"/>
        <choice id="DS4457" title="Friedrichsfelde"/>
        <choice id="DS4458" title="Friedrichshain-Kreuzberg"/>
        <choice id="DS4459" title="Karlshorst"/>
        <choice id="DS4460" title="Marzahn-Hellersdorf"/>
        <choice id="DS4461" title="Mitte"/>
        <choice id="DS4462" title="Neu-Hohenschönhausen"/>
        <choice id="DS4463" title="Neukölln"/>
        <choice id="DS4464" title="Pankow (ohne Buch)"/>
        <choice id="DS4465" title="Reinickendorf"/>
        <choice id="DS4466" title="Spandau"/>
        <choice id="DS4467" title="Steglitz-Zehlendorf"/>
        <choice id="DS4468" title="Strausberg"/>
        <choice id="DS4469" title="Tempelhof-Schöneberg"/>
        <choice id="DS4470" title="Treptow-Köpenick"/>
      </choicefield>
      <choicefield editable.expression="$city.filledOut and ( $street.filledOut or $district.filledOut ) and $district.selection.count &lt;= 1" id="SO_#DISTANCE#_I_EQ" span="6" span.s="12" title="Umkreis" tooltip="Bitte Ort und Straße oder Ort und genau einen Stadtteil auswählen" visibility="hidden">
        <choice id="1" title="1 km"/>
        <choice id="2" title="2 km"/>
        <choice id="3" title="3 km"/>
        <choice id="4" title="4 km"/>
        <choice id="5" title="5 km"/>
        <choice id="10" title="10 km"/>
        <choice id="15" title="15 km"/>
        <choice id="20" title="20 km"/>
        <choice id="50" title="50 km"/>
      </choicefield>
    </section>
    <section title="Objekt" visibility.expression="$cf_search_variants.empty? true : false">
      <numberfield editable.expression="$use_typ.selection.id!='0600' and $use_typ.selection.id!='0700' and $use_typ.selection.id!='0950'" id="SO_#ROOM_FROM#_I_GE" maxvalue="999" minvalue="0" placeholder="min." span="6" span.s="12" title="Zimmer von" visibility.expression="$use_typ.selection.id!='0600' and $use_typ.selection.id!='0700' and $use_typ.selection.id!='0950'"/>
      <numberfield editable.expression="$use_typ.selection.id!='0600' and $use_typ.selection.id!='0700' and $use_typ.selection.id!='0950'" id="SO_#ROOM_TO#_I_LE" maxvalue="999" minvalue="0" placeholder="max." span="6" span.s="12" title="Zimmer bis" visibility.expression="$use_typ.selection.id!='0600' and $use_typ.selection.id!='0700' and $use_typ.selection.id!='0950'"/>
      <numberfield editable.expression="$use_typ.selection.id!='0600'" id="SO_#SQMETER_FROM#_I_GE" maxvalue="99999" minvalue="0" placeholder="in m²" span="6" span.s="12" suffix="m²" title="Fläche von" visibility.expression="$use_typ.selection.id!='0600'"/>
      <numberfield editable.expression="$use_typ.selection.id!='0600'" id="SO_#SQMETER_TO#_I_LE" maxvalue="99999" minvalue="0" placeholder="in m²" span="6" span.s="12" suffix="m²" title="Fläche bis" visibility.expression="$use_typ.selection.id!='0600'"/>
      <choicefield editable.expression="$use_typ.selection.id!='0600' and $use_typ.selection.id!='0700' and $use_typ.selection.id!='0950' and $use_typ.selection.id!='0500'" id="SO_#FLOOR_FROM#_I_GE" placeholder="min." span="6" span.s="12" title="Geschoss von          " visibility.expression="$use_typ.selection.id!='0600' and $use_typ.selection.id!='0700' and $use_typ.selection.id!='0950' and $use_typ.selection.id!='0500'">
        <choice id="001" title="EG"/>
        <choice id="002" title="1. OG"/>
        <choice id="003" title="2. OG"/>
        <choice id="004" title="3. OG"/>
        <choice id="005" title="4. OG"/>
        <choice id="006" title="5. OG"/>
        <choice id="007" title="6. OG"/>
        <choice id="008" title="7. OG"/>
        <choice id="009" title="8. OG"/>
        <choice id="010" title="9. OG"/>
        <choice id="011" title="10. OG"/>
        <choice id="012" title="11. OG"/>
        <choice id="013" title="12. OG"/>
        <choice id="014" title="13. OG"/>
        <choice id="015" title="14. OG"/>
        <choice id="016" title="15. OG"/>
        <choice id="017" title="16. OG"/>
        <choice id="018" title="17. OG"/>
        <choice id="019" title="18. OG"/>
        <choice id="020" title="19. OG"/>
      </choicefield>
      <choicefield editable.expression="$use_typ.selection.id!='0600' and $use_typ.selection.id!='0700' and $use_typ.selection.id!='0950' and $use_typ.selection.id!='0500'" id="SO_#FLOOR_TO#_I_LE" placeholder="max." span="6" span.s="12" title="Geschoss bis          " visibility.expression="$use_typ.selection.id!='0600' and $use_typ.selection.id!='0700' and $use_typ.selection.id!='0950' and $use_typ.selection.id!='0500'">
        <choice id="001" title="EG"/>
        <choice id="002" title="1. OG"/>
        <choice id="003" title="2. OG"/>
        <choice id="004" title="3. OG"/>
        <choice id="005" title="4. OG"/>
        <choice id="006" title="5. OG"/>
        <choice id="007" title="6. OG"/>
        <choice id="008" title="7. OG"/>
        <choice id="009" title="8. OG"/>
        <choice id="010" title="9. OG"/>
        <choice id="011" title="10. OG"/>
        <choice id="012" title="11. OG"/>
        <choice id="013" title="12. OG"/>
        <choice id="014" title="13. OG"/>
        <choice id="015" title="14. OG"/>
        <choice id="016" title="15. OG"/>
        <choice id="017" title="16. OG"/>
        <choice id="018" title="17. OG"/>
        <choice id="019" title="18. OG"/>
        <choice id="020" title="19. OG"/>
      </choicefield>
      <numberfield decimaldigits="2" id="SO_#NETCD#_I_LE" maxvalue="999999" minvalue="0" span="6" span.s="12" suffix=" €" title="Kaltmiete bis"/>
      <numberfield decimaldigits="2" id="SO_#GROSSCD#_I_LE" maxvalue="999999" minvalue="0" span="6" span.s="12" suffix=" €" title="Gesamtmiete bis"/>
    </section>
    <section title="Ausstattung" visibility.expression="($use_typ.selection.id!='0600' and $use_typ.selection.id!='0700' and $use_typ.selection.id!='0950' and $cf_search_variants.empty)? true : false">
      <choicefield id="SO_#ATTR_ID#_I_EQ" meta:parent_id="" multipleChoice="true" span="6" span.s="12" title="Ausstattungsmerkmale">
        <choice id="1020" title="Aufzug"/>
        <choice id="1054" title="Bad mit Fenster"/>
        <choice id="8023" title="Balkon / Loggia"/>
        <choice id="1040" title="Einbauküche"/>
        <choice id="1202" title="Küche mit Fenster"/>
        <choice id="1022" title="barrierearm"/>
        <choice id="1021" title="barrierefrei"/>
        <choice id="1091" title="möbliert"/>
      </choicefield>
    </section>
    <section title="Suche speichern" visibility.expression="$cf_search_variants.empty? true : false">
      <checkboxfield id="SAVE_FILTER" meta:noFilterText="X" refname="SAVE_FILTER" title="Diese Suche speichern" tooltip="Speichern Sie Ihre Suche ab, um zu einem späteren Zeitpunkt darauf zurückzugreifen."/>
      <checkboxfield id="SO_#NOTIFICATIONS#_I_EQ" meta:noFilterText="X" title="Benachrichtigung erhalten" tooltip="" visibility.expression="$SAVE_FILTER.checked"/>
      <separator leftSeparator="false" topSeparator="false"/>
      <button editable="true" id="BTN_SEARCH" span="12" span.s="12" title="Suchen" topSeparator="false" url="oppc://action?id=01search_re_obj"/>
    </section>
  </sheet>
</form>


Step 4:

GET https://portal1s.easysquare.com/prorex/xmlforms?application=ESQ_IA_REOBJ&sap-client=451&command=action&name=openform&id=400C82FA-7F52-8ACA-8F8F-6349A4A95BB1&api=6.139&head-oppc-version=6.139.10

Note: same as above, but action=openform

FIXME: maybe new step 3

Step 5:

POST https://portal1s.easysquare.com/prorex/xmlforms?application=ESQ_IA_REOBJ&sap-client=451&command=action&name=save&id=5DE5B21A-26B3-4B4F-8929-AB5AB897C91C&api=6.139&head-oppc-version=6.139.10&originalId=400C82FA-7F52-8ACA-8F8F-6349A4A95BB1

* id for form is generated in https://portal1s.easysquare.com/meinehowoge/%3Cunknown%3E/easy/app/easyform/splitApp/detail/FormDetail.controller.js?eval:formatted line 1825 : f = this.oHelper.generateGuid()
  * https://portal1s.easysquare.com/meinehowoge/%3Cunknown%3E/easy/app/view/libs/Helper.js?eval:formatted line 257: return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, function(e) { var t = 16 * Math.random() | 0; return ("x" == e ? t : 3 & t | 8).toString(16).toUpperCase() })
  * FIXME looks like normal GUID

Step 6:

GET https://portal1s.easysquare.com/prorex/xmlforms?application=ESQ_IA_REOBJ&sap-client=451&command=action&name=search_re_obj&id=5DE5B21A-26B3-4B4F-8929-AB5AB897C91C&api=6.139&head-oppc-version=6.139.10&originalId=400C82FA-7F52-8ACA-8F8F-6349A4A95BB1

Response: ?deepjump=/ESQ_IA_REOBJ/ESQ_VM_REOBJ_ALL

Step 7:

GET https://portal1s.easysquare.com/prorex/xmlforms?application=ESQ_IA_REOBJ&sap-client=451&command=action&name=boxlist&api=6.139&head-oppc-version=6.139.10&_=1645905104001

Response: XML!

<?xml version="1.0" encoding="utf-8"?>
<boxlist xmlns="http://www.openpromos.com/OPPC/XMLForms" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" serviceTitle="Immobiliensuche" xsi:schemaLocation="http://www.openpromos.com/OPPC/XMLForms ..\FormSchema.xsd">
  <preferences>
    <splash impressumTitle="Impressum" supportTitle="Support" supportURL="https://portal1s.easysquare.com/meinehowoge/index.html?devStyle=howoge#support" tourTitle="Registrierung" tourURL="http://www.easysquare.com/registration-form_de.html"/>
  </preferences>
  <section title="Immobilien">
    <box boxid="ESQ_VM_REOBJ_ALL" emptyText="Leider haben wir aktuell keine Treffer für Ihre Suchkriterien!" filterFormId="F563EDED-8777-8C01-0110-69CF43F80135" filtered="true" fullscreen="false" icon="sap-icon://Promos/search" icon_bg_color="#689835" icon_color="#FFFFFF" icon_int="" style="generic" subtitle="Wohnung, WBS nicht erforderlich" title="Immobilien" type="inbox">
      <sortCriteriaCaptions>
        <sortTitle>Titel</sortTitle>
        <sortCity>Stadt</sortCity>
        <sortPostcode>Postleitzahl</sortPostcode>
        <sortDate>Datum</sortDate>
        <sortDistance>Entfernung</sortDistance>
      </sortCriteriaCaptions>
      <head>
        <id>27BD27EC-9C35-E2D3-B559-A48607203DDE</id>
        <date/>
        <address city="" lat="52.5600754" lon="13.5089916" postcode="" street=""/>
        <title>Lichtdurchflutete 2-Zimmer-Wohnung mit Südbalkon</title>
        <subtitle>Rüdickenstrasse 25, 13053 Berlin (Beispielobjekt)</subtitle>
        <details>
          <row title="Stadtteil">Alt-Hohenschönhausen</row>
          <row title="Zimmer">2 </row>
          <row title="Wohnfläche">62 m²</row>
          <row title="Gesamtmiete">793,60  EUR</row>
          <row title="Verfügbarkeit">ab 01.04.2022</row>
        </details>
        <sortCriteria>
          <criterion position="0" title="Relevanz">B</criterion>
          <criterion position="0" title="Straße">BRüdickenstrasse 25</criterion>
          <criterion position="0" title="Gesamtmiete">B000000079360</criterion>
          <criterion position="0" title="Zimmer">B000000000002</criterion>
          <criterion position="0" title="Fläche">B000000620000</criterion>
          <criterion position="0" title="Verfügbar ab">B20220401</criterion>
        </sortCriteria>
        <image resourceId="E7372CD3-92A6-A918-0604-46A9CFD1864F"/>
        <image resourceId="DBB70678-2C3E-AFDF-8F7D-D6B5E5F34C7F"/>
        <image resourceId="CED55195-C105-4E2A-2162-3FF69A8DEA59"/>
        <image resourceId="C0D04FF7-57C1-6A37-6B83-4B26AC2256E6"/>
        <image resourceId="1D3B16DA-23A7-0C35-3E20-3867837FBBB5"/>
        <headBar barColor="#9e9e9e" barTextColor="#ffffff"/>
      </head>
      <head>
        <id>33E982CD-5762-9990-1759-F3F14D27D76E</id>
        <date/>
        <address city="" lat="52.5600754" lon="13.5089916" postcode="" street=""/>
        <title>Geräumige 1-Zimmer-Wohnung im Erstbezug Neubau</title>
        <subtitle>Rüdickenstrasse 27, 13053 Berlin (Beispielobjekt)</subtitle>
        <details>
          <row title="Stadtteil">Alt-Hohenschönhausen</row>
          <row title="Zimmer">1 </row>
          <row title="Wohnfläche">43 m²</row>
          <row title="Gesamtmiete">520,30  EUR</row>
          <row title="Verfügbarkeit">ab 01.04.2022</row>
        </details>
        <sortCriteria>
          <criterion position="0" title="Relevanz">B</criterion>
          <criterion position="0" title="Straße">BRüdickenstrasse 27</criterion>
          <criterion position="0" title="Gesamtmiete">B000000052030</criterion>
          <criterion position="0" title="Zimmer">B000000000001</criterion>
          <criterion position="0" title="Fläche">B000000430000</criterion>
          <criterion position="0" title="Verfügbar ab">B20220401</criterion>
        </sortCriteria>
        <image resourceId="E7372CD3-92A6-A918-0604-46A9CFD1864F"/>
        <image resourceId="DBB70678-2C3E-AFDF-8F7D-D6B5E5F34C7F"/>
        <image resourceId="CED55195-C105-4E2A-2162-3FF69A8DEA59"/>
        <image resourceId="C0D04FF7-57C1-6A37-6B83-4B26AC2256E6"/>
        <image resourceId="1D3B16DA-23A7-0C35-3E20-3867837FBBB5"/>
        <headBar barColor="#9e9e9e" barTextColor="#ffffff"/>
      </head>
      <head>
        <id>43DB86A2-D3C2-D70C-C330-74BA5AA5C1EB</id>
        <date/>
        <address city="" lat="52.6391007" lon="13.494148135426" postcode="" street=""/>
        <title>Anmietung nur für folgende Bedarfsgruppe - Azubi, Studenten, Doktoranden und wissenschaftliche Mitarbeiter!</title>
        <subtitle>Röbellweg 26, 13125 Berlin</subtitle>
        <details>
          <row title="Stadtteil">Buch</row>
          <row title="Zimmer">1 </row>
          <row title="Wohnfläche">22 m²</row>
          <row title="Gesamtmiete">410,65  EUR</row>
          <row title="Verfügbarkeit">ab 01.05.2022</row>
        </details>
        <sortCriteria>
          <criterion position="0" title="Relevanz">B</criterion>
          <criterion position="0" title="Straße">BRöbellweg 26</criterion>
          <criterion position="0" title="Gesamtmiete">B000000041065</criterion>
          <criterion position="0" title="Zimmer">B000000000001</criterion>
          <criterion position="0" title="Fläche">B000000224400</criterion>
          <criterion position="0" title="Verfügbar ab">B20220501</criterion>
        </sortCriteria>
        <image resourceId="35736C17-052A-44B1-491D-5F34FAEF1F10"/>
        <image resourceId="C1D0613F-8577-824E-8B03-FAB6595F0BDB"/>
        <image resourceId="767485B1-2766-DC1C-A380-861D4EC327E8"/>
        <image resourceId="865A70BD-32FE-1178-FADC-131E80D220D0"/>
        <image resourceId="5E5488F5-278C-D4F9-511A-E07088203BDF"/>
        <headBar barColor="#9e9e9e" barTextColor="#ffffff"/>
      </head>
      <head>
        <id>592AC70E-DD20-509B-AC8C-C77694E72132</id>
        <date/>
        <address city="" lat="52.5600754" lon="13.5089916" postcode="" street=""/>
        <title>4-Zimmer-Wohnung mit 2 Bädern und Südbalkon</title>
        <subtitle>Rüdickenstrasse 27, 13053 Berlin (Beispielobjekt)</subtitle>
        <details>
          <row title="Stadtteil">Alt-Hohenschönhausen</row>
          <row title="Zimmer">4 </row>
          <row title="Wohnfläche">95 m²</row>
          <row title="Gesamtmiete">1273,00  EUR</row>
          <row title="Verfügbarkeit">ab 01.04.2022</row>
        </details>
        <sortCriteria>
          <criterion position="0" title="Relevanz">B</criterion>
          <criterion position="0" title="Straße">BRüdickenstrasse 27</criterion>
          <criterion position="0" title="Gesamtmiete">B000000127300</criterion>
          <criterion position="0" title="Zimmer">B000000000004</criterion>
          <criterion position="0" title="Fläche">B000000950000</criterion>
          <criterion position="0" title="Verfügbar ab">B20220401</criterion>
        </sortCriteria>
        <image resourceId="E7372CD3-92A6-A918-0604-46A9CFD1864F"/>
        <image resourceId="DBB70678-2C3E-AFDF-8F7D-D6B5E5F34C7F"/>
        <image resourceId="CED55195-C105-4E2A-2162-3FF69A8DEA59"/>
        <image resourceId="C0D04FF7-57C1-6A37-6B83-4B26AC2256E6"/>
        <image resourceId="1D3B16DA-23A7-0C35-3E20-3867837FBBB5"/>
        <headBar barColor="#9e9e9e" barTextColor="#ffffff"/>
      </head>
      <head>
        <id>661F1714-EA90-6E2F-BA6F-65A957BB77BC</id>
        <date/>
        <address city="" lat="52.5613933" lon="13.5093202" postcode="" street=""/>
        <title>3-Zimmer-Wohnung mit praktischem Grundriss</title>
        <subtitle>Rotkamp 6, 13053 Berlin (Beispielobjekt)</subtitle>
        <details>
          <row title="Stadtteil">Alt-Hohenschönhausen</row>
          <row title="Zimmer">3 </row>
          <row title="Wohnfläche">78 m²</row>
          <row title="Gesamtmiete">1045,20  EUR</row>
          <row title="Verfügbarkeit">ab 16.03.2022</row>
        </details>
        <sortCriteria>
          <criterion position="0" title="Relevanz">B</criterion>
          <criterion position="0" title="Straße">BRotkamp 6</criterion>
          <criterion position="0" title="Gesamtmiete">B000000104520</criterion>
          <criterion position="0" title="Zimmer">B000000000003</criterion>
          <criterion position="0" title="Fläche">B000000780000</criterion>
          <criterion position="0" title="Verfügbar ab">B20220316</criterion>
        </sortCriteria>
        <image resourceId="E7372CD3-92A6-A918-0604-46A9CFD1864F"/>
        <image resourceId="DBB70678-2C3E-AFDF-8F7D-D6B5E5F34C7F"/>
        <image resourceId="CED55195-C105-4E2A-2162-3FF69A8DEA59"/>
        <image resourceId="C0D04FF7-57C1-6A37-6B83-4B26AC2256E6"/>
        <image resourceId="1D3B16DA-23A7-0C35-3E20-3867837FBBB5"/>
        <headBar barColor="#9e9e9e" barTextColor="#ffffff"/>
      </head>
      <head>
        <id>7498609A-1838-C20E-354F-E240F7DF6B6C</id>
        <date/>
        <address city="" lat="52.5600754" lon="13.5089916" postcode="" street=""/>
        <title>3-Zimmer-Wohnung mit separater und geräumiger Küche</title>
        <subtitle>Rüdickenstraße 23, 13053 Berlin (Beispielobjekt)</subtitle>
        <details>
          <row title="Stadtteil">Alt-Hohenschönhausen</row>
          <row title="Zimmer">3 </row>
          <row title="Wohnfläche">81 m²</row>
          <row title="Gesamtmiete">1101,60  EUR</row>
          <row title="Verfügbarkeit">ab sofort</row>
        </details>
        <sortCriteria>
          <criterion position="0" title="Relevanz">B</criterion>
          <criterion position="0" title="Straße">BRüdickenstraße 23</criterion>
          <criterion position="0" title="Gesamtmiete">B000000110160</criterion>
          <criterion position="0" title="Zimmer">B000000000003</criterion>
          <criterion position="0" title="Fläche">B000000810000</criterion>
          <criterion position="0" title="Verfügbar ab">B20181001</criterion>
        </sortCriteria>
        <image resourceId="E7372CD3-92A6-A918-0604-46A9CFD1864F"/>
        <image resourceId="DBB70678-2C3E-AFDF-8F7D-D6B5E5F34C7F"/>
        <image resourceId="CED55195-C105-4E2A-2162-3FF69A8DEA59"/>
        <image resourceId="C0D04FF7-57C1-6A37-6B83-4B26AC2256E6"/>
        <image resourceId="1D3B16DA-23A7-0C35-3E20-3867837FBBB5"/>
        <headBar barColor="#9e9e9e" barTextColor="#ffffff"/>
      </head>
      <head>
        <id>84955258-0571-EE52-8FBA-E2432A107FAB</id>
        <date/>
        <address city="" lat="52.5613933" lon="13.5093202" postcode="" street=""/>
        <title>2-Zimmer-Wohnung im Erstbezug Neubau mit separater Küche</title>
        <subtitle>Rotkamp 6, 13053 Berlin (Beispielobjekt)</subtitle>
        <details>
          <row title="Stadtteil">Alt-Hohenschönhausen</row>
          <row title="Zimmer">2 </row>
          <row title="Wohnfläche">54 m²</row>
          <row title="Gesamtmiete">696,60  EUR</row>
          <row title="Verfügbarkeit">ab 16.03.2022</row>
        </details>
        <sortCriteria>
          <criterion position="0" title="Relevanz">B</criterion>
          <criterion position="0" title="Straße">BRotkamp 6</criterion>
          <criterion position="0" title="Gesamtmiete">B000000069660</criterion>
          <criterion position="0" title="Zimmer">B000000000002</criterion>
          <criterion position="0" title="Fläche">B000000540000</criterion>
          <criterion position="0" title="Verfügbar ab">B20220316</criterion>
        </sortCriteria>
        <image resourceId="E7372CD3-92A6-A918-0604-46A9CFD1864F"/>
        <image resourceId="DBB70678-2C3E-AFDF-8F7D-D6B5E5F34C7F"/>
        <image resourceId="CED55195-C105-4E2A-2162-3FF69A8DEA59"/>
        <image resourceId="C0D04FF7-57C1-6A37-6B83-4B26AC2256E6"/>
        <image resourceId="1D3B16DA-23A7-0C35-3E20-3867837FBBB5"/>
        <headBar barColor="#9e9e9e" barTextColor="#ffffff"/>
      </head>
      <head>
        <id>BCF488D0-DFDD-4C45-05E7-28ED0EB9C048</id>
        <date/>
        <address city="" lat="52.6279206" lon="13.4998089" postcode="" street=""/>
        <title/>
        <subtitle>Robert-Rössle-Straße 4, 13125 Berlin</subtitle>
        <details>
          <row title="Stadtteil">Buch</row>
          <row title="Zimmer">3 </row>
          <row title="Wohnfläche">85 m²</row>
          <row title="Gesamtmiete">907,87  EUR</row>
          <row title="Verfügbarkeit">ab 01.05.2022</row>
        </details>
        <sortCriteria>
          <criterion position="0" title="Relevanz">B</criterion>
          <criterion position="0" title="Straße">BRobert-Rössle-Straße 4</criterion>
          <criterion position="0" title="Gesamtmiete">B000000090787</criterion>
          <criterion position="0" title="Zimmer">B000000000003</criterion>
          <criterion position="0" title="Fläche">B000000858700</criterion>
          <criterion position="0" title="Verfügbar ab">B20220501</criterion>
        </sortCriteria>
        <image resourceId="A40EBF19-071A-B9FA-F3FA-57BFA1550083"/>
        <image resourceId="41164362-2EC0-32BD-61BB-D9072B5517D9"/>
        <image resourceId="82A1C257-3E65-9763-1E18-C4B963945A64"/>
        <image resourceId="52992F6D-50AE-9218-09E7-6B6283DA451A"/>
        <headBar barColor="#9e9e9e" barTextColor="#ffffff"/>
      </head>
      <head>
        <id>C3D7E6B8-83A1-AA73-F9FC-8D5DBFE4ABF9</id>
        <date/>
        <address city="" lat="52.4621859" lon="13.4726959" postcode="" street=""/>
        <title>II Zimmer Wohnung in der High-Deck-Siedlung in Neukölln</title>
        <subtitle>Leo-Slezak-Straße 25, 12057 Berlin</subtitle>
        <details>
          <row title="Stadtteil">Neukölln</row>
          <row title="Zimmer">1 </row>
          <row title="Wohnfläche">61 m²</row>
          <row title="Gesamtmiete">700,00  EUR</row>
          <row title="Verfügbarkeit">ab sofort</row>
        </details>
        <sortCriteria>
          <criterion position="0" title="Relevanz">B</criterion>
          <criterion position="0" title="Straße">BLeo-Slezak-Straße 25</criterion>
          <criterion position="0" title="Gesamtmiete">B000000070000</criterion>
          <criterion position="0" title="Zimmer">B000000000001</criterion>
          <criterion position="0" title="Fläche">B000000615200</criterion>
          <criterion position="0" title="Verfügbar ab">B20220201</criterion>
        </sortCriteria>
        <image resourceId="E0C0A937-F983-B9DE-D11E-7EE10EEC20AC"/>
        <headBar barColor="#9e9e9e" barTextColor="#ffffff"/>
      </head>
      <head>
        <id>D804D9E6-522A-16CB-5112-8044ACDBC792</id>
        <date/>
        <address city="" lat="52.5600754" lon="13.5089916" postcode="" street=""/>
        <title>Große 4-Zimmer-Wohnung mit zwei Bädern (Dusche &amp; Badewanne)</title>
        <subtitle>Rüdickenstrasse 25, 13053 Berlin (Beispielobjekt)</subtitle>
        <details>
          <row title="Stadtteil">Alt-Hohenschönhausen</row>
          <row title="Zimmer">4 </row>
          <row title="Wohnfläche">97 m²</row>
          <row title="Gesamtmiete">1299,80  EUR</row>
          <row title="Verfügbarkeit">ab 01.04.2022</row>
        </details>
        <sortCriteria>
          <criterion position="0" title="Relevanz">B</criterion>
          <criterion position="0" title="Straße">BRüdickenstrasse 25</criterion>
          <criterion position="0" title="Gesamtmiete">B000000129980</criterion>
          <criterion position="0" title="Zimmer">B000000000004</criterion>
          <criterion position="0" title="Fläche">B000000970000</criterion>
          <criterion position="0" title="Verfügbar ab">B20220401</criterion>
        </sortCriteria>
        <image resourceId="E7372CD3-92A6-A918-0604-46A9CFD1864F"/>
        <image resourceId="DBB70678-2C3E-AFDF-8F7D-D6B5E5F34C7F"/>
        <image resourceId="CED55195-C105-4E2A-2162-3FF69A8DEA59"/>
        <image resourceId="C0D04FF7-57C1-6A37-6B83-4B26AC2256E6"/>
        <image resourceId="1D3B16DA-23A7-0C35-3E20-3867837FBBB5"/>
        <headBar barColor="#9e9e9e" barTextColor="#ffffff"/>
      </head>
    </box>
    <box boxid="ESQ_IA_FAV_2" emptyText="Leider haben wir aktuell keine Treffer für Ihre Suchkriterien." fullscreen="false" icon="sap-icon://Promos/heart-a" icon_bg_color="#1C5D89" icon_color="#FFFFFF" icon_int="" style="generic" title="Favoriten" type="inbox">
      <sortCriteriaCaptions>
        <sortTitle>Titel</sortTitle>
        <sortCity>Stadt</sortCity>
        <sortPostcode>Postleitzahl</sortPostcode>
        <sortDate>Datum</sortDate>
        <sortDistance>Entfernung</sortDistance>
      </sortCriteriaCaptions>
    </box>
    <box boxid="ESQ_IA_SAVED_FILTER_2" emptyText="Leider haben wir aktuell keine Treffer für Ihre Suchkriterien." fullscreen="false" icon="sap-icon://Promos/search-immo-b" icon_bg_color="#577CA0" icon_color="#FFFFFF" icon_int="" style="generic" title="Gespeicherte Suche" type="inbox">
      <sortCriteriaCaptions>
        <sortTitle>Titel</sortTitle>
        <sortCity>Stadt</sortCity>
        <sortPostcode>Postleitzahl</sortPostcode>
        <sortDate>Datum</sortDate>
        <sortDistance>Entfernung</sortDistance>
      </sortCriteriaCaptions>
    </box>
    <box boxid="ESQ_IA_FILT_UNSUBSCRIBE" fullscreen="true" icon="sap-icon://Promos/tray" icon_bg_color="#577CA0" icon_color="#FFFFFF" icon_int="" style="generic" title="Abbestellen von Benachrichtigungen" type="hidden">
      <sortCriteriaCaptions>
        <sortTitle>Titel</sortTitle>
        <sortCity>Stadt</sortCity>
        <sortPostcode>Postleitzahl</sortPostcode>
        <sortDate>Datum</sortDate>
        <sortDistance>Entfernung</sortDistance>
      </sortCriteriaCaptions>
      <head>
        <id>99051868-0E60-B141-1870-D7B2E182D489</id>
        <date/>
        <address city="" postcode="" street=""/>
        <title>Benachrichtigungen abbestellt</title>
      </head>
    </box>
    <box boxid="ESQ_VM_REOBJ_HIDDEN" emptyText="Leider haben wir aktuell keine Treffer für Ihre Suchkriterien." fullscreen="false" icon="sap-icon://Promos/tray" icon_bg_color="#577CA0" icon_color="#FFFFFF" icon_int="" style="generic" title="Immobilien" type="hidden">
      <sortCriteriaCaptions>
        <sortTitle>Titel</sortTitle>
        <sortCity>Stadt</sortCity>
        <sortPostcode>Postleitzahl</sortPostcode>
        <sortDate>Datum</sortDate>
        <sortDistance>Entfernung</sortDistance>
      </sortCriteriaCaptions>
    </box>
  </section>
  <section title=""/>
</boxlist>

If more info is needed:

GET https://portal1s.easysquare.com/prorex/xmlforms?application=ESQ_IA_REOBJ&sap-client=451&command=action&name=get&id=27BD27EC-9C35-E2D3-B559-A48607203DDE&api=6.139&head-oppc-version=6.139.10

* id = item id from boxlist

Reponse: XML!

<?xml version="1.0" encoding="utf-8"?>
<form xmlns="http://www.openpromos.com/OPPC/XMLForms" xmlns:meta="http://www.openpromos.com/OPPC/XMLFormsMetaData" xmlns:oppc="http://www.openpromos.com/OPPC/XMLForms" xmlns:prv="urn:mine" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="27BD27EC-9C35-E2D3-B559-A48607203DDE" originalId="DA34A49A-DA09-A8D6-9575-B089FCD95390" xsi:schemaLocation="http://www.openpromos.com/OPPC/XMLForms ..\FormSchema.xsd">
  <head>
    <originalId>DA34A49A-DA09-A8D6-9575-B089FCD95390</originalId>
  </head>
  <actions>
    <action icon="sap-icon://Promos/heart-b" id="02fav_int" includeInQuick="true" title="Als Favorit markieren">
      <type>
        <server command="$BS_MARKQUICK" locksForm="true" waitForResponse="true"/>
      </type>
    </action>
    <action icon="sap-icon://Promos/paperplane" id="do_create_or" includeInMenu="false" includeInQuick="true" style="cancel" title="Anfragen          ">
      <type>
        <server command="do_create_or" locksForm="true" waitForResponse="true"/>
      </type>
    </action>
  </actions>
  <sheet>
    <section id="ESQ_FORM_VALIDATION" visibility="hidden">
      <textfield editable="false" id="ESQ_CHANGED" text.expression="'true'" title="Technisch: Aktualisiert?" visibility="hidden">false</textfield>
      <textfield id="ESQ_IS_IN_CONTEXT" visibility="hidden"/>
    </section>
    <section visibility="hidden">
      <textfield editable="false" id="tfaccntnr" title="acc" visibility="hidden"/>
      <textfield id="SO_#OBJID#_I_EQ" visibility="hidden">RO42788</textfield>
      <textfield id="SO_#OBJ_ID#_I_EQ" visibility="hidden">RO42788</textfield>
    </section>
    <section bottomSeparator="false" meta:print="X" topSeparator="false">
      <notefield alignment="left" span="9" span.s="12" textSize="regular" topSeparator="false">## Lichtdurchflutete 2-Zimmer-Wohnung mit Südbalkon</notefield>
      <notefield alignment="left" span="9" span.s="12" textSize="regular" topSeparator="false">### Rüdickenstrasse 25, 0200, 13053 Berlin (Beispielobjekt)</notefield>
      <notefield alignment="left" span="9" span.s="12" textSize="regular" topSeparator="false">****</notefield>
    </section>
    <section bottomSeparator="false">
      <galleryfield scale="aspectFill" topSeparator="true" zoom="true">
        <image resourceId="2B07EF92-677D-4C7B-818B-69B4364EC7CB"/>
        <image resourceId="8BCE93A1-BC5D-4015-B58B-71FB40254978"/>
        <image resourceId="0777D4C2-68B6-449D-AD62-AC6E67DFCA7D"/>
        <image resourceId="C58D4656-E354-4353-A2AA-235CD8E6E734"/>
        <image descriptionText="Lageplan Haus 1 / Haus 2" descriptionTitle="Lageplan Haus 1 / Haus 2" resourceId="339BD6C3-A9AA-432C-9A67-283D72D229B2"/>
        <image resourceId="F8C2F248-095B-44FC-8DF4-FD976416E142"/>
        <image resourceId="9FAAEFEE-0CD1-A39B-0E96-01BCDB4D8F90"/>
        <image resourceId="A9D123A2-CB03-47B7-9471-714297D6E099"/>
        <image resourceId="82FE5E8B-5250-4859-A6E7-9EC0B18C0FCB"/>
        <image resourceId="51BDEB22-98D8-4D6C-9310-5434E2366C2D"/>
        <image resourceId="1316AA73-FAD5-431F-8092-116D7D11A1EE"/>
        <image descriptionText="Grundriss" descriptionTitle="Grundriss" resourceId="090854D1-F2BC-4954-B0F8-87E9FE08C0D1"/>
        <image resourceId="185E9A33-2750-7AA4-0363-4D0A46E2DEFE"/>
        <image resourceId="FD3C9F4B-F893-305D-8C05-A8BC81D15567"/>
      </galleryfield>
      <separator leftSeparator="false" span="12" span.s="12" topSeparator="false"/>
      <notefield icon="sap-icon://Promos/floorplan" iconSize="huge" leftSeparator="false" meta:component="MEAS_A799" meta:itemname="FX_MEAS" span="3" span.m="6" span.s="6" style="item" textSize="regular" topSeparator="false">Wohnfläche          
62,00 m²</notefield>
      <notefield icon="sap-icon://Promos/house-with-euro" iconSize="huge" leftSeparator="false" meta:component="MEAS_A799" meta:itemname="FX_MEAS" span="3" span.m="6" span.s="6" style="item" textSize="regular" topSeparator="false">Gesamtmiete          
793,60 EUR</notefield>
      <notefield icon="sap-icon://Promos/door" iconSize="huge" leftSeparator="false" meta:component="MEAS_Z100" meta:itemname="FX_MEAS" span="3" span.m="6" span.s="6" style="item" textSize="regular" topSeparator="false">Zimmer          
2</notefield>
      <notefield icon="sap-icon://Promos/stopwatch" iconSize="huge" leftSeparator="false" meta:component="MEAS_Z100" meta:itemname="FX_MEAS" span="3" span.m="6" span.s="6" style="item" textSize="regular" topSeparator="false">Verfügbar ab          
01.04.2022</notefield>
    </section>
    <section bottomSeparator="false" meta:print="X" title="Angaben zum Objekt          ">
      <notefield leftSeparator="false" span="4" span.s="6" textSize="regular" titleColor="#7e7e7e" topSeparator="true">###### Nutzungsart          
Wohnung</notefield>
      <notefield leftSeparator="false" span="4" span.s="6" textSize="regular" titleColor="#7e7e7e" topSeparator="true">###### Stadtteil          
Alt-Hohenschönhausen</notefield>
      <notefield leftSeparator="false" span="4" span.s="12" textSize="regular" titleColor="#7e7e7e" topSeparator="true">###### Mietobjektnummer (Angebotsobjekt)                 
1771/14589/994 (98837)</notefield>
      <notefield leftSeparator="false" span="4" span.s="6" textSize="regular" titleColor="#7e7e7e" topSeparator="false" visibility="hidden">###### Besichtigung ab
-</notefield>
      <notefield leftSeparator="false" span="4" span.s="6" textSize="regular" titleColor="#7e7e7e" topSeparator="false">###### WBS erforderlich          
nein          </notefield>
      <notefield leftSeparator="false" span="4" span.s="6" textSize="regular" titleColor="#7e7e7e" topSeparator="false" visibility="hidden">###### Finanzierungsart
</notefield>
      <notefield id="SO_#TARGET#_I_EQ_NF" leftSeparator="false" span="4" span.s="6" textSize="regular" titleColor="#7e7e7e" topSeparator="false" visibility="hidden">###### Zielgruppe
</notefield>
      <notefield leftSeparator="false" span="4" span.s="6" textSize="regular" titleColor="#7e7e7e" topSeparator="false">###### Baujahr          
2022</notefield>
      <notefield leftSeparator="false" span="4" span.s="12" textSize="regular" titleColor="#7e7e7e" topSeparator="false">###### Gebäudeart / Anzahl Geschosse               
Neubau ab 2014 / 7</notefield>
    </section>
    <section bottomSeparator="false" title="Energieausweis          " topSeparator="false">
      <notefield leftSeparator="false" span="4" span.s="12" textSize="regular" titleColor="#7e7e7e" topSeparator="true">###### Energieausweistyp          
Bedarfsausweis mit WW</notefield>
      <notefield leftSeparator="false" span="4" span.s="12" textSize="regular" titleColor="#7e7e7e" topSeparator="true">###### Energiewert          
59.9 kWh/(m²a)</notefield>
      <notefield leftSeparator="false" span="4" span.s="12" textSize="regular" titleColor="#7e7e7e" topSeparator="true">###### Energieeffizienzklasse           
B</notefield>
      <notefield leftSeparator="false" span="4" span.s="12" textSize="regular" titleColor="#7e7e7e" topSeparator="false">###### Wesentlicher Energieträger             
Fernwärme</notefield>
      <notefield leftSeparator="false" span="4" span.s="12" textSize="regular" titleColor="#7e7e7e" topSeparator="false">###### Baujahr          
2022</notefield>
      <notefield id="SO_#EPASS_DATE#_I_EQ" leftSeparator="false" span="4" span.s="12" textSize="regular" titleColor="#7e7e7e" topSeparator="false">###### gültig bis
04.05.2031</notefield>
    </section>
    <section bottomSeparator="false" title="Dokumente          " topSeparator="false">
      <sheet icon="sap-icon://Promos/pdf" leftSeparator="false" span="4" span.s="6" title="Exposé" topSeparator="true">
        <section bottomSeparator="false" topSeparator="false">
          <pdffield height="fullscreen" resourceId="openobjprint20220226_RO42788" topSeparator="false"/>
        </section>
      </sheet>
      <sheet icon="sap-icon://Promos/pdf" leftSeparator="false" span="4" span.s="6" title="Energieausweis" topSeparator="true">
        <section bottomSeparator="false" topSeparator="false">
          <pdffield height="fullscreen" resourceId="32362AA3-F3D3-702D-C58E-0B9E409B9338" topSeparator="false"/>
        </section>
      </sheet>
    </section>
    <section bottomSeparator="false" title="Kosten          " topSeparator="false">
      <notefield leftSeparator="false" span="4" span.s="12" textSize="regular" titleColor="#7e7e7e" topSeparator="true">###### Kaltmiete          
632,40 EUR (10,20 EUR/m²)</notefield>
      <notefield leftSeparator="false" span="4" span.m="4" span.s="12" textSize="regular" titleColor="#7e7e7e" topSeparator="true">###### Betriebskosten          
99,20 EUR</notefield>
      <notefield leftSeparator="false" span="4" span.s="6" textSize="regular" titleColor="#7e7e7e" topSeparator="true">###### Heizkosten          
62,00 EUR</notefield>
      <notefield leftSeparator="false" span="4" span.s="6" textSize="regular" titleColor="#7e7e7e" topSeparator="false">###### Gesamtmiete          
793,60 EUR</notefield>
      <notefield id="SO_#SURETYCD#_I_EQ" leftSeparator="false" span="4" span.s="6" textSize="regular" titleColor="#7e7e7e" topSeparator="false">###### Kaution          
1.897,20 EUR</notefield>
      <separator leftSeparator="false" span="4" span.s="12" topSeparator="false"/>
    </section>
    <section bottomSeparator="false" id="AUSSTATTUNG" title="Ausstattung des Mietobjekts              ">
      <notefield icon="sap-icon://Promos/check" iconColor="#159010" iconSize="small" leftSeparator="false" span="4" span.s="6" topSeparator="true">Aufzug</notefield>
      <notefield icon="sap-icon://Promos/check" iconColor="#159010" iconSize="small" leftSeparator="false" span="4" span.s="6" topSeparator="true">Bad mit Dusche</notefield>
      <notefield icon="sap-icon://Promos/check" iconColor="#159010" iconSize="small" leftSeparator="false" span="4" span.s="6" topSeparator="true">Balkon / Loggia</notefield>
      <notefield icon="sap-icon://Promos/check" iconColor="#159010" iconSize="small" leftSeparator="false" span="4" span.s="6" topSeparator="false">Highspeed-Internetanschluss</notefield>
      <notefield icon="sap-icon://Promos/check" iconColor="#159010" iconSize="small" leftSeparator="false" span="4" span.s="6" topSeparator="false">offene Küche</notefield>
      <notefield leftSeparator="false" span="4" span.s="6" topSeparator="false"/>
    </section>
    <section id="objktb" title="Objektbeschreibung          ">
      <notefield icon="sap-icon://Promos/flash" iconSize="small" leftSeparator="false" span="12" span.s="12" topSeparator="true">Lichtdurchflutete 2-Zimmer-Wohnung mit Südbalkon</notefield>
      <notefield icon="sap-icon://Promos/floorplan" iconSize="small" leftSeparator="false" span="12" span.s="12" topSeparator="false">Die Wohnung verfügt über einen ansprechenden Grundriss, der die ideale Raumaufteilung aufzeigt. 

Die bodentiefen Fenster sorgen im Wohnbereich für eine einzigartige Lichtdurchflutung. Die im Wohnraum vorhandene Küche liegt separat zum Rest des Raumes in einer Nische und lässt sich somit auf Wunsch optimal abgrenzen.  

Der gesamte Raum ist mit einem ansprechenden PVC-Fußboden in Holzoptik ausgestattet. Jeder Raum der Wohnung verfügt über eine Fußbodenheizung, welche eine für jedermann individuell angenehme Raumtemperatur garantiert. 

Zeitlos und modern erscheinen die gespachtelten Wände in der Farbe warmweiß. 

Auch das Bad erhöht den Wohlfühlfaktor mit großformatigen Fliesen und hochwertiger sanitärer Ausstattung.  Zusätzlich garantiert ein Handtuchheizkörper wohlige Wärme an kalten Tagen.

Sonniges Wetter können Sie auf dem großzügigen Balkon genießen, welcher direkt an den zweiten Wohnraum angrenzt.

Bei dieser Wohneinheit handelt es sich um eine einkommensorientierte Wohnung. Bitte beachten Sie, dass Sie sich nur auf diese Wohnung bewerben können, wenn Ihr Einkommen in einem Bereich zwischen 180 und 240% liegt. Um herauszufinden, welchem Einkommensbereich Ihr Einkommen entspricht, nutzen Sie bitte den nachstehenden Einkommensrechner, welcher vom Land Berlin zur Verfügung gestellt wird: https://ssl.stadtentwicklung.berlin.de/wohnen/wbs/wbsformular.shtml
Sollte Ihr Einkommen nicht in der oben genannten Spanne liegen, bewerben Sie sich gerne für andere Wohnungen im Projekt! 

Bitte beachten Sie, dass es sich bei den Bildern in der Anzeige um Beispielfotos aus unseren Musterwohnungen handelt, da sich die inserierten Wohnungen derzeit noch im Bau befinden. Eine Besichtigung erfolgt ebenfalls ausschließlich in einer 2-Zimmer- und / oder 3-Zimmer-Musterwohnung.

</notefield>
      <notefield icon="sap-icon://Promos/housing-complex" iconSize="small" leftSeparator="false" span="12" span.s="12" topSeparator="false">Sie suchen ein Zuhause, das ruhig und trotzdem verkehrsgünstig gelegen ist? Dann haben Sie sich für das richtige Objekt entschieden.

Gerade einmal 30 Minuten vom Berliner Stadtzentrum entfernt, nahe dem Lindencenter und der Naturschutzgebiete Malchower Aue und Fauler See, befindet sich das neue HOWOGE-Neubauprojekt Mühlengrund.

Das neu entstandene Wohnobjekt umfasst 215 Wohneinheiten, 74 PKW-Stellplätze in der Tiefgarage sowie diverse Gewerbeflächen. Der Mühlengrund wird, nach Bezug aller Gewerbeeinheiten, ein in sich geschlossenes Quartier darstellen, das eine Vielzahl an notwendigen Bedarfen beinhalten wird (z. B. Lebensmitteleinzelhandel, Friseur, Spätkauf, Schnellrestaurants, Ärztezentrum etc.). 

Die zwei Gebäude verfügen über sechs und sieben Vollgeschosse. Jeder Hausaufgang ist stufenlos zugänglich und verfügt über einen Aufzug.

Abstellmöglichkeiten für Fahrräder und Kinderwagen sind ebenfalls im Innen- sowie Außenbereich zu finden. Der große Innenhof lädt mit liebevoll gestalteten Grünflächen und Sitzmöglichkeiten, sowie dem Rundweg zu verschiedenen Spielgeräten zum Verweilen oder Austoben der kleinen Bewohner ein.

Als zukünftige Mieter:innen haben Sie die Möglichkeit, Öko-Strom zu beziehen und nebenbei einen guten Beitrag für die Umwelt zu leisten. Überzeugend ist dahingehend nicht nur der Nachhaltigkeitsfaktor, sondern auch unsere preiswerten Konditionen und kundenorientierten Vertragsbedingungen.

Der Mühlengrund in Berlin-Hohenschönhausen ist sehr vielfältig: Das Linden Center ist in wenigen Gehminuten zu erreichen und bietet die Möglichkeit für Shopping-Erlebnisse. Im näheren Umkreis findet sich eine große kulinarische Vielfalt von Sushi bis hin zu Pizza und die nahe gelegenen Kleingärten oder der Malchower See laden zum Ausruhen ein.
Zudem sorgen die nahe gelegene Schwimmhalle Zingster Straße, die Anna-Seghers-Bibliothek, ein Gesundheitszentrum sowie Schulen und Kitas in der unmittelbaren Umgebung für einen bequemen Wohnalltag. Für eine optimale Versorgung im Kiez werden in den kommenden Jahren weitere Arztpraxen, Restaurants oder Supermärkte ihre Türen auf dem Mühlengrund öffnen. Dank der fußläufig entfernten Straßenbahn- und S-Bahn-Anschlüsse ist man innerhalb kürzester Zeit in Berlins Zentrum.

Warum Sie Mieter bei der HOWOGE Wohnungsbaugesellschaft mbH werden sollten? Wir bieten Ihnen einen Rundumservice. Ihr Wasserhahn tropft? Sie sind gesundheitlich eingeschränkt und brauchen Hilfe? Sie fühlen sich durch nächtlichen Lärm gestört? Unsere Hausmeister, Kiezhelfer, Concierges und die Mobilen Hausmeister sind in Ihrer Nähe und kümmern sich.

Wohnen in stabilen und sicheren Quartieren: Unsere mobilen Hausmeister bestreifen alle Quartiere der HOWOGE in der Nacht. Mit den kundenfreundlichen Telefonzeiten unserer Kundenzentren sind wir stets unkompliziert für unsere Mieter erreichbar. https://www.howoge.de/mieterservice/ansprechpartner.html

Selbst in Havarie- oder Notfällen außerhalb unserer Geschäftszeiten bieten wir einen Havariedienst, der zur Stelle ist, wenn man ihn braucht.

Wir sind eine von sechs kommunalen Wohnungsbaugesellschaften in Berlin und zählen mit rund 73.000 Mietwohnungen zu den zehn größten Vermietern deutschlandweit. Durch unsere zahlreichen Neubauprojekte und den Ankauf von Immobilien erweitern wir unseren Bestand kontinuierlich und werden so der steigenden Nachfrage nach bezahlbarem Wohnraum gerecht.

Wir gestalten Berliner Kieze sozial, zukunftsorientiert und nachhaltig. Die HOWOGE stellt nachhaltiges Denken und Handeln in den Mittelpunkt. Als eine der größten Wohnungsbaugesellschaften Berlins haben Umwelt- und Klimaschutz bei uns einen hohen Stellenwert. Unser weitreichendes Engagement wurde unter anderem bereits mit dem Deutschen Nachhaltigkeitspreis ausgezeichnet. In unseren Wohnungen in verschiedenen Stadtteilen Berlins leben insgesamt mehr als 100.000 Menschen, die ihren Kiez individuell und einzigartig machen.
</notefield>
    </section>
  </sheet>
</form>


'''

#website_url = 'https://portal1s.easysquare.com/meinehowoge/index.html' # only needed, if we need to refetch brandconfig_url

#brandconfig_url = 'https://portal1s.easysquare.com/meinehowoge/~20211124135010~/brands/howoge/brandconfig.json'
brandconfig = {
	"config": {
		"appName": "Meine HOWOGE",
		"customerIconfontPath": "icons/Howoge-Icons.json",
		"customerIconfontName": "Howoge"
	},
	"features": {
		"demoAccountUser": "WOA74263",
		"demoAccountPassword": "Ajd3z4Qd4"
	}
}
# used as "sap-ffield_b64" in payload in API requests
auth_str_username_only = base64.b64encode(f"user={brandconfig['features']['demoAccountUser']}".encode('utf-8')).decode('utf-8')
auth_str = base64.b64encode(f"user={brandconfig['features']['demoAccountUser']}&password={brandconfig['features']['demoAccountPassword']}".encode('utf-8')).decode('utf-8')

api_url = 'https://portal1s.easysquare.com/meinehowoge/api5'
xmlforms_url = 'https://portal1s.easysquare.com/prorex/xmlforms'
xmlforms_ns = {
  'x': 'http://www.openpromos.com/OPPC/XMLForms',
  'meta': 'http://www.openpromos.com/OPPC/XMLFormsMetaData'
}

default_params = {
  'api': '6.139',
  'sap-language': 'de'
}

s = requests.Session()

search_headers = {
    'accept': '*/*',
    'origin': 'https://portal1s.easysquare.com',
    'x-requested-with': 'XMLHttpRequest',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
}

common_headers = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'pragma': 'no-cache',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'cache-control': 'no-cache',
    'authority': 'portal1s.easysquare.com',
    'referer': 'https://portal1s.easysquare.com/meinehowoge/'
}
s.headers.update(common_headers)

s.cookies.update({
  'esq-alias': '/meinehowoge',
  'sap-usercontext': 'sap-client=451'
})

def scrape(params):

    api_params = {}
    api_params.update(default_params)

    # authenticate
    auth = s.post(f'{api_url}/authenticate?{urlencode(api_params)}', data=urlencode({'sap-ffield_b64':auth_str}), headers=search_headers)
    auth.raise_for_status()
    
    # submit boxlist request
    # GET https://portal1s.easysquare.com/prorex/xmlforms?application=ESQ_IA_REOBJ&sap-client=451&command=action&name=boxlist&api=6.139&head-oppc-version=6.139.10&_=1645903079761

    boxlist_params = {
      'application': 'ESQ_IA_REOBJ',
      'sap-client': 451,
      'command': 'action',
      'name': 'boxlist',
      'api': '6.139',
      'head-oppc-version': '6.139.10',
      '_': int(datetime.timestamp(datetime.now()))
    }
    boxlist = s.get(f'{xmlforms_url}?{urlencode(boxlist_params)}', headers=search_headers)

    boxlist_tree = etree.XML(boxlist.text.encode('utf-8'))
    # get search box ID
    box_search = boxlist_tree.xpath("//x:box[contains(@boxid,'ESQ_VM_REOBJ_ALL')]/@filterFormId", namespaces=xmlforms_ns)
    if len(box_search) == 0:
      raise Exception('No flat search box found')
    
    filter_form_id = box_search[0]

    # get form
    #GET https://portal1s.easysquare.com/prorex/xmlforms?application=ESQ_IA_REOBJ&sap-client=451&command=action&name=get&id=400C82FA-7F52-8ACA-8F8F-6349A4A95BB1&api=6.139&head-oppc-version=6.139.10

    forms_params = {
      'application': 'ESQ_IA_REOBJ',
      'sap-client': 451,
      'command': 'action',
      'name': 'get',
      'id': filter_form_id,
      'head-oppc-version': '6.139.10'
    }

    html_result = s.get(f'{xmlforms_url}?{urlencode(forms_params)}', headers=search_headers)

    form_tree = etree.XML(html_result.text.encode('utf-8'))

    # generate new uuid
    new_uuid = str(uuid.uuid4()).upper()

    # set id in <form>
    form_tree.attrib['id'] = new_uuid
    # set id in <head>
    head_tree = form_tree.xpath('//x:head', namespaces=xmlforms_ns)[0]
    head_id = head_tree.xpath('//x:id', namespaces=xmlforms_ns)
    if len(head_id) > 0:
      head_id[0].text = new_uuid
    else:
      head_id = etree.SubElement(head_tree, 'id')
      head_id.text = new_uuid

    # add <history>
    history = etree.SubElement(form_tree, 'history')
    save = etree.SubElement(history,'save')
    save.attrib['oldId'] = filter_form_id
    save.attrib['newId'] = new_uuid
    save.attrib['userName'] = brandconfig['features']['demoAccountUser']
    save.attrib['timestamp'] = datetime.isoformat(datetime.now(), timespec='seconds')

    # apply filter settings
    wbs_field = form_tree.xpath("//x:choicefield[contains(@id,'SO_#HAS_WBS#_I_EQ')]/x:choice[contains(@meta:field_id_overwrite,'SO_#HAS_WBS#_I_NE')]", namespaces=xmlforms_ns)
    if len(wbs_field) > 0:
      wbs_field[0].attrib['selected'] = 'true'

    area_field = form_tree.xpath("//x:numberfield[contains(@id,'SO_#SQMETER_FROM#_I_GE')]", namespaces=xmlforms_ns)
    area_field[0].text = str(params['area_min'])

    # rooms_field = form_tree.xpath("//x:numberfield[contains(@id,'SO_#ROOM_FROM#_I_GE')]", namespaces=xmlforms_ns)
    # rooms_field[0].text = '2'

    rent_field = form_tree.xpath("//x:numberfield[contains(@id,'SO_#GROSSCD#_I_LE')]", namespaces=xmlforms_ns)
    rent_field[0].text = str(params['rent_total_max'])

    filled_form_str = etree.tostring(form_tree, xml_declaration = True, pretty_print = True, encoding='UTF-8')
    
    # open form
    forms_params['name'] = 'openform'
    openform = s.get(f'{xmlforms_url}?{urlencode(forms_params)}', headers=search_headers)
    openform.raise_for_status()

    # save form
    forms_submit_params = {
      'application': 'ESQ_IA_REOBJ',
      'sap-client': 451,
      'command': 'action',
      'name': 'save',
      'id': new_uuid,
      'api': '6.139',
      'head-oppc-version': '6.139.10',
      'originalId': filter_form_id
    }

    form_submit = s.post(f'{xmlforms_url}?{urlencode(forms_submit_params)}', data=filled_form_str, headers=search_headers)
    form_submit.raise_for_status()

    # request results
    forms_submit_params['name'] = 'search_re_obj'
    form_request = s.get(f'{xmlforms_url}?{urlencode(forms_submit_params)}', headers=search_headers)
    form_request.raise_for_status()

    # get results
    results_params = {
      'application': 'ESQ_IA_REOBJ',
      'sap-client': 451,
      'command': 'action',
      'name': 'boxlist',
      'api': '6.139',
      'head-oppc-version': '6.139.10',
      '_': int(datetime.timestamp(datetime.now()))
    }
    results_request = s.get(f'{xmlforms_url}?{urlencode(results_params)}', headers=search_headers)
    results_request.raise_for_status()
    results_request.encoding = 'utf-8'

    return results_request.text.encode('utf-8')

    #https://portal1s.easysquare.com/prorex/xmlforms/image.jpg?application=ESQ_IA_REOBJ&sap-client=451&api=6.139&command=action&id=E7372CD3-92A6-A918-0604-46A9CFD1864F&name=get&head-oppc-version=6.139.10&head-oppc-id=36F02D7F-9EA7-4458-AE49-967A87FFA5C9

    #  https://portal1s.easysquare.com/meinehowoge/index.html?deeplink=%2FESQ_IA_REOBJ%2FESQ_VM_REOBJ_ALL#/formApp/%252Fsheet%252F0%252Fsection%252F2%252Fsheet%252F0%252Fsection%252F/E7372CD3-92A6-A918-0604-46A9CFD1864F/%252Fsection%252F0%252Fbox%252F0%252Fhead%252F0

    # https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqbUVFWHlqQ2hWdlFXeFJKX1hyLXJ5aFdYdU91UXxBQ3Jtc0tuRmZYNkFMSmxKZ2RfaFhGUmpMTl83cDU4U1B1dWdTMVlqdG9YbGZGUGdIUWc4NHdQNlQ0YndzbWR6TlQzcFVMelNxRm0wNU55QU1jYkdWaHhhZFRpNmRYSG9lQ0lWU2plVklvbWxLdEtnZ3hvRW5Fbw&q=https%3A%2F%2Fportal2s.easysquare.com%2Fberlinovo%2Fapi5%2Fdeeplink%3Fq%3DAPARTMENT%252fZ57_APARTM%252fESQ_VM_APPA_2%253aStorkower%2520Stra%C3%9Fe