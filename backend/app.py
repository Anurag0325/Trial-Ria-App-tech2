import psycopg2
import csv
from flask import Flask, jsonify, request, send_file
from models import *
from flask_cors import CORS
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from io import BytesIO
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import pandas as pd
from werkzeug.security import generate_password_hash
import jwt
from sqlalchemy import func
from dotenv import load_dotenv
import time
import psutil
import gc
from flask_caching import Cache
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import threading
from time import sleep
from sqlalchemy.orm import load_only

load_dotenv()

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'simple'  # In-memory cache
cache = Cache(app)

CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
app.config['SECRET_KEY'] = "anuragiitmadras"

DATABASE_URL = 'sqlite:///database.sqlite3'  # Replace with your actual DB URL
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
#     'DATABASE_URL')  # Use full URL from Render
# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:qwerty@localhost:5432/kvqadatabase"
# app.config['SECRET_KEY'] = "anuragiitmadras"


db.init_app(app)


# def create_database():
#     connection = psycopg2.connect(
#     user="postgres", password="qwerty", host="127.0.0.1", port="5432")
#     connection.autocommit = True
#     cursor = connection.cursor()
#     try:
#         cursor.execute("CREATE DATABASE kvqadatabase")
#         print("Database created successfully")
#     except psycopg2.errors.DuplicateDatabase:
#         print("Database already exists")
#     finally:
#         cursor.close()
#         connection.close()


