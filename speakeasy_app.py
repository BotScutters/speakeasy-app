from flask import Flask, request, render_template, jsonify, request, abort
# from flask_bootstrap import Bootstrap
from speakeasy_api import load_from, predict

app = Flask('SpeakeasyApp')

@app.route("/predict", methods=['POST'])
def make_prediction():
    if not request.json:
        abort(400)
    data = request.json
    response = predict(data['request'])
    # result = jsonify(response)
    result = response
    # print(result)
    return jsonify(result)
    # return render_template("result.html", response=jsonify(response))


@app.route("/")
def front():
    print('Hello World')
    return render_template("front.html")


@app.route("/result")
def result():
    return render_template("result.html")


app.run(debug=True)
