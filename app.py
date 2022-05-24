from json import JSONDecoder
from flask import Flask, redirect, url_for, request,jsonify
import pickle
from flask_cors import CORS, cross_origin
import requests
import pycld2 as cld2
import re
from stopwordsiso import stopwords
import json

app = Flask(__name__)
CORS(app)

file = open('wt_matrix', 'rb')
data = pickle.load(file)

top_10_langs_iso = ['en', 'ar', 'fr', 'de', 'it', 'pt', 'ru', 'es', 'vi', 'nl', 'fi']

# @app.route('/success/<name>')
# def success(name):
#     return 'welcome %s' % name

# @app.route('/login',methods = ['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         user = request.form['nm']
#         return redirect(url_for('success',name = user)) 
#     else:
#         user = request.args.get('nm')
#         return redirect(url_for('success',name = user))


@app.route('/analyse',methods=['POST'])
def analyse():
    doc_lang_words = []
    final_words = []
    # print(request.data)
    req_data = request.data.decode('utf-8')
    print(req_data)
    file_data = json.loads(req_data)
    file_data = file_data['text']
    file_data = ''.join(x for x in file_data if x.isprintable())
    print(file_data)

    _, _, _, detected_language = cld2.detect(file_data,  returnVectors=True)
    # print(detected_language,len(file_data))

    for lang in detected_language:
        # print(lang[3])
        if lang[3] not in top_10_langs_iso:
            continue
        # print(file_data[lang[0] : lang[0] + lang[1]])
        words = re.split(', |_|\?|!| |,|\.|\[|\]|\(|\)|\{|\}|\:|\||-|«|»', file_data[lang[0] : lang[0] + lang[1]])
        words = [word for word in words if word.isalpha() or word.count("'")]
        # words = [word for word in words if word.lower() not in stopwords(lang[3])]
        
        # fast_lang_vecs[lang[3]]['filtered'].extend(list(filter(lambda emb: emb in fast_lang_vecs[lang[3]]['word2id'].keys(), words)))
        for word in words:
            doc_lang_words.append((lang[3], word))

    for word in doc_lang_words:
        if word in data:
            final_words.append({"name":word[1],"val":data[word],"lang":word[0]})
        else:
            final_words.append({"name":word[1],"val":[0,0,0,0,0],"lang":word[0]})

    print(final_words)
    return jsonify(final_words=final_words)
    # print(doc_lang_words)

if __name__ == '__main__':
    app.run(debug = True)
