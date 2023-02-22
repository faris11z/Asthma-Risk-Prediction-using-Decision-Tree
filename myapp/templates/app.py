
from flask import Flask,request,render_template

app= Flask(__name__)
from weather_data import weather_data_,predict_,safety_check_

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather_data',methods=['POST'])
def weather_data():
    city = request.form['city']
    Fetch = request.form['Fetch']
    p,q,r,s,city = weather_data_(city)

    return render_template('index.html',Fetch=Fetch, city_ =city, temperature= p, humidity= q, pm2_= r, pm10_= s),city

@app.route('/predict',methods=['POST'])
def predict():
    gender = request.form['gender']
    predict = request.form['Predict']
    predicted_pefr,gender = predict_(gender)
    return render_template('index.html',Predict=predict, gender_ = gender, predicted_pefr_=predicted_pefr)

@app.route('/safety_check',methods=['POST'])
def safety_check():
    actual_pefr = request.form['actual_pefr']
    check = request.form['check']
    safety_result = safety_check_(actual_pefr)
    return render_template('index.html',check=check, actual_pefr_= actual_pefr, safety= safety_result)

if __name__ == "__main__":
    app.run(debug=True)