def insert_dummy_data():
    colleagues_data = [
        # {"name": "Alice Johnson", "email": "22dp1000105@ds.study.iitm.ac.in",
        #     "department": "IT", "designation": "Analyst"},
        # {"name": "Anurag Kumar GMAIL", "email": "akanuragkumar75@gmail.com",
        #     "department": "Developer", "designation": "Developer"},
        {"name": "Anurag Kumar", "email": "tech@kvqaindia.com",
            "department": "Developer", "designation": "Frontend Developer"},
        # {"name": "Anurag Gmail", "email": "akanuragkumar4@gmail.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "Ritika", "email": "training@kvqaindia.com",
        #     "department": "Leadership", "designation": "CTO"},
        # {"name": "Lav Kaushik", "email": "lav@kvqaindia.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "Ritika GMAIL", "email": "ritzgupta998@gmail.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "Ritika Fashion", "email": "ritzfashiononline@gmail.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "Lav Kaushik_temp", "email": "somag89556@cpaurl.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "Varun_temp", "email": "kafay34325@cpaurl.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "TRG_temp", "email": "hafebom642@exoular.com",
        #     "department": "Training", "designation": "Training Coordinator"},
        # {"name": "sales_temp", "email": "hasej86977@gitated.com",
        #     "department": "Sales", "designation": "Sales Head"},
        # {"name": "NoidaISO_temp", "email": "pecepi9521@cashbn.com",
        #     "department": "Noida", "designation": "Noida"},
        # {"name": "Ruby_temp", "email": "namax29728@gitated.com",
        #     "department": "IT", "designation": "IT Operations"},
        # {"name": "Babli_temp", "email": "tixiy15582@cashbn.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Shikha_temp", "email": "yolenif475@gitated.com",
        #     "department": "Operations", "designation": "Opeartion Head"},
        # {"name": "Kanchan_temp", "email": "jowis58296@cpaurl.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Info_temp", "email": "kehot22123@cpaurl.com",
        #     "department": "Operations", "designation": "Information Sharing"},
        # {"name": "Vaishali_temp", "email": "tomacob234@cpaurl.com",
        #     "department": "Certificate", "designation": "Certificate Head"},
        # {"name": "Neha_temp", "email": "dogif17943@cpaurl.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "DHR_temp", "email": "yinonoj630@kazvi.com",
        #     "department": "DHR", "designation": "DHR"},
        # {"name": "Delhi_temp", "email": "selofo8026@merotx.com",
        #     "department": "Delhi", "designation": "Delhi"},
        # {"name": "Arun_temp", "email": "xison17512@kazvi.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "OPS_temp", "email": "citeji5554@kimasoft.com",
        #     "department": "OPS", "designation": "OPS"},
        # {"name": "Lav Kaushik_temp", "email": "kixit64836@gitated.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "Varun_temp", "email": "fakewi8084@cashbn.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "TRG_temp", "email": "behawi2407@cpaurl.com",
        #     "department": "Training", "designation": "Training Coordinator"},
        # {"name": "sales_temp", "email": "powog89677@cashbn.com",
        #     "department": "Sales", "designation": "Sales Head"},
        # {"name": "NoidaISO_temp", "email": "lijojid877@cpaurl.com",
        #     "department": "Noida", "designation": "Noida"},
        # {"name": "Ruby_temp", "email": "mokob12207@cashbn.com",
        #     "department": "IT", "designation": "IT Operations"},
        # {"name": "Babli_temp", "email": "gamek16395@gitated.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Shikha_temp", "email": "kecit61211@cashbn.com",
        #     "department": "Operations", "designation": "Opeartion Head"},
        # {"name": "Kanchan_temp", "email": "veraye2238@exoular.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Info_temp", "email": "rofac89385@exoular.com",
        #     "department": "Operations", "designation": "Information Sharing"},
        # {"name": "Vaishali_temp", "email": "mogiled377@cashbn.com",
        #     "department": "Certificate", "designation": "Certificate Head"},
        # {"name": "Neha_temp", "email": "yaboba4269@exoular.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "DHR_temp", "email": "sakos22466@cashbn.com",
        #     "department": "DHR", "designation": "DHR"},
        # {"name": "Delhi_temp", "email": "hanahir357@exoular.com",
        #     "department": "Delhi", "designation": "Delhi"},
        # {"name": "Arun_temp", "email": "hisasog163@exoular.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "OPS_temp", "email": "hogihen707@cashbn.com",
        #     "department": "OPS", "designation": "OPS"},

        # # {"name": "Krishna Chaudhari", "email": "krishna.chaudhari@riaadvisory.com",
        # #     "department": "Internal IT and Cloud Ops", "designation": "Associate Consultant"},
        # # {"name": "Krishna Chaudhari GMAIL", "email": "krish.chaudhari2018@gmail.com",
        # #     "department": "Internal IT and Cloud Ops", "designation": "Associate Consultant"},
        # # {"name": "Jibin Sebastian", "email": "jibin.sebastian@riaadvisory.com",
        # #     "department": "Operations", "designation": "Consultant - Admin"},
        # # {"name": "Salman Ansari", "email": "salman.ansari@riaadvisory.com",
        # #     "department": "Internal IT and Cloud Ops", "designation": "Director - CISO"},
        # # {"name": "Deepak Nichani", "email": "deepak.nichani@riaadvisory.com",
        # #     "department": "Operations", "designation": "Senior Consultant - Admin"},
        # # {"name": "Suraj Kamble", "email": "suraj.kambale@riaadvisory.com",
        # #     "department": "Developer", "designation": "Consultant"},
        # # {"name": "IT guy", "email": "marwin.ibanez@riaadvisory.com",
        # #     "department": "Developer", "designation": "Consultant"},
        # # {"name": "Eva Adams", "email": "eva.adams@bing.com", "designation": "HR"},

        # {"name": "Ritika", "email": "tosopeg490@cpaurl.com",
        #     "department": "Leadership", "designation": "CTO"},
        # {"name": "Lav Kaushik", "email": "dojel51420@exoular.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "Varun", "email": "wenayir754@gitated.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "TRG", "email": "lapec18115@cpaurl.com",
        #     "department": "Training", "designation": "Training Coordinator"},
        # {"name": "sales", "email": "tisopa4652@cashbn.com",
        #     "department": "Sales", "designation": "Sales Head"},
        # {"name": "NoidaISO", "email": "cajoki9143@cashbn.com",
        #     "department": "Noida", "designation": "Noida"},
        # {"name": "Ruby", "email": "peway67109@gitated.com",
        #     "department": "IT", "designation": "IT Operations"},
        # {"name": "Babli", "email": "libadef322@cpaurl.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Shikha", "email": "xepesic916@gitated.com",
        #     "department": "Operations", "designation": "Opeartion Head"},
        # {"name": "Kanchan", "email": "gociy10751@cashbn.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Info", "email": "livamex757@exoular.com",
        #     "department": "Operations", "designation": "Information Sharing"},
        # {"name": "Vaishali", "email": "xovijoh828@gitated.com",
        #     "department": "Certificate", "designation": "Certificate Head"},
        # {"name": "Neha", "email": "xexeke6928@exoular.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "DHR", "email": "gimejob509@gitated.com",
        #     "department": "DHR", "designation": "DHR"},
        # {"name": "Delhi", "email": "goxasa1124@exoular.com",
        #     "department": "Delhi", "designation": "Delhi"},
        # {"name": "Arun", "email": "lihiy72683@cpaurl.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "OPS", "email": "jahep63024@cpaurl.com",
        #     "department": "OPS", "designation": "OPS"},
        # # {"name": "Anurag Kumar", "email": "akanuragkumar75@gmail.com",
        # #     "department": "Developer", "designation": "Developer"},
        # {"name": "Himanshi", "email": "xoloko1077@cpaurl.com",
        #     "department": "Data Analyzer", "designation": "Data Analyst"},
        # {"name": "Lav Kaushik_temp", "email": "halonim833@cashbn.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "Varun_temp", "email": "negono6293@cpaurl.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "TRG_temp", "email": "lawiy24270@exoular.com",
        #     "department": "Training", "designation": "Training Coordinator"},
        # {"name": "sales_temp", "email": "tahige1177@exoular.com",
        #     "department": "Sales", "designation": "Sales Head"},
        # {"name": "NoidaISO_temp", "email": "kococeh740@gitated.com",
        #     "department": "Noida", "designation": "Noida"},
        # {"name": "Ruby_temp", "email": "nived34325@exoular.com",
        #     "department": "IT", "designation": "IT Operations"},
        # {"name": "Babli_temp", "email": "xexobos196@exoular.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Shikha_temp", "email": "sales56612@gitated.com",
        #     "department": "Operations", "designation": "Opeartion Head"},
        # {"name": "Kanchan_temp", "email": "micedat270@cashbn.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Info_temp", "email": "tekixi5647@cpaurl.com",
        #     "department": "Operations", "designation": "Information Sharing"},
        # {"name": "Vaishali_temp", "email": "momila1721@exoular.com",
        #     "department": "Certificate", "designation": "Certificate Head"},
        # {"name": "Neha_temp", "email": "pahayis503@cpaurl.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "DHR_temp", "email": "kapeli3117@gitated.com",
        #     "department": "DHR", "designation": "DHR"},
        # {"name": "Delhi_temp", "email": "meroyeh366@gitated.com",
        #     "department": "Delhi", "designation": "Delhi"},
        # {"name": "Arun_temp", "email": "kobelah642@exoular.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "OPS_temp", "email": "lahif62317@cpaurl.com",
        #     "department": "OPS", "designation": "OPS"},
        # {"name": "Lav Kaushik_temp", "email": "meviv48771@cpaurl.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "Varun_temp", "email": "hocemaw465@gitated.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "TRG_temp", "email": "mahaha3694@gitated.com",
        #     "department": "Training", "designation": "Training Coordinator"},
        # {"name": "sales_temp", "email": "piwor54871@cashbn.com",
        #     "department": "Sales", "designation": "Sales Head"},
        # {"name": "NoidaISO_temp", "email": "boyev69707@gitated.com",
        #     "department": "Noida", "designation": "Noida"},
        # {"name": "Ruby_temp", "email": "nicopa4473@gitated.com",
        #     "department": "IT", "designation": "IT Operations"},
        # {"name": "Babli_temp", "email": "wejipe1972@exoular.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Shikha_temp", "email": "vojag98289@cpaurl.com",
        #     "department": "Operations", "designation": "Opeartion Head"},
        # {"name": "Kanchan_temp", "email": "jidodey631@gitated.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Info_temp", "email": "jagic62267@gitated.com",
        #     "department": "Operations", "designation": "Information Sharing"},
        # {"name": "Vaishali_temp", "email": "japige9258@cashbn.com",
        #     "department": "Certificate", "designation": "Certificate Head"},
        # {"name": "Neha_temp", "email": "jewad78723@gitated.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "DHR_temp", "email": "royed51006@gitated.com",
        #     "department": "DHR", "designation": "DHR"},
        # {"name": "Delhi_temp", "email": "lisag95068@cpaurl.com",
        #     "department": "Delhi", "designation": "Delhi"},
        # {"name": "Arun_temp", "email": "tohaxe1328@gitated.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "OPS_temp", "email": "toreh92731@cashbn.com",
        #     "department": "OPS", "designation": "OPS"},
        # {"name": "Lav Kaushik_temp", "email": "radip94739@cashbn.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "Varun_temp", "email": "dametiw700@exoular.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "TRG_temp", "email": "vedij74636@cpaurl.com",
        #     "department": "Training", "designation": "Training Coordinator"},
        # {"name": "sales_temp", "email": "wenoh43287@exoular.com",
        #     "department": "Sales", "designation": "Sales Head"},
        # {"name": "NoidaISO_temp", "email": "gosedix625@cpaurl.com",
        #     "department": "Noida", "designation": "Noida"},
        # {"name": "Ruby_temp", "email": "linij68937@exoular.com",
        #     "department": "IT", "designation": "IT Operations"},
        # {"name": "Babli_temp", "email": "femajer941@gitated.com",
        #     "department": "Sales", "designation": "Sales"},
        # # {"name": "Anurag Gmail", "email": "akanuragkumar4@gmail.com",
        # #     "department": "Leadership", "designation": "CFO"},
        # {"name": "Shikha_temp", "email": "yayawo8134@cpaurl.com",
        #     "department": "Operations", "designation": "Opeartion Head"},
        # {"name": "Kanchan_temp", "email": "rebeh48383@cashbn.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Info_temp", "email": "xigam26899@cashbn.com",
        #     "department": "Operations", "designation": "Information Sharing"},
        # {"name": "Vaishali_temp", "email": "wicale7240@gitated.com",
        #     "department": "Certificate", "designation": "Certificate Head"},
        # {"name": "Neha_temp", "email": "wihex99751@gitated.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "DHR_temp", "email": "dahefa9204@gitated.com",
        #     "department": "DHR", "designation": "DHR"},
        # {"name": "Delhi_temp", "email": "xinoh70136@cpaurl.com",
        #     "department": "Delhi", "designation": "Delhi"},
        # {"name": "Arun_temp", "email": "dojagi5552@exoular.com",
        #     "department": "Leadership", "designation": "CFO"},
        # # {"name": "Sethi", "email": "tech@kvqaindia.com",
        # #     "department": "Developer", "designation": "Frontend Developer"},
        # {"name": "OPS_temp", "email": "roroti5291@gitated.com",
        #     "department": "OPS", "designation": "OPS"},
        # {"name": "Ritika", "email": "monemo7739@gitated.com",
        #     "department": "Leadership", "designation": "CTO"},
        # {"name": "Lav Kaushik", "email": "vefisag827@gitated.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "Varun", "email": "yitifol943@cashbn.com",
        #     "department": "Leadership", "designation": "CEO"},
        # {"name": "TRG", "email": "yadohop191@gitated.com",
        #     "department": "Training", "designation": "Training Coordinator"},
        # {"name": "sales", "email": "hoveve9648@exoular.com",
        #     "department": "Sales", "designation": "Sales Head"},
        # {"name": "NoidaISO", "email": "kecagoj605@exoular.com",
        #     "department": "Noida", "designation": "Noida"},
        # {"name": "Ruby", "email": "vaxokek932@nozamas.com",
        #     "department": "IT", "designation": "IT Operations"},
        # {"name": "Babli", "email": "keboxa9939@kimasoft.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Shikha", "email": "citefe4845@merotx.com",
        #     "department": "Operations", "designation": "Opeartion Head"},
        # {"name": "Kanchan", "email": "xodowo4959@kazvi.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "Info", "email": "fipis31191@merotx.com",
        #     "department": "Operations", "designation": "Information Sharing"},
        # {"name": "Vaishali", "email": "hevoj31373@kazvi.com",
        #     "department": "Certificate", "designation": "Certificate Head"},
        # {"name": "Neha", "email": "ranin30325@nozamas.com",
        #     "department": "Sales", "designation": "Sales"},
        # {"name": "DHR", "email": "jiciya6924@nozamas.com",
        #     "department": "DHR", "designation": "DHR"},
        # {"name": "Delhi", "email": "woxola1664@merotx.com",
        #     "department": "Delhi", "designation": "Delhi"},
        # {"name": "Arun", "email": "cabepe1031@merotx.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {"name": "OPS", "email": "dolef45905@nozamas.com",
        #     "department": "OPS", "designation": "OPS"},

        # {'name': 'name_1', 'email': 'user1@mailinator.com',
        #     'department': 'department_1', 'designation': 'designation_1'},
        # {'name': 'name_2', 'email': 'user2@mailinator.com',
        #     'department': 'department_2', 'designation': 'designation_2'},
        # {'name': 'name_3', 'email': 'user3@mailinator.com',
        #     'department': 'department_3', 'designation': 'designation_3'},
        # {'name': 'name_4', 'email': 'user4@mailinator.com',
        #     'department': 'department_4', 'designation': 'designation_4'},
        # {'name': 'name_5', 'email': 'user5@mailinator.com',
        #     'department': 'department_5', 'designation': 'designation_5'},
        # {'name': 'name_6', 'email': 'user6@mailinator.com',
        #     'department': 'department_6', 'designation': 'designation_6'},
        # {'name': 'name_7', 'email': 'user7@mailinator.com',
        #     'department': 'department_7', 'designation': 'designation_7'},
        # {'name': 'name_8', 'email': 'user8@mailinator.com',
        #     'department': 'department_8', 'designation': 'designation_8'},
        # {'name': 'name_9', 'email': 'user9@mailinator.com',
        #     'department': 'department_9', 'designation': 'designation_9'},
        # {'name': 'name_10', 'email': 'user10@mailinator.com',
        #     'department': 'department_10', 'designation': 'designation_10'},
        # {'name': 'name_11', 'email': 'user11@mailinator.com',
        #     'department': 'department_11', 'designation': 'designation_11'},
        # {'name': 'name_12', 'email': 'user12@mailinator.com',
        #     'department': 'department_12', 'designation': 'designation_12'},
        # {'name': 'name_13', 'email': 'user13@mailinator.com',
        #     'department': 'department_13', 'designation': 'designation_13'},
        # {'name': 'name_14', 'email': 'user14@mailinator.com',
        #     'department': 'department_14', 'designation': 'designation_14'},
        # {'name': 'name_15', 'email': 'user15@mailinator.com',
        #     'department': 'department_15', 'designation': 'designation_15'},
        # {'name': 'name_16', 'email': 'user16@mailinator.com',
        #     'department': 'department_16', 'designation': 'designation_16'},
        # {'name': 'name_17', 'email': 'user17@mailinator.com',
        #     'department': 'department_17', 'designation': 'designation_17'},
        # {'name': 'name_18', 'email': 'user18@mailinator.com',
        #     'department': 'department_18', 'designation': 'designation_18'},
        # {'name': 'name_19', 'email': 'user19@mailinator.com',
        #     'department': 'department_19', 'designation': 'designation_19'},
        # {'name': 'name_20', 'email': 'user20@mailinator.com',
        #     'department': 'department_20', 'designation': 'designation_20'},
        # {'name': 'name_21', 'email': 'user21@mailinator.com',
        #     'department': 'department_21', 'designation': 'designation_21'},
        # {'name': 'name_22', 'email': 'user22@mailinator.com',
        #     'department': 'department_22', 'designation': 'designation_22'},
        # {'name': 'name_23', 'email': 'user23@mailinator.com',
        #     'department': 'department_23', 'designation': 'designation_23'},
        # {'name': 'name_24', 'email': 'user24@mailinator.com',
        #     'department': 'department_24', 'designation': 'designation_24'},
        # {'name': 'name_25', 'email': 'user25@mailinator.com',
        #     'department': 'department_25', 'designation': 'designation_25'},
        # {'name': 'name_26', 'email': 'user26@mailinator.com',
        #     'department': 'department_26', 'designation': 'designation_26'},
        # {'name': 'name_27', 'email': 'user27@mailinator.com',
        #     'department': 'department_27', 'designation': 'designation_27'},
        # {'name': 'name_28', 'email': 'user28@mailinator.com',
        #     'department': 'department_28', 'designation': 'designation_28'},
        # {'name': 'name_29', 'email': 'user29@mailinator.com',
        #     'department': 'department_29', 'designation': 'designation_29'},
        # {'name': 'name_30', 'email': 'user30@mailinator.com',
        #     'department': 'department_30', 'designation': 'designation_30'},
        # {'name': 'name_31', 'email': 'user31@mailinator.com',
        #     'department': 'department_31', 'designation': 'designation_31'},
        # {'name': 'name_32', 'email': 'user32@mailinator.com',
        #     'department': 'department_32', 'designation': 'designation_32'},
        # {'name': 'name_33', 'email': 'user33@mailinator.com',
        #     'department': 'department_33', 'designation': 'designation_33'},
        # {'name': 'name_34', 'email': 'user34@mailinator.com',
        #     'department': 'department_34', 'designation': 'designation_34'},
        # {'name': 'name_35', 'email': 'user35@mailinator.com',
        #     'department': 'department_35', 'designation': 'designation_35'},
        # {'name': 'name_36', 'email': 'user36@mailinator.com',
        #     'department': 'department_36', 'designation': 'designation_36'},
        # {'name': 'name_37', 'email': 'user37@mailinator.com',
        #     'department': 'department_37', 'designation': 'designation_37'},
        # {'name': 'name_38', 'email': 'user38@mailinator.com',
        #     'department': 'department_38', 'designation': 'designation_38'},
        # {'name': 'name_39', 'email': 'user39@mailinator.com',
        #     'department': 'department_39', 'designation': 'designation_39'},
        # {'name': 'name_40', 'email': 'user40@mailinator.com',
        #     'department': 'department_40', 'designation': 'designation_40'},
        # {'name': 'name_41', 'email': 'user41@mailinator.com',
        #     'department': 'department_41', 'designation': 'designation_41'},
        # {'name': 'name_42', 'email': 'user42@mailinator.com',
        #     'department': 'department_42', 'designation': 'designation_42'},
        # {'name': 'name_43', 'email': 'user43@mailinator.com',
        #     'department': 'department_43', 'designation': 'designation_43'},
        # {'name': 'name_44', 'email': 'user44@mailinator.com',
        #     'department': 'department_44', 'designation': 'designation_44'},
        # {'name': 'name_45', 'email': 'user45@mailinator.com',
        #     'department': 'department_45', 'designation': 'designation_45'},
        # {'name': 'name_46', 'email': 'user46@mailinator.com',
        #     'department': 'department_46', 'designation': 'designation_46'},
        # {'name': 'name_47', 'email': 'user47@mailinator.com',
        #     'department': 'department_47', 'designation': 'designation_47'},
        # {'name': 'name_48', 'email': 'user48@mailinator.com',
        #     'department': 'department_48', 'designation': 'designation_48'},
        # {'name': 'name_49', 'email': 'user49@mailinator.com',
        #     'department': 'department_49', 'designation': 'designation_49'},
        # {'name': 'name_50', 'email': 'user50@mailinator.com',
        #     'department': 'department_50', 'designation': 'designation_50'},
        # {'name': 'name_51', 'email': 'user51@mailinator.com',
        #     'department': 'department_51', 'designation': 'designation_51'},
        # {'name': 'name_52', 'email': 'user52@mailinator.com',
        #     'department': 'department_52', 'designation': 'designation_52'},
        # {'name': 'name_53', 'email': 'user53@mailinator.com',
        #     'department': 'department_53', 'designation': 'designation_53'},
        # {'name': 'name_54', 'email': 'user54@mailinator.com',
        #     'department': 'department_54', 'designation': 'designation_54'},
        # {'name': 'name_55', 'email': 'user55@mailinator.com',
        #     'department': 'department_55', 'designation': 'designation_55'},
        # {'name': 'name_56', 'email': 'user56@mailinator.com',
        #     'department': 'department_56', 'designation': 'designation_56'},
        # {'name': 'name_57', 'email': 'user57@mailinator.com',
        #     'department': 'department_57', 'designation': 'designation_57'},
        # {'name': 'name_58', 'email': 'user58@mailinator.com',
        #     'department': 'department_58', 'designation': 'designation_58'},
        # {'name': 'name_59', 'email': 'user59@mailinator.com',
        #     'department': 'department_59', 'designation': 'designation_59'},
        # {'name': 'name_60', 'email': 'user60@mailinator.com',
        #     'department': 'department_60', 'designation': 'designation_60'},
        # {'name': 'name_61', 'email': 'user61@mailinator.com',
        #     'department': 'department_61', 'designation': 'designation_61'},
        # {'name': 'name_62', 'email': 'user62@mailinator.com',
        #     'department': 'department_62', 'designation': 'designation_62'},
        # {'name': 'name_63', 'email': 'user63@mailinator.com',
        #     'department': 'department_63', 'designation': 'designation_63'},
        # {'name': 'name_64', 'email': 'user64@mailinator.com',
        #     'department': 'department_64', 'designation': 'designation_64'},
        # {'name': 'name_65', 'email': 'user65@mailinator.com',
        #     'department': 'department_65', 'designation': 'designation_65'},
        # {'name': 'name_66', 'email': 'user66@mailinator.com',
        #     'department': 'department_66', 'designation': 'designation_66'},
        # {'name': 'name_67', 'email': 'user67@mailinator.com',
        #     'department': 'department_67', 'designation': 'designation_67'},
        # {'name': 'name_68', 'email': 'user68@mailinator.com',
        #     'department': 'department_68', 'designation': 'designation_68'},
        # {'name': 'name_69', 'email': 'user69@mailinator.com',
        #     'department': 'department_69', 'designation': 'designation_69'},
        # {'name': 'name_70', 'email': 'user70@mailinator.com',
        #     'department': 'department_70', 'designation': 'designation_70'},
        # {'name': 'name_71', 'email': 'user71@mailinator.com',
        #     'department': 'department_71', 'designation': 'designation_71'},
        # {'name': 'name_72', 'email': 'user72@mailinator.com',
        #     'department': 'department_72', 'designation': 'designation_72'},
        # {'name': 'name_73', 'email': 'user73@mailinator.com',
        #     'department': 'department_73', 'designation': 'designation_73'},
        # {'name': 'name_74', 'email': 'user74@mailinator.com',
        #     'department': 'department_74', 'designation': 'designation_74'},
        # {'name': 'name_75', 'email': 'user75@mailinator.com',
        #     'department': 'department_75', 'designation': 'designation_75'},
        # {'name': 'name_76', 'email': 'user76@mailinator.com',
        #     'department': 'department_76', 'designation': 'designation_76'},
        # {'name': 'name_77', 'email': 'user77@mailinator.com',
        #     'department': 'department_77', 'designation': 'designation_77'},
        # {'name': 'name_78', 'email': 'user78@mailinator.com',
        #     'department': 'department_78', 'designation': 'designation_78'},
        # {'name': 'name_79', 'email': 'user79@mailinator.com',
        #     'department': 'department_79', 'designation': 'designation_79'},
        # {'name': 'name_80', 'email': 'user80@mailinator.com',
        #     'department': 'department_80', 'designation': 'designation_80'},
        # {'name': 'name_81', 'email': 'user81@mailinator.com',
        #     'department': 'department_81', 'designation': 'designation_81'},
        # {'name': 'name_82', 'email': 'user82@mailinator.com',
        #     'department': 'department_82', 'designation': 'designation_82'},
        # {'name': 'name_83', 'email': 'user83@mailinator.com',
        #     'department': 'department_83', 'designation': 'designation_83'},
        # {'name': 'name_84', 'email': 'user84@mailinator.com',
        #     'department': 'department_84', 'designation': 'designation_84'},
        # {'name': 'name_85', 'email': 'user85@mailinator.com',
        #     'department': 'department_85', 'designation': 'designation_85'},
        # {'name': 'name_86', 'email': 'user86@mailinator.com',
        #     'department': 'department_86', 'designation': 'designation_86'},
        # {'name': 'name_87', 'email': 'user87@mailinator.com',
        #     'department': 'department_87', 'designation': 'designation_87'},
        # {'name': 'name_88', 'email': 'user88@mailinator.com',
        #     'department': 'department_88', 'designation': 'designation_88'},
        # {'name': 'name_89', 'email': 'user89@mailinator.com',
        #     'department': 'department_89', 'designation': 'designation_89'},
        # {'name': 'name_90', 'email': 'user90@mailinator.com',
        #     'department': 'department_90', 'designation': 'designation_90'},
        # {'name': 'name_91', 'email': 'user91@mailinator.com',
        #     'department': 'department_91', 'designation': 'designation_91'},
        # {'name': 'name_92', 'email': 'user92@mailinator.com',
        #     'department': 'department_92', 'designation': 'designation_92'},
        # {'name': 'name_93', 'email': 'user93@mailinator.com',
        #     'department': 'department_93', 'designation': 'designation_93'},
        # {'name': 'name_94', 'email': 'user94@mailinator.com',
        #     'department': 'department_94', 'designation': 'designation_94'},
        # {'name': 'name_95', 'email': 'user95@mailinator.com',
        #     'department': 'department_95', 'designation': 'designation_95'},
        # {'name': 'name_96', 'email': 'user96@mailinator.com',
        #     'department': 'department_96', 'designation': 'designation_96'},
        # {'name': 'name_97', 'email': 'user97@mailinator.com',
        #     'department': 'department_97', 'designation': 'designation_97'},
        # {'name': 'name_98', 'email': 'user98@mailinator.com',
        #     'department': 'department_98', 'designation': 'designation_98'},
        # {'name': 'name_99', 'email': 'user99@mailinator.com',
        #     'department': 'department_99', 'designation': 'designation_99'},
        # {'name': 'name_100', 'email': 'user100@mailinator.com',
        #     'department': 'department_100', 'designation': 'designation_100'},
        # {'name': 'name_101', 'email': 'user101@mailinator.com',
        #     'department': 'department_101', 'designation': 'designation_101'},
        # {'name': 'name_102', 'email': 'user102@mailinator.com',
        #     'department': 'department_102', 'designation': 'designation_102'},
        # {'name': 'name_103', 'email': 'user103@mailinator.com',
        #     'department': 'department_103', 'designation': 'designation_103'},
        # {'name': 'name_104', 'email': 'user104@mailinator.com',
        #     'department': 'department_104', 'designation': 'designation_104'},
        # {'name': 'name_105', 'email': 'user105@mailinator.com',
        #     'department': 'department_105', 'designation': 'designation_105'},
        # {'name': 'name_106', 'email': 'user106@mailinator.com',
        #     'department': 'department_106', 'designation': 'designation_106'},
        # {'name': 'name_107', 'email': 'user107@mailinator.com',
        #     'department': 'department_107', 'designation': 'designation_107'},
        # {'name': 'name_108', 'email': 'user108@mailinator.com',
        #     'department': 'department_108', 'designation': 'designation_108'},
        # {'name': 'name_109', 'email': 'user109@mailinator.com',
        #     'department': 'department_109', 'designation': 'designation_109'},
        # {'name': 'name_110', 'email': 'user110@mailinator.com',
        #     'department': 'department_110', 'designation': 'designation_110'},
        # {'name': 'name_111', 'email': 'user111@mailinator.com',
        #     'department': 'department_111', 'designation': 'designation_111'},
        # {'name': 'name_112', 'email': 'user112@mailinator.com',
        #     'department': 'department_112', 'designation': 'designation_112'},
        # {'name': 'name_113', 'email': 'user113@mailinator.com',
        #     'department': 'department_113', 'designation': 'designation_113'},
        # {'name': 'name_114', 'email': 'user114@mailinator.com',
        #     'department': 'department_114', 'designation': 'designation_114'},
        # {'name': 'name_115', 'email': 'user115@mailinator.com',
        #     'department': 'department_115', 'designation': 'designation_115'},
        # {'name': 'name_116', 'email': 'user116@mailinator.com',
        #     'department': 'department_116', 'designation': 'designation_116'},
        # {'name': 'name_117', 'email': 'user117@mailinator.com',
        #     'department': 'department_117', 'designation': 'designation_117'},
        # {'name': 'name_118', 'email': 'user118@mailinator.com',
        #     'department': 'department_118', 'designation': 'designation_118'},
        # {'name': 'name_119', 'email': 'user119@mailinator.com',
        #     'department': 'department_119', 'designation': 'designation_119'},
        # {'name': 'name_120', 'email': 'user120@mailinator.com',
        #     'department': 'department_120', 'designation': 'designation_120'},
        # {'name': 'name_121', 'email': 'user121@mailinator.com',
        #     'department': 'department_121', 'designation': 'designation_121'},
        # {'name': 'name_122', 'email': 'user122@mailinator.com',
        #     'department': 'department_122', 'designation': 'designation_122'},
        # {'name': 'name_123', 'email': 'user123@mailinator.com',
        #     'department': 'department_123', 'designation': 'designation_123'},
        # {'name': 'name_124', 'email': 'user124@mailinator.com',
        #     'department': 'department_124', 'designation': 'designation_124'},
        # {'name': 'name_125', 'email': 'user125@mailinator.com',
        #     'department': 'department_125', 'designation': 'designation_125'},
        # {'name': 'name_126', 'email': 'user126@mailinator.com',
        #     'department': 'department_126', 'designation': 'designation_126'},
        # {'name': 'name_127', 'email': 'user127@mailinator.com',
        #     'department': 'department_127', 'designation': 'designation_127'},
        # {'name': 'name_128', 'email': 'user128@mailinator.com',
        #     'department': 'department_128', 'designation': 'designation_128'},
        # {'name': 'name_129', 'email': 'user129@mailinator.com',
        #     'department': 'department_129', 'designation': 'designation_129'},
        # {'name': 'name_130', 'email': 'user130@mailinator.com',
        #     'department': 'department_130', 'designation': 'designation_130'},
        # {'name': 'name_131', 'email': 'user131@mailinator.com',
        #     'department': 'department_131', 'designation': 'designation_131'},
        # {'name': 'name_132', 'email': 'user132@mailinator.com',
        #     'department': 'department_132', 'designation': 'designation_132'},
        # {'name': 'name_133', 'email': 'user133@mailinator.com',
        #     'department': 'department_133', 'designation': 'designation_133'},
        # {'name': 'name_134', 'email': 'user134@mailinator.com',
        #     'department': 'department_134', 'designation': 'designation_134'},
        # {'name': 'name_135', 'email': 'user135@mailinator.com',
        #     'department': 'department_135', 'designation': 'designation_135'},
        # {'name': 'name_136', 'email': 'user136@mailinator.com',
        #     'department': 'department_136', 'designation': 'designation_136'},
        # {'name': 'name_137', 'email': 'user137@mailinator.com',
        #     'department': 'department_137', 'designation': 'designation_137'},
        # {'name': 'name_138', 'email': 'user138@mailinator.com',
        #     'department': 'department_138', 'designation': 'designation_138'},
        # {'name': 'name_139', 'email': 'user139@mailinator.com',
        #     'department': 'department_139', 'designation': 'designation_139'},
        # {'name': 'name_140', 'email': 'user140@mailinator.com',
        #     'department': 'department_140', 'designation': 'designation_140'},
        # {'name': 'name_141', 'email': 'user141@mailinator.com',
        #     'department': 'department_141', 'designation': 'designation_141'},
        # {'name': 'name_142', 'email': 'user142@mailinator.com',
        #     'department': 'department_142', 'designation': 'designation_142'},
        # {'name': 'name_143', 'email': 'user143@mailinator.com',
        #     'department': 'department_143', 'designation': 'designation_143'},
        # {'name': 'name_144', 'email': 'user144@mailinator.com',
        #     'department': 'department_144', 'designation': 'designation_144'},
        # {'name': 'name_145', 'email': 'user145@mailinator.com',
        #     'department': 'department_145', 'designation': 'designation_145'},
        # {'name': 'name_146', 'email': 'user146@mailinator.com',
        #     'department': 'department_146', 'designation': 'designation_146'},
        # {'name': 'name_147', 'email': 'user147@mailinator.com',
        #     'department': 'department_147', 'designation': 'designation_147'},
        # {'name': 'name_148', 'email': 'user148@mailinator.com',
        #     'department': 'department_148', 'designation': 'designation_148'},
        # {'name': 'name_149', 'email': 'user149@mailinator.com',
        #     'department': 'department_149', 'designation': 'designation_149'},
        # {'name': 'name_150', 'email': 'user150@mailinator.com',
        #     'department': 'department_150', 'designation': 'designation_150'},
        # {'name': 'name_151', 'email': 'user151@mailinator.com',
        #     'department': 'department_151', 'designation': 'designation_151'},
        # {'name': 'name_152', 'email': 'user152@mailinator.com',
        #     'department': 'department_152', 'designation': 'designation_152'},
        # {'name': 'name_153', 'email': 'user153@mailinator.com',
        #     'department': 'department_153', 'designation': 'designation_153'},
        # {'name': 'name_154', 'email': 'user154@mailinator.com',
        #     'department': 'department_154', 'designation': 'designation_154'},
        # {'name': 'name_155', 'email': 'user155@mailinator.com',
        #     'department': 'department_155', 'designation': 'designation_155'},
        # {'name': 'name_156', 'email': 'user156@mailinator.com',
        #     'department': 'department_156', 'designation': 'designation_156'},
        # {'name': 'name_157', 'email': 'user157@mailinator.com',
        #     'department': 'department_157', 'designation': 'designation_157'},
        # {'name': 'name_158', 'email': 'user158@mailinator.com',
        #     'department': 'department_158', 'designation': 'designation_158'},
        # {'name': 'name_159', 'email': 'user159@mailinator.com',
        #     'department': 'department_159', 'designation': 'designation_159'},
        # {'name': 'name_160', 'email': 'user160@mailinator.com',
        #     'department': 'department_160', 'designation': 'designation_160'},
        # {'name': 'name_161', 'email': 'user161@mailinator.com',
        #     'department': 'department_161', 'designation': 'designation_161'},
        # {'name': 'name_162', 'email': 'user162@mailinator.com',
        #     'department': 'department_162', 'designation': 'designation_162'},
        # {'name': 'name_163', 'email': 'user163@mailinator.com',
        #     'department': 'department_163', 'designation': 'designation_163'},
        # {'name': 'name_164', 'email': 'user164@mailinator.com',
        #     'department': 'department_164', 'designation': 'designation_164'},
        # {'name': 'name_165', 'email': 'user165@mailinator.com',
        #     'department': 'department_165', 'designation': 'designation_165'},
        # {'name': 'name_166', 'email': 'user166@mailinator.com',
        #     'department': 'department_166', 'designation': 'designation_166'},
        # {'name': 'name_167', 'email': 'user167@mailinator.com',
        #     'department': 'department_167', 'designation': 'designation_167'},
        # {'name': 'name_168', 'email': 'user168@mailinator.com',
        #     'department': 'department_168', 'designation': 'designation_168'},
        # {'name': 'name_169', 'email': 'user169@mailinator.com',
        #     'department': 'department_169', 'designation': 'designation_169'},
        # {'name': 'name_170', 'email': 'user170@mailinator.com',
        #     'department': 'department_170', 'designation': 'designation_170'},
        # {'name': 'name_171', 'email': 'user171@mailinator.com',
        #     'department': 'department_171', 'designation': 'designation_171'},
        # {'name': 'name_172', 'email': 'user172@mailinator.com',
        #     'department': 'department_172', 'designation': 'designation_172'},
        # {'name': 'name_173', 'email': 'user173@mailinator.com',
        #     'department': 'department_173', 'designation': 'designation_173'},
        # {'name': 'name_174', 'email': 'user174@mailinator.com',
        #     'department': 'department_174', 'designation': 'designation_174'},
        # {'name': 'name_175', 'email': 'user175@mailinator.com',
        #     'department': 'department_175', 'designation': 'designation_175'},
        # {'name': 'name_176', 'email': 'user176@mailinator.com',
        #     'department': 'department_176', 'designation': 'designation_176'},
        # {'name': 'name_177', 'email': 'user177@mailinator.com',
        #     'department': 'department_177', 'designation': 'designation_177'},
        # {'name': 'name_178', 'email': 'user178@mailinator.com',
        #     'department': 'department_178', 'designation': 'designation_178'},
        # {'name': 'name_179', 'email': 'user179@mailinator.com',
        #     'department': 'department_179', 'designation': 'designation_179'},
        # {'name': 'name_180', 'email': 'user180@mailinator.com',
        #     'department': 'department_180', 'designation': 'designation_180'},
        # {'name': 'name_181', 'email': 'user181@mailinator.com',
        #     'department': 'department_181', 'designation': 'designation_181'},
        # {'name': 'name_182', 'email': 'user182@mailinator.com',
        #     'department': 'department_182', 'designation': 'designation_182'},
        # {'name': 'name_183', 'email': 'user183@mailinator.com',
        #     'department': 'department_183', 'designation': 'designation_183'},
        # {'name': 'name_184', 'email': 'user184@mailinator.com',
        #     'department': 'department_184', 'designation': 'designation_184'},
        # {'name': 'name_185', 'email': 'user185@mailinator.com',
        #     'department': 'department_185', 'designation': 'designation_185'},
        # {'name': 'name_186', 'email': 'user186@mailinator.com',
        #     'department': 'department_186', 'designation': 'designation_186'},
        # {'name': 'name_187', 'email': 'user187@mailinator.com',
        #     'department': 'department_187', 'designation': 'designation_187'},
        # {'name': 'name_188', 'email': 'user188@mailinator.com',
        #     'department': 'department_188', 'designation': 'designation_188'},
        # {'name': 'name_189', 'email': 'user189@mailinator.com',
        #     'department': 'department_189', 'designation': 'designation_189'},
        # {'name': 'name_190', 'email': 'user190@mailinator.com',
        #     'department': 'department_190', 'designation': 'designation_190'},
        # {'name': 'name_191', 'email': 'user191@mailinator.com',
        #     'department': 'department_191', 'designation': 'designation_191'},
        # {'name': 'name_192', 'email': 'user192@mailinator.com',
        #     'department': 'department_192', 'designation': 'designation_192'},
        # {'name': 'name_193', 'email': 'user193@mailinator.com',
        #     'department': 'department_193', 'designation': 'designation_193'},
        # {'name': 'name_194', 'email': 'user194@mailinator.com',
        #     'department': 'department_194', 'designation': 'designation_194'},
        # {'name': 'name_195', 'email': 'user195@mailinator.com',
        #     'department': 'department_195', 'designation': 'designation_195'},
        # {'name': 'name_196', 'email': 'user196@mailinator.com',
        #     'department': 'department_196', 'designation': 'designation_196'},
        # {'name': 'name_197', 'email': 'user197@mailinator.com',
        #     'department': 'department_197', 'designation': 'designation_197'},
        # {'name': 'name_198', 'email': 'user198@mailinator.com',
        #     'department': 'department_198', 'designation': 'designation_198'},
        # {'name': 'name_199', 'email': 'user199@mailinator.com',
        #     'department': 'department_199', 'designation': 'designation_199'},
        # {'name': 'name_200', 'email': 'user200@mailinator.com',
        #     'department': 'department_200', 'designation': 'designation_200'},
        # {'name': 'name_201', 'email': 'user201@mailinator.com',
        #     'department': 'department_201', 'designation': 'designation_201'},
        # {'name': 'name_202', 'email': 'user202@mailinator.com',
        #     'department': 'department_202', 'designation': 'designation_202'},
        # {'name': 'name_203', 'email': 'user203@mailinator.com',
        #     'department': 'department_203', 'designation': 'designation_203'},
        # {'name': 'name_204', 'email': 'user204@mailinator.com',
        #     'department': 'department_204', 'designation': 'designation_204'},
        # {'name': 'name_205', 'email': 'user205@mailinator.com',
        #     'department': 'department_205', 'designation': 'designation_205'},
        # {'name': 'name_206', 'email': 'user206@mailinator.com',
        #     'department': 'department_206', 'designation': 'designation_206'},
        # {'name': 'name_207', 'email': 'user207@mailinator.com',
        #     'department': 'department_207', 'designation': 'designation_207'},
        # {'name': 'name_208', 'email': 'user208@mailinator.com',
        #     'department': 'department_208', 'designation': 'designation_208'},
        # {'name': 'name_209', 'email': 'user209@mailinator.com',
        #     'department': 'department_209', 'designation': 'designation_209'},
        # {'name': 'name_210', 'email': 'user210@mailinator.com',
        #     'department': 'department_210', 'designation': 'designation_210'},
        # {'name': 'name_211', 'email': 'user211@mailinator.com',
        #     'department': 'department_211', 'designation': 'designation_211'},
        # {'name': 'name_212', 'email': 'user212@mailinator.com',
        #     'department': 'department_212', 'designation': 'designation_212'},
        # {'name': 'name_213', 'email': 'user213@mailinator.com',
        #     'department': 'department_213', 'designation': 'designation_213'},
        # {'name': 'name_214', 'email': 'user214@mailinator.com',
        #     'department': 'department_214', 'designation': 'designation_214'},
        # {'name': 'name_215', 'email': 'user215@mailinator.com',
        #     'department': 'department_215', 'designation': 'designation_215'},
        # {'name': 'name_216', 'email': 'user216@mailinator.com',
        #     'department': 'department_216', 'designation': 'designation_216'},
        # {'name': 'name_217', 'email': 'user217@mailinator.com',
        #     'department': 'department_217', 'designation': 'designation_217'},
        # {'name': 'name_218', 'email': 'user218@mailinator.com',
        #     'department': 'department_218', 'designation': 'designation_218'},
        # {'name': 'name_219', 'email': 'user219@mailinator.com',
        #     'department': 'department_219', 'designation': 'designation_219'},
        # {'name': 'name_220', 'email': 'user220@mailinator.com',
        #     'department': 'department_220', 'designation': 'designation_220'},
        # {'name': 'name_221', 'email': 'user221@mailinator.com',
        #     'department': 'department_221', 'designation': 'designation_221'},
        # {'name': 'name_222', 'email': 'user222@mailinator.com',
        #     'department': 'department_222', 'designation': 'designation_222'},
        # {'name': 'name_223', 'email': 'user223@mailinator.com',
        #     'department': 'department_223', 'designation': 'designation_223'},
        # {'name': 'name_224', 'email': 'user224@mailinator.com',
        #     'department': 'department_224', 'designation': 'designation_224'},
        # {'name': 'name_225', 'email': 'user225@mailinator.com',
        #     'department': 'department_225', 'designation': 'designation_225'},
        # {'name': 'name_226', 'email': 'user226@mailinator.com',
        #     'department': 'department_226', 'designation': 'designation_226'},
        # {'name': 'name_227', 'email': 'user227@mailinator.com',
        #     'department': 'department_227', 'designation': 'designation_227'},
        # {'name': 'name_228', 'email': 'user228@mailinator.com',
        #     'department': 'department_228', 'designation': 'designation_228'},
        # {'name': 'name_229', 'email': 'user229@mailinator.com',
        #     'department': 'department_229', 'designation': 'designation_229'},
        # {'name': 'name_230', 'email': 'user230@mailinator.com',
        #     'department': 'department_230', 'designation': 'designation_230'},
        # {'name': 'name_231', 'email': 'user231@mailinator.com',
        #     'department': 'department_231', 'designation': 'designation_231'},
        # {'name': 'name_232', 'email': 'user232@mailinator.com',
        #     'department': 'department_232', 'designation': 'designation_232'},
        # {'name': 'name_233', 'email': 'user233@mailinator.com',
        #     'department': 'department_233', 'designation': 'designation_233'},
        # {'name': 'name_234', 'email': 'user234@mailinator.com',
        #     'department': 'department_234', 'designation': 'designation_234'},
        # {'name': 'name_235', 'email': 'user235@mailinator.com',
        #     'department': 'department_235', 'designation': 'designation_235'},
        # {'name': 'name_236', 'email': 'user236@mailinator.com',
        #     'department': 'department_236', 'designation': 'designation_236'},
        # {'name': 'name_237', 'email': 'user237@mailinator.com',
        #     'department': 'department_237', 'designation': 'designation_237'},
        # {'name': 'name_238', 'email': 'user238@mailinator.com',
        #     'department': 'department_238', 'designation': 'designation_238'},
        # {'name': 'name_239', 'email': 'user239@mailinator.com',
        #     'department': 'department_239', 'designation': 'designation_239'},
        # {'name': 'name_240', 'email': 'user240@mailinator.com',
        #     'department': 'department_240', 'designation': 'designation_240'},
        # {'name': 'name_241', 'email': 'user241@mailinator.com',
        #     'department': 'department_241', 'designation': 'designation_241'},
        # {'name': 'name_242', 'email': 'user242@mailinator.com',
        #     'department': 'department_242', 'designation': 'designation_242'},
        # {'name': 'name_243', 'email': 'user243@mailinator.com',
        #     'department': 'department_243', 'designation': 'designation_243'},
        # {'name': 'name_244', 'email': 'user244@mailinator.com',
        #     'department': 'department_244', 'designation': 'designation_244'},
        # {'name': 'name_245', 'email': 'user245@mailinator.com',
        #     'department': 'department_245', 'designation': 'designation_245'},
        # {'name': 'name_246', 'email': 'user246@mailinator.com',
        #     'department': 'department_246', 'designation': 'designation_246'},
        # {'name': 'name_247', 'email': 'user247@mailinator.com',
        #     'department': 'department_247', 'designation': 'designation_247'},
        # {'name': 'name_248', 'email': 'user248@mailinator.com',
        #     'department': 'department_248', 'designation': 'designation_248'},
        # {'name': 'name_249', 'email': 'user249@mailinator.com',
        #     'department': 'department_249', 'designation': 'designation_249'},
        # {'name': 'name_250', 'email': 'user250@mailinator.com',
        #     'department': 'department_250', 'designation': 'designation_250'},
        # {'name': 'name_251', 'email': 'user251@mailinator.com',
        #     'department': 'department_251', 'designation': 'designation_251'},
        # {'name': 'name_252', 'email': 'user252@mailinator.com',
        #     'department': 'department_252', 'designation': 'designation_252'},
        # {'name': 'name_253', 'email': 'user253@mailinator.com',
        #     'department': 'department_253', 'designation': 'designation_253'},
        # {'name': 'name_254', 'email': 'user254@mailinator.com',
        #     'department': 'department_254', 'designation': 'designation_254'},
        # {'name': 'name_255', 'email': 'user255@mailinator.com',
        #     'department': 'department_255', 'designation': 'designation_255'},
        # {'name': 'name_256', 'email': 'user256@mailinator.com',
        #     'department': 'department_256', 'designation': 'designation_256'},
        # {'name': 'name_257', 'email': 'user257@mailinator.com',
        #     'department': 'department_257', 'designation': 'designation_257'},
        # {'name': 'name_258', 'email': 'user258@mailinator.com',
        #     'department': 'department_258', 'designation': 'designation_258'},
        # {'name': 'name_259', 'email': 'user259@mailinator.com',
        #     'department': 'department_259', 'designation': 'designation_259'},
        # {'name': 'name_260', 'email': 'user260@mailinator.com',
        #     'department': 'department_260', 'designation': 'designation_260'},
        # {'name': 'name_261', 'email': 'user261@mailinator.com',
        #     'department': 'department_261', 'designation': 'designation_261'},
        # {'name': 'name_262', 'email': 'user262@mailinator.com',
        #     'department': 'department_262', 'designation': 'designation_262'},
        # {'name': 'name_263', 'email': 'user263@mailinator.com',
        #     'department': 'department_263', 'designation': 'designation_263'},
        # {'name': 'name_264', 'email': 'user264@mailinator.com',
        #     'department': 'department_264', 'designation': 'designation_264'},
        # {'name': 'name_265', 'email': 'user265@mailinator.com',
        #     'department': 'department_265', 'designation': 'designation_265'},
        # {'name': 'name_266', 'email': 'user266@mailinator.com',
        #     'department': 'department_266', 'designation': 'designation_266'},
        # {'name': 'name_267', 'email': 'user267@mailinator.com',
        #     'department': 'department_267', 'designation': 'designation_267'},
        # {'name': 'name_268', 'email': 'user268@mailinator.com',
        #     'department': 'department_268', 'designation': 'designation_268'},
        # {'name': 'name_269', 'email': 'user269@mailinator.com',
        #     'department': 'department_269', 'designation': 'designation_269'},
        # {'name': 'name_270', 'email': 'user270@mailinator.com',
        #     'department': 'department_270', 'designation': 'designation_270'},
        # {'name': 'name_271', 'email': 'user271@mailinator.com',
        #     'department': 'department_271', 'designation': 'designation_271'},
        # {'name': 'name_272', 'email': 'user272@mailinator.com',
        #     'department': 'department_272', 'designation': 'designation_272'},
        # {'name': 'name_273', 'email': 'user273@mailinator.com',
        #     'department': 'department_273', 'designation': 'designation_273'},
        # {'name': 'name_274', 'email': 'user274@mailinator.com',
        #     'department': 'department_274', 'designation': 'designation_274'},
        # {'name': 'name_275', 'email': 'user275@mailinator.com',
        #     'department': 'department_275', 'designation': 'designation_275'},
        # {'name': 'name_276', 'email': 'user276@mailinator.com',
        #     'department': 'department_276', 'designation': 'designation_276'},
        # {'name': 'name_277', 'email': 'user277@mailinator.com',
        #     'department': 'department_277', 'designation': 'designation_277'},
        # {'name': 'name_278', 'email': 'user278@mailinator.com',
        #     'department': 'department_278', 'designation': 'designation_278'},
        # {'name': 'name_279', 'email': 'user279@mailinator.com',
        #     'department': 'department_279', 'designation': 'designation_279'},
        # {'name': 'name_280', 'email': 'user280@mailinator.com',
        #     'department': 'department_280', 'designation': 'designation_280'},
        # {'name': 'name_281', 'email': 'user281@mailinator.com',
        #     'department': 'department_281', 'designation': 'designation_281'},
        # {'name': 'name_282', 'email': 'user282@mailinator.com',
        #     'department': 'department_282', 'designation': 'designation_282'},
        # {'name': 'name_283', 'email': 'user283@mailinator.com',
        #     'department': 'department_283', 'designation': 'designation_283'},
        # {'name': 'name_284', 'email': 'user284@mailinator.com',
        #     'department': 'department_284', 'designation': 'designation_284'},
        # {'name': 'name_285', 'email': 'user285@mailinator.com',
        #     'department': 'department_285', 'designation': 'designation_285'},
        # {'name': 'name_286', 'email': 'user286@mailinator.com',
        #     'department': 'department_286', 'designation': 'designation_286'},
        # {'name': 'name_287', 'email': 'user287@mailinator.com',
        #     'department': 'department_287', 'designation': 'designation_287'},
        # {'name': 'name_288', 'email': 'user288@mailinator.com',
        #     'department': 'department_288', 'designation': 'designation_288'},
        # {'name': 'name_289', 'email': 'user289@mailinator.com',
        #     'department': 'department_289', 'designation': 'designation_289'},
        # {'name': 'name_290', 'email': 'user290@mailinator.com',
        #     'department': 'department_290', 'designation': 'designation_290'},
        # {'name': 'name_291', 'email': 'user291@mailinator.com',
        #     'department': 'department_291', 'designation': 'designation_291'},
        # {'name': 'name_292', 'email': 'user292@mailinator.com',
        #     'department': 'department_292', 'designation': 'designation_292'},
        # {'name': 'name_293', 'email': 'user293@mailinator.com',
        #     'department': 'department_293', 'designation': 'designation_293'},
        # {'name': 'name_294', 'email': 'user294@mailinator.com',
        #     'department': 'department_294', 'designation': 'designation_294'},
        # {'name': 'name_295', 'email': 'user295@mailinator.com',
        #     'department': 'department_295', 'designation': 'designation_295'},
        # {'name': 'name_296', 'email': 'user296@mailinator.com',
        #     'department': 'department_296', 'designation': 'designation_296'},
        # {'name': 'name_297', 'email': 'user297@mailinator.com',
        #     'department': 'department_297', 'designation': 'designation_297'},
        # {'name': 'name_298', 'email': 'user298@mailinator.com',
        #     'department': 'department_298', 'designation': 'designation_298'},
        # {'name': 'name_299', 'email': 'user299@mailinator.com',
        #     'department': 'department_299', 'designation': 'designation_299'},
        # {'name': 'name_300', 'email': 'user300@mailinator.com',
        #     'department': 'department_300', 'designation': 'designation_300'},
        # {'name': 'name_301', 'email': 'user301@mailinator.com',
        #     'department': 'department_301', 'designation': 'designation_301'},
        # {'name': 'name_302', 'email': 'user302@mailinator.com',
        #     'department': 'department_302', 'designation': 'designation_302'},
        # {'name': 'name_303', 'email': 'user303@mailinator.com',
        #     'department': 'department_303', 'designation': 'designation_303'},
        # {'name': 'name_304', 'email': 'user304@mailinator.com',
        #     'department': 'department_304', 'designation': 'designation_304'},
        # {'name': 'name_305', 'email': 'user305@mailinator.com',
        #     'department': 'department_305', 'designation': 'designation_305'},
        # {'name': 'name_306', 'email': 'user306@mailinator.com',
        #     'department': 'department_306', 'designation': 'designation_306'},
        # {'name': 'name_307', 'email': 'user307@mailinator.com',
        #     'department': 'department_307', 'designation': 'designation_307'},
        # {'name': 'name_308', 'email': 'user308@mailinator.com',
        #     'department': 'department_308', 'designation': 'designation_308'},
        # {'name': 'name_309', 'email': 'user309@mailinator.com',
        #     'department': 'department_309', 'designation': 'designation_309'},
        # {'name': 'name_310', 'email': 'user310@mailinator.com',
        #     'department': 'department_310', 'designation': 'designation_310'},
        # {'name': 'name_311', 'email': 'user311@mailinator.com',
        #     'department': 'department_311', 'designation': 'designation_311'},
        # {'name': 'name_312', 'email': 'user312@mailinator.com',
        #     'department': 'department_312', 'designation': 'designation_312'},
        # {'name': 'name_313', 'email': 'user313@mailinator.com',
        #     'department': 'department_313', 'designation': 'designation_313'},
        # {'name': 'name_314', 'email': 'user314@mailinator.com',
        #     'department': 'department_314', 'designation': 'designation_314'},
        # {'name': 'name_315', 'email': 'user315@mailinator.com',
        #     'department': 'department_315', 'designation': 'designation_315'},
        # {'name': 'name_316', 'email': 'user316@mailinator.com',
        #     'department': 'department_316', 'designation': 'designation_316'},
        # {'name': 'name_317', 'email': 'user317@mailinator.com',
        #     'department': 'department_317', 'designation': 'designation_317'},
        # {'name': 'name_318', 'email': 'user318@mailinator.com',
        #     'department': 'department_318', 'designation': 'designation_318'},
        # {'name': 'name_319', 'email': 'user319@mailinator.com',
        #     'department': 'department_319', 'designation': 'designation_319'},
        # {'name': 'name_320', 'email': 'user320@mailinator.com',
        #     'department': 'department_320', 'designation': 'designation_320'},
        # {'name': 'name_321', 'email': 'user321@mailinator.com',
        #     'department': 'department_321', 'designation': 'designation_321'},
        # {'name': 'name_322', 'email': 'user322@mailinator.com',
        #     'department': 'department_322', 'designation': 'designation_322'},
        # {'name': 'name_323', 'email': 'user323@mailinator.com',
        #     'department': 'department_323', 'designation': 'designation_323'},
        # {'name': 'name_324', 'email': 'user324@mailinator.com',
        #     'department': 'department_324', 'designation': 'designation_324'},
        # {'name': 'name_325', 'email': 'user325@mailinator.com',
        #     'department': 'department_325', 'designation': 'designation_325'},
        # {'name': 'name_326', 'email': 'user326@mailinator.com',
        #     'department': 'department_326', 'designation': 'designation_326'},
        # {'name': 'name_327', 'email': 'user327@mailinator.com',
        #     'department': 'department_327', 'designation': 'designation_327'},
        # {'name': 'name_328', 'email': 'user328@mailinator.com',
        #     'department': 'department_328', 'designation': 'designation_328'},
        # {'name': 'name_329', 'email': 'user329@mailinator.com',
        #     'department': 'department_329', 'designation': 'designation_329'},
        # {'name': 'name_330', 'email': 'user330@mailinator.com',
        #     'department': 'department_330', 'designation': 'designation_330'},
        # {'name': 'name_331', 'email': 'user331@mailinator.com',
        #     'department': 'department_331', 'designation': 'designation_331'},
        # {'name': 'name_332', 'email': 'user332@mailinator.com',
        #     'department': 'department_332', 'designation': 'designation_332'},
        # {'name': 'name_333', 'email': 'user333@mailinator.com',
        #     'department': 'department_333', 'designation': 'designation_333'},
        # {'name': 'name_334', 'email': 'user334@mailinator.com',
        #     'department': 'department_334', 'designation': 'designation_334'},
        # {'name': 'name_335', 'email': 'user335@mailinator.com',
        #     'department': 'department_335', 'designation': 'designation_335'},
        # {'name': 'name_336', 'email': 'user336@mailinator.com',
        #     'department': 'department_336', 'designation': 'designation_336'},
        # {'name': 'name_337', 'email': 'user337@mailinator.com',
        #     'department': 'department_337', 'designation': 'designation_337'},
        # {'name': 'name_338', 'email': 'user338@mailinator.com',
        #     'department': 'department_338', 'designation': 'designation_338'},
        # {'name': 'name_339', 'email': 'user339@mailinator.com',
        #     'department': 'department_339', 'designation': 'designation_339'},
        # {'name': 'name_340', 'email': 'user340@mailinator.com',
        #     'department': 'department_340', 'designation': 'designation_340'},
        # {'name': 'name_341', 'email': 'user341@mailinator.com',
        #     'department': 'department_341', 'designation': 'designation_341'},
        # {'name': 'name_342', 'email': 'user342@mailinator.com',
        #     'department': 'department_342', 'designation': 'designation_342'},
        # {'name': 'name_343', 'email': 'user343@mailinator.com',
        #     'department': 'department_343', 'designation': 'designation_343'},
        # {'name': 'name_344', 'email': 'user344@mailinator.com',
        #     'department': 'department_344', 'designation': 'designation_344'},
        # {'name': 'name_345', 'email': 'user345@mailinator.com',
        #     'department': 'department_345', 'designation': 'designation_345'},
        # {'name': 'name_346', 'email': 'user346@mailinator.com',
        #     'department': 'department_346', 'designation': 'designation_346'},
        # {'name': 'name_347', 'email': 'user347@mailinator.com',
        #     'department': 'department_347', 'designation': 'designation_347'},
        # {'name': 'name_348', 'email': 'user348@mailinator.com',
        #     'department': 'department_348', 'designation': 'designation_348'},
        # {'name': 'name_349', 'email': 'user349@mailinator.com',
        #     'department': 'department_349', 'designation': 'designation_349'},
        # {'name': 'name_350', 'email': 'user350@mailinator.com',
        #     'department': 'department_350', 'designation': 'designation_350'},
        # {'name': 'name_351', 'email': 'user351@mailinator.com',
        #     'department': 'department_351', 'designation': 'designation_351'},
        # {'name': 'name_352', 'email': 'user352@mailinator.com',
        #     'department': 'department_352', 'designation': 'designation_352'},
        # {'name': 'name_353', 'email': 'user353@mailinator.com',
        #     'department': 'department_353', 'designation': 'designation_353'},
        # {'name': 'name_354', 'email': 'user354@mailinator.com',
        #     'department': 'department_354', 'designation': 'designation_354'},
        # {'name': 'name_355', 'email': 'user355@mailinator.com',
        #     'department': 'department_355', 'designation': 'designation_355'},
        # {'name': 'name_356', 'email': 'user356@mailinator.com',
        #     'department': 'department_356', 'designation': 'designation_356'},
        # {'name': 'name_357', 'email': 'user357@mailinator.com',
        #     'department': 'department_357', 'designation': 'designation_357'},
        # {'name': 'name_358', 'email': 'user358@mailinator.com',
        #     'department': 'department_358', 'designation': 'designation_358'},
        # {'name': 'name_359', 'email': 'user359@mailinator.com',
        #     'department': 'department_359', 'designation': 'designation_359'},
        # {'name': 'name_360', 'email': 'user360@mailinator.com',
        #     'department': 'department_360', 'designation': 'designation_360'},
        # {'name': 'name_361', 'email': 'user361@mailinator.com',
        #     'department': 'department_361', 'designation': 'designation_361'},
        # {'name': 'name_362', 'email': 'user362@mailinator.com',
        #     'department': 'department_362', 'designation': 'designation_362'},
        # {'name': 'name_363', 'email': 'user363@mailinator.com',
        #     'department': 'department_363', 'designation': 'designation_363'},
        # {'name': 'name_364', 'email': 'user364@mailinator.com',
        #     'department': 'department_364', 'designation': 'designation_364'},
        # {'name': 'name_365', 'email': 'user365@mailinator.com',
        #     'department': 'department_365', 'designation': 'designation_365'},
        # {'name': 'name_366', 'email': 'user366@mailinator.com',
        #     'department': 'department_366', 'designation': 'designation_366'},
        # {'name': 'name_367', 'email': 'user367@mailinator.com',
        #     'department': 'department_367', 'designation': 'designation_367'},
        # {'name': 'name_368', 'email': 'user368@mailinator.com',
        #     'department': 'department_368', 'designation': 'designation_368'},
        # {'name': 'name_369', 'email': 'user369@mailinator.com',
        #     'department': 'department_369', 'designation': 'designation_369'},
        # {'name': 'name_370', 'email': 'user370@mailinator.com',
        #     'department': 'department_370', 'designation': 'designation_370'},
        # {'name': 'name_371', 'email': 'user371@mailinator.com',
        #     'department': 'department_371', 'designation': 'designation_371'},
        # {'name': 'name_372', 'email': 'user372@mailinator.com',
        #     'department': 'department_372', 'designation': 'designation_372'},
        # {'name': 'name_373', 'email': 'user373@mailinator.com',
        #     'department': 'department_373', 'designation': 'designation_373'},
        # {'name': 'name_374', 'email': 'user374@mailinator.com',
        #     'department': 'department_374', 'designation': 'designation_374'},
        # {'name': 'name_375', 'email': 'user375@mailinator.com',
        #     'department': 'department_375', 'designation': 'designation_375'},
        # {'name': 'name_376', 'email': 'user376@mailinator.com',
        #     'department': 'department_376', 'designation': 'designation_376'},
        # {'name': 'name_377', 'email': 'user377@mailinator.com',
        #     'department': 'department_377', 'designation': 'designation_377'},
        # {'name': 'name_378', 'email': 'user378@mailinator.com',
        #     'department': 'department_378', 'designation': 'designation_378'},
        # {'name': 'name_379', 'email': 'user379@mailinator.com',
        #     'department': 'department_379', 'designation': 'designation_379'},
        # {'name': 'name_380', 'email': 'user380@mailinator.com',
        #     'department': 'department_380', 'designation': 'designation_380'},
        # {'name': 'name_381', 'email': 'user381@mailinator.com',
        #     'department': 'department_381', 'designation': 'designation_381'},
        # {'name': 'name_382', 'email': 'user382@mailinator.com',
        #     'department': 'department_382', 'designation': 'designation_382'},
        # {'name': 'name_383', 'email': 'user383@mailinator.com',
        #     'department': 'department_383', 'designation': 'designation_383'},
        # {'name': 'name_384', 'email': 'user384@mailinator.com',
        #     'department': 'department_384', 'designation': 'designation_384'},
        # {'name': 'name_385', 'email': 'user385@mailinator.com',
        #     'department': 'department_385', 'designation': 'designation_385'},
        # {'name': 'name_386', 'email': 'user386@mailinator.com',
        #     'department': 'department_386', 'designation': 'designation_386'},
        # {'name': 'name_387', 'email': 'user387@mailinator.com',
        #     'department': 'department_387', 'designation': 'designation_387'},
        # {'name': 'name_388', 'email': 'user388@mailinator.com',
        #     'department': 'department_388', 'designation': 'designation_388'},
        # {'name': 'name_389', 'email': 'user389@mailinator.com',
        #     'department': 'department_389', 'designation': 'designation_389'},
        # {'name': 'name_390', 'email': 'user390@mailinator.com',
        #     'department': 'department_390', 'designation': 'designation_390'},
        # {'name': 'name_391', 'email': 'user391@mailinator.com',
        #     'department': 'department_391', 'designation': 'designation_391'},
        # {'name': 'name_392', 'email': 'user392@mailinator.com',
        #     'department': 'department_392', 'designation': 'designation_392'},
        # {'name': 'name_393', 'email': 'user393@mailinator.com',
        #     'department': 'department_393', 'designation': 'designation_393'},
        # {'name': 'name_394', 'email': 'user394@mailinator.com',
        #     'department': 'department_394', 'designation': 'designation_394'},
        # {'name': 'name_395', 'email': 'user395@mailinator.com',
        #     'department': 'department_395', 'designation': 'designation_395'},
        # {'name': 'name_396', 'email': 'user396@mailinator.com',
        #     'department': 'department_396', 'designation': 'designation_396'},
        # {'name': 'name_397', 'email': 'user397@mailinator.com',
        #     'department': 'department_397', 'designation': 'designation_397'},
        # {'name': 'name_398', 'email': 'user398@mailinator.com',
        #     'department': 'department_398', 'designation': 'designation_398'},
        # {'name': 'name_399', 'email': 'user399@mailinator.com',
        #     'department': 'department_399', 'designation': 'designation_399'},
        # {'name': 'name_400', 'email': 'user400@mailinator.com',
        #     'department': 'department_400', 'designation': 'designation_400'},
        # {'name': 'name_401', 'email': 'user401@mailinator.com',
        #     'department': 'department_401', 'designation': 'designation_401'},
        # {'name': 'name_402', 'email': 'user402@mailinator.com',
        #     'department': 'department_402', 'designation': 'designation_402'},
        # {'name': 'name_403', 'email': 'user403@mailinator.com',
        #     'department': 'department_403', 'designation': 'designation_403'},
        # {'name': 'name_404', 'email': 'user404@mailinator.com',
        #     'department': 'department_404', 'designation': 'designation_404'},
        # {'name': 'name_405', 'email': 'user405@mailinator.com',
        #     'department': 'department_405', 'designation': 'designation_405'},
        # {'name': 'name_406', 'email': 'user406@mailinator.com',
        #     'department': 'department_406', 'designation': 'designation_406'},
        # {'name': 'name_407', 'email': 'user407@mailinator.com',
        #     'department': 'department_407', 'designation': 'designation_407'},
        # {'name': 'name_408', 'email': 'user408@mailinator.com',
        #     'department': 'department_408', 'designation': 'designation_408'},
        # {'name': 'name_409', 'email': 'user409@mailinator.com',
        #     'department': 'department_409', 'designation': 'designation_409'},
        # {'name': 'name_410', 'email': 'user410@mailinator.com',
        #     'department': 'department_410', 'designation': 'designation_410'},
        # {'name': 'name_411', 'email': 'user411@mailinator.com',
        #     'department': 'department_411', 'designation': 'designation_411'},
        # {'name': 'name_412', 'email': 'user412@mailinator.com',
        #     'department': 'department_412', 'designation': 'designation_412'},
        # {'name': 'name_413', 'email': 'user413@mailinator.com',
        #     'department': 'department_413', 'designation': 'designation_413'},
        # {'name': 'name_414', 'email': 'user414@mailinator.com',
        #     'department': 'department_414', 'designation': 'designation_414'},
        # {'name': 'name_415', 'email': 'user415@mailinator.com',
        #     'department': 'department_415', 'designation': 'designation_415'},
        # {'name': 'name_416', 'email': 'user416@mailinator.com',
        #     'department': 'department_416', 'designation': 'designation_416'},
        # {'name': 'name_417', 'email': 'user417@mailinator.com',
        #     'department': 'department_417', 'designation': 'designation_417'},
        # {'name': 'name_418', 'email': 'user418@mailinator.com',
        #     'department': 'department_418', 'designation': 'designation_418'},
        # {'name': 'name_419', 'email': 'user419@mailinator.com',
        #     'department': 'department_419', 'designation': 'designation_419'},
        # {'name': 'name_420', 'email': 'user420@mailinator.com',
        #     'department': 'department_420', 'designation': 'designation_420'},
        # {'name': 'name_421', 'email': 'user421@mailinator.com',
        #     'department': 'department_421', 'designation': 'designation_421'},
        # {'name': 'name_422', 'email': 'user422@mailinator.com',
        #     'department': 'department_422', 'designation': 'designation_422'},
        # {'name': 'name_423', 'email': 'user423@mailinator.com',
        #     'department': 'department_423', 'designation': 'designation_423'},
        # {'name': 'name_424', 'email': 'user424@mailinator.com',
        #     'department': 'department_424', 'designation': 'designation_424'},
        # {'name': 'name_425', 'email': 'user425@mailinator.com',
        #     'department': 'department_425', 'designation': 'designation_425'},
        # {'name': 'name_426', 'email': 'user426@mailinator.com',
        #     'department': 'department_426', 'designation': 'designation_426'},
        # {'name': 'name_427', 'email': 'user427@mailinator.com',
        #     'department': 'department_427', 'designation': 'designation_427'},
        # {'name': 'name_428', 'email': 'user428@mailinator.com',
        #     'department': 'department_428', 'designation': 'designation_428'},
        # {'name': 'name_429', 'email': 'user429@mailinator.com',
        #     'department': 'department_429', 'designation': 'designation_429'},
        # {'name': 'name_430', 'email': 'user430@mailinator.com',
        #     'department': 'department_430', 'designation': 'designation_430'},
        # {'name': 'name_431', 'email': 'user431@mailinator.com',
        #     'department': 'department_431', 'designation': 'designation_431'},
        # {'name': 'name_432', 'email': 'user432@mailinator.com',
        #     'department': 'department_432', 'designation': 'designation_432'},
        # {'name': 'name_433', 'email': 'user433@mailinator.com',
        #     'department': 'department_433', 'designation': 'designation_433'},
        # {'name': 'name_434', 'email': 'user434@mailinator.com',
        #     'department': 'department_434', 'designation': 'designation_434'},
        # {'name': 'name_435', 'email': 'user435@mailinator.com',
        #     'department': 'department_435', 'designation': 'designation_435'},
        # {'name': 'name_436', 'email': 'user436@mailinator.com',
        #     'department': 'department_436', 'designation': 'designation_436'},
        # {'name': 'name_437', 'email': 'user437@mailinator.com',
        #     'department': 'department_437', 'designation': 'designation_437'},
        # {'name': 'name_438', 'email': 'user438@mailinator.com',
        #     'department': 'department_438', 'designation': 'designation_438'},
        # {'name': 'name_439', 'email': 'user439@mailinator.com',
        #     'department': 'department_439', 'designation': 'designation_439'},
        # {'name': 'name_440', 'email': 'user440@mailinator.com',
        #     'department': 'department_440', 'designation': 'designation_440'},
        # {'name': 'name_441', 'email': 'user441@mailinator.com',
        #     'department': 'department_441', 'designation': 'designation_441'},
        # {'name': 'name_442', 'email': 'user442@mailinator.com',
        #     'department': 'department_442', 'designation': 'designation_442'},
        # {'name': 'name_443', 'email': 'user443@mailinator.com',
        #     'department': 'department_443', 'designation': 'designation_443'},
        # {'name': 'name_444', 'email': 'user444@mailinator.com',
        #     'department': 'department_444', 'designation': 'designation_444'},
        # {'name': 'name_445', 'email': 'user445@mailinator.com',
        #     'department': 'department_445', 'designation': 'designation_445'},
        # {'name': 'name_446', 'email': 'user446@mailinator.com',
        #     'department': 'department_446', 'designation': 'designation_446'},
        # {'name': 'name_447', 'email': 'user447@mailinator.com',
        #     'department': 'department_447', 'designation': 'designation_447'},
        # {'name': 'name_448', 'email': 'user448@mailinator.com',
        #     'department': 'department_448', 'designation': 'designation_448'},
        # {'name': 'name_449', 'email': 'user449@mailinator.com',
        #     'department': 'department_449', 'designation': 'designation_449'},
        # {'name': 'name_450', 'email': 'user450@mailinator.com',
        #     'department': 'department_450', 'designation': 'designation_450'},
        # {'name': 'name_451', 'email': 'user451@mailinator.com',
        #     'department': 'department_451', 'designation': 'designation_451'},
        # {'name': 'name_452', 'email': 'user452@mailinator.com',
        #     'department': 'department_452', 'designation': 'designation_452'},
        # {'name': 'name_453', 'email': 'user453@mailinator.com',
        #     'department': 'department_453', 'designation': 'designation_453'},
        # {'name': 'name_454', 'email': 'user454@mailinator.com',
        #     'department': 'department_454', 'designation': 'designation_454'},
        # {'name': 'name_455', 'email': 'user455@mailinator.com',
        #     'department': 'department_455', 'designation': 'designation_455'},
        # {'name': 'name_456', 'email': 'user456@mailinator.com',
        #     'department': 'department_456', 'designation': 'designation_456'},
        # {'name': 'name_457', 'email': 'user457@mailinator.com',
        #     'department': 'department_457', 'designation': 'designation_457'},
        # {'name': 'name_458', 'email': 'user458@mailinator.com',
        #     'department': 'department_458', 'designation': 'designation_458'},
        # {'name': 'name_459', 'email': 'user459@mailinator.com',
        #     'department': 'department_459', 'designation': 'designation_459'},
        # {"name": "Anurag Kumar", "email": "akanuragkumar75@gmail.com",
        #     "department": "Developer", "designation": "Developer"},
        # {'name': 'name_460', 'email': 'user460@mailinator.com',
        #     'department': 'department_460', 'designation': 'designation_460'},
        # {'name': 'name_461', 'email': 'user461@mailinator.com',
        #     'department': 'department_461', 'designation': 'designation_461'},
        # {'name': 'name_462', 'email': 'user462@mailinator.com',
        #     'department': 'department_462', 'designation': 'designation_462'},
        # {'name': 'name_463', 'email': 'user463@mailinator.com',
        #     'department': 'department_463', 'designation': 'designation_463'},
        # {'name': 'name_464', 'email': 'user464@mailinator.com',
        #     'department': 'department_464', 'designation': 'designation_464'},
        # {'name': 'name_465', 'email': 'user465@mailinator.com',
        #     'department': 'department_465', 'designation': 'designation_465'},
        # {'name': 'name_466', 'email': 'user466@mailinator.com',
        #     'department': 'department_466', 'designation': 'designation_466'},
        # {'name': 'name_467', 'email': 'user467@mailinator.com',
        #     'department': 'department_467', 'designation': 'designation_467'},
        # {'name': 'name_468', 'email': 'user468@mailinator.com',
        #     'department': 'department_468', 'designation': 'designation_468'},
        # {'name': 'name_469', 'email': 'user469@mailinator.com',
        #     'department': 'department_469', 'designation': 'designation_469'},
        # {'name': 'name_470', 'email': 'user470@mailinator.com',
        #     'department': 'department_470', 'designation': 'designation_470'},
        # {'name': 'name_471', 'email': 'user471@mailinator.com',
        #     'department': 'department_471', 'designation': 'designation_471'},
        # {'name': 'name_472', 'email': 'user472@mailinator.com',
        #     'department': 'department_472', 'designation': 'designation_472'},
        # {'name': 'name_473', 'email': 'user473@mailinator.com',
        #     'department': 'department_473', 'designation': 'designation_473'},
        # {'name': 'name_474', 'email': 'user474@mailinator.com',
        #     'department': 'department_474', 'designation': 'designation_474'},
        # {'name': 'name_475', 'email': 'user475@mailinator.com',
        #     'department': 'department_475', 'designation': 'designation_475'},
        # {'name': 'name_476', 'email': 'user476@mailinator.com',
        #     'department': 'department_476', 'designation': 'designation_476'},
        # {'name': 'name_477', 'email': 'user477@mailinator.com',
        #     'department': 'department_477', 'designation': 'designation_477'},
        # {'name': 'name_478', 'email': 'user478@mailinator.com',
        #     'department': 'department_478', 'designation': 'designation_478'},
        # {'name': 'name_479', 'email': 'user479@mailinator.com',
        #     'department': 'department_479', 'designation': 'designation_479'},
        # {'name': 'name_480', 'email': 'user480@mailinator.com',
        #     'department': 'department_480', 'designation': 'designation_480'},
        # {'name': 'name_481', 'email': 'user481@mailinator.com',
        #     'department': 'department_481', 'designation': 'designation_481'},
        # {'name': 'name_482', 'email': 'user482@mailinator.com',
        #     'department': 'department_482', 'designation': 'designation_482'},
        # {'name': 'name_483', 'email': 'user483@mailinator.com',
        #     'department': 'department_483', 'designation': 'designation_483'},
        # {'name': 'name_484', 'email': 'user484@mailinator.com',
        #     'department': 'department_484', 'designation': 'designation_484'},
        # {'name': 'name_485', 'email': 'user485@mailinator.com',
        #     'department': 'department_485', 'designation': 'designation_485'},
        # {'name': 'name_486', 'email': 'user486@mailinator.com',
        #     'department': 'department_486', 'designation': 'designation_486'},
        # {'name': 'name_487', 'email': 'user487@mailinator.com',
        #     'department': 'department_487', 'designation': 'designation_487'},
        # {'name': 'name_488', 'email': 'user488@mailinator.com',
        #     'department': 'department_488', 'designation': 'designation_488'},
        # {'name': 'name_489', 'email': 'user489@mailinator.com',
        #     'department': 'department_489', 'designation': 'designation_489'},
        # {'name': 'name_490', 'email': 'user490@mailinator.com',
        #     'department': 'department_490', 'designation': 'designation_490'},
        # {'name': 'name_491', 'email': 'user491@mailinator.com',
        #     'department': 'department_491', 'designation': 'designation_491'},
        # {'name': 'name_492', 'email': 'user492@mailinator.com',
        #     'department': 'department_492', 'designation': 'designation_492'},
        # {'name': 'name_493', 'email': 'user493@mailinator.com',
        #     'department': 'department_493', 'designation': 'designation_493'},
        # {'name': 'name_494', 'email': 'user494@mailinator.com',
        #     'department': 'department_494', 'designation': 'designation_494'},
        # {'name': 'name_495', 'email': 'user495@mailinator.com',
        #     'department': 'department_495', 'designation': 'designation_495'},
        # {'name': 'name_496', 'email': 'user496@mailinator.com',
        #     'department': 'department_496', 'designation': 'designation_496'},
        # {'name': 'name_497', 'email': 'user497@mailinator.com',
        #     'department': 'department_497', 'designation': 'designation_497'},
        # {'name': 'name_498', 'email': 'user498@mailinator.com',
        #     'department': 'department_498', 'designation': 'designation_498'},
        # {'name': 'name_499', 'email': 'user499@mailinator.com',
        #     'department': 'department_499', 'designation': 'designation_499'},
        # {'name': 'name_500', 'email': 'user500@mailinator.com',
        #     'department': 'department_500', 'designation': 'designation_500'},
        # {'name': 'name_501', 'email': 'user501@mailinator.com',
        #     'department': 'department_501', 'designation': 'designation_501'},
        # {'name': 'name_502', 'email': 'user502@mailinator.com',
        #     'department': 'department_502', 'designation': 'designation_502'},
        # {'name': 'name_503', 'email': 'user503@mailinator.com',
        #     'department': 'department_503', 'designation': 'designation_503'},
        # {'name': 'name_504', 'email': 'user504@mailinator.com',
        #     'department': 'department_504', 'designation': 'designation_504'},
        # {'name': 'name_505', 'email': 'user505@mailinator.com',
        #     'department': 'department_505', 'designation': 'designation_505'},
        # {'name': 'name_506', 'email': 'user506@mailinator.com',
        #     'department': 'department_506', 'designation': 'designation_506'},
        # {'name': 'name_507', 'email': 'user507@mailinator.com',
        #     'department': 'department_507', 'designation': 'designation_507'},
        # {'name': 'name_508', 'email': 'user508@mailinator.com',
        #     'department': 'department_508', 'designation': 'designation_508'},
        # {'name': 'name_509', 'email': 'user509@mailinator.com',
        #     'department': 'department_509', 'designation': 'designation_509'},
        # {'name': 'name_510', 'email': 'user510@mailinator.com',
        #     'department': 'department_510', 'designation': 'designation_510'},
        # {'name': 'name_511', 'email': 'user511@mailinator.com',
        #     'department': 'department_511', 'designation': 'designation_511'},
        # {'name': 'name_512', 'email': 'user512@mailinator.com',
        #     'department': 'department_512', 'designation': 'designation_512'},
        # {'name': 'name_513', 'email': 'user513@mailinator.com',
        #     'department': 'department_513', 'designation': 'designation_513'},
        # {'name': 'name_514', 'email': 'user514@mailinator.com',
        #     'department': 'department_514', 'designation': 'designation_514'},
        # {'name': 'name_515', 'email': 'user515@mailinator.com',
        #     'department': 'department_515', 'designation': 'designation_515'},
        # {'name': 'name_516', 'email': 'user516@mailinator.com',
        #     'department': 'department_516', 'designation': 'designation_516'},
        # {'name': 'name_517', 'email': 'user517@mailinator.com',
        #     'department': 'department_517', 'designation': 'designation_517'},
        # {'name': 'name_518', 'email': 'user518@mailinator.com',
        #     'department': 'department_518', 'designation': 'designation_518'},
        # {'name': 'name_519', 'email': 'user519@mailinator.com',
        #     'department': 'department_519', 'designation': 'designation_519'},
        # {'name': 'name_520', 'email': 'user520@mailinator.com',
        #     'department': 'department_520', 'designation': 'designation_520'},
        # {'name': 'name_521', 'email': 'user521@mailinator.com',
        #     'department': 'department_521', 'designation': 'designation_521'},
        # {'name': 'name_522', 'email': 'user522@mailinator.com',
        #     'department': 'department_522', 'designation': 'designation_522'},
        # {'name': 'name_523', 'email': 'user523@mailinator.com',
        #     'department': 'department_523', 'designation': 'designation_523'},
        # {'name': 'name_524', 'email': 'user524@mailinator.com',
        #     'department': 'department_524', 'designation': 'designation_524'},
        # {'name': 'name_525', 'email': 'user525@mailinator.com',
        #     'department': 'department_525', 'designation': 'designation_525'},
        # {'name': 'name_526', 'email': 'user526@mailinator.com',
        #     'department': 'department_526', 'designation': 'designation_526'},
        # {'name': 'name_527', 'email': 'user527@mailinator.com',
        #     'department': 'department_527', 'designation': 'designation_527'},
        # {'name': 'name_528', 'email': 'user528@mailinator.com',
        #     'department': 'department_528', 'designation': 'designation_528'},
        # {'name': 'name_529', 'email': 'user529@mailinator.com',
        #     'department': 'department_529', 'designation': 'designation_529'},
        # {'name': 'name_530', 'email': 'user530@mailinator.com',
        #     'department': 'department_530', 'designation': 'designation_530'},
        # {'name': 'name_531', 'email': 'user531@mailinator.com',
        #     'department': 'department_531', 'designation': 'designation_531'},
        # {'name': 'name_532', 'email': 'user532@mailinator.com',
        #     'department': 'department_532', 'designation': 'designation_532'},
        # {'name': 'name_533', 'email': 'user533@mailinator.com',
        #     'department': 'department_533', 'designation': 'designation_533'},
        # {'name': 'name_534', 'email': 'user534@mailinator.com',
        #     'department': 'department_534', 'designation': 'designation_534'},
        # {'name': 'name_535', 'email': 'user535@mailinator.com',
        #     'department': 'department_535', 'designation': 'designation_535'},
        # {'name': 'name_536', 'email': 'user536@mailinator.com',
        #     'department': 'department_536', 'designation': 'designation_536'},
        # {'name': 'name_537', 'email': 'user537@mailinator.com',
        #     'department': 'department_537', 'designation': 'designation_537'},
        # {'name': 'name_538', 'email': 'user538@mailinator.com',
        #     'department': 'department_538', 'designation': 'designation_538'},
        # {'name': 'name_539', 'email': 'user539@mailinator.com',
        #     'department': 'department_539', 'designation': 'designation_539'},
        # {'name': 'name_540', 'email': 'user540@mailinator.com',
        #     'department': 'department_540', 'designation': 'designation_540'},
        # {'name': 'name_541', 'email': 'user541@mailinator.com',
        #     'department': 'department_541', 'designation': 'designation_541'},
        # {'name': 'name_542', 'email': 'user542@mailinator.com',
        #     'department': 'department_542', 'designation': 'designation_542'},
        # {'name': 'name_543', 'email': 'user543@mailinator.com',
        #     'department': 'department_543', 'designation': 'designation_543'},
        # {'name': 'name_544', 'email': 'user544@mailinator.com',
        #     'department': 'department_544', 'designation': 'designation_544'},
        # {'name': 'name_545', 'email': 'user545@mailinator.com',
        #     'department': 'department_545', 'designation': 'designation_545'},
        # {'name': 'name_546', 'email': 'user546@mailinator.com',
        #     'department': 'department_546', 'designation': 'designation_546'},
        # {'name': 'name_547', 'email': 'user547@mailinator.com',
        #     'department': 'department_547', 'designation': 'designation_547'},
        # {'name': 'name_548', 'email': 'user548@mailinator.com',
        #     'department': 'department_548', 'designation': 'designation_548'},
        # {'name': 'name_549', 'email': 'user549@mailinator.com',
        #     'department': 'department_549', 'designation': 'designation_549'},
        # {'name': 'name_550', 'email': 'user550@mailinator.com',
        #     'department': 'department_550', 'designation': 'designation_550'},
        # {'name': 'name_551', 'email': 'user551@mailinator.com',
        #     'department': 'department_551', 'designation': 'designation_551'},
        # {'name': 'name_552', 'email': 'user552@mailinator.com',
        #     'department': 'department_552', 'designation': 'designation_552'},
        # {'name': 'name_553', 'email': 'user553@mailinator.com',
        #     'department': 'department_553', 'designation': 'designation_553'},
        # {'name': 'name_554', 'email': 'user554@mailinator.com',
        #     'department': 'department_554', 'designation': 'designation_554'},
        # {'name': 'name_555', 'email': 'user555@mailinator.com',
        #     'department': 'department_555', 'designation': 'designation_555'},
        # {'name': 'name_556', 'email': 'user556@mailinator.com',
        #     'department': 'department_556', 'designation': 'designation_556'},
        # {'name': 'name_557', 'email': 'user557@mailinator.com',
        #     'department': 'department_557', 'designation': 'designation_557'},
        # {'name': 'name_558', 'email': 'user558@mailinator.com',
        #     'department': 'department_558', 'designation': 'designation_558'},
        # {'name': 'name_559', 'email': 'user559@mailinator.com',
        #     'department': 'department_559', 'designation': 'designation_559'},
        # {'name': 'name_560', 'email': 'user560@mailinator.com',
        #     'department': 'department_560', 'designation': 'designation_560'},
        # {'name': 'name_561', 'email': 'user561@mailinator.com',
        #     'department': 'department_561', 'designation': 'designation_561'},
        # {'name': 'name_562', 'email': 'user562@mailinator.com',
        #     'department': 'department_562', 'designation': 'designation_562'},
        # {'name': 'name_563', 'email': 'user563@mailinator.com',
        #     'department': 'department_563', 'designation': 'designation_563'},
        # {'name': 'name_564', 'email': 'user564@mailinator.com',
        #     'department': 'department_564', 'designation': 'designation_564'},
        # {'name': 'name_565', 'email': 'user565@mailinator.com',
        #     'department': 'department_565', 'designation': 'designation_565'},
        # {'name': 'name_566', 'email': 'user566@mailinator.com',
        #     'department': 'department_566', 'designation': 'designation_566'},
        # {'name': 'name_567', 'email': 'user567@mailinator.com',
        #     'department': 'department_567', 'designation': 'designation_567'},
        # {'name': 'name_568', 'email': 'user568@mailinator.com',
        #     'department': 'department_568', 'designation': 'designation_568'},
        # {'name': 'name_569', 'email': 'user569@mailinator.com',
        #     'department': 'department_569', 'designation': 'designation_569'},
        # {'name': 'name_570', 'email': 'user570@mailinator.com',
        #     'department': 'department_570', 'designation': 'designation_570'},
        # {'name': 'name_571', 'email': 'user571@mailinator.com',
        #     'department': 'department_571', 'designation': 'designation_571'},
        # {'name': 'name_572', 'email': 'user572@mailinator.com',
        #     'department': 'department_572', 'designation': 'designation_572'},
        # {'name': 'name_573', 'email': 'user573@mailinator.com',
        #     'department': 'department_573', 'designation': 'designation_573'},
        # {'name': 'name_574', 'email': 'user574@mailinator.com',
        #     'department': 'department_574', 'designation': 'designation_574'},
        # {'name': 'name_575', 'email': 'user575@mailinator.com',
        #     'department': 'department_575', 'designation': 'designation_575'},
        # {'name': 'name_576', 'email': 'user576@mailinator.com',
        #     'department': 'department_576', 'designation': 'designation_576'},
        # {'name': 'name_577', 'email': 'user577@mailinator.com',
        #     'department': 'department_577', 'designation': 'designation_577'},
        # {'name': 'name_578', 'email': 'user578@mailinator.com',
        #     'department': 'department_578', 'designation': 'designation_578'},
        # {'name': 'name_579', 'email': 'user579@mailinator.com',
        #     'department': 'department_579', 'designation': 'designation_579'},
        # {'name': 'name_580', 'email': 'user580@mailinator.com',
        #     'department': 'department_580', 'designation': 'designation_580'},
        # {'name': 'name_581', 'email': 'user581@mailinator.com',
        #     'department': 'department_581', 'designation': 'designation_581'},
        # {'name': 'name_582', 'email': 'user582@mailinator.com',
        #     'department': 'department_582', 'designation': 'designation_582'},
        # {'name': 'name_583', 'email': 'user583@mailinator.com',
        #     'department': 'department_583', 'designation': 'designation_583'},
        # {'name': 'name_584', 'email': 'user584@mailinator.com',
        #     'department': 'department_584', 'designation': 'designation_584'},
        # {'name': 'name_585', 'email': 'user585@mailinator.com',
        #     'department': 'department_585', 'designation': 'designation_585'},
        # {'name': 'name_586', 'email': 'user586@mailinator.com',
        #     'department': 'department_586', 'designation': 'designation_586'},
        # {'name': 'name_587', 'email': 'user587@mailinator.com',
        #     'department': 'department_587', 'designation': 'designation_587'},
        # {'name': 'name_588', 'email': 'user588@mailinator.com',
        #     'department': 'department_588', 'designation': 'designation_588'},
        # {'name': 'name_589', 'email': 'user589@mailinator.com',
        #     'department': 'department_589', 'designation': 'designation_589'},
        # {'name': 'name_590', 'email': 'user590@mailinator.com',
        #     'department': 'department_590', 'designation': 'designation_590'},
        # {'name': 'name_591', 'email': 'user591@mailinator.com',
        #     'department': 'department_591', 'designation': 'designation_591'},
        # {'name': 'name_592', 'email': 'user592@mailinator.com',
        #     'department': 'department_592', 'designation': 'designation_592'},
        # {'name': 'name_593', 'email': 'user593@mailinator.com',
        #     'department': 'department_593', 'designation': 'designation_593'},
        # {'name': 'name_594', 'email': 'user594@mailinator.com',
        #     'department': 'department_594', 'designation': 'designation_594'},
        # {'name': 'name_595', 'email': 'user595@mailinator.com',
        #     'department': 'department_595', 'designation': 'designation_595'},
        # {'name': 'name_596', 'email': 'user596@mailinator.com',
        #     'department': 'department_596', 'designation': 'designation_596'},
        # {'name': 'name_597', 'email': 'user597@mailinator.com',
        #     'department': 'department_597', 'designation': 'designation_597'},
        # {'name': 'name_598', 'email': 'user598@mailinator.com',
        #     'department': 'department_598', 'designation': 'designation_598'},
        # {'name': 'name_599', 'email': 'user599@mailinator.com',
        #     'department': 'department_599', 'designation': 'designation_599'},
        # {'name': 'name_600', 'email': 'user600@mailinator.com',
        #     'department': 'department_600', 'designation': 'designation_600'},
        # {'name': 'name_601', 'email': 'user601@mailinator.com',
        #     'department': 'department_601', 'designation': 'designation_601'},
        # {'name': 'name_602', 'email': 'user602@mailinator.com',
        #     'department': 'department_602', 'designation': 'designation_602'},
        # {'name': 'name_603', 'email': 'user603@mailinator.com',
        #     'department': 'department_603', 'designation': 'designation_603'},
        # {'name': 'name_604', 'email': 'user604@mailinator.com',
        #     'department': 'department_604', 'designation': 'designation_604'},
        # {'name': 'name_605', 'email': 'user605@mailinator.com',
        #     'department': 'department_605', 'designation': 'designation_605'},
        # {'name': 'name_606', 'email': 'user606@mailinator.com',
        #     'department': 'department_606', 'designation': 'designation_606'},
        # {'name': 'name_607', 'email': 'user607@mailinator.com',
        #     'department': 'department_607', 'designation': 'designation_607'},
        # {'name': 'name_608', 'email': 'user608@mailinator.com',
        #     'department': 'department_608', 'designation': 'designation_608'},
        # {'name': 'name_609', 'email': 'user609@mailinator.com',
        #     'department': 'department_609', 'designation': 'designation_609'},
        # {'name': 'name_610', 'email': 'user610@mailinator.com',
        #     'department': 'department_610', 'designation': 'designation_610'},
        # {'name': 'name_611', 'email': 'user611@mailinator.com',
        #     'department': 'department_611', 'designation': 'designation_611'},
        # {'name': 'name_612', 'email': 'user612@mailinator.com',
        #     'department': 'department_612', 'designation': 'designation_612'},
        # {'name': 'name_613', 'email': 'user613@mailinator.com',
        #     'department': 'department_613', 'designation': 'designation_613'},
        # {'name': 'name_614', 'email': 'user614@mailinator.com',
        #     'department': 'department_614', 'designation': 'designation_614'},
        # {'name': 'name_615', 'email': 'user615@mailinator.com',
        #     'department': 'department_615', 'designation': 'designation_615'},
        # {'name': 'name_616', 'email': 'user616@mailinator.com',
        #     'department': 'department_616', 'designation': 'designation_616'},
        # {'name': 'name_617', 'email': 'user617@mailinator.com',
        #     'department': 'department_617', 'designation': 'designation_617'},
        # {'name': 'name_618', 'email': 'user618@mailinator.com',
        #     'department': 'department_618', 'designation': 'designation_618'},
        # {'name': 'name_619', 'email': 'user619@mailinator.com',
        #     'department': 'department_619', 'designation': 'designation_619'},
        # {'name': 'name_620', 'email': 'user620@mailinator.com',
        #     'department': 'department_620', 'designation': 'designation_620'},
        # {'name': 'name_621', 'email': 'user621@mailinator.com',
        #     'department': 'department_621', 'designation': 'designation_621'},
        # {'name': 'name_622', 'email': 'user622@mailinator.com',
        #     'department': 'department_622', 'designation': 'designation_622'},
        # {'name': 'name_623', 'email': 'user623@mailinator.com',
        #     'department': 'department_623', 'designation': 'designation_623'},
        # {'name': 'name_624', 'email': 'user624@mailinator.com',
        #     'department': 'department_624', 'designation': 'designation_624'},
        # {'name': 'name_625', 'email': 'user625@mailinator.com',
        #     'department': 'department_625', 'designation': 'designation_625'},
        # {'name': 'name_626', 'email': 'user626@mailinator.com',
        #     'department': 'department_626', 'designation': 'designation_626'},
        # {'name': 'name_627', 'email': 'user627@mailinator.com',
        #     'department': 'department_627', 'designation': 'designation_627'},
        # {'name': 'name_628', 'email': 'user628@mailinator.com',
        #     'department': 'department_628', 'designation': 'designation_628'},
        # {'name': 'name_629', 'email': 'user629@mailinator.com',
        #     'department': 'department_629', 'designation': 'designation_629'},
        # {'name': 'name_630', 'email': 'user630@mailinator.com',
        #     'department': 'department_630', 'designation': 'designation_630'},
        # {'name': 'name_631', 'email': 'user631@mailinator.com',
        #     'department': 'department_631', 'designation': 'designation_631'},
        # {'name': 'name_632', 'email': 'user632@mailinator.com',
        #     'department': 'department_632', 'designation': 'designation_632'},
        # {'name': 'name_633', 'email': 'user633@mailinator.com',
        #     'department': 'department_633', 'designation': 'designation_633'},
        # {'name': 'name_634', 'email': 'user634@mailinator.com',
        #     'department': 'department_634', 'designation': 'designation_634'},
        # {'name': 'name_635', 'email': 'user635@mailinator.com',
        #     'department': 'department_635', 'designation': 'designation_635'},
        # {'name': 'name_636', 'email': 'user636@mailinator.com',
        #     'department': 'department_636', 'designation': 'designation_636'},
        # {'name': 'name_637', 'email': 'user637@mailinator.com',
        #     'department': 'department_637', 'designation': 'designation_637'},
        # {'name': 'name_638', 'email': 'user638@mailinator.com',
        #     'department': 'department_638', 'designation': 'designation_638'},
        # {'name': 'name_639', 'email': 'user639@mailinator.com',
        #     'department': 'department_639', 'designation': 'designation_639'},
        # {'name': 'name_640', 'email': 'user640@mailinator.com',
        #     'department': 'department_640', 'designation': 'designation_640'},
        # {'name': 'name_641', 'email': 'user641@mailinator.com',
        #     'department': 'department_641', 'designation': 'designation_641'},
        # {'name': 'name_642', 'email': 'user642@mailinator.com',
        #     'department': 'department_642', 'designation': 'designation_642'},
        # {'name': 'name_643', 'email': 'user643@mailinator.com',
        #     'department': 'department_643', 'designation': 'designation_643'},
        # {'name': 'name_644', 'email': 'user644@mailinator.com',
        #     'department': 'department_644', 'designation': 'designation_644'},
        # {'name': 'name_645', 'email': 'user645@mailinator.com',
        #     'department': 'department_645', 'designation': 'designation_645'},
        # {'name': 'name_646', 'email': 'user646@mailinator.com',
        #     'department': 'department_646', 'designation': 'designation_646'},
        # {'name': 'name_647', 'email': 'user647@mailinator.com',
        #     'department': 'department_647', 'designation': 'designation_647'},
        # {'name': 'name_648', 'email': 'user648@mailinator.com',
        #     'department': 'department_648', 'designation': 'designation_648'},
        # {'name': 'name_649', 'email': 'user649@mailinator.com',
        #     'department': 'department_649', 'designation': 'designation_649'},
        # {'name': 'name_650', 'email': 'user650@mailinator.com',
        #     'department': 'department_650', 'designation': 'designation_650'},
        # {'name': 'name_651', 'email': 'user651@mailinator.com',
        #     'department': 'department_651', 'designation': 'designation_651'},
        # {'name': 'name_652', 'email': 'user652@mailinator.com',
        #     'department': 'department_652', 'designation': 'designation_652'},
        # {'name': 'name_653', 'email': 'user653@mailinator.com',
        #     'department': 'department_653', 'designation': 'designation_653'},
        # {'name': 'name_654', 'email': 'user654@mailinator.com',
        #     'department': 'department_654', 'designation': 'designation_654'},
        # {'name': 'name_655', 'email': 'user655@mailinator.com',
        #     'department': 'department_655', 'designation': 'designation_655'},
        # {'name': 'name_656', 'email': 'user656@mailinator.com',
        #     'department': 'department_656', 'designation': 'designation_656'},
        # {'name': 'name_657', 'email': 'user657@mailinator.com',
        #     'department': 'department_657', 'designation': 'designation_657'},
        # {'name': 'name_658', 'email': 'user658@mailinator.com',
        #     'department': 'department_658', 'designation': 'designation_658'},
        # {'name': 'name_659', 'email': 'user659@mailinator.com',
        #     'department': 'department_659', 'designation': 'designation_659'},
        # {'name': 'name_660', 'email': 'user660@mailinator.com',
        #     'department': 'department_660', 'designation': 'designation_660'},
        # {'name': 'name_661', 'email': 'user661@mailinator.com',
        #     'department': 'department_661', 'designation': 'designation_661'},
        # {'name': 'name_662', 'email': 'user662@mailinator.com',
        #     'department': 'department_662', 'designation': 'designation_662'},
        # {'name': 'name_663', 'email': 'user663@mailinator.com',
        #     'department': 'department_663', 'designation': 'designation_663'},
        # {'name': 'name_664', 'email': 'user664@mailinator.com',
        #     'department': 'department_664', 'designation': 'designation_664'},
        # {'name': 'name_665', 'email': 'user665@mailinator.com',
        #     'department': 'department_665', 'designation': 'designation_665'},
        # {'name': 'name_666', 'email': 'user666@mailinator.com',
        #     'department': 'department_666', 'designation': 'designation_666'},
        # {'name': 'name_667', 'email': 'user667@mailinator.com',
        #     'department': 'department_667', 'designation': 'designation_667'},
        # {'name': 'name_668', 'email': 'user668@mailinator.com',
        #     'department': 'department_668', 'designation': 'designation_668'},
        # {'name': 'name_669', 'email': 'user669@mailinator.com',
        #     'department': 'department_669', 'designation': 'designation_669'},
        # {'name': 'name_670', 'email': 'user670@mailinator.com',
        #     'department': 'department_670', 'designation': 'designation_670'},
        # {'name': 'name_671', 'email': 'user671@mailinator.com',
        #     'department': 'department_671', 'designation': 'designation_671'},
        # {'name': 'name_672', 'email': 'user672@mailinator.com',
        #     'department': 'department_672', 'designation': 'designation_672'},
        # {'name': 'name_673', 'email': 'user673@mailinator.com',
        #     'department': 'department_673', 'designation': 'designation_673'},
        # {'name': 'name_674', 'email': 'user674@mailinator.com',
        #     'department': 'department_674', 'designation': 'designation_674'},
        # {'name': 'name_675', 'email': 'user675@mailinator.com',
        #     'department': 'department_675', 'designation': 'designation_675'},
        # {"name": "Sethi", "email": "tech@kvqaindia.com",
        #     "department": "Developer", "designation": "Frontend Developer"},
        # {'name': 'name_676', 'email': 'user676@mailinator.com',
        #     'department': 'department_676', 'designation': 'designation_676'},
        # {'name': 'name_677', 'email': 'user677@mailinator.com',
        #     'department': 'department_677', 'designation': 'designation_677'},
        # {'name': 'name_678', 'email': 'user678@mailinator.com',
        #     'department': 'department_678', 'designation': 'designation_678'},
        # {'name': 'name_679', 'email': 'user679@mailinator.com',
        #     'department': 'department_679', 'designation': 'designation_679'},
        # {'name': 'name_680', 'email': 'user680@mailinator.com',
        #     'department': 'department_680', 'designation': 'designation_680'},
        # {'name': 'name_681', 'email': 'user681@mailinator.com',
        #     'department': 'department_681', 'designation': 'designation_681'},
        # {'name': 'name_682', 'email': 'user682@mailinator.com',
        #     'department': 'department_682', 'designation': 'designation_682'},
        # {'name': 'name_683', 'email': 'user683@mailinator.com',
        #     'department': 'department_683', 'designation': 'designation_683'},
        # {'name': 'name_684', 'email': 'user684@mailinator.com',
        #     'department': 'department_684', 'designation': 'designation_684'},
        # {'name': 'name_685', 'email': 'user685@mailinator.com',
        #     'department': 'department_685', 'designation': 'designation_685'},
        # {'name': 'name_686', 'email': 'user686@mailinator.com',
        #     'department': 'department_686', 'designation': 'designation_686'},
        # {'name': 'name_687', 'email': 'user687@mailinator.com',
        #     'department': 'department_687', 'designation': 'designation_687'},
        # {'name': 'name_688', 'email': 'user688@mailinator.com',
        #     'department': 'department_688', 'designation': 'designation_688'},
        # {'name': 'name_689', 'email': 'user689@mailinator.com',
        #     'department': 'department_689', 'designation': 'designation_689'},
        # {'name': 'name_690', 'email': 'user690@mailinator.com',
        #     'department': 'department_690', 'designation': 'designation_690'},
        # {'name': 'name_691', 'email': 'user691@mailinator.com',
        #     'department': 'department_691', 'designation': 'designation_691'},
        # {'name': 'name_692', 'email': 'user692@mailinator.com',
        #     'department': 'department_692', 'designation': 'designation_692'},
        # {'name': 'name_693', 'email': 'user693@mailinator.com',
        #     'department': 'department_693', 'designation': 'designation_693'},
        # {'name': 'name_694', 'email': 'user694@mailinator.com',
        #     'department': 'department_694', 'designation': 'designation_694'},
        # {'name': 'name_695', 'email': 'user695@mailinator.com',
        #     'department': 'department_695', 'designation': 'designation_695'},
        # {'name': 'name_696', 'email': 'user696@mailinator.com',
        #     'department': 'department_696', 'designation': 'designation_696'},
        # {'name': 'name_697', 'email': 'user697@mailinator.com',
        #     'department': 'department_697', 'designation': 'designation_697'},
        # {'name': 'name_698', 'email': 'user698@mailinator.com',
        #     'department': 'department_698', 'designation': 'designation_698'},
        # {'name': 'name_699', 'email': 'user699@mailinator.com',
        #     'department': 'department_699', 'designation': 'designation_699'},
        # {'name': 'name_700', 'email': 'user700@mailinator.com',
        #     'department': 'department_700', 'designation': 'designation_700'},
        # {'name': 'name_701', 'email': 'user701@mailinator.com',
        #     'department': 'department_701', 'designation': 'designation_701'},
        # {'name': 'name_702', 'email': 'user702@mailinator.com',
        #     'department': 'department_702', 'designation': 'designation_702'},
        # {'name': 'name_703', 'email': 'user703@mailinator.com',
        #     'department': 'department_703', 'designation': 'designation_703'},
        # {'name': 'name_704', 'email': 'user704@mailinator.com',
        #     'department': 'department_704', 'designation': 'designation_704'},
        # {'name': 'name_705', 'email': 'user705@mailinator.com',
        #     'department': 'department_705', 'designation': 'designation_705'},
        # {'name': 'name_706', 'email': 'user706@mailinator.com',
        #     'department': 'department_706', 'designation': 'designation_706'},
        # {'name': 'name_707', 'email': 'user707@mailinator.com',
        #     'department': 'department_707', 'designation': 'designation_707'},
        # {'name': 'name_708', 'email': 'user708@mailinator.com',
        #     'department': 'department_708', 'designation': 'designation_708'},
        # {'name': 'name_709', 'email': 'user709@mailinator.com',
        #     'department': 'department_709', 'designation': 'designation_709'},
        # {'name': 'name_710', 'email': 'user710@mailinator.com',
        #     'department': 'department_710', 'designation': 'designation_710'},
        # {'name': 'name_711', 'email': 'user711@mailinator.com',
        #     'department': 'department_711', 'designation': 'designation_711'},
        # {'name': 'name_712', 'email': 'user712@mailinator.com',
        #     'department': 'department_712', 'designation': 'designation_712'},
        # {'name': 'name_713', 'email': 'user713@mailinator.com',
        #     'department': 'department_713', 'designation': 'designation_713'},
        # {'name': 'name_714', 'email': 'user714@mailinator.com',
        #     'department': 'department_714', 'designation': 'designation_714'},
        # {'name': 'name_715', 'email': 'user715@mailinator.com',
        #     'department': 'department_715', 'designation': 'designation_715'},
        # {'name': 'name_716', 'email': 'user716@mailinator.com',
        #     'department': 'department_716', 'designation': 'designation_716'},
        # {'name': 'name_717', 'email': 'user717@mailinator.com',
        #     'department': 'department_717', 'designation': 'designation_717'},
        # {'name': 'name_718', 'email': 'user718@mailinator.com',
        #     'department': 'department_718', 'designation': 'designation_718'},
        # {'name': 'name_719', 'email': 'user719@mailinator.com',
        #     'department': 'department_719', 'designation': 'designation_719'},
        # {'name': 'name_720', 'email': 'user720@mailinator.com',
        #     'department': 'department_720', 'designation': 'designation_720'},
        # {'name': 'name_721', 'email': 'user721@mailinator.com',
        #     'department': 'department_721', 'designation': 'designation_721'},
        # {'name': 'name_722', 'email': 'user722@mailinator.com',
        #     'department': 'department_722', 'designation': 'designation_722'},
        # {'name': 'name_723', 'email': 'user723@mailinator.com',
        #     'department': 'department_723', 'designation': 'designation_723'},
        # {'name': 'name_724', 'email': 'user724@mailinator.com',
        #     'department': 'department_724', 'designation': 'designation_724'},
        # {'name': 'name_725', 'email': 'user725@mailinator.com',
        #     'department': 'department_725', 'designation': 'designation_725'},
        # {'name': 'name_726', 'email': 'user726@mailinator.com',
        #     'department': 'department_726', 'designation': 'designation_726'},
        # {'name': 'name_727', 'email': 'user727@mailinator.com',
        #     'department': 'department_727', 'designation': 'designation_727'},
        # {'name': 'name_728', 'email': 'user728@mailinator.com',
        #     'department': 'department_728', 'designation': 'designation_728'},
        # {'name': 'name_729', 'email': 'user729@mailinator.com',
        #     'department': 'department_729', 'designation': 'designation_729'},
        # {'name': 'name_730', 'email': 'user730@mailinator.com',
        #     'department': 'department_730', 'designation': 'designation_730'},
        # {'name': 'name_731', 'email': 'user731@mailinator.com',
        #     'department': 'department_731', 'designation': 'designation_731'},
        # {'name': 'name_732', 'email': 'user732@mailinator.com',
        #     'department': 'department_732', 'designation': 'designation_732'},
        # {'name': 'name_733', 'email': 'user733@mailinator.com',
        #     'department': 'department_733', 'designation': 'designation_733'},
        # {'name': 'name_734', 'email': 'user734@mailinator.com',
        #     'department': 'department_734', 'designation': 'designation_734'},
        # {'name': 'name_735', 'email': 'user735@mailinator.com',
        #     'department': 'department_735', 'designation': 'designation_735'},
        # {'name': 'name_736', 'email': 'user736@mailinator.com',
        #     'department': 'department_736', 'designation': 'designation_736'},
        # {'name': 'name_737', 'email': 'user737@mailinator.com',
        #     'department': 'department_737', 'designation': 'designation_737'},
        # {'name': 'name_738', 'email': 'user738@mailinator.com',
        #     'department': 'department_738', 'designation': 'designation_738'},
        # {'name': 'name_739', 'email': 'user739@mailinator.com',
        #     'department': 'department_739', 'designation': 'designation_739'},
        # {'name': 'name_740', 'email': 'user740@mailinator.com',
        #     'department': 'department_740', 'designation': 'designation_740'},
        # {'name': 'name_741', 'email': 'user741@mailinator.com',
        #     'department': 'department_741', 'designation': 'designation_741'},
        # {'name': 'name_742', 'email': 'user742@mailinator.com',
        #     'department': 'department_742', 'designation': 'designation_742'},
        # {'name': 'name_743', 'email': 'user743@mailinator.com',
        #     'department': 'department_743', 'designation': 'designation_743'},
        # {'name': 'name_744', 'email': 'user744@mailinator.com',
        #     'department': 'department_744', 'designation': 'designation_744'},
        # {'name': 'name_745', 'email': 'user745@mailinator.com',
        #     'department': 'department_745', 'designation': 'designation_745'},
        # {'name': 'name_746', 'email': 'user746@mailinator.com',
        #     'department': 'department_746', 'designation': 'designation_746'},
        # {'name': 'name_747', 'email': 'user747@mailinator.com',
        #     'department': 'department_747', 'designation': 'designation_747'},
        # {'name': 'name_748', 'email': 'user748@mailinator.com',
        #     'department': 'department_748', 'designation': 'designation_748'},
        # {'name': 'name_749', 'email': 'user749@mailinator.com',
        #     'department': 'department_749', 'designation': 'designation_749'},
        # {'name': 'name_750', 'email': 'user750@mailinator.com',
        #     'department': 'department_750', 'designation': 'designation_750'},
        # {'name': 'name_751', 'email': 'user751@mailinator.com',
        #     'department': 'department_751', 'designation': 'designation_751'},
        # {'name': 'name_752', 'email': 'user752@mailinator.com',
        #     'department': 'department_752', 'designation': 'designation_752'},
        # {'name': 'name_753', 'email': 'user753@mailinator.com',
        #     'department': 'department_753', 'designation': 'designation_753'},
        # {'name': 'name_754', 'email': 'user754@mailinator.com',
        #     'department': 'department_754', 'designation': 'designation_754'},
        # {'name': 'name_755', 'email': 'user755@mailinator.com',
        #     'department': 'department_755', 'designation': 'designation_755'},
        # {'name': 'name_756', 'email': 'user756@mailinator.com',
        #     'department': 'department_756', 'designation': 'designation_756'},
        # {'name': 'name_757', 'email': 'user757@mailinator.com',
        #     'department': 'department_757', 'designation': 'designation_757'},
        # {'name': 'name_758', 'email': 'user758@mailinator.com',
        #     'department': 'department_758', 'designation': 'designation_758'},
        # {'name': 'name_759', 'email': 'user759@mailinator.com',
        #     'department': 'department_759', 'designation': 'designation_759'},
        # {'name': 'name_760', 'email': 'user760@mailinator.com',
        #     'department': 'department_760', 'designation': 'designation_760'},
        # {'name': 'name_761', 'email': 'user761@mailinator.com',
        #     'department': 'department_761', 'designation': 'designation_761'},
        # {'name': 'name_762', 'email': 'user762@mailinator.com',
        #     'department': 'department_762', 'designation': 'designation_762'},
        # {'name': 'name_763', 'email': 'user763@mailinator.com',
        #     'department': 'department_763', 'designation': 'designation_763'},
        # {'name': 'name_764', 'email': 'user764@mailinator.com',
        #     'department': 'department_764', 'designation': 'designation_764'},
        # {'name': 'name_765', 'email': 'user765@mailinator.com',
        #     'department': 'department_765', 'designation': 'designation_765'},
        # {'name': 'name_766', 'email': 'user766@mailinator.com',
        #     'department': 'department_766', 'designation': 'designation_766'},
        # {'name': 'name_767', 'email': 'user767@mailinator.com',
        #     'department': 'department_767', 'designation': 'designation_767'},
        # {'name': 'name_768', 'email': 'user768@mailinator.com',
        #     'department': 'department_768', 'designation': 'designation_768'},
        # {'name': 'name_769', 'email': 'user769@mailinator.com',
        #     'department': 'department_769', 'designation': 'designation_769'},
        # {'name': 'name_770', 'email': 'user770@mailinator.com',
        #     'department': 'department_770', 'designation': 'designation_770'},
        # {'name': 'name_771', 'email': 'user771@mailinator.com',
        #     'department': 'department_771', 'designation': 'designation_771'},
        # {'name': 'name_772', 'email': 'user772@mailinator.com',
        #     'department': 'department_772', 'designation': 'designation_772'},
        # {'name': 'name_773', 'email': 'user773@mailinator.com',
        #     'department': 'department_773', 'designation': 'designation_773'},
        # {'name': 'name_774', 'email': 'user774@mailinator.com',
        #     'department': 'department_774', 'designation': 'designation_774'},
        # {'name': 'name_775', 'email': 'user775@mailinator.com',
        #     'department': 'department_775', 'designation': 'designation_775'},
        # {'name': 'name_776', 'email': 'user776@mailinator.com',
        #     'department': 'department_776', 'designation': 'designation_776'},
        # {'name': 'name_777', 'email': 'user777@mailinator.com',
        #     'department': 'department_777', 'designation': 'designation_777'},
        # {'name': 'name_778', 'email': 'user778@mailinator.com',
        #     'department': 'department_778', 'designation': 'designation_778'},
        # {'name': 'name_779', 'email': 'user779@mailinator.com',
        #     'department': 'department_779', 'designation': 'designation_779'},
        # {'name': 'name_780', 'email': 'user780@mailinator.com',
        #     'department': 'department_780', 'designation': 'designation_780'},
        # {'name': 'name_781', 'email': 'user781@mailinator.com',
        #     'department': 'department_781', 'designation': 'designation_781'},
        # {'name': 'name_782', 'email': 'user782@mailinator.com',
        #     'department': 'department_782', 'designation': 'designation_782'},
        # {'name': 'name_783', 'email': 'user783@mailinator.com',
        #     'department': 'department_783', 'designation': 'designation_783'},
        # {'name': 'name_784', 'email': 'user784@mailinator.com',
        #     'department': 'department_784', 'designation': 'designation_784'},
        # {'name': 'name_785', 'email': 'user785@mailinator.com',
        #     'department': 'department_785', 'designation': 'designation_785'},
        # {'name': 'name_786', 'email': 'user786@mailinator.com',
        #     'department': 'department_786', 'designation': 'designation_786'},
        # {'name': 'name_787', 'email': 'user787@mailinator.com',
        #     'department': 'department_787', 'designation': 'designation_787'},
        # {'name': 'name_788', 'email': 'user788@mailinator.com',
        #     'department': 'department_788', 'designation': 'designation_788'},
        # {'name': 'name_789', 'email': 'user789@mailinator.com',
        #     'department': 'department_789', 'designation': 'designation_789'},
        # {'name': 'name_790', 'email': 'user790@mailinator.com',
        #     'department': 'department_790', 'designation': 'designation_790'},
        # {'name': 'name_791', 'email': 'user791@mailinator.com',
        #     'department': 'department_791', 'designation': 'designation_791'},
        # {'name': 'name_792', 'email': 'user792@mailinator.com',
        #     'department': 'department_792', 'designation': 'designation_792'},
        # {'name': 'name_793', 'email': 'user793@mailinator.com',
        #     'department': 'department_793', 'designation': 'designation_793'},
        # {'name': 'name_794', 'email': 'user794@mailinator.com',
        #     'department': 'department_794', 'designation': 'designation_794'},
        # {'name': 'name_795', 'email': 'user795@mailinator.com',
        #     'department': 'department_795', 'designation': 'designation_795'},
        # {'name': 'name_796', 'email': 'user796@mailinator.com',
        #     'department': 'department_796', 'designation': 'designation_796'},
        # {'name': 'name_797', 'email': 'user797@mailinator.com',
        #     'department': 'department_797', 'designation': 'designation_797'},
        # {'name': 'name_798', 'email': 'user798@mailinator.com',
        #     'department': 'department_798', 'designation': 'designation_798'},
        # {'name': 'name_799', 'email': 'user799@mailinator.com',
        #     'department': 'department_799', 'designation': 'designation_799'},
        # {'name': 'name_800', 'email': 'user800@mailinator.com',
        #     'department': 'department_800', 'designation': 'designation_800'},
        # {'name': 'name_801', 'email': 'user801@mailinator.com',
        #     'department': 'department_801', 'designation': 'designation_801'},
        # {'name': 'name_802', 'email': 'user802@mailinator.com',
        #     'department': 'department_802', 'designation': 'designation_802'},
        # {'name': 'name_803', 'email': 'user803@mailinator.com',
        #     'department': 'department_803', 'designation': 'designation_803'},
        # {'name': 'name_804', 'email': 'user804@mailinator.com',
        #     'department': 'department_804', 'designation': 'designation_804'},
        # {'name': 'name_805', 'email': 'user805@mailinator.com',
        #     'department': 'department_805', 'designation': 'designation_805'},
        # {'name': 'name_806', 'email': 'user806@mailinator.com',
        #     'department': 'department_806', 'designation': 'designation_806'},
        # {'name': 'name_807', 'email': 'user807@mailinator.com',
        #     'department': 'department_807', 'designation': 'designation_807'},
        # {'name': 'name_808', 'email': 'user808@mailinator.com',
        #     'department': 'department_808', 'designation': 'designation_808'},
        # {'name': 'name_809', 'email': 'user809@mailinator.com',
        #     'department': 'department_809', 'designation': 'designation_809'},
        # {'name': 'name_810', 'email': 'user810@mailinator.com',
        #     'department': 'department_810', 'designation': 'designation_810'},
        # {'name': 'name_811', 'email': 'user811@mailinator.com',
        #     'department': 'department_811', 'designation': 'designation_811'},
        # {'name': 'name_812', 'email': 'user812@mailinator.com',
        #     'department': 'department_812', 'designation': 'designation_812'},
        # {'name': 'name_813', 'email': 'user813@mailinator.com',
        #     'department': 'department_813', 'designation': 'designation_813'},
        # {'name': 'name_814', 'email': 'user814@mailinator.com',
        #     'department': 'department_814', 'designation': 'designation_814'},
        # {'name': 'name_815', 'email': 'user815@mailinator.com',
        #     'department': 'department_815', 'designation': 'designation_815'},
        # {'name': 'name_816', 'email': 'user816@mailinator.com',
        #     'department': 'department_816', 'designation': 'designation_816'},
        # {'name': 'name_817', 'email': 'user817@mailinator.com',
        #     'department': 'department_817', 'designation': 'designation_817'},
        # {'name': 'name_818', 'email': 'user818@mailinator.com',
        #     'department': 'department_818', 'designation': 'designation_818'},
        # {'name': 'name_819', 'email': 'user819@mailinator.com',
        #     'department': 'department_819', 'designation': 'designation_819'},
        # {'name': 'name_820', 'email': 'user820@mailinator.com',
        #     'department': 'department_820', 'designation': 'designation_820'},
        # {'name': 'name_821', 'email': 'user821@mailinator.com',
        #     'department': 'department_821', 'designation': 'designation_821'},
        # {'name': 'name_822', 'email': 'user822@mailinator.com',
        #     'department': 'department_822', 'designation': 'designation_822'},
        # {'name': 'name_823', 'email': 'user823@mailinator.com',
        #     'department': 'department_823', 'designation': 'designation_823'},
        # {'name': 'name_824', 'email': 'user824@mailinator.com',
        #     'department': 'department_824', 'designation': 'designation_824'},
        # {'name': 'name_825', 'email': 'user825@mailinator.com',
        #     'department': 'department_825', 'designation': 'designation_825'},
        # {'name': 'name_826', 'email': 'user826@mailinator.com',
        #     'department': 'department_826', 'designation': 'designation_826'},
        # {'name': 'name_827', 'email': 'user827@mailinator.com',
        #     'department': 'department_827', 'designation': 'designation_827'},
        # {'name': 'name_828', 'email': 'user828@mailinator.com',
        #     'department': 'department_828', 'designation': 'designation_828'},
        # {'name': 'name_829', 'email': 'user829@mailinator.com',
        #     'department': 'department_829', 'designation': 'designation_829'},
        # {'name': 'name_830', 'email': 'user830@mailinator.com',
        #     'department': 'department_830', 'designation': 'designation_830'},
        # {'name': 'name_831', 'email': 'user831@mailinator.com',
        #     'department': 'department_831', 'designation': 'designation_831'},
        # {'name': 'name_832', 'email': 'user832@mailinator.com',
        #     'department': 'department_832', 'designation': 'designation_832'},
        # {'name': 'name_833', 'email': 'user833@mailinator.com',
        #     'department': 'department_833', 'designation': 'designation_833'},
        # {'name': 'name_834', 'email': 'user834@mailinator.com',
        #     'department': 'department_834', 'designation': 'designation_834'},
        # {'name': 'name_835', 'email': 'user835@mailinator.com',
        #     'department': 'department_835', 'designation': 'designation_835'},
        # {'name': 'name_836', 'email': 'user836@mailinator.com',
        #     'department': 'department_836', 'designation': 'designation_836'},
        # {'name': 'name_837', 'email': 'user837@mailinator.com',
        #     'department': 'department_837', 'designation': 'designation_837'},
        # {'name': 'name_838', 'email': 'user838@mailinator.com',
        #     'department': 'department_838', 'designation': 'designation_838'},
        # {'name': 'name_839', 'email': 'user839@mailinator.com',
        #     'department': 'department_839', 'designation': 'designation_839'},
        # {'name': 'name_840', 'email': 'user840@mailinator.com',
        #     'department': 'department_840', 'designation': 'designation_840'},
        # {'name': 'name_841', 'email': 'user841@mailinator.com',
        #     'department': 'department_841', 'designation': 'designation_841'},
        # {'name': 'name_842', 'email': 'user842@mailinator.com',
        #     'department': 'department_842', 'designation': 'designation_842'},
        # {'name': 'name_843', 'email': 'user843@mailinator.com',
        #     'department': 'department_843', 'designation': 'designation_843'},
        # {'name': 'name_844', 'email': 'user844@mailinator.com',
        #     'department': 'department_844', 'designation': 'designation_844'},
        # {'name': 'name_845', 'email': 'user845@mailinator.com',
        #     'department': 'department_845', 'designation': 'designation_845'},
        # {'name': 'name_846', 'email': 'user846@mailinator.com',
        #     'department': 'department_846', 'designation': 'designation_846'},
        # {'name': 'name_847', 'email': 'user847@mailinator.com',
        #     'department': 'department_847', 'designation': 'designation_847'},
        # {'name': 'name_848', 'email': 'user848@mailinator.com',
        #     'department': 'department_848', 'designation': 'designation_848'},
        # {'name': 'name_849', 'email': 'user849@mailinator.com',
        #     'department': 'department_849', 'designation': 'designation_849'},
        # {'name': 'name_850', 'email': 'user850@mailinator.com',
        #     'department': 'department_850', 'designation': 'designation_850'},
        # {'name': 'name_851', 'email': 'user851@mailinator.com',
        #     'department': 'department_851', 'designation': 'designation_851'},
        # {'name': 'name_852', 'email': 'user852@mailinator.com',
        #     'department': 'department_852', 'designation': 'designation_852'},
        # {'name': 'name_853', 'email': 'user853@mailinator.com',
        #     'department': 'department_853', 'designation': 'designation_853'},
        # {'name': 'name_854', 'email': 'user854@mailinator.com',
        #     'department': 'department_854', 'designation': 'designation_854'},
        # {'name': 'name_855', 'email': 'user855@mailinator.com',
        #     'department': 'department_855', 'designation': 'designation_855'},
        # {'name': 'name_856', 'email': 'user856@mailinator.com',
        #     'department': 'department_856', 'designation': 'designation_856'},
        # {'name': 'name_857', 'email': 'user857@mailinator.com',
        #     'department': 'department_857', 'designation': 'designation_857'},
        # {'name': 'name_858', 'email': 'user858@mailinator.com',
        #     'department': 'department_858', 'designation': 'designation_858'},
        # {'name': 'name_859', 'email': 'user859@mailinator.com',
        #     'department': 'department_859', 'designation': 'designation_859'},
        # {"name": "Anurag Gmail", "email": "akanuragkumar4@gmail.com",
        #     "department": "Leadership", "designation": "CFO"},
        # {'name': 'name_860', 'email': 'user860@mailinator.com',
        #     'department': 'department_860', 'designation': 'designation_860'},
        # {'name': 'name_861', 'email': 'user861@mailinator.com',
        #     'department': 'department_861', 'designation': 'designation_861'},
        # {'name': 'name_862', 'email': 'user862@mailinator.com',
        #     'department': 'department_862', 'designation': 'designation_862'},
        # {'name': 'name_863', 'email': 'user863@mailinator.com',
        #     'department': 'department_863', 'designation': 'designation_863'},
        # {'name': 'name_864', 'email': 'user864@mailinator.com',
        #     'department': 'department_864', 'designation': 'designation_864'},
        # {'name': 'name_865', 'email': 'user865@mailinator.com',
        #     'department': 'department_865', 'designation': 'designation_865'},
        # {'name': 'name_866', 'email': 'user866@mailinator.com',
        #     'department': 'department_866', 'designation': 'designation_866'},
        # {'name': 'name_867', 'email': 'user867@mailinator.com',
        #     'department': 'department_867', 'designation': 'designation_867'},
        # {'name': 'name_868', 'email': 'user868@mailinator.com',
        #     'department': 'department_868', 'designation': 'designation_868'},
        # {'name': 'name_869', 'email': 'user869@mailinator.com',
        #     'department': 'department_869', 'designation': 'designation_869'},
        # {'name': 'name_870', 'email': 'user870@mailinator.com',
        #     'department': 'department_870', 'designation': 'designation_870'},
        # {'name': 'name_871', 'email': 'user871@mailinator.com',
        #     'department': 'department_871', 'designation': 'designation_871'},
        # {'name': 'name_872', 'email': 'user872@mailinator.com',
        #     'department': 'department_872', 'designation': 'designation_872'},
        # {'name': 'name_873', 'email': 'user873@mailinator.com',
        #     'department': 'department_873', 'designation': 'designation_873'},
        # {'name': 'name_874', 'email': 'user874@mailinator.com',
        #     'department': 'department_874', 'designation': 'designation_874'},
        # {'name': 'name_875', 'email': 'user875@mailinator.com',
        #     'department': 'department_875', 'designation': 'designation_875'},
        # {'name': 'name_876', 'email': 'user876@mailinator.com',
        #     'department': 'department_876', 'designation': 'designation_876'},
        # {'name': 'name_877', 'email': 'user877@mailinator.com',
        #     'department': 'department_877', 'designation': 'designation_877'},
        # {'name': 'name_878', 'email': 'user878@mailinator.com',
        #     'department': 'department_878', 'designation': 'designation_878'},
        # {'name': 'name_879', 'email': 'user879@mailinator.com',
        #     'department': 'department_879', 'designation': 'designation_879'},
        # {'name': 'name_880', 'email': 'user880@mailinator.com',
        #     'department': 'department_880', 'designation': 'designation_880'},
        # {'name': 'name_881', 'email': 'user881@mailinator.com',
        #     'department': 'department_881', 'designation': 'designation_881'},
        # {'name': 'name_882', 'email': 'user882@mailinator.com',
        #     'department': 'department_882', 'designation': 'designation_882'},
        # {'name': 'name_883', 'email': 'user883@mailinator.com',
        #     'department': 'department_883', 'designation': 'designation_883'},
        # {'name': 'name_884', 'email': 'user884@mailinator.com',
        #     'department': 'department_884', 'designation': 'designation_884'},
        # {'name': 'name_885', 'email': 'user885@mailinator.com',
        #     'department': 'department_885', 'designation': 'designation_885'}

    ]

    # colleagues = [Colleagues(name=data['name'], email=data['email'],
    #                          designation=data['designation']) for data in colleagues_data]

    for data in colleagues_data:
        existing_colleague = Colleagues.query.filter_by(
            email=data['email']).first()
        if not existing_colleague:
            colleague = Colleagues(
                name=data['name'], email=data['email'], department=data['department'], designation=data['designation'])
            db.session.add(colleague)

    users_data = [
        {"email": "tech@kvqaindia.com",
            "username": "tech@kvqaindia", "password": "asdfgh"}
    ]

    for data in users_data:
        existing_user = User.query.filter_by(email=data['email']).first()
        if not existing_user:
            user = User(email=data['email'], username=data['username'])
            user.set_password(data['password'])
            db.session.add(user)

    db.session.commit()


