#!/usr/bin/env python
from flask import Flask, render_template, redirect, session, url_for, request, jsonify
from flask_cors import CORS, cross_origin
from Input import Input
from Model import Model
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/foo": {"origins": "*"}})

data_input = Input()
model = Model()

@app.route("/")
def hello():
    # How can we customize this message with the session?
    return "hello"

@app.route("/save", methods=["GET", "POST"])
@cross_origin(origin='localhost',headers=['Content-Type','Access-Control-Allow-Origin'])
def save():
    data = request.json['data']
    print data
    data_input.save_to_file(data)
    data_input.readFromFile()
    return "SAVED"

@app.route("/train")
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def train():
    global model
    data_input.readFromFile()
    data_input.processData()
    x, y = data_input.getData()
    # print x
    model.model(len(x[0]),len(y[0]))
    model.model_train_init(x,y,50000)
    return "TRAINED"

@app.route("/predict", methods=["GET", "POST"])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
def predict():
    data = request.json["data"]
    x = data_input.processPredictData(data)
    model.model(27,9)
    y, y_list = model.predict([x])
    data = {"prediction":y, "debug":y_list}
    # print y
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
