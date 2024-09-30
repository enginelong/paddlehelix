"""
PaddleHelix任务结果批量下载工具API使用示例
"""

import os

from cli.client import APIClient

# 下载多个任务执行结果
print("=================== 多个任务执行结果批量下载 ===================")
output_dir = os.path.join(os.getenv("PROJECT_ROOT"), "output")
task_id = [65106, 65107, 65108]
download_dir = APIClient.Common.download_task_results(output_dir, task_id)
print(f"download task results files into {download_dir}")
