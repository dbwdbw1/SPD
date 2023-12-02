import base64
import json
from typing import Dict

import requests

import utils.common
import utils.request
from consts import headers, app_key
from image_search.token import Token


def get_data(filename: str) -> Dict[str, str]:
    # get file bytes
    with open(filename, "rb") as f:
        b64_bytes = base64.b64encode(f.read())
    data = json.dumps(
        {
            "imageBase64": str(b64_bytes).replace("b'", "").replace("'", ""),
            "appName": "searchImageUpload",
            "appKey": "pvvljh1grxcmaay2vgpe9nb68gg9ueg2",
        },
        separators=(",", ":"),
    )
    return {"data": data}


# 上传图片业务类
class Ali1688Upload(Token):
    def __init__(self, api: str = "mtop.1688.imageService.putImage", hostname="h5api.m.taobao.com"):
        super(Ali1688Upload, self).__init__(api=api, hostname=hostname)
        self.upload_url = f"https://{self.hostname}/h5/{self.api.lower()}/1.0"
        self.request()
        self._get_token()

    def get_params(self, data: str, t: int, jsv: str = "2.4.11") -> Dict[str, str]:
        sign_str = self.get_sign(data=data, t=t)
        params = {
            "jsv": jsv,
            "appKey": app_key,
            "t": str(t),
            "api": self.api,
            "ecode": "0",
            "v": "1.0",
            "type": "originaljson",
            "dataType": "jsonp",
            "sign": sign_str,
        }
        return params

    def upload(self, filename: str) -> requests.request:
        # upload image
        t = utils.common.now()
        data = get_data(filename=filename)
        params = self.get_params(data=data.get("data", ""), t=t)
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        req = utils.request.request_post(
            url=self.upload_url,
            params=params,
            headers=headers,
            data=data,
            cookies=self.cookies.get_dict(),
        )
        return req
