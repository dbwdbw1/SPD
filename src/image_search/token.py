from typing import Dict

import requests
from requests.cookies import RequestsCookieJar

import src.utils.common
from src import consts
from src.consts import app_key
from src.image_search.sign import Sign
from src.utils.request import request_get


# 图片搜索的参数prepare
class Token(object):
    def __init__(self, api: str, hostname: str):
        self.api = api
        self.hostname = hostname
        self.token_url = f"https://{self.hostname}/h5/{self.api.lower()}/1.0/"
        self.cookies: RequestsCookieJar
        super(Token, self).__init__()

    def get_token_params(self) -> Dict[str, str]:
        params = {
            "jsv": "2.7.0",
            "appKey": app_key,
            "t": str(src.utils.common.now()),
            "api": self.api,
            "v": "1.0",
            "type": "json",
            "dataType": "jsonp",
            "callback": "mtopjsonp1",
        }
        return params

    def request(self) -> requests.request:
        params = self.get_token_params()
        req = request_get(url=self.token_url, params=params, headers=consts.headers)
        self.cookies: RequestsCookieJar = req.cookies
        return req

    def _get_token(self):
        if not self.cookies or not self.cookies.get("_m_h5_tk", ""):
            raise Exception("cookie not found _m_h5_tk")

        cookie_list = self.cookies.get("_m_h5_tk", "").split("_")
        if len(cookie_list) < 2:
            raise Exception("cookie _m_h5_tk not found '_' ")

        self.token: str = cookie_list[0]

    def get_sign(self, data: str, t: int) -> str:
        text = f"{self.token}&{t}&{app_key}&{data}"
        sign = Sign()
        sign_str = sign.sign(text)
        return sign_str