with app.app_context():
    # create_database()
    db.create_all()
    insert_dummy_data()


class EmailTemplate:
    def __init__(self, template_file):

        with open(template_file, 'r') as file:
            self.template = file.read()

    def generate_email(self, sender_name, sender_email, recipient_name, subject):

        email_content = self.template
        email_content = email_content.replace('{{sender_name}}', sender_name)
        email_content = email_content.replace('{{sender_email}}', sender_email)
        email_content = email_content.replace(
            '{{recipient_name}}', recipient_name)
        email_content = email_content.replace('{{subject}}', subject)

        email_content = email_content.replace('\n', '<br>')
        email_content = email_content.replace('\n\n', '</p><p>')
        email_content = f"<p>{email_content}</p>"

        return email_content


@app.route('/')
def home():
    return 'Hello World'


@app.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     email = data.get('email')
#     username = data.get('username')
#     password = data.get('password')
#     if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
#         return jsonify({'message': 'User with this email or username already exists!'}), 409
#     new_user = User(email=email, username=username)
#     new_user.set_password(password)
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message': 'User registered successfully'}), 201
def register():
    data = request.get_json()

    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not username or not password:
        return jsonify({"message": "All fields are required."}), 400

    # Check if the user already exists
    existing_user = User.query.filter(
        (User.email == email) | (User.username == username)).first()
    if existing_user:
        return jsonify({"message": "User with this email or username already exists."}), 400

    try:
        # Create a new user
        new_user = User(email=email, username=username,
                        password_hash=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error registering user: {str(e)}"}), 500


@app.route('/login', methods=['POST'])
def login():
    credentials = request.json
    username = credentials.get('username')
    password = credentials.get('password')

    user = User.query.filter_by(
        username=username).first()

    if user and user.check_password(password):
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(
            payload, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({"message": "Login Successful", "access_token": token}), 200

    return jsonify({"message": "Invalid username or password"}), 401


@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logged out successfully"}), 200


emailed_candidates = []


# @app.route('/send_email', methods=['GET', 'POST'])
# def send_email():
#     global emailed_candidates
#     emailed_candidates = []

#     templates_dir = os.path.join(os.path.dirname(__file__), 'templates')

#     colleagues = Colleagues.query.all()

#     # part_size = len(colleagues) // 3
#     # group1 = colleagues[:part_size]
#     # group2 = colleagues[part_size:2*part_size]
#     # group3 = colleagues[2*part_size:]

#     part_size = len(colleagues) // 4
#     group1 = colleagues[:part_size]
#     group2 = colleagues[part_size:2*part_size]
#     group3 = colleagues[2*part_size:3*part_size]
#     group4 = colleagues[3*part_size:]

#     department_config = {
#         'HR': {
#             'email': os.getenv('HR_EMAIL'),
#             'password': os.getenv('HR_PASSWORD'),
#             'template': 'hr_email_template.html',
#             'subject': "Update Your Payroll Information for Q4",
#             'action_name': "Update Payroll Information"
#         },
#         'Leadership': {
#             'email': os.getenv('LEADERSHIP_EMAIL'),
#             'password': os.getenv('LEADERSHIP_PASSWORD'),
#             'template': 'leadership_template.html',
#             'subject': "Strategic Plan Review for Q4 - Action Required",
#             'action_name': "Review Strategic Plan"
#         },
#         'Developer': {
#             'email': os.getenv('DEVELOPER_EMAIL'),
#             'password': os.getenv('DEVELOPER_PASSWORD'),
#             'template': 'developer_template.html',
#             'subject': "Security Patch Deployment for Development Tools",
#             'action_name': "Download Security Patch"
#         },

#         'Account': {
#             'email': os.getenv('ACCOUNT_EMAIL'),
#             'password': os.getenv('ACCOUNT_PASSWORD'),
#             'template': 'accounts_email_template.html',
#             'subject': "System Update for new Compliance Standards",
#             'action_name': "Update Credential"
#         }
#     }

#     # send_group_email(group1, department_config['HR'], templates_dir)
#     # send_group_email(group2, department_config['Leadership'], templates_dir)
#     # send_group_email(group3, department_config['Developer'], templates_dir)

#     # return jsonify({'message': 'Phishing emails sent to colleagues.'})

#     try:
#         send_group_email(group1, department_config['HR'], templates_dir)
#         send_group_email(
#             group2, department_config['Leadership'], templates_dir)
#         send_group_email(group3, department_config['Developer'], templates_dir)
#         send_group_email(group4, department_config['Account'], templates_dir)

#         return jsonify({
#             'message': 'Phishing emails sent to colleagues.',
#             'emailed_candidates': emailed_candidates
#         }), 200

#     except Exception as e:
#         return jsonify({'message': f'Error sending emails: {str(e)}'}), 500


# def send_group_email(group, config, templates_dir):
#     """Helper function to send emails to a group with specific department config."""
#     from_email = config['email']
#     password = config['password']
#     email_subject = config['subject']
#     action_name = config['action_name']

#     with open(os.path.join(templates_dir, config['template'])) as f:
#         email_template = f.read()

#     for colleague in group:
#         tracking_link = f"https://ria-app.vercel.app/phishing_test/{colleague.id}"

#         print(f"Generated tracking link for {colleague.name}: {tracking_link}")

#         to_email = colleague.email
#         msg = MIMEMultipart('related')
#         msg['Subject'] = email_subject
#         msg['From'] = from_email
#         msg['To'] = to_email

#         body = email_template.replace("{{recipient_name}}", colleague.name)
#         body = body.replace("{{action_link}}", tracking_link)
#         body = body.replace("{{action_name}}", action_name)
#         body = body.replace("{{email_subject}}", email_subject)

#         html_content = f"""
#         <html>
#             <body>
#                 {body}
#             </body>
#         </html>
#         """
#         msg.attach(MIMEText(html_content, 'html'))

#         try:
#             # with smtplib.SMTP('smtp.gmail.com', 587) as server:
#             #     server.starttls()
#             #     server.login(from_email, password)
#             #     server.send_message(msg)
#             # print(f"Email sent to {colleague.email}")

#             # with smtplib.SMTP_SSL('smtp.secureserver.net', 465) as server:
#             #     server.login(from_email, password)
#             #     server.send_message(msg)
#             # print(f"Email sent to {colleague.email}")

#             with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#                 server.starttls()
#                 server.login(from_email, password)
#                 server.send_message(msg)
#             print(f"Email sent to {colleague.email}")

#             # emailed_candidates.append({
#             #     'name': colleague.name,
#             #     'email': colleague.email,
#             #     'designation': colleague.designation
#             # })
#             update_email_log(colleague)
#             emailed_candidates.append({
#                 'name': colleague.name,
#                 'email': colleague.email,
#                 'designation': colleague.designation
#             })
#             print("Emailed candidates list after sending:", emailed_candidates)

#         except Exception as e:
#             print(f"Failed to send email to {colleague.email}: {str(e)}")

# @app.route('/send_email', methods=['GET', 'POST'])
# def send_email():
#     global emailed_candidates
#     emailed_candidates = []

#     templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
#     colleagues = Colleagues.query.all()

#     part_size = len(colleagues) // 4
#     group1 = colleagues[:part_size]
#     group2 = colleagues[part_size:2*part_size]
#     group3 = colleagues[2*part_size:3*part_size]
#     group4 = colleagues[3*part_size:]

#     department_config = {
#         'HR': {
#             'email': os.getenv('HR_EMAIL'),
#             'password': os.getenv('HR_PASSWORD'),
#             'template': 'hr_email_template.html',
#             'subject': "Update Your Payroll Information for Q4",
#             'action_name': "Update Payroll Information"
#         },
#         'Leadership': {
#             'email': os.getenv('LEADERSHIP_EMAIL'),
#             'password': os.getenv('LEADERSHIP_PASSWORD'),
#             'template': 'leadership_template.html',
#             'subject': "Strategic Plan Review for Q4 - Action Required",
#             'action_name': "Review Strategic Plan"
#         },
#         'Developer': {
#             'email': os.getenv('DEVELOPER_EMAIL'),
#             'password': os.getenv('DEVELOPER_PASSWORD'),
#             'template': 'developer_template.html',
#             'subject': "Security Patch Deployment for Development Tools",
#             'action_name': "Download Security Patch"
#         },
#         'Account': {
#             'email': os.getenv('ACCOUNT_EMAIL'),
#             'password': os.getenv('ACCOUNT_PASSWORD'),
#             'template': 'accounts_email_template.html',
#             'subject': "System Update for new Compliance Standards",
#             'action_name': "Update Credential"
#         }
#     }

#     try:
#         send_group_email(group1, department_config['HR'], templates_dir)
#         send_group_email(
#             group2, department_config['Leadership'], templates_dir)
#         send_group_email(group3, department_config['Developer'], templates_dir)
#         send_group_email(group4, department_config['Account'], templates_dir)

#         return jsonify({
#             'message': 'Emails sent to colleagues.',
#             'emailed_candidates': emailed_candidates
#         }), 200

#     except Exception as e:
#         return jsonify({'message': f'Error sending emails: {str(e)}'}), 500


# def send_group_email(group, config, templates_dir, batch_size=10, delay=10):
#     """Helper function to send emails to a group in small batches."""
#     from_email = config['email']
#     password = config['password']
#     email_subject = config['subject']
#     action_name = config['action_name']

#     with open(os.path.join(templates_dir, config['template'])) as f:
#         email_template = f.read()

#     try:
#         with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#             server.starttls()
#             server.login(from_email, password)

#             for i in range(0, len(group), batch_size):
#                 batch = group[i:i + batch_size]

#                 for colleague in batch:
#                     # tracking_link = f"https://ria-app.vercel.app/phishing_test/{colleague.id}"
#                     tracking_link = f"https://trial-ria-app.vercel.app/phishing_test/{colleague.id}"
#                     to_email = colleague.email
#                     msg = MIMEMultipart('related')
#                     msg['Subject'] = email_subject
#                     msg['From'] = from_email
#                     msg['To'] = to_email

#                     body = email_template.replace(
#                         "{{recipient_name}}", colleague.name)
#                     body = body.replace("{{action_link}}", tracking_link)
#                     body = body.replace("{{action_name}}", action_name)
#                     body = body.replace("{{email_subject}}", email_subject)

#                     html_content = f"""
#                     <html>
#                         <body>
#                             {body}
#                         </body>
#                     </html>
#                     """
#                     msg.attach(MIMEText(html_content, 'html'))

#                     try:
#                         server.send_message(msg)
#                         print(f"Email sent to {colleague.email}")

#                         update_email_log(colleague)
#                         emailed_candidates.append({
#                             'name': colleague.name,
#                             'email': colleague.email,
#                             'designation': colleague.designation
#                         })

#                     except Exception as e:
#                         print(
#                             f"Failed to send email to {colleague.email}: {str(e)}")

#                 # Delay between each batch to manage CPU load
#                 time.sleep(delay)
#                 cpu_usage, memory_usage = log_system_usage()
#                 if memory_usage > 80:  # If memory usage exceeds 80%, trigger garbage collection
#                     print("High memory usage, performing garbage collection.")
#                     gc.collect()

#     except Exception as e:
#         print(f"Error in connecting or sending emails: {str(e)}")


#######

# @app.route('/send_email', methods=['GET', 'POST'])
# def send_email():
#     global emailed_candidates
#     emailed_candidates = []

#     templates_dir = os.path.join(os.path.dirname(__file__), 'templates')

#     # Define group sizes
#     groups = [
#         {'start': 0, 'end': 400, 'config': 'Developer'},
#         {'start': 400, 'end': 788, 'config': 'Developer'},
#         {'start': 788, 'end': 802, 'config': 'Leadership'},
#         {'start': 802, 'end': 986, 'config': 'HR'},
#         {'start': 986, 'end': 1000, 'config': 'Account'}
#     ]

#     department_config = {
#         'HR': {
#             'email': os.getenv('HR_EMAIL'),
#             'password': os.getenv('HR_PASSWORD'),
#             'template': 'hr_email_template.html',
#             'subject': "Update Your Payroll Information for Q4",
#             'action_name': "Update Payroll Information"
#         },
#         'Leadership': {
#             'email': os.getenv('LEADERSHIP_EMAIL'),
#             'password': os.getenv('LEADERSHIP_PASSWORD'),
#             'template': 'leadership_template.html',
#             'subject': "Strategic Plan Review for Q4 - Action Required",
#             'action_name': "Review Strategic Plan"
#         },
#         'Developer': {
#             'email': os.getenv('DEVELOPER_EMAIL'),
#             'password': os.getenv('DEVELOPER_PASSWORD'),
#             'template': 'developer_template.html',
#             'subject': "Security Patch Deployment for Development Tools",
#             'action_name': "Download Security Patch"
#         },
#         'Account': {
#             'email': os.getenv('ACCOUNT_EMAIL'),
#             'password': os.getenv('ACCOUNT_PASSWORD'),
#             'template': 'accounts_email_template.html',
#             'subject': "System Update for new Compliance Standards",
#             'action_name': "Update Credential"
#         }
#     }

#     try:
#         # Process each group separately
#         for group in groups:
#             send_group_email_in_batches(
#                 start_idx=group['start'],
#                 end_idx=group['end'],
#                 config=department_config[group['config']],
#                 templates_dir=templates_dir
#             )

#         return jsonify({
#             'message': 'Emails sent to colleagues.',
#             'emailed_candidates': emailed_candidates
#         }), 200

#     except Exception as e:
#         return jsonify({'message': f'Error sending emails: {str(e)}'}), 500


# def send_group_email_in_batches(start_idx, end_idx, config, templates_dir, batch_size=5, delay=15):
#     """Send emails to a subset of the database in small batches."""
#     from_email = config['email']
#     password = config['password']
#     email_subject = config['subject']
#     action_name = config['action_name']

#     with open(os.path.join(templates_dir, config['template'])) as f:
#         email_template = f.read()

#     try:
#         with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#             server.starttls()
#             server.login(from_email, password)

#             # Load the data in small batches
#             for i in range(start_idx, end_idx, batch_size):
#                 batch = Colleagues.query.filter(
#                     Colleagues.id >= i + 1,
#                     Colleagues.id < i + batch_size + 1
#                 ).all()

#                 if not batch:
#                     break  # Stop if there are no more records

#                 for colleague in batch:
#                     tracking_link = f"https://trial-ria-app.vercel.app/phishing_test/{colleague.id}"
#                     to_email = colleague.email
#                     msg = MIMEMultipart('related')
#                     msg['Subject'] = email_subject
#                     msg['From'] = from_email
#                     msg['To'] = to_email

#                     body = email_template.replace(
#                         "{{recipient_name}}", colleague.name)
#                     body = body.replace("{{action_link}}", tracking_link)
#                     body = body.replace("{{action_name}}", action_name)
#                     body = body.replace("{{email_subject}}", email_subject)

#                     html_content = f"""
#                     <html>
#                         <body>
#                             {body}
#                         </body>
#                     </html>
#                     """
#                     msg.attach(MIMEText(html_content, 'html'))

#                     try:
#                         server.send_message(msg)
#                         print(f"Email sent to {colleague.email}")

#                         update_email_log(colleague)
#                         emailed_candidates.append({
#                             'name': colleague.name,
#                             'email': colleague.email,
#                             'designation': colleague.designation
#                         })

#                     except Exception as e:
#                         print(
#                             f"Failed to send email to {colleague.email}: {str(e)}")

#                 # Delay between each batch to manage CPU load
#                 time.sleep(delay)
#                 cpu_usage, memory_usage = log_system_usage()
#                 if memory_usage > 70:  # If memory usage exceeds 70%, trigger garbage collection
#                     print("High memory usage, performing garbage collection.")
#                     gc.collect()

#     except Exception as e:
#         print(f"Error in connecting or sending emails: {str(e)}")


#######


# groups = [
#     {'start': 0, 'end': 400, 'config': 'Developer'},
#     {'start': 400, 'end': 788, 'config': 'Developer'},
#     {'start': 788, 'end': 802, 'config': 'Leadership'},
#     {'start': 802, 'end': 986, 'config': 'HR'},
#     {'start': 986, 'end': 1000, 'config': 'Account'}
# ]

# department_config = {
#     'HR': {
#         'email': os.getenv('HR_EMAIL'),
#         'password': os.getenv('HR_PASSWORD'),
#         'template': 'hr_email_template.html',
#         'subject': "Update Your Payroll Information for Q4",
#         'action_name': "Update Payroll Information"
#     },
#     'Leadership': {
#         'email': os.getenv('LEADERSHIP_EMAIL'),
#         'password': os.getenv('LEADERSHIP_PASSWORD'),
#         'template': 'leadership_template.html',
#         'subject': "Strategic Plan Review for Q4 - Action Required",
#         'action_name': "Review Strategic Plan"
#     },
#     'Developer': {
#         'email': os.getenv('DEVELOPER_EMAIL'),
#         'password': os.getenv('DEVELOPER_PASSWORD'),
#         'template': 'developer_template.html',
#         'subject': "Security Patch Deployment for Development Tools",
#         'action_name': "Download Security Patch"
#     },
#     'Account': {
#         'email': os.getenv('ACCOUNT_EMAIL'),
#         'password': os.getenv('ACCOUNT_PASSWORD'),
#         'template': 'accounts_email_template.html',
#         'subject': "System Update for new Compliance Standards",
#         'action_name': "Update Credential"
#     }
# }

# templates_dir = os.path.join(os.path.dirname(__file__), 'templates')


# @app.route('/send_email', methods=['GET', 'POST'])
# def send_email():
#     """API to trigger email sending process."""
#     global emailed_candidates
#     emailed_candidates = []  # Reset the emailed candidates log

#     try:
#         # Call the function to send emails group by group
#         send_emails_by_group(groups, department_config, templates_dir)

#         return jsonify({'message': 'Emails are being sent successfully.', 'status': 'success'}), 200

#     except Exception as e:
#         return jsonify({'message': f'Error: {str(e)}', 'status': 'error'}), 500


# def send_emails_by_group(groups, department_config, templates_dir):
#     """Send emails group by group."""
#     global emailed_candidates

#     for group in groups:
#         config = department_config[group['config']]
#         print(f"Processing group: {group['config']}")

#         # Load the template for the group
#         with open(os.path.join(templates_dir, config['template'])) as f:
#             email_template = f.read()

#         send_emails_in_batches(
#             start_idx=group['start'],
#             end_idx=group['end'],
#             config=config,
#             templates_dir=templates_dir,
#             email_template=email_template,
#             batch_size=5,  # 5 emails per batch
#             email_delay=2,  # 2 seconds between emails
#             batch_delay=15  # 15 seconds between batches
#         )

#         # Clean up after finishing a group
#         gc.collect()  # Release memory
#         time.sleep(10)  # 10 seconds delay before the next group


# def send_emails_in_batches(start_idx, end_idx, config, templates_dir, email_template, batch_size, email_delay, batch_delay):
#     """Send emails in smaller batches with delays."""
#     from_email = config['email']
#     password = config['password']
#     email_subject = config['subject']
#     action_name = config['action_name']
#     training_link = "https://trial-ria-app.vercel.app/phishing_test/common_training_link"  # Common link

#     try:
#         with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#             server.starttls()
#             server.login(from_email, password)

#             for i in range(start_idx, end_idx, batch_size):
#                 # Query the batch
#                 batch = Colleagues.query.filter(
#                     Colleagues.id >= i + 1,
#                     Colleagues.id < i + batch_size + 1
#                 ).options(load_only(Colleagues.id, Colleagues.name, Colleagues.email, Colleagues.designation)).all()

#                 if not batch:
#                     break  # Stop if no more records

#                 for colleague in batch:
#                     to_email = colleague.email
#                     msg = MIMEMultipart('related')
#                     msg['Subject'] = email_subject
#                     msg['From'] = from_email
#                     msg['To'] = to_email

#                     # Replace placeholders in the email template
#                     body = email_template.replace(
#                         "{{recipient_name}}", colleague.name)
#                     body = body.replace("{{action_link}}", training_link)
#                     body = body.replace("{{action_name}}", action_name)
#                     body = body.replace("{{email_subject}}", email_subject)

#                     html_content = f"""
#                     <html>
#                         <body>
#                             {body}
#                         </body>
#                     </html>
#                     """
#                     msg.attach(MIMEText(html_content, 'html'))

#                     try:
#                         server.send_message(msg)
#                         print(f"Email sent to {colleague.email}")

#                         # Log email sent
#                         update_email_log(colleague)
#                         emailed_candidates.append({
#                             'name': colleague.name,
#                             'email': colleague.email,
#                             'designation': colleague.designation
#                         })

#                     except Exception as e:
#                         print(
#                             f"Failed to send email to {colleague.email}: {str(e)}")

#                     # Delay between emails
#                     time.sleep(email_delay)

#                 # Clean up after processing a batch
#                 gc.collect()
#                 time.sleep(batch_delay)

#     except Exception as e:
#         print(f"Error in sending emails: {str(e)}")


# New code

groups = [
    {'start': 0, 'end': 400, 'config': 'Developer'},
    {'start': 400, 'end': 788, 'config': 'Developer_1'},
    {'start': 788, 'end': 802, 'config': 'Leadership'},
    {'start': 802, 'end': 986, 'config': 'HR'},
    {'start': 986, 'end': 1001, 'config': 'Account'}
]

# groups = [
#     {'start': 0, 'end': 40, 'config': 'Developer'},
#     # {'start': 400, 'end': 788, 'config': 'Developer'},
#     {'start': 40, 'end': 78, 'config': 'Leadership'},
#     {'start': 78, 'end': 94, 'config': 'HR'},
#     {'start': 94, 'end': 120, 'config': 'Account'}
# ]

department_config = {
    'HR': {
        'email': os.getenv('HR_EMAIL'),
        'password': os.getenv('HR_PASSWORD'),
        'template': 'hr_email_template.html',
        'subject': "Update Your Payroll Information for Q4",
        'action_name': "Update Payroll Information"
    },
    'Leadership': {
        'email': os.getenv('LEADERSHIP_EMAIL'),
        'password': os.getenv('LEADERSHIP_PASSWORD'),
        'template': 'leadership_template.html',
        'subject': "Strategic Plan Review for Q4 - Action Required",
        'action_name': "Review Strategic Plan"
    },
    'Developer': {
        'email': os.getenv('DEVELOPER_EMAIL'),
        'password': os.getenv('DEVELOPER_PASSWORD'),
        'template': 'developer_template.html',
        'subject': "Security Patch Deployment for Development Tools",
        'action_name': "Download Security Patch"
    },
    'Developer_1': {
        'email': os.getenv('DEVELOPER_1_EMAIL'),
        'password': os.getenv('DEVELOPER_1_PASSWORD'),
        'template': 'developer_template.html',
        'subject': "Security Patch Deployment for Development Tools",
        'action_name': "Download Security Patch"
    },
    'Account': {
        'email': os.getenv('ACCOUNT_EMAIL'),
        'password': os.getenv('ACCOUNT_PASSWORD'),
        'template': 'accounts_email_template.html',
        'subject': "System Update for new Compliance Standards",
        'action_name': "Update Credential"
    }
}

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
# common_training_link = "https://trial-ria-app.vercel.app/phishing_test/common_training_link"
# common_training_link = f"https://trial-ria-app.vercel.app/phishing_test/{colleague.id}"


# @app.route('/send_email', methods=['GET', 'POST'])
# def send_email():
#     """API to trigger email sending process."""
#     try:
#         # Process each group
#         for group in groups:
#             config = department_config[group['config']]
#             print(f"Processing group: {group['config']}")

#             # Load the email template once per group
#             with open(os.path.join(templates_dir, config['template'])) as f:
#                 email_template = f.read()

#             # SMTP connection setup
#             with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#                 server.starttls()
#                 server.login(config['email'], config['password'])

#                 # Process emails in batches
#                 for i in range(group['start'], group['end'], 5):  # Batch size = 5
#                     # Query a batch of emails
#                     batch = Colleagues.query.filter(
#                         Colleagues.id >= i + 1,
#                         Colleagues.id < i + 6  # 5 emails per batch
#                     ).with_entities(Colleagues.id, Colleagues.name, Colleagues.email, Colleagues.designation).yield_per(5)

#                     if not batch:
#                         break  # No more records in the group

#                     for colleague in batch:
#                         to_email = colleague.email
#                         msg = MIMEMultipart('related')
#                         msg['Subject'] = config['subject']
#                         msg['From'] = config['email']
#                         msg['To'] = to_email

#                         # Replace placeholders in the email template
#                         body = email_template.replace(
#                             "{{recipient_name}}", colleague.name)
#                         body = body.replace("{{action_link}}", common_training_link)
#                         body = body.replace("{{action_name}}", config['action_name'])
#                         body = body.replace("{{email_subject}}", config['subject'])

#                         html_content = f"""
#                         <html>
#                             <body>
#                                 {body}
#                             </body>
#                         </html>
#                         """
#                         msg.attach(MIMEText(html_content, 'html'))

#                         try:
#                             server.send_message(msg)
#                             print(f"Email sent to {colleague.email}")

#                             # Log email sent (store in database or a file)
#                             update_email_log(colleague)
#                             emailed_candidates.append({
#                                 'name': colleague.name,
#                                 'email': colleague.email,
#                                 'designation': colleague.designation
#                             })

#                         except Exception as e:
#                             print(f"Failed to send email to {colleague.email}: {str(e)}")

#                         # Delay between emails
#                         time.sleep(dynamic_delay())

#                     # Clean up batch from memory
#                     del batch
#                     gc.collect()
#                     time.sleep(15)  # Batch delay

#             # Clean up group from memory
#             del email_template
#             gc.collect()
#             time.sleep(10)  # Group delay

#         return jsonify({'message': 'Emails have been sent successfully.', 'status': 'success'}), 200

#     except Exception as e:
#         return jsonify({'message': f'Error: {str(e)}', 'status': 'error'}), 500


# @app.route('/send_email', methods=['POST'])
# def send_email():
#     try:
#         emails_sent = []  # Keep track of sent emails
#         failed_emails = []  # Track failed emails for debugging

#         # SMTP connection setup
#         with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#             server.starttls()
#             server.login(os.getenv('DEVELOPER_1_EMAIL'), os.getenv('DEVELOPER_1_PASSWORD'))
#               # Adjust based on department

#             # server.login(os.getenv('ACCOUNT_EMAIL'), os.getenv('ACCOUNT_PASSWORD'))

#             # Fetch emails from the database for a specific group
#             for colleague in Colleagues.query.filter(Colleagues.id >= 1, Colleagues.id <= 400):  # Adjust range for each group
#                 to_email = colleague.email
#                 config = department_config['Developer_1']  # Adjust based on group
#                 msg = MIMEMultipart('related')
#                 msg['Subject'] = config['subject']
#                 msg['From'] = config['email']
#                 msg['To'] = to_email

#                 # Prepare the email body
#                 with open(os.path.join('templates', config['template'])) as f:
#                     email_template = f.read()

#                 common_training_link = f"https://trial-ria-app.vercel.app/phishing_test/{colleague.id}"

#                 body = email_template.replace("{{recipient_name}}", colleague.name)
#                 body = body.replace("{{action_link}}", common_training_link)
#                 body = body.replace("{{action_name}}", config['action_name'])
#                 body = body.replace("{{email_subject}}", config['subject'])

#                 html_content = f"<html><body>{body}</body></html>"
#                 msg.attach(MIMEText(html_content, 'html'))

#                 try:
#                     # Send the email
#                     server.send_message(msg)
#                     emails_sent.append(colleague.email)  # Track successful email

#                     # Log the email in the database
#                     update_email_log(colleague)

#                     # Log progress with a print statement (to avoid Gunicorn timeout)
#                     print(f"Email successfully sent to: {colleague.email}")

#                     # Optional: delay to avoid too rapid sending
#                     time.sleep(1)  # Small delay between emails

#                 except Exception as e:
#                     print(f"Failed to send email to {colleague.email}: {str(e)}")
#                     failed_emails.append(colleague.email)  # Track failed email

#         # After processing all emails, print a completion log
#         print(f"All emails processed. Sent: {len(emails_sent)}, Failed: {len(failed_emails)}")

#         return jsonify({
#             'message': 'Emails sent successfully.',
#             'status': 'success',
#             'emails_sent': emails_sent,
#             'failed_emails': failed_emails
#         }), 200

#     except Exception as e:
#         print(f"Error occurred: {str(e)}")
#         return jsonify({'message': f"Error: {str(e)}", 'status': 'error'}), 500

# Send mail code with dynamic group selection

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        emails_sent = []  # Keep track of sent emails
        failed_emails = []  # Track failed emails for debugging

        # SMTP connection setup
        with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
            server.starttls()

            # Iterate through groups and send emails for each group
            for group in groups:
                start, end, department = group['start'], group['end'], group['config']
                config = department_config[department]

                # Log in to the SMTP server with the current department's credentials
                try:
                    server.login(config['email'], config['password'])
                except Exception as e:
                    print(f"Login failed for {config['email']}: {str(e)}")
                    return jsonify({
                        'message': f"SMTP login failed for {config['email']}",
                        'status': 'error',
                        'error': str(e)
                    }), 500

                # Fetch colleagues in the current group
                colleagues = Colleagues.query.filter(
                    Colleagues.id >= start, Colleagues.id < end).all()

                for colleague in colleagues:
                    to_email = colleague.email
                    msg = MIMEMultipart('related')
                    msg['Subject'] = config['subject']
                    msg['From'] = config['email']
                    msg['To'] = to_email

                    # Prepare the email body
                    with open(os.path.join('templates', config['template'])) as f:
                        email_template = f.read()

                    common_training_link = f"https://trial-ria-app-tech2.vercel.app/phishing_test/{colleague.id}"

                    body = email_template.replace(
                        "{{recipient_name}}", colleague.name)
                    body = body.replace(
                        "{{action_link}}", common_training_link)
                    body = body.replace(
                        "{{action_name}}", config['action_name'])
                    body = body.replace("{{email_subject}}", config['subject'])

                    html_content = f"<html><body>{body}</body></html>"
                    msg.attach(MIMEText(html_content, 'html'))

                    try:
                        # Send the email
                        server.send_message(msg)
                        # Track successful email
                        emails_sent.append(colleague.email)

                        # Log the email in the database
                        update_email_log(colleague)

                        # Log progress
                        print(f"Email successfully sent to: {colleague.email}")

                        # Optional: delay to avoid rapid sending
                        time.sleep(1)  # Small delay between emails

                    except Exception as e:
                        print(
                            f"Failed to send email to {colleague.email}: {str(e)}")
                        # Track failed email
                        failed_emails.append(colleague.email)

        # After processing all groups, print a completion log
        print(
            f"All emails processed. Sent: {len(emails_sent)}, Failed: {len(failed_emails)}")

        return jsonify({
            'message': 'Emails sent successfully.',
            'status': 'success',
            'emails_sent': emails_sent,
            'failed_emails': failed_emails
        }), 200

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'message': f"Error: {str(e)}", 'status': 'error'}), 500


