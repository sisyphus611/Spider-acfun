因为经常逛A站的文章区，学习了python的爬虫相关知识后便萌生了爬取acfun文章区相关数据的念头。
A站文章区采用了Ajax来渲染，因此需要通过抓包的方式来获取JSON数据，进一步进行采集分析
先写了一个小爬虫（Verson 0.01）小试牛刀，爬取了A站文章区综合版块“文章标题”、“阅读数”、“评论数”，共计上万条数据并存入了本地的Mysql数据库。
接着慢慢完善。。。
待续