"""
PaddleHelix鉴权
"""
import hashlib
import hmac
import time
import urllib

Host = "chpc.bj.baidubce.com"
Method = "POST"
Query = ""
SignedHeaders = "content-type;host;x-bce-date"
AuthExpireTime = 1800


class APIAuthUtil:
    def __init__(self, ak: str = "", sk: str = ""):
        self.__ak = ak
        self.__sk = sk

        assert len(self.__ak.strip()) > 0, "AK 为空"
        assert len(self.__sk.strip()) > 0, "SK 为空"

    def generate_header(self, uri: str = "", **kwargs) -> dict:
        assert len(uri) > 0, "uri 为空"
        x_bce_date = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
        header = {
            "Host": Host,
            "content-type": "application/json;charset=utf-8",
            "x-bce-date": x_bce_date
        }
        result = []
        for key, value in header.items():
            tempStr = str(urllib.parse.quote(key.lower(), safe="")) + ":" + str(urllib.parse.quote(value, safe=""))
            result.append(tempStr)
        result.sort()
        canonicalRequest = "".join([Method, "\n", urllib.parse.quote(uri), "\n", Query, "\n", "\n".join(result)])
        authStringPrefix = "".join(["bce-auth-v1", "/", self.__ak, "/", x_bce_date, "/", str(AuthExpireTime)])
        signingKey = hmac.new(self.__sk.encode('utf-8'), authStringPrefix.encode('utf-8'), hashlib.sha256)
        Signature = hmac.new((signingKey.hexdigest()).encode('utf-8'), canonicalRequest.encode('utf-8'), hashlib.sha256)
        header['Authorization'] = authStringPrefix + "/" + SignedHeaders + "/" + Signature.hexdigest()
        return header
