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


# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
# app.config['SECRET_KEY'] = "anuragiitmadras"

# DATABASE_URL = 'sqlite:///database.sqlite3'  # Replace with your actual DB URL
# engine = create_engine(DATABASE_URL)
# Session = sessionmaker(bind=engine)

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL')  # Use full URL from Render
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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
        {'name': 'Janhavi Kulkarni', 'email': 'janhavi.kulkarni@riaadvisory.com', 'department': 'Training', 'designation': 'Senior Consultant - Training'},
        {'name': 'Neo Lucena Baquing', 'email': 'neo.baquing@riaadvisory.com', 'department': 'Training', 'designation': 'Project Manager'},
        {'name': 'Ambarish Ashok Vaidya', 'email': 'ambarish.vaidya@riaadvisory.com', 'department': 'Finance', 'designation': 'Director-Finance Controller'},
        {'name': 'Chetan Bhati', 'email': 'chetan.bhati@riaadvisory.com', 'department': 'Finance', 'designation': 'Senior Manager-Finance'},
        {'name': 'Deepali Koli', 'email': 'deepali.koli@riaadvisory.com', 'department': 'Finance', 'designation': 'Senior Account Executive'},
        {'name': 'Gunjan Walia', 'email': 'gunjan.walia@riaadvisory.com', 'department': 'Finance', 'designation': 'Management Trainee'},
        {'name': 'Jana Marek', 'email': 'jana_marek@yahoo.com', 'department': 'Finance', 'designation': 'Contractor'},
        {'name': 'Narendra Gondal', 'email': 'narendra.gondal@riaadvisory.com', 'department': 'Finance', 'designation': 'Associate Consultant'},
        {'name': 'Poonam Ajmire Ashok Ajmire', 'email': 'poonam.ajmire@riaadvisory.com', 'department': 'Finance', 'designation': 'Finance Executive'},    
        {'name': 'Prakhar Lodha', 'email': 'prakhar.lodha@riaadvisory.com', 'department': 'Finance', 'designation': 'Finance Manager'},
        {'name': 'Richa Bhatia', 'email': 'richa.bhatia@riaadvisory.com', 'department': 'Finance', 'designation': 'Senior Manager-Finance'},
        {'name': 'Samapti Shah', 'email': 'samapti.shah@riaadvisory.com', 'department': 'Finance', 'designation': 'Accounts Head'},
        {'name': 'Santosh Gangadhar Inde', 'email': 'santosh.inde@riaadvisory.com', 'department': 'Finance', 'designation': 'Principal Consultant'},      
        {'name': 'Tanisha Singh', 'email': 'tanisha.singh@riaadvisory.com', 'department': 'Finance', 'designation': 'Management Trainee'},
        {'name': 'Vaibhav Suresh Joshi', 'email': 'vaibhav.joshi@riaadvisory.com', 'department': 'Finance', 'designation': 'Manager - Finance'},
        {'name': 'Vilma Silvederio', 'email': 'vilma.silvederio@riaadvisory.com', 'department': 'Finance', 'designation': 'Contractor'},
        {'name': 'Vinay Subhash Kale', 'email': 'vinay.kale@riaadvisory.com', 'department': 'Finance', 'designation': 'Assistant Manager-Finance'},       
        {'name': 'Aaron D Lewicki', 'email': 'aaron.lewicki@tmgconsulting.com', 'department': 'OCM', 'designation': 'Manager'},
        {'name': 'Aaron Stuart Mcclune', 'email': 'aaron.mcclune@tmgconsulting.com', 'department': 'PMO', 'designation': 'Project Manager'},
        {'name': 'Abhay Anil More', 'email': 'abhay.more@tmgconsulting.com', 'department': 'Risk', 'designation': 'Developer'},
        {'name': 'Aditi Singh', 'email': 'aditi.singh@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Aejaz Ahmed', 'email': 'aejaz.ahmed@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Akhila Japa', 'email': 'akhila.japa@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Akriti Dubey', 'email': 'akriti.dubey@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Al Sheil', 'email': 'al.sheil@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Alexander T Obrien', 'email': 'alec.obrien@tmgconsulting.com', 'department': 'Advisory Services', 'designation': 'Vice President'},     
        {'name': 'Edward Alexander Broussard Iv', 'email': 'alex.broussard@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Senior Functional Consultant'},
        {'name': 'Alexandra Damaskina', 'email': 'alexandra.damaskina@tmgconsulting.com', 'department': 'PMO', 'designation': 'Senior Project Manager'},  
        {'name': 'Allen Wesley Greer', 'email': 'allen.greer@tmgconsulting.com', 'department': 'Conversion Services', 'designation': 'Conversion Architect'},
        {'name': 'Amanda Claire Baak', 'email': 'amanda.baak@tmgconsulting.com', 'department': 'Sales & Marketing', 'designation': 'Vice President'},     
        {'name': 'Amy N Ford', 'email': 'amy.ford@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Consultant'},
        {'name': 'Anand Sathyamurthy', 'email': 'anand.sathamurthy@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Andreas Stephan Moeller', 'email': 'andreas.moeller@tmgconsulting.com', 'department': 'Conversion Services', 'designation': 'Conversion Architect'},
        {'name': 'Andrew John Repko', 'email': 'andrew.repko@tmgconsulting.com', 'department': 'Advisory Services', 'designation': 'Senior Consultant'},  
        {'name': 'Andries Frederik Brand', 'email': 'andries.brand@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Director'},     
        {'name': 'Angeline Baquirin Angcanan', 'email': 'angeline.angcanan@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Senior Manager'},
        {'name': 'Ankush Reddy', 'email': 'ankush.reddy@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Anwar Howard', 'email': 'anwar.howard@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Arthur Maldonado', 'email': 'arthur.maldonado@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Ashfaq Moghal', 'email': 'ashfaq.moghal@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Beatrice Kiarie', 'email': 'beatrice.kiarie@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Beverly Marquez', 'email': 'beverly.marquez@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Architect'},
        {'name': 'William O Fenstermaker', 'email': 'bill.fenstermaker@tmgconsulting.com', 'department': 'Sales & Marketing', 'designation': 'Vice President'},
        {'name': 'Billy Almond', 'email': 'billy.almond@tmgconsulting.com', 'department': 'Technical Services', 'designation': 'It Secuirty Manager Of Technical Services'},
        {'name': 'Roberto Santos Organista', 'email': 'bobot.organista@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Solution Architect'},
        {'name': 'Brian Jonson', 'email': 'brian.johnson@tmgconsulting.com', 'department': 'Technical Services', 'designation': 'Senior Architect'},      
        {'name': 'Brooks Yates', 'email': 'brooks.yates@tmgconsulting.com', 'department': 'Technical Services', 'designation': 'Vice President - Technical Services, Ciso, Cto'},
        {'name': 'Cara Lynn Tritt', 'email': 'cara.tritt@tmgconsulting.com', 'department': 'AMI', 'designation': 'Senior Manager'},
        {'name': 'Chanakya Pola', 'email': 'chanakya.pola@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Chanakya Pola-Info', 'email': 'chanakya.x.pola@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Christopher R Goodloe', 'email': 'chris.goodloe@tmgconsulting.com', 'department': 'OCM', 'designation': 'Director'},
        {'name': 'Christopher C Montoya', 'email': 'chris.montoya@tmgconsulting.com', 'department': 'PMO', 'designation': 'Vice President'},
        {'name': 'Colin Bletcher', 'email': 'colin.bletcher@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Courtney Chrisman Graham', 'email': 'courtney.graham@tmgconsulting.com', 'department': 'PMO', 'designation': 'Consultant'},
        {'name': 'Cristina Marie Sillorequez Mabandos', 'email': 'cristina.mabandos@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Solution Architect'},
        {'name': 'Daniel Nguyen', 'email': 'daniel.nguyen@tmgconsulting.com', 'department': 'PMO', 'designation': 'Project Manager'},
        {'name': 'Dante Perez Magtoto', 'email': 'dante.magtoto@tmgconsulting.com', 'department': 'PMO', 'designation': 'Senior Director'},
        {'name': 'Deborah Gail Montgomery', 'email': 'debbie.montgomery@tmgconsulting.com', 'department': 'PMO', 'designation': 'Senior Consultant'},     
        {'name': 'Debra Ardoline', 'email': 'debra.ardoline@tmgconsulting.com', 'department': 'Advisory Services', 'designation': 'Vice President'},      
        {'name': 'Deepika Bommena', 'email': 'deepika.bommena@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Dilip Chavan', 'email': 'dilip.chavan@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Edward Chipeta', 'email': 'edward.chipeta@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Emma Daigle', 'email': 'emma.daigle@tmgconsulting.com', 'department': 'Sales & Marketing', 'designation': 'Contractor'},
        {'name': 'Ericia Kathleen Caras', 'email': 'ericia.caras@tmgconsulting.com', 'department': 'HR', 'designation': 'Resource Manager'},
        {'name': 'Erik Mallia Best Jr', 'email': 'erik.best@tmgconsulting.com', 'department': 'Technical Services', 'designation': 'Technical Architect'},
        {'name': 'Franco Antonio Reyes Roig', 'email': 'franco.roig@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Senior Functional Consultant'},
        {'name': 'Gregory E Galluzzi', 'email': 'greg.galluzzi@tmgconsulting.com', 'department': 'Advisory Services', 'designation': 'Senior Vice President'},
        {'name': 'Hannah Hartwell', 'email': 'hannah.hartwell@tmgconsulting.com', 'department': 'OCM', 'designation': 'Principal Consultant'},
        {'name': 'Hedilyn Pasco Ago', 'email': 'hedi.ago@tmgconsulting.com', 'department': 'Advisory Services', 'designation': 'Senior Director'},        
        {'name': 'Helena Arroyo', 'email': 'helena.arroyo@tmgconsulting.com', 'department': 'Testing', 'designation': 'Senior Consulting Advisor'},       
        {'name': 'Henry Kinler', 'email': 'henry.kinler@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Irina Narovsky', 'email': 'irina.narovsky@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Architect'},
        {'name': 'Jaikar Chodavarapu', 'email': 'jaikar.chodavarapu@tmgconsulting.com', 'department': 'Conversion Services', 'designation': 'Consultant'},
        {'name': 'Jakob Michael Clark', 'email': 'jakob.clark@tmgconsulting.com', 'department': 'Advisory Services', 'designation': 'Consultant'},        
        {'name': 'Jam Dionisio', 'email': 'jam.dionisio@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'James Darron Koenig', 'email': 'james.koenig@tmgconsulting.com', 'department': 'AMI', 'designation': 'Senior Consultant'},
        {'name': 'Janmejay Singh', 'email': 'janmejay.singh@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Jason Imran Ali', 'email': 'jason.ali@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Senior Functional Consultant'},
        {'name': 'Jason Dale Parks', 'email': 'jason.parks@tmgconsulting.com', 'department': 'Conversion Services', 'designation': 'Director'},
        {'name': 'Jayakar Akarapu', 'email': 'jayakar.akarapu@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Jillian LaPorta', 'email': 'jillian.laporta@tmgconsulting.com', 'department': 'Sales & Marketing', 'designation': 'Contractor'},        
        {'name': 'Jonathan Russell Chevalier', 'email': 'jon.chevalier@tmgconsulting.com', 'department': 'Risk', 'designation': 'Sr.Director'},
        {'name': 'Jonathan Jay Jaffin', 'email': 'jon.jaffin@tmgconsulting.com', 'department': 'Technical Services', 'designation': 'Director'},
        {'name': 'Jonah Nathaniel Hepting', 'email': 'jonah.hepting@tmgconsulting.com', 'department': 'Sales & Marketing', 'designation': 'Manager'},     
        {'name': 'Jonathan Hassell', 'email': 'jonathan.hassell@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Jose Villalobos', 'email': 'jose.villalobos@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Juan Enriquez', 'email': 'juan.enriquez@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Justin Brooks Jones', 'email': 'justin.jones@tmgconsulting.com', 'department': 'Conversion Services', 'designation': 'Conversion Architect'},
        {'name': 'Katherine Joven Ceresia', 'email': 'kate.ceresia@tmgconsulting.com', 'department': 'PMO', 'designation': 'Project Manager'},
        {'name': 'Katz Lim', 'email': 'kathlenn.lim@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Kenric Neil Maness', 'email': 'ken.maness@tmgconsulting.com', 'department': 'Sales & Marketing', 'designation': 'Vice President'},      
        {'name': 'Kendal Major', 'email': 'kendal.major@tmgconsulting.com', 'department': 'OCM', 'designation': 'Consultant'},
        {'name': 'Ketan Amin', 'email': 'ketan.amin@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Kimberly Dianne Nguyen - Arbogast', 'email': 'kim.arbogast@tmgconsulting.com', 'department': 'PMO', 'designation': 'Project Manager'},  
        {'name': 'Kisha Gresham', 'email': 'kisha.gresham@tmgconsulting.com', 'department': 'Sales & Marketing', 'designation': 'Contractor'},
        {'name': 'Koteswara Nalabothu', 'email': 'koteswara.rao@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Kundan Chaturvedi', 'email': 'kundan.chaturvedi@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Lakshmi Ravindran', 'email': 'lakshmi.ravindran@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Linda Gao', 'email': 'linda.gao@tmgconsulting.com', 'department': 'Risk', 'designation': 'Senior Consultant'},
        {'name': 'Lynette Murray', 'email': 'lynette.murray@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Mario M Bauer', 'email': 'mario.bauer@tmgconsulting.com', 'department': 'Leadership', 'designation': 'Chief Executive Officer'},        
        {'name': 'Mart Gil Retumban Abareta', 'email': 'mart.gil.abareta@tmgconsulting.com', 'department': 'Account Management', 'designation': 'Senior Functional Consultant'},
        {'name': 'Matthew James Glanvill', 'email': 'matthew.glanvill@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Consultant'},
        {'name': 'Max Almond', 'email': 'max.almond@tmgconsulting.com', 'department': 'Risk', 'designation': 'Risk Advisor'},
        {'name': 'May Christine Arellano Mistiola', 'email': 'may.mistiola@tmgconsulting.com', 'department': 'Testing', 'designation': 'Consultant'},     
        {'name': 'Melanie Tran', 'email': 'melanie.tran@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Consultant'},
        {'name': 'Melvin Manalastas', 'email': 'melvin.manalastas@tmgconsulting.com', 'department': 'PMO', 'designation': 'Architectural Team Manager'},
        {'name': 'Michelle Lynn Boggie', 'email': 'michelle.boggie@tmgconsulting.com', 'department': 'Advisory Services', 'designation': 'Vice President'},
        {'name': 'Michelle Zhang', 'email': 'michelle.zhang@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Principal Consultant'},
        {'name': 'Mohan Madhavarapu', 'email': 'mohan.madhavarapu@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Murray Scheibe', 'email': 'murray.scheibe@tmgconsulting.com', 'department': 'PMO', 'designation': 'Senior Consultant'},
        {'name': 'Ngoc Nhu Nguyen', 'email': 'ngoc.nguyen@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Consultant'},
        {'name': 'Niaz Fairooz', 'email': 'niaz.fairooz@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Nicholas Roland Noble', 'email': 'nick.noble@tmgconsulting.com', 'department': 'Risk', 'designation': 'Director'},
        {'name': "Nicole Rene' Scott", 'email': 'nicole.scott@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Solution Architect'},
        {'name': 'Nirdesh Mittal', 'email': 'nirdesh.mittal@tmgconsulting.com', 'department': 'Advisory Services', 'designation': 'Director'},
        {'name': 'Aletha Pamela Glanvill', 'email': 'pam.glanvill@tmgconsulting.com', 'department': 'Leadership', 'designation': 'President & Evp'},      
        {'name': 'Patrick Shelton', 'email': 'patrick.shelton@tmgconsulting.com', 'department': 'PMO', 'designation': 'Project Manager'},
        {'name': 'Pavan Maridi', 'email': 'pavan.maridi@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Peter Doyon', 'email': 'pete.doyon@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Phillip Wiley Mccarty', 'email': 'phil.mccarty@tmgconsulting.com', 'department': 'Conversion Services', 'designation': 'Technical Architect'},
        {'name': 'Prabhat Shukla', 'email': 'prabhat.shukla@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Prabhu Murugesan', 'email': 'prabhu.murugesan@tmgconsulting.com', 'department': 'Technical Services', 'designation': 'Senior Technical Architect'},
        {'name': 'Prakash Peram', 'email': 'prakash.peram@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Senior Consultant'},     
        {'name': 'Prashant Kumar', 'email': 'prashant.kumar@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Praveen Perala', 'email': 'praveen.perala@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Priyanka Singh', 'email': 'priyanka.singh@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Radha Sangu', 'email': 'radha.sangu@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Rahul Chavan', 'email': 'rahul.chavan@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Rahul Maurya', 'email': 'rahul.maurya@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Rajesh Reddy', 'email': 'rajesh.reddy@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Ralph Lousteau', 'email': 'ralph.lousteau@tmgconsulting.com', 'department': 'Advisory Services', 'designation': 'Vice President'},      
        {'name': 'Ram Adusumalli', 'email': 'ram.adusumalli@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Ritesh Kumar', 'email': 'ritesh.kumar@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Robert Black Hunter', 'email': 'robert.hunter@tmgconsulting.com', 'department': 'Account Management', 'designation': 'Vice President'}, 
        {'name': 'Robert Rodney Thomas', 'email': 'robert.thomas@tmgconsulting.com', 'department': 'Account Management', 'designation': 'Vice President'},
        {'name': 'Robin Jeanne Souder', 'email': 'robin.souder@tmgconsulting.com', 'department': 'PMO', 'designation': 'Senior Consultant'},
        {'name': 'Rohan Kalyanshetty', 'email': 'rohan.kalyanshetty@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Computer System Analyst'},
        {'name': 'Roopesh Rekhawar', 'email': 'roopesh.rekhawar@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Senior Consultant'},
        {'name': 'Sai Polampalli', 'email': 'sai.polampalli@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Sai Vallurupalli', 'email': 'sai.vallurupalli@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Saman Saatsaz', 'email': 'saman.saatsaz@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Senior Manager'},        
        {'name': 'Sandeep Dhanajkar', 'email': 'sandeep.dhanajkar@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Sara Ann Mckirryher', 'email': 'sara.mckirryher@tmgconsulting.com', 'department': 'Testing', 'designation': 'Senior Consultant'},       
        {'name': 'Satish Kalia', 'email': 'satish.kalia@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Scott Mandeh', 'email': 'scott.mandeh@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Solution Architect'},      
        {'name': 'Scott Smeaton', 'email': 'scott.smeaton@tmgconsulting.com', 'department': 'Advisory Services', 'designation': 'Senior Consultant'},     
        {'name': 'Scott Phillip Smith', 'email': 'scott.smith@tmgconsulting.com', 'department': 'Account Management', 'designation': 'Senior Consultant'},
        {'name': 'Shannon Maurice Laney', 'email': 'shannon.laney@tmgconsulting.com', 'department': 'PMO', 'designation': 'Director'},
        {'name': 'Shannon Hale Myers', 'email': 'shannon.myers@tmgconsulting.com', 'department': 'OCM', 'designation': 'Senior Consultant'},
        {'name': 'Brittain Shea Murray', 'email': 'shea.murray@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Functional Architect'},
        {'name': 'Shravan Thammali', 'email': 'shravan.thammali@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Sima Anad', 'email': 'seema.anand@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Soujanya Katta', 'email': 'soujanya.katta@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Stan McHann', 'email': 'stan.mchann@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Stephanie Zhuang', 'email': 'stephanie.zhuang@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Steven Obosnenko', 'email': 'steve.obosnenko@tmgconsulting.com', 'department': 'Sales & Marketing', 'designation': 'Senior Client Relationship Executive'},
        {'name': 'Steven Banks', 'email': 'steven.banks@tmgconsulting.com', 'department': 'Testing', 'designation': 'Manager'},
        {'name': 'Suchendra Kumar', 'email': 'suchendra.kumar@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Sudeep Kumar Kappadan', 'email': 'sudeep.kappadan@tmgconsulting.com', 'department': 'Advisory Services', 'designation': 'Executive Vice President'},
        {'name': 'Tammy Fenstermaker', 'email': 'tammy.fenstermaker@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Tejswi Nerella', 'email': 'tejaswi.prakash@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Todd Reid Hagen', 'email': 'todd.hagen@tmgconsulting.com', 'department': 'Sales & Marketing', 'designation': 'Director'},
        {'name': 'Todd Walter Stocker', 'email': 'todd.stocker@tmgconsulting.com', 'department': 'AMI', 'designation': 'Vice President'},
        {'name': 'Antonio Bernard Redmond', 'email': 'tony.redmond@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Senior Functional Consultant'},
        {'name': 'Tristan J West', 'email': 'tristan.west@tmgconsulting.com', 'department': 'Advisory Services', 'designation': 'Senior Director'},       
        {'name': 'Tuan Duc Tran', 'email': 'tuan.tran@tmgconsulting.com', 'department': 'Solution Delivery', 'designation': 'Senior Manager'},
        {'name': 'Vianney Prudencio', 'email': 'vianney.prudencio@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Velimira Jordanova', 'email': 'villi.jordanova@tmgconsulting.com', 'department': 'Testing', 'designation': 'Director'},
        {'name': 'Vinay Kumar', 'email': 'vinay.kumar@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Vinayak Gadgil', 'email': 'vinayak.gadgil@tmgconsulting.com', 'department': 'Delivery', 'designation': 'Contractor'},
        {'name': 'Yogesh Dhaybar', 'email': 'yogesh.dhaybar@tmgconsulting.com', 'department': 'Account Management', 'designation': 'Senior Functional Consultant'},
        {'name': 'Noreen Jensen', 'email': 'noreen.jensen@riaadvisory.com', 'department': 'Advisory Services', 'designation': 'Vice President'},
        {'name': 'Abhishek Surwade', 'email': 'abhishek.surwade@riaadvisory.com', 'department': 'HR', 'designation': 'Senior Technical Recruiter'},       
        {'name': 'Abigail Aquino Atienza', 'email': 'abigail.atienza@riaadvisory.com', 'department': 'HR', 'designation': 'Senior HR Consultant'},        
        {'name': 'Ankita Garg', 'email': 'ankita.garg@riaadvisory.com', 'department': 'HR', 'designation': 'Senior HR Consultant'},
        {'name': 'Apurva Suryakant Gutte', 'email': 'apurva.gutte@riaadvisory.com', 'department': 'HR', 'designation': 'HR Consultant'},
        {'name': 'Gabriela Fernandez', 'email': 'gabriela.fernandez@riaadvisory.com', 'department': 'HR', 'designation': 'Administrative Assistant'},     
        {'name': 'Gayatri Kaustubh Tamhane', 'email': 'gayatri.tamhane@riaadvisory.com', 'department': 'HR', 'designation': 'Technical Recruiter'},       
        {'name': 'Gianna Emilyn Earnshaw Real', 'email': 'gianna.real@riaadvisory.com', 'department': 'HR', 'designation': 'HR Associate Manager'},       
        {'name': 'Ivon Jasmin Chahal', 'email': 'ivon.chahal@riaadvisory.com', 'department': 'HR', 'designation': 'Executive Assistant'},
        {'name': 'Jusef Cielo Mangalindan', 'email': 'jusef.mangalindan@riaadvisory.com', 'department': 'HR', 'designation': 'Human Resources Manager'},
        {'name': 'Ketaki Devdatt Godbole', 'email': 'ketaki.godbole@riaadvisory.com', 'department': 'HR', 'designation': 'Senior Technical Recruiter'},   
        {'name': 'Linson Mathew Michael', 'email': 'linson.mathew@riaadvisory.com', 'department': 'HR', 'designation': 'Director - Talent Acquisition'},  
        {'name': 'Renuka Ritesh Bhanushali', 'email': 'renuka.bhanushali@riaadvisory.com', 'department': 'HR', 'designation': 'HR Manager'},
        {'name': 'Rishita Sourabh Bane', 'email': 'rishita.bane@riaadvisory.com', 'department': 'HR', 'designation': 'Senior Technical Recruiter'},       
        {'name': 'Sailee Kamat', 'email': 'sailee.kamat@riaadvisory.com', 'department': 'HR', 'designation': 'Associate Technical Recruiter'},
        {'name': 'Shivani Chavan', 'email': 'shivani.randive@riaadvisory.com', 'department': 'HR', 'designation': 'Consultant'},
        {'name': 'Vishwa Vijay Deshpande', 'email': 'vishwa.deshpande@riaadvisory.com', 'department': 'HR', 'designation': 'Associate Consultant - HR'},  
        {'name': 'Wilson Santelices Co', 'email': 'wilson.co@riaadvisory.com', 'department': 'HR', 'designation': 'Associate Consultant - HR'},
        {'name': 'Shrutarshi Saha', 'email': 'shrutarshi.saha@riaadvisory.com', 'department': 'IT Infra', 'designation': 'Software Consultant'},
        {'name': 'Anudeep Navaratnakumar', 'email': 'anudeep.navaratnakumar@riaadvisory.com', 'department': 'IT Infra', 'designation': 'Principal Consultant'},
        {'name': 'Shiva Vinugunta', 'email': 'shiva.vinugunta@riaadvisory.com', 'department': 'IT Infra', 'designation': 'Consultant'},
        {'name': 'Pradipkumar Parsotam Kothadiya', 'email': 'pradipkumar.kothadiya@riaadvisory.com', 'department': 'IT Infra', 'designation': 'Senior Principal Consultant'},
        {'name': 'Sharvari Kumbhar', 'email': 'sharvari.kumbhar@riaadvisory.com', 'department': 'IT Infra', 'designation': 'Consultant'},
        {'name': 'Sachin Narendra Naiksatam', 'email': 'sachin.naiksatam@riaadvisory.com', 'department': 'IT Helpdesk', 'designation': 'Consulting Director'},
        {'name': 'Soham Prafulladatta Kulkarni', 'email': 'soham.kulkarni@riaadvisory.com', 'department': 'IT Infra', 'designation': 'Consultant'},       
        {'name': 'Monika Munot', 'email': 'monika.munot@riaadvisory.com', 'department': 'IT Infra', 'designation': 'Senior Consultant'},
        {'name': 'Suraj Kamble', 'email': 'suraj.kambale@riaadvisory.com', 'department': 'IT Helpdesk', 'designation': 'Consultant'},
        {'name': 'Marwin Ducusin Ibañez', 'email': 'marwin.ibanez@riaadvisory.com', 'department': 'IT Infra', 'designation': 'System Administrator'},     
        {'name': 'Hesusito Jr. Oclares Pineda', 'email': 'hesusito.pineda@riaadvisory.com', 'department': 'IT Helpdesk', 'designation': 'IT Support Specialist'},
        {'name': 'Nicholas Brandon Knight', 'email': 'nick.knight@riaadvisory.com', 'department': 'IT Infra', 'designation': 'Senior Consultant'},        
        {'name': 'Raul Garay', 'email': 'raul.garay@riaadvisory.com', 'department': 'IT Infra', 'designation': 'Consultant'},
        {'name': 'Zaheer Goolam Mahomed', 'email': 'zaheer.mahomed@riaadvisory.com', 'department': 'IT Infra', 'designation': 'Consultant'},
        {'name': 'Tejas Bhagvatprasad Babu', 'email': 'tejas.babu@riaadvisory.com', 'department': 'IT Infra', 'designation': 'Senior Project Manager'},   
        {'name': 'Saravana Jagadeesan', 'email': 'saravanakumar.jagadeesan@riaadvisory.com', 'department': 'IT Infra', 'designation': 'Consulting Technical Director'},
        {'name': 'Abira Bhowmick', 'email': 'abira.bhowmick@riaadvisory.com', 'department': 'Sales & Marketing', 'designation': 'Principal Consultant'},  
        {'name': 'Benicio Suarez', 'email': 'benicio.suarez@riaadvisory.com', 'department': 'Sales & Marketing', 'designation': 'Managing Director'},     
        {'name': 'Bhavik Kakkar', 'email': 'bhavik.kakkar@riaadvisory.com', 'department': 'Sales & Marketing', 'designation': 'Business Analyst'},        
        {'name': 'Clera Anthony Varghese', 'email': 'clera.varghese@riaadvisory.com', 'department': 'Sales & Marketing', 'designation': 'Senior Principal Consultant'},
        {'name': 'Deepa Muralidhar', 'email': 'deepa.muralidhar@riaadvisory.com', 'department': 'Sales & Marketing', 'designation': 'Senior Manager - Bids & RFX'},
        {'name': 'Dhanesh Madhavi', 'email': 'dhanesh.madhavi@riaadvisory.com', 'department': 'Sales & Marketing', 'designation': 'Senior Consultant'},   
        {'name': 'Jacob Matthew Aaron', 'email': 'jacob.aaron@riaadvisory.com', 'department': 'Sales & Marketing', 'designation': 'Customer Success Associate  Sales'},
        {'name': 'Jacqueline Isabel Suarez', 'email': 'jacqueline.suarez@riaadvisory.com', 'department': 'Sales & Marketing', 'designation': 'Customer Success Associate'},
        {'name': 'Julie Sheth', 'email': 'julie.sheth@riaadvisory.com', 'department': 'Sales & Marketing', 'designation': 'Senior Consultant - Customer Success'},
        {'name': 'Manish Deepak', 'email': 'manish.deepak@riaadvisory.com', 'department': 'Sales & Marketing', 'designation': 'Sales Director'},
        {'name': 'Miles Underwood', 'email': 'miles.underwood@riaadvisory.com', 'department': 'Sales & Marketing', 'designation': 'Consultant'},
        {'name': 'Peter Sarsany', 'email': 'peter.sarsany@tmconsulting.com', 'department': 'Sales & Marketing', 'designation': 'Vice President'},
        {'name': 'Rajeshkumar Narayan Kotian', 'email': 'rajesh.kotian@riaadvisory.com', 'department': 'Sales & Marketing', 'designation': 'Director - Customer Success'},
        {'name': 'Ravi T Sharma', 'email': 'ravi.sharma@riaadvisory.com', 'department': 'Sales & Marketing', 'designation': 'Sales Operations Consultant'},
        {'name': 'Sadna PG', 'email': 'sadna.pg@riaadvisory.com', 'department': 'Sales & Marketing', 'designation': 'Senior Principal Consultant'},       
        {'name': 'Shivangi Sinha', 'email': 'shivangi.sinha@riaadvisory.com', 'department': 'Sales & Marketing', 'designation': 'Senior Consultant'},     
        {'name': 'Snehal Pradip Gupte', 'email': 'snehal.gupte@riaadvisory.com', 'department': 'Sales & Marketing', 'designation': 'Consultant'},
        {'name': 'Deepak Amar Nichani', 'email': 'deepak.nichani@riaadvisory.com', 'department': 'Operations', 'designation': 'Senior Consultant - Admin'},
        {'name': 'Jibin Sebastian', 'email': 'jibin.sebastian@riaadvisory.com', 'department': 'Operations', 'designation': 'Consultant - Admin'},
        {'name': 'Saket Pabby', 'email': 'saket.pabby@riaadvisory.com', 'department': 'Leadership', 'designation': 'Founder & CEO'},
        {'name': 'Sameer Khetarpal', 'email': 'sameer.khetarpal@riaadvisory.com', 'department': 'Leadership', 'designation': 'Managing Partner'},
        {'name': 'Supriya Mukhapadhyay', 'email': 'supriya.mukhapadhyay@riaadvisory.com', 'department': 'Leadership', 'designation': 'Managing Partner'}, 
        {'name': 'Emin Eker', 'email': 'emin.eker@riaadvisory.com', 'department': 'Leadership', 'designation': 'Managing Partner'},
        {'name': 'Kamal Shukla', 'email': 'kamal.shukla@riaadvisory.com', 'department': 'Leadership', 'designation': 'Partner'},
        {'name': 'Gregory Brown', 'email': 'greg.brown@riaadvisory.com', 'department': 'Leadership', 'designation': 'Chief Business Officer'},
        {'name': 'Sameer Deo', 'email': 'sameer.deo@riaadvisory.com', 'department': 'Leadership', 'designation': 'Head of India Operations'},
        {'name': 'Anil Valecha', 'email': 'anil.valecha@riaadvisory.com', 'department': 'Leadership', 'designation': 'Chief Financial Officer'},
        {'name': 'Arnold Lantin Holgado', 'email': 'arnold.holgado@riaadvisory.com', 'department': 'Leadership', 'designation': 'Country Head'},
        {'name': 'MD Salman Ansari', 'email': 'salman.ansari@riaadvisory.com', 'department': 'Internal IT and Cloud Ops', 'designation': 'Director - CISO'},
        {'name': 'Valliappan Narayanan', 'email': 'valli.narayanan@riaadvisory.com', 'department': 'Leadership', 'designation': 'Managing Partner'},
        {'name': 'Akshay Sabhikhi', 'email': 'akshay.sabhikhi@riaadvisory.com', 'department': 'Leadership', 'designation': 'Chief Executive Officer of RIA Products'},
        {'name': 'Mario M Bauer', 'email': 'mario.bauer@tmgconsulting.com', 'department': 'Leadership', 'designation': 'Chief Executive Officer'},        
        {'name': 'Aletha Pamela Glanvill', 'email': 'pam.glanvill@tmgconsulting.com', 'department': 'Leadership', 'designation': 'President & Evp'},
        {"name": "Krishna Chaudhari", "email": "krishna.chaudhari@riaadvisory.com",
            "department": "Internal IT and Cloud Ops", "designation": "Associate Consultant"},
        {"name": "Deepak Nichani", "email": "deepak.nichani@riaadvisory.com",
            "department": "Operations", "designation": "Senior Consultant - Admin"},  
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
    {'start': 238, 'end': 242, 'config': 'Developer'},
    # {'start': 0, 'end': 226, 'config': 'Developer_1'},
    # {'start': 788, 'end': 802, 'config': 'Leadership'},
    # {'start': 802, 'end': 986, 'config': 'HR'},
    # {'start': 226, 'end': 242, 'config': 'Account'}
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
        'subject': "Strategic Plan Review for Q4 - Action Required",
        'action_name': "Review Strategic Plan"
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
