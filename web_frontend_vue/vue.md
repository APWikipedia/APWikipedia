# Mian Steps
1. Download node.js - which incloud npm
2. cd web_frontend_vue
3. npm install
4. npm run serve

# TODO
* 使用vue router实现页面home和页面result切换 ✔
* 分页 ✔ - 总数据条数length，限制显示在页面上的页面数为10个, 页码CSS样式
* 搜索框优化高级搜索选项 - 默认是ranked_search，然后另一个是other_search (mixed_search) - 解决高级搜索不能直接输入问题 ✔ select的CSS样式
  * query search example:
    1 Happiness
    2 Edinburgh AND SCOTLAND
    3 income AND taxes
    4 "income taxes"
    5 #20(income, taxes)
    6 "middle east" AND peace
    7 "islam religion"
    8 "Financial times" AND NOT BBC
    9 "wall street" AND "dow jones"
    10 #15(dow,stocks)
* spell check和搜索扩展
* tags的显示

# Others
## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).