def dynamic_delay():
    """Calculate delay based on system resource usage."""
    memory_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent(interval=0.1)
    if memory_usage > 80 or cpu_usage > 80:
        return 15  # Increase delay under high load
    elif memory_usage < 50 and cpu_usage < 50:
        return 10  # Decrease delay under low load
    return 5  # Default delay


# def send_group_email(group, config, templates_dir, batch_size=10, delay=10):
#     from_email = config['email']
#     password = config['password']
#     email_subject = config['subject']
#     action_name = config['action_name']

#     with open(os.path.join(templates_dir, config['template'])) as f:
#         email_template = f.read()

#     with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#         server.starttls()
#         server.login(from_email, password)

#         for i in range(0, len(group), batch_size):
#             batch = group[i:i + batch_size]  # Process emails in batches
#             for colleague in batch:
#                 tracking_link = f"https://ria-app.vercel.app/phishing_test/{colleague.id}"
#                 body = email_template.replace(
#                     "{{recipient_name}}", colleague.name)
#                 body = body.replace("{{action_link}}", tracking_link)
#                 body = body.replace("{{action_name}}", action_name)
#                 body = body.replace("{{email_subject}}", email_subject)

#                 msg = MIMEMultipart('related')
#                 msg['Subject'] = email_subject
#                 msg['From'] = from_email
#                 msg['To'] = colleague.email
#                 msg.attach(MIMEText(body, 'html'))

