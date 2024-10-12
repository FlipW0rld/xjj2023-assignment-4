from flask import Flask, request, jsonify, send_from_directory
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

newsgroups = fetch_20newsgroups(subset='all')
documents = newsgroups.data[:200]  

vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X = vectorizer.fit_transform(documents)

svd = TruncatedSVD(n_components=100)
X_reduced = svd.fit_transform(X)
X_reduced = normalize(X_reduced)

@app.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    query_vec = vectorizer.transform([query])
    query_reduced = svd.transform(query_vec)
    query_reduced = normalize(query_reduced)
    
    similarities = cosine_similarity(query_reduced, X_reduced)[0]
    top_indices = np.argsort(similarities)[::-1][:5]

    results = [
    {"document": documents[i], "similarity": round(similarities[i], 2)}
    for i in top_indices
    ]

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)

