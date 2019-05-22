import json
import os
import pickle
import re

from PIL import Image
import requests
from io import BytesIO
import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import nltk


def load_from(filepath):
    """
    Unpickles item and returns item from path
    Input: filepath to pickled object
    Output: unpickled object
    """
    with open(filepath, 'rb') as f:
        item = pickle.load(f)
    return item
    

def predict(req=''):
    print('I predict?')
    vectorizer = load_from('model/vectorizer.pkl')
    svd = load_from('model/svd.pkl')
    X_topics = load_from('model/X_topics.pkl')
    drink_list = load_from('model/drink_list.pkl')
    
    if not req:
        test_str = 'A smoky mezcal based Manhattan variation with a bitter amaro'

    patterns = ['<.*>', '\n', '\r', '\xa0', '   ', '  ']
    for pattern in patterns:
        req = re.sub(pattern, ' ', req)
    req = req.lower()

    y_doc_vec = vectorizer.transform([req])
    y_topic = svd.transform(y_doc_vec)
    
    cosine_sims = cosine_similarity(X_topics, y_topic).flatten()
    cos_sims_sorted = pd.Series(
        cosine_sims, 
        index=X_topics.index,
        name='Cosine Similarity'
    ).sort_values(ascending=False)
    drink_prediction = cos_sims_sorted.index[0]

    result = drink_list[drink_prediction]
    result.update({'name': drink_prediction})
    
    print("I'll make you a")
    print(drink_prediction)
    print('\nThe recipe for that is:')
    print(result['recipe'])
    print('\nThis cocktail came from:')
    print(result["url"])
    
    print(result['img'])
    result.update({'recipe_html': result['recipe'].to_html()})
    print('I did it!')
    return result


if __name__ == '__main__':
    pass  # print(predict_ratings(example))
