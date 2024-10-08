"""
PaddleHelix任务结果下载工具API使用示例
"""

import os

from cli.client import APIClient
from utils import file_util

# 下载单个任务执行结果
print("=================== 单个任务执行结果下载 ===================")
output_dir = file_util.assemble_file_path('output')
task_id = 65106
download_dir = APIClient.Common.download_task_result(output_dir, task_id)
print(f"download task: {task_id} result files into {download_dir}")
