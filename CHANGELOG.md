# 更新日志

### 2024/05/18

* 1.调整目录结构
* 2.修复了进聊天页面时新增的弹窗“优先使用网页版”
* 3.支持了自动发送话术
* 4.支持了轮询等待回复（目前固定轮询次数，后续考虑优化）

### 2024/02/04

* 1.增加openpyxl、Pillow依赖
* 2.优化聊天界面停留时间
* 3.将爬取商品信息写入excel，并且每个商品需要下载图片，并以合适的格式嵌入excel
* 4.优化爬取逻辑 -> 每张图片爬取10个

### 2024/01/06

* 1.打通上传图片->使用生成的链接进行搜索->爬取的流程
* 2.研究了一下add_cookie，理论上不被强制跳转login.taobao.com的话可以实现免登
* 3.增加点击“价格排序”功能（未启用，很可能不是图片所搜的）
* 4.支持了商品详情页点击旺旺聊天并跳转界面、点击“使用网页版”的功能

### 2023/12/02

* 1.集成图片搜索功能（集成后的主流程还没有接入，只是有了这个功能）
* 2.关闭sqlite日志
* 3.跳过某些页面获取不到商品信息或工厂信息导致的crash
* 4.增加部分注释、优化格式

### 2023/08/26

增加登录校验，登录过后可以减少爬取两三个数据后的滑动验证码拦截
