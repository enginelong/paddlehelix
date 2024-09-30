"""
HelixFold3模型API调用
"""
import os
from typing import Any

import requests

from api.auth import APIAuthUtil
from api.code import ErrorCode
from api.config import HOST, SCHEME
from api.registry import ServerAPIRegistry
from api.structures import SubmitTaskResponse
from utils import file_util


class HelixFold3Client:
    def __init__(self, ak: str = "", sk: str = ""):
        self._ak = ak
        self._sk = sk
        self.__authClient = APIAuthUtil(ak, sk)

    def submit(self, data: dict = None, **kwargs) -> SubmitTaskResponse:
        """
        HelixFold3任务提交API
        :param data:
            examples:
                {
                    "entities": [
                        {
                            "type": "ion",
                            "count": 2,
                            "ccd": "CA"
                        }
                    ],
                    "recycle": 20,
                    "ensemble": 10,
                    "name": "test-demo"
                }
        :return:
            examples:
                {
                    "code": 0,
                    "msg": "",
                    "data": {
                        "task_id": 65593
                    }
                }
        """
        # 尝试从JSON文件中加载数据
        file_path = kwargs.get("file_path", "")
        if len(file_path) > 0:
            data = file_util.parse_json_from_file(file_path)
        if data is None or len(data) == 0:
            return SubmitTaskResponse(code=ErrorCode.FAILURE.value, msg="", data=None)
        response = requests.post("".join([SCHEME, HOST, ServerAPIRegistry.HelixFold3.submit.uri]),
                                 headers=self.__authClient.generate_header(ServerAPIRegistry.HelixFold3.submit.uri),
                                 json=data)
        idx, filename = kwargs.get("idx", 0), kwargs.get("filename", "")
        if response.status_code == 200:
            respJson = response.json()
            if respJson.get("code") == ErrorCode.SUCCESS.value:
                return SubmitTaskResponse(
                    code=ErrorCode.SUCCESS.value,
                    msg=respJson.get("msg", ""),
                    data=respJson.get("data", None)
                )
        return SubmitTaskResponse(code=ErrorCode.FAILURE.value, msg="")

    def batch_submit(self, data: list[dict[str, Any]] = None, **kwargs) -> list[SubmitTaskResponse]:
        """
        HelixFold3任务批量提交API
        :param data:
            examples:
                [
                    {
                        "entities": [
                            {
                                "type": "ion",
                                "count": 2,
                                "ccd": "CA"
                            }
                        ],
                        "recycle": 20,
                        "ensemble": 10,
                        "name": "test-demo"
                    },
                    {xxx}
                ]
        :return:
            examples:
                [
                    {
                        "code": 0,
                        "msg": "",
                        "data": {
                            "task_id": 65593
                        }
                    }
                ]
        """
        res = []
        if data is None or len(data) == 0:
            file_path = kwargs.get("file_path", "")
            if len(file_path) > 0:
                data = file_util.parse_json_list_from_file(file_path)

        if data is not None and len(data) > 0:
            for idx, task in enumerate(data):
                res.append(self.submit(task, idx=idx))
            return res
        file_dir = kwargs.get("file_dir", "")
        if len(file_dir) <= 0:
            return res
        files = [(os.path.join(file_dir, file), file) for file in os.listdir(file_dir)
                 if os.path.isfile(os.path.join(file_dir, file))]
        for file_path, filename in files:
            res.append(self.submit(file_path=file_path, filename=filename))
        return res
