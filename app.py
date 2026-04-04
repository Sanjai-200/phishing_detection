from flask import Flask, render_template, request
import pickle
import os

MODEL_PATH = "phishing.pkl"

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError("phishing.pkl not found!")

with open(MODEL_PATH, "rb") as f:
    data = pickle.load(f)

model = data["model"]
vectorizer = data["vectorizer"]

app = Flask(__name__)

def predict_url(url):
    vectorized = vectorizer.transform([url])
    prediction = model.predict(vectorized)[0]
    probability = model.predict_proba(vectorized)[0]

    if prediction == 1:
         result = "Phishing " 
    else :
         result = "Legitimate "
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
