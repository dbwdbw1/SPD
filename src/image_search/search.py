from typing import Dict

import requests

from src.consts import headers
from src.utils.request import request_get


# 图片搜索 1688 业务类
class Ali1688ImageSearch(object):
    def __init__(self):
        self.url = "https://s.1688.com/youyuan/index.htm"
        super(Ali1688ImageSearch, self).__init__()

    def get_params(self, image_id: str) -> Dict[str, str]:
        params = {"tab": "imageSearch", "imageId": image_id, "imageIdList": image_id}
        return params

    def request(self, image_id: str) -> requests.request:
        params = self.get_params(image_id=image_id)
        req = request_get(url=self.url, params=params, headers=headers)
        return req
