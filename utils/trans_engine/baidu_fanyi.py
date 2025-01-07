import requests
import random
import json
from hashlib import md5


class Baidu:
    def __init__(self, appid, appkey):
        self.appid = appid
        self.appkey = appkey
        endpoint = "https://api.fanyi.baidu.com"
        path = "/api/trans/vip/translate"
        self.url = endpoint + path

    def _make_md5(self, s, encoding="utf-8"):
        return md5(s.encode(encoding)).hexdigest()

    def setProxy(self, address: str = "", port: int = 0, unset=False):
        pass

    def translate(self, text, fromLang="auto", toLang="zh") -> tuple:
        query = text
        salt = random.randint(32768, 65536)
        sign = self._make_md5(self.appid + query + str(salt) + self.appkey)

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "appid": self.appid,
            "q": query,
            "from": fromLang,
            "to": toLang,
            "salt": salt,
            "sign": sign,
        }

        r = requests.post(self.url, params=payload, headers=headers)
        result_json = json.loads(r.text)
        result_list = []

        if "error_code" in result_json:
            return result_json["error_msg"], f"失败 {r.status_code if r else '未知'}"
        else:
            for result in result_json["trans_result"]:

                result_list.append(result["dst"])
            return "\n".join(result_list), "成功"

    def baidu_zh2en(self, text: str) -> tuple:
        return self.translate(text, "zh", "en")

    def baidu_en2zh(self, text: str) -> tuple:
        return self.translate(text, "en", "zh")

    def en2zh(self, text: str) -> tuple:
        return self.baidu_en2zh(text)

    def zh2en(self, text: str) -> tuple:
        return self.baidu_zh2en(text)


if __name__ == "__main__":
    baidu = Baidu("xxxx", "xxxx")
    print(baidu.baidu_en2zh("hello world"))
    print(baidu.baidu_zh2en("请问你是谁"))
    print(md5("xxxx".encode("utf-8")).hexdigest())
