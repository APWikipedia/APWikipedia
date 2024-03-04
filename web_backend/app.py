import sys
from flask import Flask, current_app
from flask_restful import Api
from flask_cors import CORS
from web_backend.api.resources import SearchResource, RankedSearchResource
from engine.search_engine import SearchEngine
import json

app = Flask(__name__)
CORS(app) # 解决跨域问题
api = Api(app)

def load_metadata(metadata_file):
    with open(metadata_file, 'r', encoding='utf-8') as file:
        return json.load(file)
    
# 初始化 SearchEngine 实例并保存为全局变量
app.search_engine = SearchEngine("engine/inverted_index.json")
app.metadata = load_metadata('engine/metadata.json')


api.add_resource(SearchResource, '/search')
api.add_resource(RankedSearchResource, '/ranked_search')

if __name__ == '__main__':
    app.run(debug=True)
