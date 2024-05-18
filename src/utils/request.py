import contextlib

import requests


# 获取post方法的request对象
def request_post(
        url, params=None, data=None, files=None, headers=None, timeout=10, cookies=None
):
    with contextlib.closing(
            requests.post(
                url=url,
                params=params,
                data=data,
                files=files,
                headers=headers,
                cookies=cookies,
                timeout=timeout,
            )
    ) as req:
        return req


# 获取get方法的request对象
def request_get(url, params=None, headers=None, timeout=10, cookies=None):
    with contextlib.closing(
            requests.get(
                url=url, params=params, headers=headers, cookies=cookies, timeout=timeout
            )
    ) as req:
        return req
