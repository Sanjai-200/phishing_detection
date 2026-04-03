from flask import Flask, render_template, request
import pickle
import os
import subprocess

MODEL_PATH = "phishing.pkl"


with open(MODEL_PATH, "rb") as f:
    data = pickle.load(f)

model = data["model"]
vectorizer = data["vectorizer"]

app = Flask(__name__)

def predict_url(url):
    vectorized = vectorizer.transform([url])
    prediction = model.predict(vectorized)[0]
    probability = model.predict_proba(vectorized)[0]

    result = "Phishing 🚨" if prediction == 1 else "Legitimate ✅"
    confidence = round(max(probability) * 100, 2)

    return result, confidence

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    score = None
    url = ""

    if request.method == "POST":
        url = request.form.get("url", "")

        if url:
            result, score = predict_url(url)

    return render_template("index.html", result=result, score=score, url=url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
