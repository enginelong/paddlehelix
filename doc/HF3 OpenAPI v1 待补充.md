# HF3 OpenAPI

通过OpenAPI进行批量任务预测适用于生产环境。目前限制白名单使用，如需使用请工单联系开通。



## 接口说明

#### **准备工作**

1. 获取生成接口鉴权信息所需的访问密钥ID(AK)及秘密访问密钥(SK)，参考：[如何获取AKSK](https://cloud.baidu.com/doc/Reference/s/9jwvz2egb)﻿
2. 开通 CHPC 服务：[开通页](https://console.bce.baidu.com/chpc/#/landing)﻿

#### **接口描述**

该接口可用于提交和查看HelixFold任务。

#### **接口鉴权**

1. 百度云如何对您的API请求进行鉴权

   当您将HTTP请求发送到百度智能云时，您需要对您的请求进行签名计算，以便百度智能云可以识别您的身份。您将使用百度智能云的访问密钥来进行签名计算，该访问密钥包含**访问密钥ID**(Access Key Id, 后文简称**AK**)和**秘密访问密钥**(Secret Access Key, 后文简称**SK**).

   了解如何创建、查看和下载Access Key Id(AK)和Secret Access Key(SK), 请参考[如何获取AKSK](https://cloud.baidu.com/doc/Reference/s/9jwvz2egb)﻿

2. 签名API请求

   在请求签名之前，请先计算请求的哈希(摘要)。然后，您使用哈希值、来自请求的其他信息以及您的秘密访问密钥(Secret Access Key，SK)，计算另一个称为**签名(Signature)**的哈希, 得到**签名**后，进行一定规则的拼装成最终的**认证字符串**，也就是最终您需要包含在API请求中的**Authorization**字段。

您可以通过以下方式携带认证字符串：

- - 在HTTP Header中包含认证字符串
  - 在URL中包含认证字符串用户也可以将认证字符串放在HTTP请求Query String的authorization参数中。常用于生成URL给第三方使用的场景，例如要临时把某个数据开放给他人下载。关于如何在URL中包含认证字符串，请参考[在URL中包含认证字符串](https://cloud.baidu.com/doc/Reference/s/3jwvz1x2e)。

您可以参看[从零开始用Python调用API接口](https://cloud.baidu.com/doc/APIGUIDE/s/3k1mz24k5)，视频的前半部分介绍了百度智能云鉴权认证机制，帮助您更快的进行了解。

3. 使用 Python 进行请求的鉴权代码样例

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import hashlib
import hmac
import urllib
import time

# 1.AK/SK、host、method、URL绝对路径、querystring
AK = "input your AK"
SK = "input your SK"
host = "chpc.bj.baidubce.com"
method = "POST"
query = ""
URI = "/api/submit/helixfold3"

# 2.x-bce-date
x_bce_date = time.gmtime()
x_bce_date = time.strftime('%Y-%m-%dT%H:%M:%SZ',x_bce_date)

# 3.header和signedHeaders
header = {
        "Host":host,
        "content-type":"application/json;charset=utf-8",
        "x-bce-date":x_bce_date
        }
signedHeaders = "content-type;host;x-bce-date"

# 4.认证字符串前缀
authStringPrefix = "bce-auth-v1" + "/" +AK + "/" +x_bce_date + "/" +"1800"

# 5.生成CanonicalRequest
#5.1生成CanonicalURI
CanonicalURI = urllib.parse.quote(URI)        # windows下为urllib.parse.quote，Linux下为urllib.quote
#5.2生成CanonicalQueryString
CanonicalQueryString = query           # 如果您调用的接口的query比较复杂的话，需要做额外处理
#5.3生成CanonicalHeaders
result = []
for key,value in header.items():
    tempStr = str(urllib.parse.quote(key.lower(),safe="")) + ":" + str(urllib.parse.quote(value,safe=""))
    result.append(tempStr)
result.sort()
CanonicalHeaders = "\n".join(result)
#5.4拼接得到CanonicalRequest
CanonicalRequest = method + "\n" + CanonicalURI + "\n" + CanonicalQueryString +"\n" + CanonicalHeaders

# 6.生成signingKey
signingKey = hmac.new(SK.encode('utf-8'),authStringPrefix.encode('utf-8'),hashlib.sha256)

# 7.生成Signature
Signature = hmac.new((signingKey.hexdigest()).encode('utf-8'),CanonicalRequest.encode('utf-8'),hashlib.sha256)

# 8.生成Authorization并放到header里
header['Authorization'] = authStringPrefix + "/" +signedHeaders + "/" +Signature.hexdigest()

# 9.发送API请求并接受响应
import requests
import json

body={
      "name" : "QQQQQQ"      
      }

url = "http://"+host + URI 

r = requests.put(url,headers = header,data=json.dumps(body))

print(r.text)
```

﻿

#### **接口信息**

**HelixFold3 作业提交**

| 内容     | 说明                                             |
| -------- | ------------------------------------------------ |
| HTTP方法 | POST                                             |
| 请求地址 | http://chpc.bj.baidubce.com/api/submit/helixfold |
| 接口鉴权 | 详见上方“接口鉴权”部分说明                       |

请求参数：

```JSON
{
  "name": "Protein-RNA-Ion: PDB 8AW3",           # string | 任务名，如未指定，则系统自动生成
  "recycle": 4,                                      # 可选，int | 范围[1,100]。模型推理参数，影响模型效果，越大越好。如果用户不设置，默认设为4。
	"ensemble": 1,                                     # 可选，int | 范围[1,100]。模型推理参数，影响模型效果，越大越好。如果用户不设置，默认设为1。
  "entities": [                                      # list | 定义各种实体。支持的实体类型：“protein”，“dna”，“rna”，“ion”，“ligand”。注：每个任务中所有实体加起来总token数量不能超过2000，不同实体的token计算方式见下方注释或参见HelixFold3 FAQ部分。
    {
      "type": "protein",                             # string | 实体类型（此处以蛋白为例）
      "sequence": "GPDSMEEVVVPEEPPKLVSALATYVQQERLCTMFLSIANKLLPLKP",    # string | 蛋白序列，仅支持20种标准氨基酸。一个氨基酸算做一个token，最大不可超过2000。
      "count": 1                                     # int | 实体复制数量
    },
    {
      "type": "ion",                                 # string | 实体类型（此处以离子为例）
      "ccd": "ZN",                                   # string | 离子的CCD标准名字。目前支持的离子列表请参考下一个代码块“离子CCD列表”。一个离子算作一个token。
      "count": 2                                     # int | 实体复制数量。实体为离子时，数量不可超过50。
    },
    {
      "type": "dna",                                 # string | 实体类型（此处以DNA为例）
      "sequence": "ACGTTTACGGGG",                    # string | DNA序列，仅支持4种标准脱氧核糖核酸ATCG。一个核苷酸算做一个token，最大不可超过2000。
      "count": 1                                     # int | 实体复制数量
    },
    {
      "type": "ligand",                              # string | 实体类型（此处以配体为例）
      "ccd": "ATP",                                  # string | 支持用户用CCD输入小分子配体，CCD和下方的SMILES只需输入其中一个即可。如果两个字段中都有输入，则以CCD的输入为准。配体中的一个原子算做一个token。注：水、助剂和少量特殊的配体目前是模型所不支持的，我们会将这些配体从CCD列表中除去，如果您通过输入SMILES的方式进行了这些输入，可能会造成结果的表现下降。具体不支持的配体的CCD列表参见[HelixFold3 FAQ]。
      "smiles": "CCccc(O)ccc",                       # string | 小分子的SMILES，重核数量需在50以内。SMILES和上方的CCD只需输入其中一个即可。如果两个字段中都有输入，则以CCD的输入为准。配体中的一个原子算做一个token。
      "count": 1                                     # int | 实体复制数量。实体为配体时，数量不可超过50。
    },
    {
      "type": "ion",                                 # 同上离子部分。
      "ccd": "ZN",
      "count": 1
    },
    {
      "type": "dna",                                 # 同上 dna 部分。
      "sequence": "CCCCGTAAACGT",
      "count": 1
    },
    {
      "type": "rna",                                 # string | 实体类型（此处以RNA为例）
      "sequence": "ACCCCCCC",                        # string | 序列，仅支持4种标准核糖核酸AUCG。一个核苷酸算做一个token，最大不可超过2000。
      "count": 1                                     # int | 实体复制数量。
    }
  ]
}
```

返回参数

```go
{
    "code": 0,         # int | 状态码
    "msg": "xxx",      # string ｜ 提示信息
    "data": {
        "task_id": 123 # uint64 ｜ 任务ID
    }
}
```

﻿

**HelixFold3 任务结果查询**

| 内容     | 说明                                      |
| -------- | ----------------------------------------- |
| HTTP方法 | POST                                      |
| 请求地址 | http://chpc.bj.baidubce.com/api/task/info |
| 接口鉴权 | 详见上方“接口鉴权”部分说明                |

请求参数

```go
{
   "task_id": 123 # uint64 ｜ 任务ID
}
```

返回参数

```go
{
    "code": 0,                 # int | 状态码
    "msg": "xxx",              # string ｜ 提示信息
    "data": {
		"status":   10,        # 任务执行状态
		"run_time": 123,       # 任务执行时间
		"result": "http:xxx",  # 结果临时下载URL
	}
}
```



## API示例

该部分提供了一个封装好地API示例。您可以将下方代码保存至本地文件，替换代码中的信息即可轻松调用API。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HelixFold3模型的API调用
    1、使用测试类测试功能时，注意在TestHF3中修改AK、SK
    2、测试获取任务执行结果API时，注意参数task_id是执行提交任务API后成功响应时返回的任务ID
"""

import hashlib
import hmac
import os
import urllib
import time
from typing import Any

import requests


# 定义业务请求成功、失败码
CODE_SUCCESS = 0
CODE_FAILURE = 1

# 定义基础请求变量
Host = "chpc.bj.baidubce.com"
Method = "POST"
Query = ""
SignedHeaders = "content-type;host;x-bce-date"
AuthExpireTime = 1800  # second


class AuthUtil:
    def __init__(self, ak: str = "", sk: str = ""):
        self.__ak = ak
        self.__sk = sk

        assert len(self.__ak.strip()) > 0, "AK 为空"
        assert len(self.__sk.strip()) > 0, "SK 为空"


    def generate_header(self, uri: str = "") -> dict:
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


class SubmitTaskResponse:
    def __init__(self, code: int = 0, msg: str = "", data: dict = None):
        self.code = code
        self.msg = msg
        self.data = self.Data(data)

    class Data:
        def __init__(self, sub_data: dict = None):
            self.task_id = sub_data["task_id"] if sub_data is not None else 0


class QueryTaskInfoResponse:
    def __init__(self, code: int = 0, msg: str = "", data: dict = None):
        self.code = code
        self.msg = msg
        self.data = self.Data(data)

    class Data:
        def __init__(self, sub_data: dict = None):
            self.status = sub_data.get("status", 0) if sub_data else 0
            self.run_time = sub_data.get("run_time", 0) if sub_data else 0
            self.result = sub_data.get("result", "") if sub_data else ""


class APIClient:
    def __init__(self, ak: str = "", sk: str = ""):
        self.ak = os.getenv('AK', ak)
        self.sk = os.getenv("SK", sk)
        self.__authClient = AuthUtil(ak, sk)

    def submit(self, data: dict, uri: str) -> SubmitTaskResponse:
        response = requests.post(APIClient.assemble_url(uri),
                                 headers=self.__authClient.generate_header(uri),
                                 json=data)
        if response.status_code == 200:
            respJson = response.json()
            if respJson.get("code") == CODE_SUCCESS:
                return SubmitTaskResponse(
                    code=CODE_SUCCESS,
                    msg=respJson.get("msg", ""),
                    data=respJson.get("data", None)
                )
        return SubmitTaskResponse(code=CODE_FAILURE, msg="", data=None)

    def batch_submit(self, data: list[dict[str, Any]], uri: str) -> list[SubmitTaskResponse]:
        res = []
        for task in data:
            response = requests.post(APIClient.assemble_url(uri), json=task, headers=self.__authClient.generate_header(uri))
            if response.status_code == 200:
                respJson = response.json()
                if respJson.get("code") == CODE_SUCCESS:
                    res.append(SubmitTaskResponse(
                        code=CODE_SUCCESS,
                        msg=respJson.get("msg", ""),
                        data=respJson.get("data", None)
                    ))
                else:
                    res.append(SubmitTaskResponse(
                        code=CODE_FAILURE,
                        msg="",
                        data=None
                    ))
        return res

    def query_task_info(self, data: dict, uri: str) -> QueryTaskInfoResponse:
        response = requests.post(APIClient.assemble_url(uri),
                                 headers=self.__authClient.generate_header(uri),
                                 json=data)
        if response.status_code == 200:
            respJson = response.json()
            if respJson.get("code") == CODE_SUCCESS:
                return QueryTaskInfoResponse(code=CODE_SUCCESS,
                    msg=respJson.get("msg", ""),
                    data=respJson.get("data", None)
                )
        return QueryTaskInfoResponse(code=CODE_FAILURE, msg="", data=None)

    @staticmethod
    def assemble_url(uri: str) -> str:
        return "".join(["http://", Host, uri])


# class TestHF3:
#     client = APIClient("xxx", "xxx")
#
#     @classmethod
#     def test_submit(cls):
#         data = {
#             "name": "7xwo_chain_F_22",
#             "entities": [
#                 {
#                     "type": "protein",
#                     "sequence": "HKTDSFVGLMA",
#                     "count": 2
#                 }
#             ]
#         }
#         resp = cls.client.submit(data, "/api/submit/helixfold3")
#         output = f"code: {resp.code} msg: {resp.msg} taskID: {resp.data.task_id}"
#         print(output)
#
#     @classmethod
#     def test_get_task_info(cls):
#         data = {
#             "task_id": 111
#         }
#         resp = cls.client.query_task_info(data, "/api/task/info")
#         output = f"code: {resp.code} msg: {resp.msg} result: {resp.data.result}"
#         print(output)
#
#     @classmethod
#     def test_batch_submit(cls):
#         data = [
#             {
#                 "name": "7xwo_chain_F_22",
#                 "entities": [
#                     {
#                         "type": "protein",
#                         "sequence": "HKTDSFVGLMA",
#                         "count": 2
#                     }
#                 ]
#             },
#             {
#                 "name": "7xwo_chain_F_23",
#                 "entities": [
#                     {
#                         "type": "protein",
#                         "sequence": "HKTDSFVGLMA",
#                         "count": 4
#                     }
#                 ]
#             }
#         ]
#         resp = cls.client.batch_submit(data, "/api/submit/helixfold3")
#         for r in resp:
#             output = f"code: {r.code} msg: {r.msg} taskID: {r.data.task_id}"
#             print(output)
#
#
# if __name__ == '__main__':
#     # 测试HelixFold3任务提交功能
#     print("============ 测试HelixFold3任务提交功能 ============")
#     TestHF3.test_submit()
#
#     # 测试HelixFold3任务批量提交功能
#     print("============ 测试HelixFold3任务批量提交功能 ============")
#     TestHF3.test_batch_submit()
#
#     # 测试HelixFold3任务结果获取功能，taskID是任务提交功能中获取得到的任务ID
#     print("============ 测试HelixFold3任务结果获取功能 ============")
#     TestHF3.test_get_task_info()
```



## 批量提交API

该部分给您提供一个可以用于批量提交API的示例。您可以将下方代码保存至本地文件，根据操作步骤执行即可轻松批量提交HelixFold3任务。

```
见上述API示例
```

