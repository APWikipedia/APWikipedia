import sys
from pathlib import Path 

root_path = str(Path(__file__).parent.parent.resolve()) 
if root_path not in sys.path: 
    sys.path.append(root_path)
    
from flask import Flask, current_app
from flask_restful import Api
from flask_cors import CORS
from web_backend.api.resources import SearchResource, RankedSearchResource
from engine.search_engine import SearchEngine
import json
from collections import defaultdict
def default_dict_list():
    return defaultdict(list)



app = Flask(__name__)
CORS(app) # 解决跨域问题
api = Api(app)

def load_metadata(metadata_file):
    with open(metadata_file, 'r', encoding='utf-8') as file:
        return json.load(file)
    
# 初始化 SearchEngine 实例并保存为全局变量
app.search_engine = SearchEngine("engine/lightweight_index.pkl", "engine/heavyweight_index.pkl")
app.metadata = load_metadata('engine/metadata.json')


api.add_resource(SearchResource, '/search')
api.add_resource(RankedSearchResource, '/ranked_search')

if __name__ == '__main__':
    app.run(debug=True)
