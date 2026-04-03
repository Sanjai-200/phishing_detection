from datasets import load_dataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

ds = load_dataset("Mitake/PhishingURLsANDBenignURLs")
df = pd.DataFrame(ds["train"])

df = df.sample(n=60000, random_state=42)
df = df.dropna(subset=["url", "label"])

X = df["url"]
y = df["label"]

vectorizer = TfidfVectorizer(
    analyzer="char",
    ngram_range=(2, 4),
    max_features=6000
)

X_vectorized = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=500)
model.fit(X_train, y_train)


with open("phishing.pkl", "wb") as f:
    pickle.dump({
        "model": model,
        "vectorizer": vectorizer
    }, f)

print("Model saved")
