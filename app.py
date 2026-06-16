from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import pickle
import pandas as pd
import numpy as np
from flask import session
import uuid
import json
from datetime import datetime
from dbconnect import *

import mysql.connector
from datetime import datetime
import os
import os
import hashlib
from datetime import datetime
import numpy as np
import random
import requests
from sklearn.metrics.pairwise import cosine_similarity


from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy

import os

import matplotlib.pyplot as plt

import google.generativeai as genai
import requests
from flask import Flask, request, jsonify, render_template, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
import hashlib
import json
from time import time
from datetime import datetime
from dbconnect import inserquery, inserquerypara,recoredselect  # Assuming your dbconnect methods for MySQL
import MySQLdb
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/drugdiscover'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
genai.configure(api_key="AIzaSyD6X8T-QPhObaJntlQyjUvaDQjoHlt65-c")

side_effects_by_stage = {
    1: ["Mild headache", "Dizziness", "Nausea", "Dry mouth", "Fatigue", "Drowsiness", 
        "Upset stomach", "Constipation", "Diarrhea", "Skin rash"],
    
    2: ["Mild itching", "Heartburn", "Muscle cramps", "Increased thirst", "Loss of appetite", 
        "Blurred vision", "Anxiety", "Tremors", "Sweating", "Shortness of breath"],
    
    3: ["Chest pain", "Irregular heartbeat", "Severe allergic reaction", "Fainting", "Seizures", 
        "Liver damage", "Kidney failure", "Severe dehydration", "Internal bleeding", "Anaphylaxis"],
    
    4: ["Multiple organ failure", "Coma", "Respiratory failure", "Cardiac arrest", "Septic shock", 
        "Brain swelling", "Paralysis", "Uncontrolled bleeding", "Total kidney shutdown", "Death"]
}

# Function to determine interaction type and stage based on dosage
def determine_interaction(dosage_sum):
    if dosage_sum <= 500:
        return 0, 1
    elif 501 <= dosage_sum <= 1500:
        return 1, 2
    elif 1501 <= dosage_sum <= 2500:
        return 2, 3
    else:
        return 2, 4
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}
safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction="You are an expert at teaching science to kids. Your task is to engage in conversations about science and answer questions. Explain scientific concepts so that they are easily understandable. Use analogies and examples that are relatable. Use humor and make the conversation both educational and interesting. Ask questions so that you can better understand the user and improve the educational experience. Suggest way that these concepts can be related to the real world with observations and experiments.",
)
stage_actions = {
    1: "Monitor symptoms, hydration, rest, mild pain relief.",
    2: "Discontinue or adjust dosage, consult a doctor.",
    3: "Immediate medical attention, monitor vitals, possible hospitalization.",
    4: "Emergency intervention, ICU care, life support measures."
}


chat_session = model.start_chat(
    history=[]
)
CORS(app, resources={r"/*": {"origins": "*"}}) 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("input.csv")
df = df.dropna()

import MySQLdb  # You can use pymysql as an alternative
from datetime import datetime
import hashlib
import pickle

with open("randomforestmodelstage", "rb") as f:
    rf_model = pickle.load(f)

with open("randomforestmodelinteraction_type.pkl", "rb") as f:
    rf_model_interaction = pickle.load(f)

with open("feature.pkl", "rb") as f:
       label_encoders= pickle.load(f)

@app.route('/')
def hello():
    message= ''
    return render_template("index.html")

@app.route('/index')
def index():
    message= ''
    return render_template("index.html")

@app.route('/signup')
def signup():
    message= ''
    return render_template("signup.html",message = message)





@app.route('/signin')
def signin():
    message= ''
    return render_template("signin.html",message = message)


@app.route('/DrugDiscovery')
def DrugDiscovery():
      return render_template("DrugDiscovery.html",  name=session['name'])


@app.route('/register', methods=["POST"])
def register():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        username = request.form["name"]
       
        mno = request.form["mno"]
      
        sql1 = '''INSERT INTO account(username,  mno, email, password) 
                  VALUES ("%s", "%s", "%s", "%s")''' % (username,  mno, email, password)
        inserquery(sql1)
        message = f"{email} account Created Successfully"
        

    return render_template('index.html', message=message)

@app.route('/drugdiscover', methods=["POST"])
def drugdiscover():
    if request.method == 'POST':
        drug1 = request.form["drug1"]
        drug2 = request.form["drug2"]
        drug3 = request.form["drug3"]
        dosage1 = int(request.form["dosage1"])
        dosage2 = int(request.form["dosage2"])
        dosage3 = int(request.form["dosage3"])
        df1 = pd.DataFrame([{
                "drug1": drug1,
                "drug2": drug2,
                "drug3": drug3,
                "dosage1": dosage1,
                "dosage2": dosage2,
                "dosage3": dosage3
            }])
        for col in ["drug1", "drug2", "drug3"]:
                df1[col] = df1[col].map(label_encoders[col])
        Xtest = df1[["drug1", "drug2", "drug3", "dosage1", "dosage2", "dosage3"]]
        print(Xtest)
        y_pred_stage = rf_model.predict(Xtest)
        y_pred_interaction = rf_model_interaction.predict(Xtest)
        dosage_sum=dosage1+dosage2+dosage3
        interaction_type, stage = determine_interaction(dosage_sum)
        side_effect = random.choice(side_effects_by_stage[stage])
        stagesinteartion=max(interaction_type, y_pred_interaction[0])
        intrtationlablre=["Moderate","Mild","Severe"]
        intearctiotype=intrtationlablre[stagesinteartion]
    
        stagesprdictinteartion=max(y_pred_stage[0], stage)
        finalstaage=stage_actions[stagesprdictinteartion]
        
      
        data=[side_effect,intearctiotype,finalstaage]
        message=  f''' "drug1": {drug1}
                "drug2": {drug2}
                "drug3": {drug3}
                "dosage1": {dosage1}
                "dosage2": {dosage2}
                "dosage3": {dosage3} 
                side_effects : {side_effect} I neeed description with sugession'''
        response = chat_session.send_message(message)

        model_response = response.text
        print(model_response)


    return render_template('DrugDiscovery.html', message=data, model_response=model_response,side_effects=True )


@app.route('/authorised', methods=["POST"])
def authorised():
    email = request.form["email"]
    password = request.form["password"]
    dataQuery = "SELECT * FROM account WHERE email='%s' AND password='%s'" % (email, password)
    dataInfo = recoredselect(dataQuery)
    if dataInfo:
        session['id'] = dataInfo[0][0]
        session['name'] = dataInfo[0][1]
        
        return render_template('dashboard.html', name=session['name'])
    else:
        return render_template('index.html', message="Invalid credentials")


if __name__ == '__main__':
    app.run(debug=True)
