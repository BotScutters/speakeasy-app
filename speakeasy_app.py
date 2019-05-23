from flask import Flask, request, render_template, jsonify, request, abort
import boto3
from io import BytesIO
import os
import pickle
# from flask_bootstrap import Bootstrap
from speakeasy_api import predict

app = Flask('SpeakeasyApp', static_url_path='/static')

def load_from(filepath):
    """
    Unpickles item and returns item from path
    Input: filepath to pickled object
    Output: unpickled object
    """
    with open(filepath, 'rb') as f:
        item = pickle.load(f)
    return item


def load_pkl(file):
    s3 = boto3.resource('s3')
    with BytesIO() as data:
        s3.Bucket("speakeasy-binaries").download_fileobj(file, data)
        data.seek(0)    # move back to the beginning after writing
        pkl = pickle.load(data)
    return pkl
    
vectorizer = load_pkl('vectorizer.pkl')
svd = load_pkl('svd.pkl')
X_topics = load_pkl('X_topics.pkl')
drink_list = load_pkl('drink_list.pkl')
model = vectorizer, svd, X_topics, drink_list

# drink = drink_list["'75' Cocktail (Vermeire's 1922 recipe)"]
# print(drink)

@app.route("/predict", methods=['POST'])
def make_prediction():
    if not request.json:
        abort(400)
    data = request.json
    print('wuddup')
    result = predict(model, req=data['request'])
    print('Made prediction')
    return jsonify(result)


@app.route("/")
def front():
    print('Hello World')
    return render_template("front.html")


@app.route("/result")
def result():
    return render_template("result.html")

if __name__ == "main":
    app.run(debug=False)
# app.run(debug=True)
