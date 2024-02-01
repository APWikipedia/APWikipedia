import pandas as pd
from dataset import DATA_CSV_PATH
from joblib import dump
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

MODEL_PATH = "classifier/svm_classifier.joblib"
VECTORIZER_PATH = "classifier/tfidf_vectorizer.joblib"

if __name__ == "__main__":
    df = pd.read_csv(DATA_CSV_PATH)
    print(
        f"Loaded dataset from {DATA_CSV_PATH } \n \
          having {len(df)} articles and {df['category'].nunique()} categories."
    )
    print(f"{df.head()}")

    texts = df["token"]
    labels = df["category"]

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42
    )

    # Already applied stopping
    tfidf_vectorizer = TfidfVectorizer(stop_words=None)
    X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)

    svm_classifier = SVC(kernel="linear")
    svm_classifier.fit(X_train_tfidf, y_train)

    X_test_tfidf = tfidf_vectorizer.transform(X_test)

    # predictions = svm_classifier.predict(X_test_tfidf)

    # for article, prediction in zip(X_test, predictions):
    #     print(f"article: {article}\npredicted category: {prediction}\n")

    # Save model
    dump(svm_classifier, MODEL_PATH)
    dump(tfidf_vectorizer, VECTORIZER_PATH)

    print(f"Save model to {MODEL_PATH}")
    print(f"Save TF-IDF Vectorizer to {VECTORIZER_PATH}")
