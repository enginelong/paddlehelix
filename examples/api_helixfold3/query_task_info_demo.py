"""
HelixFold3模型获取任务执行结果API使用示例
    1、查询任务执行结果API中task_id是执行提交任务API后成功响应时返回的任务ID
"""

from cli.client import APIClient


# 查询单个任务执行结果
print("=================== 单个任务执行结果查询 ===================")
task_id = 65106
resp = APIClient.Common.query_task_info(task_id)
output = f"code: {resp.code} msg: {resp.msg} result: {resp.data.result}"
print(output)



