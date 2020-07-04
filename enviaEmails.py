import smtplib
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app import EmailModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost:5432/enviaemail"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#
# class Email:
#     def __init__(self, emailenvio, emailentrega):
#         self.emailenvio = emailenvio
#         self.emailentrega = emailentrega


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/novo')
def novo():
    return render_template('novo.html', titulo='Novo smtp email')


@app.route('/criar', methods=['POST', ])
def criar():
    strsmtphost = request.form['smtphost']
    intsmtpport = request.form['smtpport']
    strauthemail = request.form['authemail']
    strauthsenha = request.form['authsenha']

    stremailenvio = request.form['emailenvio']
    stremailentrega = request.form['emailentrega']

    listemailenvio = formataemail(stremailenvio)
    listemailentrega = formataemail(stremailentrega)

    enviaemail(strsmtphost, intsmtpport, strauthemail, strauthsenha, listemailenvio[0], listemailentrega)

    # print(listemailenvio)
    # print('--------')
    # print(listemailentrega)
    return redirect('/')


@app.route('/email', methods=['POST', 'GET'])
def handle_emails():
    if request.method == 'POST':

        new_email = EmailModel(host=request.form.get("host"), port=request.form.get("port"),
                               mail=request.form.get("mail"),
                               password=request.form.get("password"))
        db.session.add(new_email)
        db.session.commit()
        return render_template('novo.html')

    elif request.method == 'GET':
        emails = EmailModel.query.all()
        print(emails)
        results = [
            {
                "host": email.host,
                "port": email.port,
                "mail": email.mail,
                "password": email.password,
            } for email in emails]

        return render_template('novo.html', emails=results)


def formataemail(stremails):
    # print('////ENTROU FORMATA EMAILS////')
    stremails = stremails.replace("\r\n", "")
    stremails = stremails.replace(" ", "")
    stremails = stremails.replace("\r", "")
    stremails = stremails.replace("\n", "")

    listemail = stremails.split(',')
    listemail = list(filter(None, listemail))
    return listemail


def enviaemail(host, port, authemail, authpass, emailenvio, lstemailsentrega):
    # conexão com os servidores
    smtp_ssl_host = host
    smtp_ssl_port = port
    # username ou email para logar no servidor
    username = authemail
    password = authpass

    print(emailenvio)
    print(lstemailsentrega)
    from_addr = emailenvio
    to_addrs = lstemailsentrega

    # somente texto
    message = MIMEText('Hello World 2')
    message['subject'] = 'Hello'
    message['from'] = from_addr
    message['to'] = ', '.join(to_addrs)

    # conectaremos de forma segura usando SSL
    server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    # para interagir com um servidor externo precisaremos
    # fazer login nele
    server.login(username, password)
    server.sendmail(from_addr, to_addrs, message.as_string())
    server.quit()


app.run(debug=True)
