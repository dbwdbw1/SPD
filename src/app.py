from sqlit_spider.run_1688 import start_crawler
from src.image_search.run_image_search import get_image_search_url

# 总入口
# 1.获取图片搜索url列表
# 2.启动浏览器模拟人爬取信息
if __name__ == '__main__':
    image2url = get_image_search_url()
    start_crawler(image2url)
