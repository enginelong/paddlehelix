"""
HelixFold3模型任务批量提交API使用示例
    1、批量提交任务API目前指在客户端循环提交，暂不支持服务端批量提交
"""
import os

from utils import file_util
from cli.client import APIClient


# 直接输入JSON数据
print("=================== 直接输入JSON批量提交任务 ===================")
data = [
    {
        "name": "7xwo_chain_F_22",
        "entities": [
            {
                "type": "protein",
                "sequence": "HKTDSFVGLMA",
                "count": 2
            }
        ]
    },
    {
        "name": "7xwo_chain_F_23",
        "entities": [
            {
                "type": "protein",
                "sequence": "HKTDSFVGLMA",
                "count": 4
            }
        ]
    }
]
resp = APIClient.HelixFold3.batch_submit(data)
for r in resp:
    print(f"code: {r.code} msg: {r.msg} taskID: {r.data.task_id}")


# 从JSON列表文件加载数据，对应文件在case_files/api_helixfold3_1
print("=================== 输入JSON文件路径批量提交任务 ===================")
path = file_util.assemble_file_path("examples/case_files/api_helixfold3_2")
data = file_util.parse_json_list_from_file(path)
resp = APIClient.HelixFold3.batch_submit(file_path=path)
for r in resp:
    print(f"code: {r.code} msg: {r.msg} taskID: {r.data.task_id}")

