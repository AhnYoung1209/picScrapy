# picScrapy
1. 一些设置
```
# 爬取深度
DEPTH_LIMIT = 3
# 图片存放位置
IMAGES_STORE = '/home/jwang/Videos/Pic'
# 图片最小宽度
IMAGES_MIN_WIDTH = 500
# 图片最小高度
IMAGES_MIN_HEIGHT = 500
```
还有一些选项需要注意：
```
# 下载延迟，别把别人人站点拖垮了，慢点
DOWNLOAD_DELAY = 0.2
# 爬虫并发数，默认是 16
CONCURRENT_REQUESTS = 20
```

2. 启动爬虫
```
python3 -m scrapy crawl pic --loglevel INFO
```
一般会有很多异常，比如那个不满足图片大小会抛异常，不影响运行