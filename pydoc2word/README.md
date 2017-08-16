### 功能
提取指定目录下文件（股票相关新闻等）的关键字，持久化到数据库。

### 用法
在pydoc2word目录下执行：

1. 查看帮助: <br/>
 `python -m doc2word --h` <br/>
 `python -m doc2word --help`

2. 默认参数执行，离线生产股票相关关键字并持久化到数据库: <br/>
 `python -m doc2word`

2. 启动NLP REST API接口服务，默认端口18080，也可自行指定端口: 
   相关接口协议可参考 [新闻驱动股票自动选取系统-接口协议](http://121.43.73.92:8090/pages/viewpage.action?pageId=4587754)<br/>
 `python -m doc2word --server`
 
3. 训练IDF，参数为 -G 或 --gen-idf，参数值为要训练IDF的语料根目录，多个目录以半角逗号(,)分隔: <br/>
 `python -m doc2word -G /path/some_path1,/path/some_path2`

<span style='color:red;'>
*注意:* <br/>
*所有默认参数都在*`{PYDOC2WORD_HOME}/doc2word/settings.py`*中，*
*可以自行修改，也可以通过命令行接口传入参数覆盖默认参数。*
<span/>

**TODO list**

1. local版本增加日志debug信息。
2. 增加spark版本实现。
3. 增加mr2版本实现。