#                 try:
#                     server.send_message(msg)
#                     print(f"Email sent to {colleague.email}")
#                 except Exception as e:
#                     print(
#                         f"Failed to send email to {colleague.email}: {str(e)}")
#                 finally:
#                     del msg  # Explicitly delete the message object to free memory

#             time.sleep(delay)  # Delay before the next batch

# def log_system_usage():
#     # CPU Usage
#     cpu_usage = psutil.cpu_percent()  # Overall CPU usage as a percentage
#     cpu_count = psutil.cpu_count()  # Total number of CPU cores

#     # Memory Usage
#     memory = psutil.virtual_memory()
#     memory_usage = memory.percent  # Memory usage as a percentage
#     memory_total = memory.total  # Total memory (in bytes)
#     memory_available = memory.available  # Available memory (in bytes)
#     memory_used = memory.used  # Used memory (in bytes)

#     print(f"CPU Usage: {cpu_usage}%")
#     print(f"Number of CPU cores: {cpu_count}")
#     print(f"Memory Usage: {memory_usage}%")
#     print(f"Total Memory: {memory_total / (1024 ** 3):.2f} GB")
#     print(f"Used Memory: {memory_used / (1024 ** 3):.2f} GB")
#     print(f"Available Memory: {memory_available / (1024 ** 3):.2f} GB")

