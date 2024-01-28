from flask import current_app
from flask_restful import Resource, request

class SearchResource(Resource):
    def post(self):
        data = request.get_json()
        query = data.get('query')
        if query:
            results = current_app.search_engine.execute_query(query)
            return {"results": results}, 200
        return {"message": "Query cannot be blank!"}, 400

class RankedSearchResource(Resource):
    def post(self):
        data = request.get_json()
        query = data.get('query')
        if query:
            results = current_app.search_engine.ranked_search(query)
            return {"results": results}, 200
        return {"message": "Query cannot be blank!"}, 400
