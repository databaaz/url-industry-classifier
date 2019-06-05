from flask import Flask, jsonify
from flask import request
import requests
from utils import fetch_landing_page
from langdetect import detect
import re 
import pickle
# from sklearn.ensemble import VotingClassifier
# from sklearn.feature_extraction.text import TfidfVectorizer


class_mapping = {0:"Auto", 1:"CPG", 2:"Financial Services", 3:"Other", 4:"Retail", 5:"Travel"}

# Loading transformers and models
with open('../models/tfidf_en.pkl', 'rb') as f:
	tfidf_en = pickle.load(f)
with open('../models/model_ensemble.pkl', 'rb') as f:
	model = pickle.load(f)


app = Flask(__name__)

@app.route('/')
def index():
	return 'Welcome to Classifier API. Please send requests to /classifier'


@app.route('/classifier', methods=['POST'])
def classifier():
	if not request.json or not 'url' in request.json:
		abort(400)
	url = request.json["url"]
	print("URL:", url)
	content = fetch_landing_page(url)
	if content is not None:
		lang = detect(content)
		print(lang)
		if lang != 'en':
			response = {
			'error': 'Language of target site `{}` not supported yet. Only English Language supported'.format(lang)
		}
		else:
			content = re.sub('[^a-zA-Z ]', " ", content)
			new_vector = tfidf_en.transform([content])
			X_new = new_vector.toarray()
			y_new = model.predict(X_new)
			y_class = class_mapping[y_new[0]]
			response = {
				'url': url,
				'category': y_class

			}

	else:
		response = {
			'error': 'URL {} not found or took too long to respond'.format(url)
		}

	return jsonify(response)


if __name__ == '__main__':
	app.run(debug = True)