# return cpu_usage, cpu_count, memory_usage, memory_total, memory_used, memory_available

def log_system_usage():
    # CPU Usage
    cpu_usage = psutil.cpu_percent()  # Overall CPU usage as a percentage

    # Memory Usage
    memory = psutil.virtual_memory()
    memory_usage = memory.percent  # Memory usage as a percentage

    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_usage}%")

    return cpu_usage, memory_usage

# Send email function
# def send_group_email(group, config, templates_dir, batch_size=10, delay=10):
#     """Helper function to send emails to a group in small batches."""
#     from_email = config['email']
#     password = config['password']
#     email_subject = config['subject']
#     action_name = config['action_name']

#     # Load the email template from cache or file
#     email_template = cache.get('email_template')
#     if email_template is None:
#         with open(os.path.join(templates_dir, config['template'])) as f:
#             email_template = f.read()
#         cache.set('email_template', email_template)

#     try:
#         # Connect to the SMTP server
#         with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#             server.starttls()
#             server.login(from_email, password)

#             # Process emails in batches
#             for i in range(0, len(group), batch_size):
#                 batch = group[i:i + batch_size]

#                 for colleague in batch:
#                     tracking_link = f"https://ria-app.vercel.app/phishing_test/{colleague.id}"
#                     to_email = colleague.email
#                     msg = MIMEMultipart('related')
#                     msg['Subject'] = email_subject
#                     msg['From'] = from_email
#                     msg['To'] = to_email

