import json

from joblib import load
from topics import DOCUMENT_TOPICS_PATH
from train import MODEL_PATH, VECTORIZER_PATH

LABEL_PATH = "classifier/labels.json"

svm_classifier = load(MODEL_PATH)
tfidf_vectorizer = load(VECTORIZER_PATH)

if __name__ == "__main__":
    with open(DOCUMENT_TOPICS_PATH, "r") as f:
        document_topics = json.load(f)
    print(f"loaded document topics file from {DOCUMENT_TOPICS_PATH}")

    document_labels = {}

    for document_name, topics in document_topics.items():
        topic_texts = [" ".join(tokens) for tokens in topics]

        topic_texts_tfidf = tfidf_vectorizer.transform(topic_texts)

        predictions = svm_classifier.predict(topic_texts_tfidf)

        # Remove duplicated topics
        unique_predictions = list(set(predictions))

        document_labels[document_name] = unique_predictions

    with open(LABEL_PATH, "w") as f:
        json.dump(document_labels, f, ensure_ascii=False, indent=4)

    print(f"Labeled {len(document_topics)} documents, dump labels to {LABEL_PATH}")
