# app/app.py

from flask import Flask, render_template, request, jsonify, make_response
import joblib
import pandas as pd
from .feature_extraction import extract_features
from .config_db import get_db_connection
from datetime import datetime
import csv
import io
import math

app = Flask(__name__)

# --------------------------------------------------
# Load ML model and DB connection
# --------------------------------------------------
model = joblib.load("app/model/phishing_model.pkl")
db = get_db_connection()
collection = db.prediction_logs


# --------------------------------------------------
# HOME + PREDICTION
# --------------------------------------------------
@app.route('/', methods=['GET', 'POST'])
def home():
    acc = 0
    try:
        with open("app/model/accuracy.txt", "r") as f:
            acc = f.read()
    except:
        pass

    if request.method == "POST":
        url = request.form['url']

        features = extract_features(url)
        df = pd.DataFrame([features])

        input_features = df[['url_length', 'has_at_symbol', 'has_https', 'num_digits',
                             'has_hyphen', 'num_dots', 'has_suspicious_words', 'has_ip', 'domain_length']]

        prediction = model.predict(input_features)[0]
        result = "🚨 Phishing Website Detected!" if prediction == 1 else "✅ Legitimate Website"

        log_data = {
            "url": url,
            "prediction": result,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        collection.insert_one(log_data)

        return render_template('result.html', url=url, result=result, accuracy=acc)

    return render_template('index.html', accuracy=acc)


# --------------------------------------------------
# ROUTE: Dashboard Page
# --------------------------------------------------
@app.route('/logs')
def logs_page():
    return render_template('dashboard.html')


# --------------------------------------------------
# API: Get logs (Search, Filter, Pagination)
# --------------------------------------------------
@app.route('/api/logs')
def api_logs():

    q = request.args.get('q', '').strip()
    status = request.args.get('status', 'all')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 15))

    query = {}

    if q:
        query['url'] = {'$regex': q, '$options': 'i'}

    if status == 'phishing':
        query['prediction'] = {'$regex': 'Phishing', '$options': 'i'}
    elif status == 'safe':
        query['prediction'] = {'$not': {'$regex': 'Phishing', '$options': 'i'}}

    total = collection.count_documents(query)

    cursor = collection.find(query, {'_id': 0}).sort('timestamp', -1).skip((page - 1) * per_page).limit(per_page)

    logs = list(cursor)

    return jsonify({
        "logs": logs,
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": math.ceil(total / per_page)
    })


# --------------------------------------------------
# API: Stats for Pie Chart
# --------------------------------------------------
@app.route('/api/stats')
def api_stats():
    phishing = collection.count_documents({"prediction": {"$regex": "Phishing"}})
    total = collection.count_documents({})
    safe = total - phishing

    return jsonify({
        "phishing": phishing,
        "safe": safe,
        "total": total
    })


# --------------------------------------------------
# DOWNLOAD CSV
# --------------------------------------------------
@app.route('/download_logs')
def download_logs():

    q = request.args.get('q', '').strip()
    status = request.args.get('status', 'all')

    query = {}

    if q:
        query['url'] = {'$regex': q, '$options': 'i'}

    if status == 'phishing':
        query['prediction'] = {'$regex': 'Phishing', '$options': 'i'}
    elif status == 'safe':
        query['prediction'] = {'$not': {'$regex': 'Phishing', '$options': 'i'}}

    cursor = collection.find(query, {'_id': 0}).sort('timestamp', -1)

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['URL', 'Prediction', 'Timestamp'])

    for log in cursor:
        cw.writerow([log['url'], log['prediction'], log['timestamp']])

    response = make_response(si.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=logs.csv"
    response.headers["Content-Type"] = "text/csv"

    return response


# --------------------------------------------------
# Run App
# --------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
