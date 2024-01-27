from joblib import load
from train import MODEL_PATH, VECTORIZER_PATH

svm_classifier = load(MODEL_PATH)
tfidf_vectorizer = load(VECTORIZER_PATH)

new_texts = [
    "SVM is a kind of mechine learning method",
    "CNN is the shorthand of convolutional Neural network",
]

new_texts_tfidf = tfidf_vectorizer.transform(new_texts)

predictions = svm_classifier.predict(new_texts_tfidf)

for text, prediction in zip(new_texts, predictions):
    print(f"key words: {text}\npredicted category: {prediction}\n")
