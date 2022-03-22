from flask import Flask, render_template, redirect, url_for, request, jsonify
from jinja2 import TemplateNotFound
from flask_bootstrap import Bootstrap
from flask_mail import Mail, Message
import dojoconf
from mail import *


# IMPORTATE LEER ANTES DE HACER UN COMMIT A ESTE ARCHIVO... ES NECESARIO QUITAR EL PUERTO al final de la linea..

app = Flask(__name__)

# Mail credentials
app.config['MAIL_SERVER'] = dojoconf.MAIL_SERVER
app.config['MAIL_PORT'] = dojoconf.MAIL_PORT
app.config['MAIL_USERNAME'] = dojoconf.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = dojoconf.MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = dojoconf.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = bool(dojoconf.MAIL_USE_SSL)
mail = Mail(app)

counter = 1
@app.route('/', defaults={'path': 'index_v1.html'}, methods=['GET','POST'])
@app.route('/<path>')
def index(path):
    global counter
    counter += 1

    direccion1 = "https://www.google.com/maps/place/San+Jose+1844,+Villa+Alemana,+Valpara%C3%ADso/@-33.0617373,-71.3857534,17z/data=!4m5!3m4!1s0x9689d82068bf04af:0x752f1d32614a02cc!8m2!3d-33.0616969!4d-71.3836291"
    direccion2 = "https://www.google.com/maps/place/Lago+Llanquihue+3026,+Villa+Alemana,+Valpara%C3%ADso/@-33.0420342,-71.3996401,17z/data=!3m1!4b1!4m5!3m4!1s0x9689d9cd1d3f10d1:0xdc842eb2d945d6a5!8m2!3d-33.0420387!4d-71.3974514"

    # Mail logic
    recipients = request.form.get("recipients")

    #redirect logic
    try:
        if not path.endswith('.html'):
            path += '.html'

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template(path, direccion=direccion1, direccion2=direccion2)

    except TemplateNotFound:
        #return render_template('page-404.html'), 404
        return "Not found", 404
    except:
        return "chao", 500, "Sent"


@app.route('/send_message',methods=['POST'])
def send_message():
    if request.method == "POST":
        suscriptor = request.form['suscriptor']
        print(suscriptor)
        send_mail(subject="prueba",
                  sender="elopez.perto@gmail.com",
                  recipients=suscriptor,
                  html_body=render_template('reminder.html'),
                  text_body="saludos",
                  cc=None,
                  bcc=None)
    return render_template('gracias.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)