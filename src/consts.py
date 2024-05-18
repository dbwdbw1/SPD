DEFAULT_1688_URL_PREFIX = "https://s.1688.com/selloffer/"

LOGIN_URL_PREFIX = 'https://login.taobao.com'

# 登录
LOGIN_URL = "https://login.taobao.com/?redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253D%25252F%25252Fmy.1688.com%25252F&style=tao_custom&from=1688web"

# 行星减速器
url = 'https://s.1688.com/selloffer/offer_search.htm?keywords=%D0%D0%D0%C7%BC%F5%CB%D9%C6%F7&n=y&netType=1%2C11%2C16&spm=a260k.dacugeneral.search.0'
# 硬齿面减速机、行星减速机
# url1 = 'https://s.1688.com/selloffer/offer_search.htm?keywords=%D0%D0%D0%C7%BC%F5%CB%D9%C6%F7&n=y&netType=1%2C11%2C16&spm=a260k.dacugeneral.search.0&beginPage=1&featurePair=1835%3A44231132%3B3310%3A23539333%3B9112%3A94585628'

url1 = 'https://s.1688.com/selloffer/offer_search.htm?keywords=%D0%D0%D0%C7%BC%F5%CB%D9%C6%F7&spm=a26352.13672862.searchbox.input'
# 当前页（断了之后）
# url5 = 'https://s.1688.com/selloffer/offer_search.htm?keywords=%D0%D0%D0%C7%BC%F5%CB%D9%C6%F7&n=y&netType=16&spm=a260k.dacugeneral.search.0&beginPage=5#sm-filtbar'
NOW_URL = 'https://s.1688.com/selloffer/offer_search.htm?keywords=%D0%D0%D0%C7%BC%F5%CB%D9%C6%F7&spm=&beginPage=1&featurePair=1835%3A44231132#sm-filt'

# 通用header
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

# 查询图片api的app_key
app_key = "12574478"

# 每张图片爬取商品数量
GET_GOODS_INFO_COUNT = 10

# 图片在Excel中的统一宽度
PIC_WIDTH = 90

# 图片在Excel中的统一高度
PIC_HEIGHT = 90

# Excel中，图片单元格的宽度
PIC_CELL_WIDTH = 12.25

# Excel中，图片单元格的高度
PIC_CELL_HEIGHT = 80.10

# Excel中，商品url单元格的高度
GOODS_URL_CELL_WIDTH = 60

# Excel中，商品标题单元格的高度
GOODS_TITLE_CELL_WIDTH = 60

# 聊天界面固定话术
CHAT_QUESTIONS = [
    '你好'
]

# 聊天界面等待回复的最大轮询次数
MAX_POLLING_TIMES = 10

# 聊天界面单词轮询等待回复的秒数
POLLING_WAIT_SECONDS = 6

# 无回复的预设
NO_REPLY_MESSAGE = "no_reply"
