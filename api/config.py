"""
公共请求变量
"""

# 请求变量
SCHEME = "http://"
HOST = "chpc.bj.baidubce.com"

# 任务状态
ApiTaskStatusDoing = 2    # 运行中
ApiTaskStatusCancel = 3      # 取消
ApiTaskStatusSucc = 1     # 成功
ApiTaskStatusFailed = -1  # 失败