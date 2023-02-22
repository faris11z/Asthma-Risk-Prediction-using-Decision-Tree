#!/usr/bin/env python
# coding: utf-8

# Importing Packages
import pandas as pd
from sklearn.tree import DecisionTreeClassifier as dtc
import requests
from bs4 import BeautifulSoup




#joblib.dump(model, 'PEFR_predictor.joblib')

#model = joblib.load('PEFR_predictor.joblib')


# Getting Weather Metrics 
def weather_data_(city):
    #city = input("Enter City:")
    city = str(city)
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

    return p,q,r,s,city


data=pd.read_csv("PEFR_Data_set.csv")
data.shape

# Training Model
def predict_(gender):
    
    p,q,r,s,city = weather_data_(city)
    
    X=data.drop(columns=['Age','Height','PEFR'])
    y=data['PEFR']
    model=dtc()
    model.fit(X,y)
    g = int(gender)
    prediction = model.predict([[g,p,q,r,s]])
    predicted_pefr = prediction[0]
    print("Predicted Pefr: ",predicted_pefr)
    
    return predicted_pefr,gender


def safety_check_(actual_pefr):
    #actual_pefr = float(input("Enter Actual PEFR value: "))
    predicted_pefr,gender = predict_(gender)
    perpefr = (actual_pefr/predicted_pefr)*100

    # Display Output

    if perpefr >= 80:
        safety_result='SAFE'
    elif perpefr >= 50:
        safety_result='MODERATE'
    else:
        safety_result= 'RISK'
    print(safety_result)

    return safety_result