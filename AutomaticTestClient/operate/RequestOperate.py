import requests


class HttpRequest(object):
    """不记录任何的请求方法"""

    @classmethod
    def request(cls, method, url, data=None, headers=None):
        method = method.upper()
        if method == 'POST':
            return requests.post(url=url, data=data, headers=headers)
        elif method == 'GET':
            return requests.get(url=url, params=data, headers=headers)


class HttpSession(object):
    """记录Session的方法"""

    def __init__(self):
        self.session = requests.session()

    def request(self, method, url, data=None, json=None, headers=None, cookies=None, files=None):
        method = method.upper()
        if method == 'POST':
            return self.session.post(url=url, data=data, json=json, headers=headers, cookies=cookies, files=files, verify=False)
        elif method == 'GET':
            return self.session.get(url=url, params=data, json=json, headers=headers, cookies=cookies, files=files, verify=False)
        elif method == 'PUT':
            return self.session.put(url=url, params=data, json=json, headers=headers, cookies=cookies, files=files, verify=False)

    def close(self):
        """断开session连接的方法"""
        self.session.close()
