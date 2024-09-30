"""
HelixFold3模型任务提交API使用示例
"""
import os

from utils import file_util
from cli.client import APIClient


# 直接输入JSON数据
print("=================== 直接输入JSON提交任务 ===================")
data = {
    "name": "7xwo_chain_F_22",
    "recycle": 4,
    "ensemble": 1,
    "entities": [
        {
            "type": "protein",
            "sequence": "HKTDSFVGLMA",
            "count": 2
        }
    ]
}
resp = APIClient.HelixFold3.submit(data)
print(f"code: {resp.code} msg: {resp.msg} taskID: {resp.data.task_id}")


# 从JSON文件加载数据，对应文件在case_files/api_helixfold3_1
print("=================== 输入JSON文件路径提交任务 ===================")
path = os.path.join(os.getenv("PROJECT_ROOT"), "examples/case_files/api_helixfold3_1")
data = file_util.parse_json_from_file(path)
resp = APIClient.HelixFold3.submit(file_path=path)
print(f"code: {resp.code} msg: {resp.msg} taskID: {resp.data.task_id}")
