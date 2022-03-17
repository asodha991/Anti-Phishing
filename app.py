# from foo import bar
from flask import Flask, render_template, request
from features_for_new_datapoint import predict
# import numpy as np
# import pandas as pd
import pickle
import datetime as dt

app = Flask(__name__)

current_date = dt.date.today()
@app.route('/')
  
def home():
    return render_template('test.html', date = current_date)

@app.route('/result', methods = ['POST', 'GET'])
def result():
    output = request.form.to_dict()
    name = output["fname"]
    print(name)
    p = predict(name)
    print(p)
    p = int(p[0])
    print(p)
    if p == 1:
        Status = "Legitimate Website"
    else:
        Status = "Phishing Website"

    return render_template('test.html',URL = name, name = Status, date = current_date)

if __name__ == "__main__":
    app.run(host= '0.0.0.0', port =80)
    
