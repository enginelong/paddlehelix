"""
PaddleHelix任务取消API使用示例
"""

import os

from cli.client import APIClient
from utils import file_util

# 取消单个任务
print("=================== 取消任务 ===================")
task_id = 65106
APIClient.Common.cancel_task(task_id)


# 批量取消任务
print("=================== 批量取消任务 ===================")
task_ids = [65106, 65107, 65108]
APIClient.Common.cancel_task(task_id)
