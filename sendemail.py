#coding: utf-8

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import logging
import config
import yaml
import dogpics

from jinja2 import Environment, select_autoescape


env = Environment(
    autoescape=select_autoescape()
)

logger = logging.getLogger(__name__)

email_account: config.EmailAccount = None

tpl_text_email = u"""Hundi: {{dogpic}}

Duuuu, ich rieche neue neue Inserate! *schwanzwedel*

===

{% for site, flats in sites.items() %}
Bei {{site|capitalize}} gibt's {{flats|length}} neue Angebote:

{% for flat in flats %}

Titel: {{flat.title}}
Link: {{flat.link}}

Adresse: {{flat.addr}} {% if flat.kiez|length %}({{flat.kiez}}){% endif %}
{% if flat.pos %}Google Maps: https://www.google.de/maps/place/{{flat.pos.lat}},{{flat.pos.long}}{% endif %}

Angebotsdetails:{% for key, value in flat.properties.items() %}
- {{key}}: {{value}}{% endfor %}
{% if flat.landlord|length %}- Vermieter: {{flat.landlord}}
{% if flat.features|length %}
Besonderheiten:{% for feature in flat.features %}
- {{feature}}{% endfor %}
{% endif %}{% endif %}
========{% endfor %}

{% endfor %}
"""

tpl_html_email = u"""
<h3>Duuuu, ich rieche neue neue Inserate! *schwanzwedel*</h3>

<p><img src="{{dogpic}}" width="600" /></p>

{% for site, flats in sites.items() %}
<h4>Bei {{site|capitalize}} gibt's <strong>{{flats|length}}</strong> neue Angebote</h4>

{% for flat in flats %}
<p>
<a href="{{flat.link}}">{{flat.title}}</a><br />
<br />
Addresse: {{flat.addr}} {% if flat.kiez|length %}({{flat.kiez}}){% endif %}{% if flat.pos %} (<a href="https://www.google.de/maps/place/{{flat.pos.lat}},{{flat.pos.long}}">Google Maps</a>){% endif %}<br />
<br />
Angebotsdetails:<br/>
<ul>{% for key, value in flat.properties.items() %}
<li>{{key}}: {{value}}</li>{% endfor %}
{% if flat.landlord|length %}<li>Vermieter: {{flat.landlord}}</li>{% endif %}
</ul>
<br />
{% if flat.features|length %}
Besonderheiten:<br/>
<ul>
{% for feature in flat.features %}
<li>{{feature}}</li>{% endfor %}
</ul>
<br />
{% endif %}
<hr />
{% endfor %}
<br /><br />
{% endfor %}
"""

def get_dogpic():
    try:
        return dogpics.get_random_dogpic()
    except Exception as e:
        logging.error(e)
        return dogpics.DEFAULTDOG


def create_email_body(sites, dogpic, tpl):
    template = env.from_string(tpl)

    return template.render(sites=sites, dogpic=dogpic)

def create_email(sites, emails, account: config.EmailAccount):
    dogpic = get_dogpic()

    msg = MIMEMultipart('alternative')

    plain = MIMEText(create_email_body(sites, dogpic, tpl_text_email), "text", _charset="utf-8")
    html = MIMEText(create_email_body(sites, dogpic, tpl_html_email), "html", _charset="utf-8")
    msg.attach(plain)
    msg.attach(html)

    email_from = Header(account.name_from, 'utf-8')
    email_from.append(f'<{account.email_from}>', 'ascii')

    new_flats = sum([len(flats) for flats in sites.values()])
    if new_flats == 1:
        new_msg = 'neues Wohnungsangebot'
    else:
        new_msg = 'neue Wohnungsangebote'

    msg['Subject'] = Header(f'{new_flats} {new_msg} erschnüffelt', 'utf-8')
    msg["From"] = email_from
    msg["To"] = ", ".join(emails)
    return msg

def send_email(sites, emails):
    global email_account
    if email_account is None:
        email_account = config.get_mail_account()

    msg = create_email(sites, emails, email_account)

    try:
        logger.info("Sending email to: {}".format(", ".join(emails)))
        s = smtplib.SMTP_SSL(email_account.host, email_account.port)
        s.login(email_account.username, email_account.password)
        s.sendmail(msg["From"].__str__(), emails, msg.as_string())
        s.quit()
    except Exception as e:
        logger.error(e)
        logger.debug(msg.as_string())
        raise

def test_format_body(sites):
    print(create_email_body(sites, dogpics.DEFAULTDOG, tpl_html_email))