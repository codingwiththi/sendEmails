from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
# postgres://ywulvpqopzvplr:329e34da03b9d271584693ebb458a0f8d74668a62dde5a89a1edaf9045bf375a@ec2-50-17-90-177.compute-1.amazonaws.com:5432/d70tf4f8bs590r
# postgresql://postgres:root@localhost:5432/enviaemail
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "postgres://ywulvpqopzvplr:329e34da03b9d271584693ebb458a0f8d74668a62dde5a89a1edaf9045bf375a@ec2-50-17-90-177.compute-1.amazonaws.com:5432/d70tf4f8bs590r"
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class EmailModel(db.Model):
    __tablename__ = 'smtpemail'

    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String())
    port = db.Column(db.Integer())
    mail = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, host, port, mail, password):
        self.host = host
        self.port = port
        self.mail = mail
        self.password = password

    def __repr__(self):
        return f"<SMTPEmail {self.mail}>"

# @app.route('/email', methods=['POST', 'GET'])
# def handle_emails():
#     print('oba')
#     if request.method == 'POST':
#         if request.is_json:
#             data = request.get_json()
#             new_email = EmailModel(host=data['host'], port=data['port'], mail=data['mail'],
#                                    password=data['password'])
#             db.session.add(new_email)
#             db.session.commit()
#             return {"message": f"car {new_email.mail} has been created successfully."}
#         else:
#             return {"error": "The request payload is not in JSON format"}
#
#     elif request.method == 'GET':
#         cars = EmailModel.query.all()
#         results = [
#             {
#                 "name": car.name,
#                 "model": car.model,
#                 "doors": car.doors
#             } for car in cars]
#
#         return {"count": len(results), "cars": results}
