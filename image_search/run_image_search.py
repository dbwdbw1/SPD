import os

from image_search.search import Ali1688ImageSearch
from image_search.upload import Ali1688Upload


# 1.扫描固定路径图片
# 2.上传获取image_id
# 3.获取url列表
def get_image_search_url():
    images = list_image_files("resource")
    upload = Ali1688Upload()
    image_search = Ali1688ImageSearch()
    urls = []
    for images in images:
        res = upload.upload(filename=images)
        image_id = res.json().get("data", {}).get("imageId", "")
        if not image_id:
            raise Exception("not image id")
        print(image_id)
        # search goods by image id
        req = image_search.request(image_id=image_id)
        print('1688: ', req.url)
        urls.append(req.url)
    return urls


# 获取目录下所有图片的路径
def list_image_files(directory):
    files = os.listdir(directory)
    file_paths = []
    # 遍历文件
    for file in files:
        # 判断文件是否为图片文件（这里简单地通过扩展名判断）
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            # 输出图片文件名
            full_path = os.path.join(directory, file)
            print(full_path)
            file_paths.append(full_path)
    return file_paths