#                     # Customize the email body with the colleague's name and tracking link
#                     body = email_template.replace("{{recipient_name}}", colleague.name)
#                     body = body.replace("{{action_link}}", tracking_link)
#                     body = body.replace("{{action_name}}", action_name)
#                     body = body.replace("{{email_subject}}", email_subject)

#                     html_content = f"""
#                     <html>
#                         <body>
#                             {body}
#                         </body>
#                     </html>
#                     """
#                     msg.attach(MIMEText(html_content, 'html'))

#                     try:
#                         server.send_message(msg)
#                         print(f"Email sent to {colleague.email}")

#                         # Log the sent email details
#                         update_email_log(colleague)

#                     except Exception as e:
#                         print(f"Failed to send email to {colleague.email}: {str(e)}")

#                 # Delay between batches to prevent overloading the CPU
#                 time.sleep(delay)

#                 # Log system usage and perform garbage collection
#                 cpu_usage, memory_usage = log_system_usage()
#                 if memory_usage > 80:  # If memory usage exceeds 80%, trigger garbage collection
#                     print("High memory usage, performing garbage collection.")
#                     gc.collect()

#     except Exception as e:
#         print(f"Error in connecting or sending emails: {str(e)}")

# # Email sending route
# @app.route('/send_email', methods=['GET', 'POST'])
# def send_email():
#     global emailed_candidates
#     emailed_candidates = []

