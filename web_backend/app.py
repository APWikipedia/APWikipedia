import sys
#sys.path.insert(0, 'c:\\Users\\sheny\\Desktop\\TTDS\\cw3\\APWikipedia') # 在我的电脑上运行时出现了找不到web_backend和engine的问题，通过此方法解决
from flask import Flask, current_app
from flask_restful import Api
from flask_cors import CORS
from web_backend.api.resources import SearchResource, RankedSearchResource
from engine.search_engine import SearchEngine

app = Flask(__name__)
CORS(app) # 解决跨域问题
api = Api(app)

# 初始化 SearchEngine 实例并保存为全局变量
app.search_engine = SearchEngine("engine/inverted_index.json")

api.add_resource(SearchResource, '/search')
api.add_resource(RankedSearchResource, '/ranked_search')

if __name__ == '__main__':
    app.run(debug=True)
