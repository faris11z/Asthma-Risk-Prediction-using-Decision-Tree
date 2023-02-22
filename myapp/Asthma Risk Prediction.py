#!/usr/bin/env python
# coding: utf-
# Importing Packages

import pandas as pd
from sklearn.tree import DecisionTreeClassifier as dtc
import joblib
import requests
from bs4 import BeautifulSoup
import eel

eel.init("web")

@eel.expose



# Importing DataSet
def predictor(city,g,actual_pefr):

    g = int(g)
    actual_pefr = int(actual_pefr)

    data=pd.read_csv("PEFR_Data_set.csv")
    data.shape

    # Training Model

    X=data.drop(columns=['Age','Height','PEFR'])
    y=data['PEFR']
    model=dtc()
    model.fit(X,y)

    #joblib.dump(model, 'PEFR_predictor.joblib')



    #model = joblib.load('PEFR_predictor.joblib')


    # Getting Weather Metrics 

    #city = input("Enter City:")
    url = f'https://www.iqair.com/in-en/india/tamil-nadu/{city}'
    r = requests.get(url)
    soup = BeautifulSoup(r.content,'html.parser')
    aqi_dict = []
    s = soup.find('table',class_ = "aqi-overview-detail__other-pollution-table")

                 
    for x in s:
        aqi_dict.append(x.text)
    #print(aqi_dict)    
    aqi = aqi_dict[1]
    #print(aqi)
    a=aqi.split(" ")
    #print(a)
    pm2_index = a.index("PM2.5")

    pm2 = a[pm2_index +1][0:2]


    if 'PM10' not in aqi_dict :
        pm10 = 1.38 * float(pm2)
    else:
        pm10_index = a.index("PM10")
        pm10 = a[pm10_index+ 1][0:2]

    t = soup.find('div', class_="weather__detail")
    y = t.text
    temp_index = y.find('Temperature')+11
    degree_index = y.find('°')
    temp = y[temp_index : degree_index]

    hum_index = y.find('Humidity')+8
    perc_index = y.find('%')
    hum = y[hum_index:perc_index]


    

    # Predicting Live Values

    #g=int(input("Enter Gender (1-Male/0-Female): "))
    p=temp
    q=hum
    r=pm2
    s=pm10


    prediction = model.predict([[g,p,q,r,s]])
    predicted_pefr = prediction[0]

    #actual_pefr = float(input("Enter Actual PEFR value: "))

    perpefr = (actual_pefr/predicted_pefr)*100
    predicted_pefr = str(predicted_pefr)
    # Display Output
    #print("Predicted Pefr: ",predicted_pefr)
    if perpefr >= 80:
        s='Predicted PEFR Value is ' + predicted_pefr +' .So You are in SAFE Zone'
        return s
    elif perpefr >= 50:
        s='Predicted PEFR Value is ' + predicted_pefr +' .So You are in MODERATE Zone'
        return s
    else:
        s='Predicted PEFR Value is ' + predicted_pefr +' .So You are in RISK'
        return s


#print(predictor("chennai",1,500))

eel.start("index2.html")
