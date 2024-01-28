from flask import Flask, current_app
from flask_restful import Api
from web_backend.api.resources import SearchResource, RankedSearchResource
from engine.search_engine import SearchEngine

app = Flask(__name__)
api = Api(app)

# 初始化 SearchEngine 实例并保存为全局变量
app.search_engine = SearchEngine("engine/inverted_index.json")

api.add_resource(SearchResource, '/search')
api.add_resource(RankedSearchResource, '/ranked_search')

if __name__ == '__main__':
    app.run(debug=True)
