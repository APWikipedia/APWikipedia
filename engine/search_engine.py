import json
import math
import re
from typing import List, Set, Tuple

from nltk.stem import PorterStemmer


class SearchEngine:
    def __init__(self, index_file: str) -> None:
        self.inverted_index = self.load_index(index_file)
        self.ps = PorterStemmer()
        self.stop_words = set(
            open("./preprocess/ttds_2023_english_stop_words.txt", encoding="utf-8")
            .read()
            .splitlines()
        )

    @staticmethod
    def load_index(index_file: str) -> dict:
        with open(index_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def execute_query(self, query: str) -> Set[int]:
        """
        Entry function for queires.boolean.txt
        Check for query type
        """
        tokens = self.query_preprocess(query)
        if "#" in query:  # Check for proximity query
            return self.proximity_search(query)
        elif '"' in query:  # Check for phrase query
            if "AND" in query or "OR" in query:
                return self.mix_search(query)
            return self.phrase_search(tokens)
        elif any(op in query for op in ["AND", "OR", "NOT"]):
            return self.mix_search(query)
        else:
            return self.phrase_search(tokens)

    def query_preprocess(self, query: str) -> List[str]:
        """
        Preprosess the query into token list for further search
        """
        tokens = re.findall(r"\b\w+\b", query.lower())
        boolean_operators = ["and", "or", "not"]

        processed_tokens = []
        for word in tokens:
            if word in boolean_operators:
                processed_tokens.append(word.upper())
            elif word.isalpha() and word not in self.stop_words:
                processed_tokens.append(self.ps.stem(word))
        return processed_tokens

    def mix_search(self, text: str) -> Set[str]:
        """
        Special search with both operators (AND, OR, NOT) and phrases
        """

        def extract_positions(phrase, words):
            # Extract the position of a phrase or word
            if phrase:
                pos = set(self.phrase_search(phrase))
            else:
                pos = set()

            for word in words:
                if word.upper() not in ["AND", "OR", "NOT"]:
                    stemmed_word = self.ps.stem(word.lower())
                    if stemmed_word in self.inverted_index:
                        pos = pos.union(set(self.inverted_index[stemmed_word].keys()))
            return pos

        result = set()
        phrases = re.findall(r'"(.*?)"', text)
        other_words = re.sub(r'"(.*?)"', "", text).split()

        if phrases:
            pos1 = extract_positions(phrases[0], other_words)
            pos2 = extract_positions(
                phrases[1] if len(phrases) > 1 else None, other_words
            )

            if "AND" in text:
                result = (
                    pos1.intersection(pos2) if "AND NOT" not in text else pos1 - pos2
                )
            elif "OR" in text:
                result = (
                    pos1.union(pos2)
                    if "OR NOT" not in text
                    else pos1.union(set(self.index.keys()) - pos2)
                )

        return result

    def phrase_search(self, phrase_tokens: List[str]) -> Set[int]:
        """
        Phase search
        Find all documents if they contain token from the phrase query statement
        """
        # phrase_tokens = self.query_preprocess(query)
        # print(f"Preprocessed tokens: {phrase_tokens}")
        if not phrase_tokens or phrase_tokens[0] not in self.inverted_index:
            return set()

        docs = set(self.inverted_index[phrase_tokens[0]].keys())
        for token in phrase_tokens[1:]:
            if token not in self.inverted_index:
                return set()
            docs &= set(self.inverted_index[token].keys())

        result_docs = []
        for doc in docs:
            positions = [self.inverted_index[token][doc] for token in phrase_tokens]
            for pos in positions[0]:
                if all([(pos + i) in positions[i] for i in range(1, len(positions))]):
                    result_docs.append(doc)
                    break
        return set(result_docs)

    def compute_positions_within_distance(
        self, positions1: List[int], positions2: List[int], distance: int
    ) -> bool:
        """
        Check if any pair of positions between two lists are within a specified distance.
        """
        i, j = 0, 0
        while i < len(positions1) and j < len(positions2):
            if abs(positions1[i] - positions2[j]) <= distance:
                return True
            if positions1[i] < positions2[j]:
                i += 1
            else:
                j += 1
        return False

    def proximity_search(self, query: str) -> Set[int]:
        """
        Promimity search, only for query like this: #20(income, taxes)
        """
        # Match the terms and required distance
        match = re.match(r"#(\d+)\((\w+),\s*(\w+)\)", query)
        if not match:
            return set()

        distance = int(match.group(1))
        token1 = self.ps.stem(match.group(2))
        token2 = self.ps.stem(match.group(3))

        # Check if in the index
        if token1 not in self.inverted_index or token2 not in self.inverted_index:
            return set()

        # Find articles if two terms are closed less than the required distance
        results = set()
        for doc_id in self.inverted_index[token1]:
            if doc_id in self.inverted_index[token2]:
                positions1 = self.inverted_index[token1][doc_id]
                positions2 = self.inverted_index[token2][doc_id]
                if self.compute_positions_within_distance(
                    positions1, positions2, distance
                ):
                    results.add(doc_id)

        return results

    def compute_idf(self) -> None:
        """
        Calculate the IDF value of each word according to the formula
        """
        self.idf = {}
        N = len({doc_id for postings in self.inverted_index.values() for doc_id in postings})
        for term, postings in self.inverted_index.items():
            df = len(postings)
            self.idf[term] = math.log10(N / df)

    def compute_tf_idf(self) -> None:
        """
        Calculate the TFIDF value for each word in each document according to the formula
        """
        self.tf_idf = {}
        for term, postings in self.inverted_index.items():
            if term not in self.tf_idf:
                self.tf_idf[term] = {}
            for doc_id, positions in postings.items():
                tf = len(positions)
                self.tf_idf[term][doc_id] = (1 + math.log10(tf)) * self.idf[term]

    def ranked_search(self, query: str) -> List[Tuple[int, float]]:
        """
        TFIDF search, use TF-IDF value to return ranked search result
        """
        self.compute_idf()
        self.compute_tf_idf()
        query_tokens = self.query_preprocess(query)

        doc_scores = {}
        for token in query_tokens:
            if token in self.tf_idf:
                for doc_id, weight in self.tf_idf[token].items():
                    if doc_id not in doc_scores:
                        doc_scores[doc_id] = 0
                    doc_scores[doc_id] += weight
        # Sort documents in descending order of TF-IDF score
        ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        return ranked_docs[:150]  # Return first 150 documents


if __name__ == "__main__":
    engine = SearchEngine("engine/inverted_index.json")
    # query = "income taxes"
    # query =  "#20(income, taxes)"
    # query = '"AI algorithm" OR bayes'
    query = 'algorithm'
    # result = engine.execute_query(query)
    result  = engine.ranked_search(query)
    print(result)
