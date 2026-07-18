import pandas as pd
import joblib
import os
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dataset_path = os.path.join(BASE_DIR, "dataset.csv")

df = pd.read_csv(dataset_path)

# Keep only required columns
df = df[["Comment", "Sentiment"]]

# Rename columns
df = df.rename(columns={
    "Comment": "text",
    "Sentiment": "label"
})

# Remove missing values
df = df.dropna()

# Remove leading/trailing spaces
df["text"] = df["text"].astype(str).str.strip()
df["label"] = df["label"].astype(str).str.strip().str.lower()

# ----------------- Debugging -----------------
print("First 5 rows:")
print(df.head())

print("\nColumns:")
print(df.columns.tolist())

print("\nDataset shape:")
print(df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nUnique labels:")
print(df["label"].unique())

print("\nLabel counts:")
print(df["label"].value_counts())
# ---------------------------------------------


def clean_text(text):
    text = str(text).lower()

    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text

df["text"] = df["text"].apply(clean_text)

X = df["text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=10000,
    ngram_range=(1, 2),
    min_df=2
)

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

model = LinearSVC(dual="auto")

model.fit(X_train, y_train)

print("Classes:", model.classes_)

pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, pred))

print("\nClassification Report:")
print(classification_report(y_test, pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, pred))

models_dir = os.path.join(BASE_DIR, "..", "models")
os.makedirs(models_dir, exist_ok=True)

joblib.dump(
    model,
    os.path.join(models_dir, "sentiment_model.pkl")
)

joblib.dump(
    vectorizer,
    os.path.join(models_dir, "tfidf_vectorizer.pkl")
)

print("\nModel saved successfully!")