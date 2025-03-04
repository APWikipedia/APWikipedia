import gzip
import json
import math
import pickle
import re
import time
from typing import List, Set, Tuple

from nltk.stem import PorterStemmer


class SearchEngine:
    def __init__(self, index_file_with_tfidf: str, index_file_with_position: str) -> None:
        self.inverted_index_with_tfidf = self.load_index(index_file_with_tfidf)
        self.inverted_index_with_position = self.load_index(index_file_with_position)
        self.ps = PorterStemmer()
        self.stop_words = set(
            open("./engine/ttds_2023_english_stop_words.txt", encoding="utf-8")
            .read()
            .splitlines()
        )

    @staticmethod
    def load_index(index_file: str) -> dict:
        """
        使用pickle加载倒排索引
        """
        with open(index_file, 'rb') as file:
            return pickle.load(file)
        
    # @staticmethod
    # def load_index(index_file: str) -> dict:
    #     """
    #     Load the zipped inverted index from the file
    #     """
    #     with gzip.open(index_file, "rt", encoding="utf-8") as file:
    #         return json.load(file)

    
    def execute_query(self, query: str, page_number: int = 1, page_size: int = 10) -> Set[int]:
        """
        Entry function for queires.boolean.txt
        Check for query type
        """
        tokens = self.query_preprocess(query)
        if "#" in query:  # Check for proximity query
            return self.proximity_search(query, page_number, page_size)
        elif "'" in query:  # Check for phrase query
            if "AND" in query or "OR" in query:
                return self.mix_search(query, page_number, page_size)
            return self.phrase_search(tokens, page_number, page_size)
        elif any(op in query for op in ["AND", "OR", "NOT"]):
            return self.mix_search(query, page_number, page_size)
        else:
            return self.phrase_search(tokens, page_number, page_size)

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


    def _extract_positions(self, phrase: str, words: List[str]) -> Set[int]:
        pos = set()
        if phrase:
            phrase_result = self.phrase_search(phrase)
            if isinstance(phrase_result, set):
                pos.update(phrase_result)
        for word in words:
            if word.upper() not in ["AND", "OR", "NOT"]:
                word_positions = self.inverted_index_with_position.get(self.ps.stem(word.lower()), {})
                pos.update(word_positions.keys())
        return pos


    def mix_search(self, text: str, page_number: int = 1, page_size: int = 10) -> Tuple[List[str], int]:
        """
        Special search with both operators (AND, OR, NOT) and phrases
        """
        phrases = re.findall(r"'(.*?)'", text)
        other_words = re.sub(r"'(.*?)'", "", text).split()
        extracted_positions = [self._extract_positions(phrase, other_words) for phrase in phrases + [None] * (2 - len(phrases))]

        if "AND" in text:
            result = extracted_positions[0].intersection(extracted_positions[1]) if "AND NOT" not in text else extracted_positions[0] - extracted_positions[1]
        elif "OR" in text:
            result = extracted_positions[0].union(extracted_positions[1]) if "OR NOT" not in text else extracted_positions[0].union(set(self.inverted_index_with_position.keys()) - extracted_positions[1])
        else:
            result = set()

        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        return list(result)[start_index:end_index], len(result)

    def phrase_search(self, phrase_tokens: List[str], page_number: int = 1, page_size: int = 10) -> Set[int]:
        """
        Phase search
        Find all documents if they contain token from the phrase query statement
        """
        # phrase_tokens = self.query_preprocess(query)
        # print(f"Preprocessed tokens: {phrase_tokens}")
        if not phrase_tokens or phrase_tokens[0] not in self.inverted_index_with_position:
            return set()

        docs = set(self.inverted_index_with_position[phrase_tokens[0]].keys())
        for token in phrase_tokens[1:]:
            if token not in self.inverted_index_with_position:
                return set()
            docs &= set(self.inverted_index_with_position[token].keys())

        result_docs = set()
        for doc in docs:
            positions = [self.inverted_index_with_position[token][doc] for token in phrase_tokens]
            for pos in positions[0]:
                if all([(pos + i) in positions[i] for i in range(1, len(positions))]):
                    result_docs.add(doc)
                    break
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        return list(result_docs)[start_index:end_index] , len(result_docs)

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

    def proximity_search(self, query: str, page_number: int = 1, page_size: int = 10) -> Set[int]:
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
        if token1 not in self.inverted_index_with_position or token2 not in self.inverted_index_with_position:
            return set()

        # Find articles if two terms are closed less than the required distance
        results = set()
        for doc_id in self.inverted_index_with_position[token1]:
            if doc_id in self.inverted_index_with_position[token2]:
                positions1 = self.inverted_index_with_position[token1][doc_id]
                positions2 = self.inverted_index_with_position[token2][doc_id]
                if self.compute_positions_within_distance(
                    positions1, positions2, distance
                ):
                    results.add(doc_id)
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        return list(results)[start_index:end_index], len(results)

    def ranked_search(self, query: str, page_number: int = 1, page_size: int = 10) -> List[Tuple[str, float]]:
        """
        Use TF-IDF values to return ranked search results
        """
        query_tokens = self.query_preprocess(query)

        doc_scores = {}
        for token in query_tokens:
            if token in self.inverted_index_with_tfidf:
                print(f"Token type: {type(token)}, Token value: {token}")
                for doc_id, tf_idf_value in self.inverted_index_with_tfidf[token].items():
                    if doc_id not in doc_scores:
                        doc_scores[doc_id] = 0
                    doc_scores[doc_id] += tf_idf_value

        # Sort documents in descending order of their scores
        ranked_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        return ranked_docs[start_index:end_index] , len(ranked_docs) # Return top 10 documents

if __name__ == "__main__":
    start_time = time.time()
    engine = SearchEngine("engine/lightweight_index.pkl", "engine/heavyweight_index.pkl")
    load_time = time.time() - start_time
    print(f"Load time: {load_time:.2f}s")
    # query = "income taxes"
    # query =  "#20(income, taxes)"
    query = "'AI algorithm' OR bayes"
    # query = "ai"
    # results = engine.ranked_search(query)
    results, _ = engine.execute_query(query)
    query_time = time.time()  - start_time
    print(f"Query time: {query_time*1000}ms")
    print(results)
    metadata={}
    
    # with open('engine/metadata.json', 'r', encoding='utf-8') as f:
    #     metadata = json.load(f)
    
    # articles = []
    # for title, score in results:
    #     # 在元数据列表中搜索匹配的标题
    #     for article in metadata:
    #         if article['title'] == title:
    #             # 找到匹配的文章后，添加到最终结果列表中
    #             articles.append(article)
    #             break  # 匹配到后就跳出循环，继续下一个搜索结果

    
    # query_time = time.time() - load_time
    # print(f"Query time: {query_time:.2f}s")
    # print(articles)

