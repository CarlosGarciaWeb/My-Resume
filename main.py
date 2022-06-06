from email.message import EmailMessage
import os
import pandas as pd
import smtplib
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired
from datetime import date


# ---------------------------------- Age Calculation ------------------------------------------------------------------

year_born = 1995

year = date.today().year

month = date.today().month

age = year-year_born if month >= 2 else year-year_born-1
print(age)
print("Something")

# ---------------------------------- Certifications list ---------------------------------------------------------------
img_folder = "static/images/Certifications"


def organize_cert_path():
    arr = os.listdir(img_folder)

    # print(arr)

    img_path = [f"{img_folder}/{img}" for img in arr]

    return img_path


organize_cert_path()
# print(img_path)


# ---------------------------------- Flask set up App ------------------------------------------------------------------

app = Flask(__name__)

bootstrap = Bootstrap(app)



# ---------------------------------- DataBase SQLite -------------------------------------------------------------------
# ---------------------------------- images certifications -------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///certifications.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get['RESUME_KEY']
db = SQLAlchemy(app)


# Create table
class Certifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(500), unique=True, nullable=False)
    url = db.Column(db.String(1000), unique=True, nullable=False)

    def __repr__(self):
        return f'<Certifications {self.path}'


if not os.path.isfile('sqlite:///certifications.db'):
    db.create_all()

# DB AND INFO ADDED COMMENTING OUT CODE TO ADD INFO TO DATABASE
# cert_list = organize_cert_path()
# cert_url = pd.read_excel("professional experiences.xlsx", sheet_name="Sheet2").columns

# if cert_list:
#     for position in range(0, len(cert_list)):
#         new_cert = Certifications(id=position+1, path=cert_list[position], url=cert_url[position])
#         db.session.add(new_cert)
#         db.session.commit()




# ---------------------------------- Email component contact me --------------------------------------------------------

email = os.environ.get('TEST_EMAIL')
appps = os.environ.get('APP_PASS')

def Content(name, from_email, Message):
    message_content = f"""
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email</title>
</head>
    <h1>Email from:  {name}| Sent from: {from_email}</h1>
<body>
    <p>{Message}</p>
</body>
</html>
    
    
    """
    return message_content


# ---------------------------------- Experiences lists ---------------------------------------------------------------

df = pd.read_excel("professional experiences.xlsx")

experience_companies = df.columns

jobs_list = [df[companies].tolist() for companies in experience_companies]

experience_list = []

for list in range(len(jobs_list)):
    new_job_list = []
    for item in jobs_list[list]:
        if type(item) == str:
            new_job_list.append(item)
    experience_list.append(new_job_list)

# print(experience_list)

# new_job_list = [items for items in jobs_list if type(items) == str]
# use this to tap into the item of every job experience and remove nan's
# for item in items:
#     if type(item) == str:
#         print(item)


# ---------------------------------- Backend --------------------------------------------------------------------------

@app.route("/")
def home():
    img_info = db.session.query(Certifications).all()
    active_cert = img_info[0]
    cert_items = img_info[1:]
    job_title = [titles[0] for titles in experience_list]
    job_resp = [resp[1:-1] for resp in experience_list]
    job_date = [date[-1] for date in experience_list]
    return render_template("index.html", img_actv=active_cert, cert_items=cert_items, company=experience_companies
                           , job_date=job_date, job_resp=job_resp, job_title=job_title, age=age)


# -------------------------------- Download CV ------------------------------------------------------------------------

@app.route("/download")
def download():
    return send_from_directory('static', filename='Carlos Garcia English Resume 2022.pdf')


@app.route("/send-email", methods=['GET', 'POST'])
def send_email():
    if request.method == "POST": 
        msg = EmailMessage()
        msg["From"] = email
        msg['Subject'] = request.form.get('subject')
        print(request.form.get('subject'))
        sender_name = request.form.get('name')
        sender_email = request.form.get('email')
        sender_message = request.form.get('message')
        print(sender_email, sender_message, sender_name)
        msg['To'] = os.environ.get('MY_EMAIL')
        msg_content = Content(name=sender_name, from_email=sender_email, Message= sender_message)
        msg.set_content(msg_content, subtype='html')
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(email, appps)
            smtp.send_message(msg)
        return redirect(url_for('home'))


# host='0.0.0.0', port='5000',
if __name__ == "__main__":
    app.run( debug=True)