#     templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
#     colleagues = Colleagues.query.all()

#     # Define groupings
#     part_size = len(colleagues) // 5
#     group1 = colleagues[:8]
#     group2 = colleagues[8:13]
#     group3 = colleagues[13:18]
#     group4 = colleagues[18:20]
#     group5 = colleagues[20:]

#     # Department configuration
#     department_config = {
#         'HR': {
#             'email': os.getenv('HR_EMAIL'),
#             'password': os.getenv('HR_PASSWORD'),
#             'template': 'hr_email_template.html',
#             'subject': "Update Your Payroll Information for Q4",
#             'action_name': "Update Payroll Information"
#         },
#         'Leadership': {
#             'email': os.getenv('LEADERSHIP_EMAIL'),
#             'password': os.getenv('LEADERSHIP_PASSWORD'),
#             'template': 'leadership_template.html',
#             'subject': "Strategic Plan Review for Q4 - Action Required",
#             'action_name': "Review Strategic Plan"
#         },
#         'Developer': {
#             'email': os.getenv('DEVELOPER_EMAIL'),
#             'password': os.getenv('DEVELOPER_PASSWORD'),
#             'template': 'developer_template.html',
#             'subject': "Security Patch Deployment for Development Tools",
#             'action_name': "Download Security Patch"
#         },

#         'Developer_1': {
#             'email': os.getenv('DEVELOPER_EMAIL_1'),
#             'password': os.getenv('DEVELOPER_PASSWORD_1'),
#             'template': 'developer_template.html',
#             'subject': "Security Patch Deployment for Development Tools",
#             'action_name': "Download Security Patch"
#         },


#         'Account': {
#             'email': os.getenv('ACCOUNT_EMAIL'),
#             'password': os.getenv('ACCOUNT_PASSWORD'),
#             'template': 'accounts_email_template.html',
#             'subject': "System Update for new Compliance Standards",
#             'action_name': "Update Credential"
#         }
#     }

#     try:
#         # Send emails for each group
#         send_group_email(group1, department_config['Developer'], templates_dir)
#         send_group_email(group2, department_config['Developer_1'], templates_dir)
#         send_group_email(group3, department_config['HR'], templates_dir)
#         send_group_email(group4, department_config['Account'], templates_dir)
#         send_group_email(group5, department_config['Leadership'], templates_dir)

#         return jsonify({
#             'message': 'Emails sent to colleagues.',
#             'emailed_candidates': emailed_candidates
#         }), 200

#     except Exception as e:
#         return jsonify({'message': f'Error sending emails: {str(e)}'}), 500


# def send_group_email(group_start, group_end, config, templates_dir, batch_size=10, delay=10):
#     """Helper function to send emails to a group in small batches."""
#     from_email = config['email']
#     password = config['password']
#     email_subject = config['subject']
#     action_name = config['action_name']

#     # Load the email template from cache or file
#     email_template = cache.get('email_template')
#     if email_template is None:
#         with open(os.path.join(templates_dir, config['template'])) as f:
#             email_template = f.read()
#         cache.set('email_template', email_template)

#     try:
#         # Connect to the SMTP server
#         with smtplib.SMTP('smtpout.secureserver.net', 587) as server:
#             server.starttls()
#             server.login(from_email, password)

#             # Query the database for the batch of colleagues
#             session = Session()
#             colleagues = session.query(Colleagues).slice(group_start, group_end).all()

#             # Process emails in batches
#             for i in range(0, len(colleagues), batch_size):
#                 batch = colleagues[i:i + batch_size]

#                 for colleague in batch:
#                     tracking_link = f"https://ria-app.vercel.app/phishing_test/{colleague.id}"
#                     to_email = colleague.email
#                     msg = MIMEMultipart('related')
#                     msg['Subject'] = email_subject
#                     msg['From'] = from_email
#                     msg['To'] = to_email

#                     # Customize the email body with the colleague's name and tracking link
#                     body = email_template.replace("{{recipient_name}}", colleague.name)
#                     body = body.replace("{{action_link}}", tracking_link)
#                     body = body.replace("{{action_name}}", action_name)
#                     body = body.replace("{{email_subject}}", email_subject)

#                     html_content = f"""
#                     <html>
#                         <body>
#                             {body}
#                         </body>
#                     </html>
#                     """
#                     msg.attach(MIMEText(html_content, 'html'))

#                     try:
#                         server.send_message(msg)
#                         print(f"Email sent to {colleague.email}")

#                         # Log the sent email details
#                         update_email_log(colleague)

#                     except Exception as e:
#                         print(f"Failed to send email to {colleague.email}: {str(e)}")

#                 # Delay between batches to prevent overloading the CPU
#                 time.sleep(delay)

#                 # Log system usage and perform garbage collection
#                 cpu_usage, memory_usage = log_system_usage()
#                 if memory_usage > 80:  # If memory usage exceeds 80%, trigger garbage collection
#                     print("High memory usage, performing garbage collection.")
#                     gc.collect()

#     except Exception as e:
#         print(f"Error in connecting or sending emails: {str(e)}")

# # Email sending route
# @app.route('/send_email', methods=['GET', 'POST'])
# def send_email():
#     global emailed_candidates
#     emailed_candidates = []

#     templates_dir = os.path.join(os.path.dirname(__file__), 'templates')

#     # Define the range of colleagues for each group based on your specified ranges
#     group_ranges = [
#         (1, 8),    # Group 1 (First 400 colleagues)
#         (8, 14),  # Group 2 (Next 388 colleagues)
#         (14, 18),  # Group 3 (Next 14 colleagues)
#         (18, 20),  # Group 4 (Next 184 colleagues)
#         (20, 21)  # Group 5 (Remaining 14 colleagues)
#     ]

#     # Department configuration
#     department_config = {
#         'HR': {
#             'email': os.getenv('HR_EMAIL'),
#             'password': os.getenv('HR_PASSWORD'),
#             'template': 'hr_email_template.html',
#             'subject': "Update Your Payroll Information for Q4",
#             'action_name': "Update Payroll Information"
#         },
#         'Leadership': {
#             'email': os.getenv('LEADERSHIP_EMAIL'),
#             'password': os.getenv('LEADERSHIP_PASSWORD'),
#             'template': 'leadership_template.html',
#             'subject': "Strategic Plan Review for Q4 - Action Required",
#             'action_name': "Review Strategic Plan"
#         },
#         'Developer': {
#             'email': os.getenv('DEVELOPER_EMAIL'),
#             'password': os.getenv('DEVELOPER_PASSWORD'),
#             'template': 'developer_template.html',
#             'subject': "Security Patch Deployment for Development Tools",
#             'action_name': "Download Security Patch"
#         },
#         'Account': {
#             'email': os.getenv('ACCOUNT_EMAIL'),
#             'password': os.getenv('ACCOUNT_PASSWORD'),
#             'template': 'accounts_email_template.html',
#             'subject': "System Update for new Compliance Standards",
#             'action_name': "Update Credential"
#         }
#     }

#     try:
#         # Send emails for each group
#         send_group_email(group_ranges[0][0], group_ranges[0][1], department_config['Developer'], templates_dir)
#         send_group_email(group_ranges[1][0], group_ranges[1][1], department_config['Developer'], templates_dir)
#         send_group_email(group_ranges[2][0], group_ranges[2][1], department_config['HR'], templates_dir)
#         send_group_email(group_ranges[3][0], group_ranges[3][1], department_config['Account'], templates_dir)
#         send_group_email(group_ranges[4][0], group_ranges[4][1], department_config['Leadership'], templates_dir)

#         return jsonify({
#             'message': 'Emails sent to colleagues.',
#             'emailed_candidates': emailed_candidates
#         }), 200

#     except Exception as e:
#         return jsonify({'message': f'Error sending emails: {str(e)}'}), 500


# def update_email_log(colleague):
#     """Single function to update the record in the EmailLogs table."""
#     try:
#         # Create a new email log entry
#         email_log = EmailLogs(
#             colleague_id=colleague.id,
#             email_address=colleague.email
#         )
#         db.session.add(email_log)
#         db.session.commit()
#         print(f"Email log added for {colleague.name}")
#     except Exception as e:
#         db.session.rollback()
#         print(f"Failed to log email for {colleague.name}: {str(e)}")


def update_email_log(colleague):
    """Function to update the record in the EmailLogs table."""
    try:
        # Capture the current time for when the email is sent
        sent_date = datetime.utcnow()

        # Create a new email log entry with colleague's details and sent date
        email_log = EmailLogs(
            colleague_id=colleague.id,
            email_address=colleague.email,
            sent_date=sent_date  # Store the sent date
        )

        # Add to session and commit to save it in the database
        db.session.add(email_log)
        db.session.commit()
        print(f"Email log added for {colleague.name}")

    except Exception as e:
        db.session.rollback()
        print(f"Failed to log email for {colleague.name}: {str(e)}")


@app.route('/phishing_test/<int:colleague_id>', methods=['GET'])
def phishing_test(colleague_id):
    print(f'Phishing test accessed for colleague ID: {colleague_id}')

    colleague = Colleagues.query.get(colleague_id)
    if not colleague:
        return jsonify({'error': 'Colleague not found.'}), 404

    return jsonify({'message': 'Tracking link accessed successfully', 'colleague_id': colleague_id})


# @app.route('/generate_emailed_candidates_report', methods=['GET', 'POST'])
# def generate_emailed_candidates_report():
#     global emailed_candidates

#     if not emailed_candidates:
#         print("No candidates in emailed_candidates:",
#               emailed_candidates)
#         return jsonify({'error': 'No successfully emailed candidates.'}), 400

#     print("Generating CSV for:", emailed_candidates)

#     try:
#         csv_file_path = "emailed_candidates_report.csv"
#         with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
#             fieldnames = ['name', 'email', 'department',
#                           'designation', 'clicked_date']
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#             writer.writeheader()
#             writer.writerows(emailed_candidates)

#         return send_file(csv_file_path, as_attachment=True)
#     except Exception as e:
#         print(f"Error generating report: {str(e)}")
#         return jsonify({'error': str(e)}), 500


@app.route('/generate_emailed_candidates_report', methods=['GET'])
def generate_emailed_candidates_report():
    try:
        # Fetch all email logs
        email_logs = EmailLogs.query.all()
        if not email_logs:
            return jsonify({'error': 'No candidates have been emailed yet.'}), 400

        # Prepare list of emailed candidates with additional fields
        emailed_candidates = []
        for log in email_logs:
            colleague = log.colleague  # Get colleague related to the log
            emailed_candidates.append({
                'name': colleague.name,  # Get colleague name
                'email': log.email_address,  # Get email from log
                'department': colleague.department,  # Get department from colleague model
                'designation': colleague.designation,  # Get designation from colleague model
                # Format sent date
                # 'sent_date': log.sent_date.strftime('%Y-%m-%d %H:%M:%S')
                'sent_date': log.sent_date.strftime('%Y-%m-%d')
            })

        # Generate CSV report
        csv_file_path = "emailed_candidates_report.csv"
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'email', 'department',
                          'designation', 'sent_date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(emailed_candidates)

        # Return the CSV file as download
        return send_file(csv_file_path, as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/users')
def users():
    user = Colleagues.query.all()
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email, 'department': u.department, 'designation': u.designation} for u in user])


@app.route('/phising_click/<int:colleague_id>', methods=['POST'])
def phising_click(colleague_id):
    print(f'Received request for colleague ID: {colleague_id}')

    colleague = Colleagues.query.get(colleague_id)
    if not colleague:
        return jsonify({'error': 'Colleague not found.'}), 404

    report = Reports.query.filter_by(colleague_id=colleague_id).first()

    if report:
        report.clicked = True
        report.clicked_date = datetime.now()
        print(
            f"Updated clicked_date for existing report: {report.clicked_date}")

    else:
        report = Reports(
            colleague_id=colleague_id,
            clicked=True,
            clicked_date=datetime.now(),
            answered=False,
            answers={}
        )
        db.session.add(report)
        print(f"Created new report with clicked_date: {report.clicked_date}")

    db.session.commit()

    candidate_data = {
        'id': colleague.id,
        'name': colleague.name,
        'email': colleague.email,
        'department': colleague.department,
        'designation': colleague.designation
    }

    return jsonify({'message': 'Click recorded', 'candidate': candidate_data})


@app.route('/reports', methods=['GET'])
def get_reports():
    reports = Reports.query.all()
    report_data = [{'id': r.id, 'colleague_id': r.colleague_id, 'clicked': r.clicked,
                    'answered': r.answered, 'answers': r.answers, 'status': r.status, 'score': r.score, 'clicked_date': r.clicked_date} for r in reports]
    return jsonify(report_data)


@app.route('/phishing_opened/<int:colleague_id>', methods=['GET'])
def phishing_opened(colleague_id):
    report = Reports.query.filter_by(colleague_id=colleague_id).first()
    print(
        f'Processing click for colleague ID: {colleague_id} | Existing report: {report}')

    if report:
        report.clicked = True
        print(f'Updated existing report for ID {colleague_id} to clicked=True')
    else:
        report = Reports(colleague_id=colleague_id,
                         clicked=True, answered=False, answers={}, clicked_date=datetime.now())
        db.session.add(report)
        print(f'Created new report for ID {colleague_id} with clicked=True')

    db.session.commit()
    return jsonify({'message': 'Thank you for participating in our phishing awareness program.', 'showPopup': True})


@app.route('/generate_reports', methods=['GET', 'POST'])
def generate_reports():
    try:
        reports = Reports.query.all()
        report_data = []

        for report in reports:
            colleague = Colleagues.query.get(report.colleague_id)
            report_entry = {
                'Colleague Name': colleague.name,
                'Colleague Email': colleague.email,
                'Department': colleague.department,
                'Designation': colleague.designation,
                'Link Clicked': 'Yes' if report.clicked else 'No',
                'Score': report.score,
                'Status': report.status,
                'Completion Date': report.clicked_date.strftime('%Y-%m-%d') if report.clicked_date else None,
            }
            report_data.append(report_entry)

        csv_file_path = "candidate_reports.csv"
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Colleague Name', 'Colleague Email', 'Department',
                          'Designation', 'Link Clicked', 'Score',
                          'Status', 'Completion Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for data in report_data:
                writer.writerow(data)

        return send_file(csv_file_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/upload_colleagues_data', methods=['POST'])
def upload_colleagues_data():
    try:
        db.session.query(Colleagues).delete()

        file = request.files['file']
        if file and file.filename.endswith('.xlsx'):
            df = pd.read_excel(file)
            for _, row in df.iterrows():
                colleague = Colleagues(
                    name=row['Full Name'],
                    email=row['Work Email'],
                    department=row['Department'],
                    designation=row['Job Title']
                )
                db.session.add(colleague)

            db.session.commit()
            return jsonify({'message': 'Data uploaded successfully'}), 200
        else:
            return jsonify({'message': 'Invalid file format. Please upload an .xlsx file.'}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error processing file: {str(e)}'}), 500


@app.route('/get_all_reports', methods=['GET'])
def get_all_reports():
    try:
        reports = Reports.query.all()
        report_data = [{'id': r.id, 'colleague_id': r.colleague_id, 'clicked': r.clicked,
                        'answered': r.answered, 'answers': r.answers, 'status': r.status, 'score': r.score, 'clicked_date': r.clicked_date} for r in reports]
        return jsonify({'reports': report_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate_dashboard_clicked_report', methods=['GET'])
def generate_dashboard_clicked_report():
    clicked_reports = Reports.query.filter_by(clicked=True).all()

    if not clicked_reports:
        return jsonify({'error': 'No candidates have clicked the link.'}), 400

    clicked_candidates = []
    for report in clicked_reports:
        colleague = report.colleague
        clicked_candidates.append({
            'name': colleague.name,
            'email': colleague.email,
            'department': colleague.department,
            'designation': colleague.designation,
            'clicked_date': report.clicked_date.strftime('%Y-%m-%d') if report.clicked_date else None
        })

    try:
        csv_file_path = "dashboard_clicked_candidates_report.csv"
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'email', 'department',
                          'designation', 'clicked_date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(clicked_candidates)

        return send_file(csv_file_path, as_attachment=True)

    except Exception as e:
        print(f"Error generating report: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
