"""
存放各种API对应的请求、响应体数据结构
"""

import json
from api.code import ErrorCode


class SubmitTaskResponse:
    def __init__(self, code: int = 0, msg: str = "", data: dict = None):
        self.code = code
        self.msg = msg
        self.data = self.Data(data)

    class Data:
        def __init__(self, sub_data: dict = None):
            self.task_id = sub_data["task_id"] if sub_data is not None else 0
            # self.idx = sub_data["idx"] if sub_data is not None else 0
            # self.filename = sub_data["filename"] if sub_data is not None else ""

        def to_json(self):
            return {
                "task_id": self.task_id
            }

    def to_json(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data.to_json()
        }


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

            self.__result_dict = None
            if len(self.result) > 0:
                self.__result_dict = json.loads(self.result)

        def get_urls(self) -> tuple:
            return self.get_download_url(), self.get_file_url(), self.get_log_url()

        def get_download_url(self) -> str:
            if self.__result_dict is not None:
                return self.__result_dict['download_url']
            return ""

        def get_file_url(self) -> str:
            if self.__result_dict is not None:
                return self.__result_dict['file_url']
            return ""

        def get_log_url(self) -> str:
            if self.__result_dict is not None:
                return self.__result_dict['log_path']
            return ""

        def to_json(self):
            return {
                "status": self.status,
                "run_time": self.run_time,
                "result": self.result
            }

    def to_json(self):
        return {
            "code": self.code,
            "msg": self.msg,
            "data": self.data.to_json()
        }

