import json
import re
import urllib.request

from PIL import Image
import requests
from io import BytesIO

import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
import nltk


# def load_from(filepath):
#     """
#     Unpickles item and returns item from path
#     Input: filepath to pickled object
#     Output: unpickled object
#     """
#     with open(filepath, 'rb') as f:
#         item = pickle.load(f)
#     return item
    

def predict(model, req=''):
    print('I predict?')
    (vectorizer, svd, X_topics, drink_list) = model

    if not req:
        req = 'A smoky mezcal based Manhattan variation with a bitter amaro'

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
    drink = drink_list[drink_prediction]
    # result = drink_list[drink_prediction]
    # result.update({'name': drink_prediction})
    # result.update({'recipe_html': result['recipe'].to_html()})

    image_url = drink['img']
    local_filename = 'image.jpg'
    local_filename, headers = urllib.request.urlretrieve(image_url)

    # img = Image.open(BytesIO(requests.get(img_url).content))

    print(local_filename)
    result = {
        'drink_request': req,
        'name': drink_prediction,
        'img': image_url,
        'url': drink['url'],
        'recipe': drink['recipe'].to_html()
    }

    response = requests.get(image_url)
    im = Image.open(BytesIO(response.content))
    im = im.convert('RGBA')
    data = np.array(im)
    # just use the rgb values for comparison
    rgb = data[:,:,:3]
    color = [246, 213, 139]   # Original value
    black = [0,0,0, 255]
    white = [255,255,255,255]
    mask = np.all(rgb == color, axis = -1)
    # change all pixels that match color to white
    data[mask] = white

    # change all pixels that don't match color to black
    ##data[np.logical_not(mask)] = black
    new_im = Image.fromarray(data)
    new_im.save('static/new_file.tif')

    return result


if __name__ == '__main__':
    pass  # print(predict_ratings(example))
