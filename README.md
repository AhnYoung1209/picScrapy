# picScrapy
此爬虫可以爬取该站所有分类图片，仅作实验和参考，请勿用于其他用途
1. 一些设置
```
# 爬取深度
DEPTH_LIMIT = 5
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
python3 -m scrapy crawl pic
```
