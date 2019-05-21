import os
import json
import pickle
import numpy as np
import pandas as pd
from xgboost import XGBClassifier

model = pickle.load(open("model/model.pickle", "rb"))
columns = pickle.load(open("model/model_columns.pickle", "rb"))


def recommendation():
    pass


def predict_ratings(data):
    data2 = {}
    for k, v in data.items():
        data2[k] = [v]
    query = pd.get_dummies(pd.DataFrame.from_dict(data2))

    for col in columns:
        if col not in query.columns:
            query[col] = 0

    query = query[columns]
    prob_5stars = model.predict_proba(query)[0, 1]

    print(query.shape)

    # Recommendation
    score = {}
    for col in list(columns[14:42]):
        rec = query.copy()
        if query[col][0] == 0:
            rec[col][0] = 1
        prob_new = model.predict_proba(rec)[0, 1]
        score[col] = prob_new

    highest = max(score, key=score.get)

    result = {
        'result': str(prob_5stars),
        'add': highest,
        'improvement': str(score.get(highest))
    }

    return result


if __name__ == '__main__':
    pass  # print(predict_ratings(example))
