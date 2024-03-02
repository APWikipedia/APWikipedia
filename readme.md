# APWikipedia开发手册

## TODO

**1. WebFrontEnd (Full functions) Yueshuang**

**2. WebBackEnd (optimize Storage and Speed) Yuhang**

**3. Tags, LM Yongteng**

**4. L2R TianYue**

**5. Host Online**

## 预处理和查询

**1. 首先merge原数据data**

`python preprocess/merge_file.py`

**2. 将merge_data进行preprocess转换成corpus**

`python preprocess/text_to_corpus.py`

**3.  利用preprocess_data建立index**

`python engine/build_index.py`

**4. 进行查询**

`python engine/search_engine.py`



## 模型训练

**1. 首先准备好dataset**

`python classifier/dataset.py`

**2. 模型训练**

`python classifier/train.py`

**3. 进行预测**

`python classifier/prediction.py`



# 前后端交互
**初始化项目**
```
pip install -e .
```

**目前地址：**

http://localhost:5000/search

http://localhost:5000/ranked_search



**前端请求格式：**

```json
{
    "method": "POST",
    "headers": {
        "Content-Type": "application/json"
    },
    "body": "{\"query\": \"查询的query\"}"
}
```



**后端返回格式（以ranked_search为例，只展示了前5个）：**

```json
{
    "results": [
        [
            "List of algorithms",
            3.972015502288635
        ],
        [
            "Algorithmic bias",
            3.7962575657266253
        ],
        [
            "Quantum computing",
            3.5730074374728025
        ],
        [
            "Algorithm characterizations",
            3.5118537578407514
        ],
        [
            "Genetic algorithm",
            3.4437181445296674
        ]
    ]
}

```
