import os
import pandas as pd
import smtplib
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap4
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

bootstrap = Bootstrap4(app)

app.secret_key = "THIS IS A SECRET KEY $%12&*(VNIJG"

# ---------------------------------- DataBase SQLite -------------------------------------------------------------------
# ---------------------------------- images certifications -------------------------------------------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///certifications.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

if __name__ == "__main__":
    app.run(debug=True)
