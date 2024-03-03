import argparse
import ast
import json
import sys
from pprint import pprint

import pandas as pd
from dataset import DATA_CSV_PATH
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel

PICKLE_PATH = "classifier/data.pickle"
MODEL_PATH = "classifier/lada_model.gensim"
DOCUMENT_TOPICS_PATH = "classifier/document_topics.json"


def setup_args(parser):
    parser.add_argument(
        "--pickle",
        type=bool,
        default=False,
        help="If pickle provided",
    )
    parser.add_argument(
        "--train",
        type=bool,
        default=False,
        help="Flag for training LDA model",
    )
    parser.add_argument(
        "--topics",
        type=bool,
        default=False,
        help="Flag for dump document topics to json file",
    )


def get_lda_mode(df, common_dictionary):
    common_corpus = [common_dictionary.doc2bow(doc) for doc in total_corpus]
    if args.train:
        print("training LDA model...")
        lda_model = LdaModel(
            common_corpus,
            num_topics=20,
            id2word=common_dictionary,
            # passes=5,
            random_state=17,
        )
        lda_model.save(MODEL_PATH)
        print(f"saved model to {MODEL_PATH}")
    else:
        lda_model = LdaModel.load(MODEL_PATH)
        print(f"loaded model from {MODEL_PATH}")
    return lda_model


def extract_topics(df, common_dictionary, lda_model):
    # Create a dictionary to hold filenames and their top topics
    document_topics = {}

    for index, row in df.iterrows():
        if not row["name"]:
            continue

        document_name = row["name"]

        # Convert the document into a bag-of-words format
        doc_bow = common_dictionary.doc2bow(row["token"])

        # Get the document's topic distribution
        doc_topics = lda_model.get_document_topics(doc_bow, minimum_probability=0)

        # Sort the topics by their contribution to the document and pick the top 5
        top_topics = sorted(doc_topics, key=lambda x: x[1], reverse=True)[:5]

        # Extract the topic indices and contributions, converting contributions to native float
        # top_topic_indices_and_scores = [(topic[0], float(topic[1])) for topic in top_topics]

        # Extract the topic indices
        top_topic_indices = [topic[0] for topic in top_topics]

        # Get the top 3 topics' words and contributions
        # top_topics_words = [{
        #     'topic_id': idx,
        #     'score': score,
        #     'words': [(word, float(value)) for word, value in lda_model.show_topic(idx, topn=10)]
        # } for idx, score in top_topic_indices_and_scores]

        top_topics_words = [
            [str(word) for word, _ in lda_model.show_topic(topic_idx, topn=10)]
            for topic_idx in top_topic_indices
        ]

        # Store the result
        document_topics[document_name] = top_topics_words

        if index % 5000 == 0:
            print(f"Stored topics for {index} documents")

    return document_topics


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    setup_args(parser)
    args = parser.parse_args(sys.argv[1:])
    pprint(f"Parsed Arguments: {vars(args)}")

    df = None
    if args.pickle:
        df = pd.read_pickle(PICKLE_PATH)
    else:
        df = pd.read_csv(DATA_CSV_PATH)
        # Convert the 'token' column back to lists from string representation
        df["token"] = df["token"].apply(ast.literal_eval)
        df.to_pickle(PICKLE_PATH)
    print(
        f"Loaded dataset from {DATA_CSV_PATH } \n \
        having {len(df)} articles and {df['category'].nunique()} categories."
    )
    print(f"{df.head()}")

    total_corpus = df["token"].tolist()
    df["name"] = df["name"].astype(str)
    common_dictionary = Dictionary(total_corpus)
    lda_model = get_lda_mode(df, common_dictionary)
    print(f"loaded model {lda_model}")

    if args.topics:
        document_topics = extract_topics(df, common_dictionary, lda_model)
        with open(DOCUMENT_TOPICS_PATH, "w") as f:
            json.dump(document_topics, f, ensure_ascii=False, indent=4)
