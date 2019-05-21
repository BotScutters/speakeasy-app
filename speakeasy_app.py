from flask import Flask, request, render_template, jsonify, request, abort
# from flask_bootstrap import Bootstrap
from speakeasy_api import predict_ratings

app = Flask('SpeakeasyApp')
amenities = ['24-hour check-in', 'Air conditioning', 'BBQ grill', 'Bed linens',
             'Cable TV', 'Coffee maker', 'Dishwasher', 'Elevator']


@app.route("/predict", methods=['POST'])
def make_prediction():
    if not request.json:
        abort(400)
    data = request.json
    response = predict_ratings(data)

    return jsonify(response)
    # return render_template("result.html", response=jsonify(response))


@app.route("/")
def front():
    return render_template("front.html")


@app.route("/rate")
def index():
    amenity_list = [{'id': amenity.replace(' ', '_').replace('-', '_').replace('/', '_'),
                     'label': amenity} for amenity in amenities]
    return render_template("index.html", amenities=amenity_list)


app.run(debug=True)
