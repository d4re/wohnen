#coding: utf-8

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import logging

import config
import dogpics

from jinja2 import Environment, select_autoescape
env = Environment(
    autoescape=select_autoescape()
)

logger = logging.getLogger(__name__)

tpl_text_email = u"""Dog: {{dogpic}}

===

'Schab {{flats|length}} neue Inserate!

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
"""

tpl_html_email = u"""
<h3>'Schab {{flats|length}} neue Inserate!</h3>

<p><img src="{{dogpic}}" /></p>

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
"""

def get_dogpic():
    try:
        return dogpics.get_random_dogpic()
    except Exception as e:
        logging.error(e)
        return dogpics.DEFAULTDOG


def create_email_body(flats, dogpic, tpl):
    template = env.from_string(tpl)

    return template.render(flats=flats, dogpic=dogpic)

def create_email(flats, emails, site):
    dogpic = get_dogpic()

    msg = MIMEMultipart('alternative')

    plain = MIMEText(create_email_body(flats, dogpic, tpl_text_email), "text", _charset="utf-8")
    html = MIMEText(create_email_body(flats, dogpic, tpl_html_email), "html", _charset="utf-8")
    msg.attach(plain)
    msg.attach(html)

    email_from = Header(config.name_from, 'utf-8')
    email_from.append(f'<{config.email_from}>', 'ascii')

    msg['Subject'] = f'{len(flats)} neue Wohnungen auf {site}'
    msg["From"] = email_from
    msg["To"] = ", ".join(emails)
    return msg

def send_email(flats, emails, site):
    msg = create_email(flats, emails, site)

    try:
        logger.info("Sending email to: {}".format(", ".join(emails)))
        s = smtplib.SMTP(config.smtp_server)
        s.sendmail(msg["From"].__str__(), emails, msg.as_string())
        s.quit()
    except Exception as e:
        logger.error(e)
        logger.debug(msg.as_string())
        raise

def test_format_body(flats_gen):
    flats = []
    for flat in flats_gen:
        flats.append(flat)
    print(create_email_body(flats, dogpics.DEFAULTDOG, tpl_html_email))
