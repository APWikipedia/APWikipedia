from flask import current_app
from flask_restful import Resource, request

class SearchResource(Resource):
    def post(self):
        data = request.get_json()
        query = data.get('query')
        if query:
            results = current_app.search_engine.execute_query(query)
            if isinstance(results, set):
                results = list(results)            
            return {"results": results}, 200
        return {"message": "Query cannot be blank!"}, 400

# class RankedSearchResource(Resource):
#     def post(self):
#         data = request.get_json()
#         query = data.get('query')
#         if query:
#             results = current_app.search_engine.ranked_search(query)
#             if isinstance(results, set):
#                 results = list(results)        
#             return {"results": results}, 200
#         return {"message": "Query cannot be blank!"}, 400
class RankedSearchResource(Resource):
    def post(self):
        data = request.get_json()
        query = data.get('query')
        ranked_results = current_app.search_engine.ranked_search(query)
        if query:
            results = []
            for title, _ in ranked_results:
                for article in current_app.metadata:
                    if article['title'] == title:
                        results.append(article)
                        break 
            return {"results": results}, 200
        return {"message": "Query cannot be blank!"}, 400

