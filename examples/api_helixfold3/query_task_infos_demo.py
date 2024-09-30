"""
HelixFold3模型批量获取任务执行结果API使用示例
    1、批量查询任务执行结果API中task_ids是执行批量提交任务API后成功响应时返回的任务ID列表
"""

from cli.client import APIClient


# 查询多个任务执行结果
print("=================== 多个任务执行结果批量查询 ===================")
task_ids = [65106, 65107, 65108]
resp = APIClient.Common.query_task_infos(task_ids)
for r in resp:
    print(f"code: {r.code} msg: {r.msg} result: {r.data.result}")



