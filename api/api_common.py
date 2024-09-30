"""
通用API调用，例如查询任务执行结果
"""

import os

import requests

from api.auth import APIAuthUtil
from api.code import ErrorCode
from api.config import HOST, SCHEME
from api.registry import ServerAPIRegistry
from api.structures import QueryTaskInfoResponse
from utils import file_util


class CommonClient:
    def __init__(self, ak: str = "", sk: str = ""):
        self._ak = ak
        self._sk = sk
        self.__authClient = APIAuthUtil(ak, sk)

    def cancel_task(self, task_id: int = 0, **kwargs):
        """
        取消任务
        :param task_id: 任务ID
        """
        if task_id <= 0:
            return
        requests.post("".join([SCHEME, HOST, ServerAPIRegistry.Common.cancel_task.uri]),
                      headers=self.__authClient.generate_header(ServerAPIRegistry.Common.cancel_task.uri),
                      json={"task_id": task_id})

    def batch_cancel_task(self, task_ids: list = None, **kwargs):
        """
        批量取消任务
        :param task_ids: 任务ID列表
        """
        if task_ids is None or len(task_ids) <= 0:
            return
        for task_id in task_ids:
            requests.post("".join([SCHEME, HOST, ServerAPIRegistry.Common.cancel_task.uri]),
                          headers=self.__authClient.generate_header(ServerAPIRegistry.Common.cancel_task.uri),
                          json={"task_id": task_id})

    def query_task_info(self, task_id: int = 0, **kwargs) -> QueryTaskInfoResponse:
        """
        HelixFold3查询任务处理结果API
        :param task_id: 任务ID
        :return:
            examples:
                {
                    "code": 0,
                    "msg": "",
                    "data": {
                        "status": 10, # 10:运行中，20:取消，30:完成，40:失败
                        "run_time", 10,
                        "result": "{"download_url":"https://","error_code":0,"file_url":"https://","log_path":"https://","rudder_task_id":54423}"
                    }
                }
        """
        if task_id <= 0:
            return QueryTaskInfoResponse(code=ErrorCode.FAILURE.value, msg="", data=None)
        response = requests.post("".join([SCHEME, HOST, ServerAPIRegistry.Common.query_task_info.uri]),
                                 headers=self.__authClient.generate_header(ServerAPIRegistry.Common.query_task_info.uri),
                                 json={"task_id": task_id})
        if response.status_code == 200:
            respJson = response.json()
            if respJson.get("code") == ErrorCode.SUCCESS.value:
                return QueryTaskInfoResponse(code=ErrorCode.SUCCESS.value,
                                             msg=respJson.get("msg", ""),
                                             data=respJson.get("data", None)
                                             )
        return QueryTaskInfoResponse(code=ErrorCode.FAILURE.value, msg="", data=None)

    def query_task_infos(self, task_ids: list[int] = None, **kwargs) -> list[QueryTaskInfoResponse]:
        """
        HelixFold3批量查询任务处理结果API
        :param task_ids: 任务ID列表
        :return:
            examples:
                [
                    {
                        "code": 0,
                        "msg": "",
                        "data": {
                            "status": 10, # 10:运行中，20:取消，30:完成，40:失败
                            "run_time", 10,
                            "result": "{"download_url":"https://","error_code":0,"file_url":"https://","log_path":"https://","rudder_task_id":54423}"
                        }
                    }
                ]
        """
        res = []
        if task_ids is None or len(task_ids) <= 0:
            return res
        for task_id in task_ids:
            response = requests.post("".join([SCHEME, HOST, ServerAPIRegistry.Common.query_task_info.uri]),
                                     headers=self.__authClient.generate_header(ServerAPIRegistry.Common.query_task_info.uri),
                                     json={"task_id": task_id})
            if response.status_code == 200:
                respJson = response.json()
                if respJson.get("code") == ErrorCode.SUCCESS.value:
                    res.append(QueryTaskInfoResponse(
                        code=ErrorCode.SUCCESS.value,
                        msg=respJson.get("msg", ""),
                        data=respJson.get("data", None)))
                else:
                    res.append(QueryTaskInfoResponse(code=ErrorCode.FAILURE.value, msg="", data=None))
        return res

    def download_task_result(self, save_dir: str, task_id: int, idx: int = 0, filename: str = "") -> str:
        """
        下载任务结果
        :param idx: task提交时的顺序索引
        :param filename: task提交时所属文件的文件名
        :param save_dir: 保存目录
        :param task_id: 任务ID
        :return: 文件保存目录 download_dir + '/' + task_id
        """
        try:
            file_util.create_directories(save_dir)
        except RuntimeError:
            return ""
        taskInfo = self.query_task_info(task_id)
        if taskInfo.code != ErrorCode.SUCCESS.value:
            return ""
        target_filename = str(task_id)
        if idx > 0:
            target_filename = "".join([str(idx), '-', target_filename])
        elif len(filename) > 0:
            target_filename = "".join([filename, '-', target_filename])
        target_dir = os.path.join(save_dir, target_filename)
        file_util.clear_dir(target_dir)
        download_url, file_url, log_url = taskInfo.data.get_urls()
        file_util.download_file(target_dir, file_util.parse_filename_from_url(download_url), download_url)
        file_util.download_file(target_dir, file_util.parse_filename_from_url(file_url), file_url)
        file_util.download_file(target_dir, file_util.parse_filename_from_url(log_url), log_url)
        return target_dir

    def download_task_results(self, save_dir: str, task_ids: list[int]) -> list[str]:
        """
        批量下载任务结果
        :param save_dir: 保存目录
        :param task_ids: 任务ID列表
        :return: 文件保存目录列表，对于每个task的结果文件，保存目录为 download_dir + '/' + task_id
        """
        res = []
        parentDir = file_util.generate_directory_name()
        for task_id in task_ids:
            res.append(self.download_task_result(os.path.join(save_dir, parentDir), task_id))
        return res
