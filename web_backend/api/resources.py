from flask import current_app
from flask_restful import Resource, request
import time

class SearchResource(Resource):
    def post(self):
        start_time = time.time() * 1000
        data = request.get_json()
        query = data.get('query')
        if query:
            search_results = current_app.search_engine.execute_query(query)
            results = []
            for title in search_results:
                for article in current_app.metadata:
                    if article['title'] == title:
                        results.append(article)
                        break
            search_time = time.time() * 1000 - start_time             
            return {"results": results,
                    "search_time(Ms)": search_time}, 200
        return {"message": "Query cannot be blank!"}, 400

class RankedSearchResource(Resource):
    def post(self):
        start_time = time.time() * 1000
        data = request.get_json()
        query = data.get('query')
        page_number = data.get('page_number', 1)
        page_size = data.get('page_size', 10)
        if query:
            ranked_results = current_app.search_engine.ranked_search(query, page_number, page_size)
            results = []
            for title, _ in ranked_results:
                for article in current_app.metadata:
                    if article['title'] == title:
                        results.append(article)
                        break 
            search_time = time.time() * 1000 - start_time
            return {"results": results,
                    "search_time(Ms)": search_time,
                    "page_number": page_number,
                    "page_size": page_size}, 200
        return {"message": "Query cannot be blank!"}, 400

