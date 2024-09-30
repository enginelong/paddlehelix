"""
命令行指令执行器
"""
import os.path
import time

from api.code import ErrorCode
from api.config import ApiTaskStatusFailed, ApiTaskStatusDoing, ApiTaskStatusCancel
from cli.client import APIClient
from utils import file_util


def execute(input_path: str, output_path: str):
    # 数据校验
    if not os.path.exists(input_path):
        print(f"input_path: {input_path} is not exist")
        return
    if not os.path.exists(output_path):
        file_util.create_directories(output_path)

    # 1、获取文件数据
    submitType = 'single'
    if os.path.isfile(input_path):
        contentType = file_util.check_json_type(input_path)
        if contentType != 'list' and contentType != 'dict':
            print("文件内容格式错误，正确格式为JSON列表/JSON")
            return
        if contentType == 'list':
            submitType = 'batch'
    else:
        submitType = 'batch'

    # 2、提交任务
    if submitType == 'single':
        single_task_execute(input_path, output_path)
        return
    batch_task_execute(input_path, output_path)


def single_task_execute(input_path: str, output_path: str):
    print("开始提交任务")
    resp = APIClient.HelixFold3.submit(file_path=input_path)
    if resp.code == ErrorCode.FAILURE.value:
        print("任务提交失败")
        return
    taskID = resp.data.task_id
    print(f"任务提交成功，任务ID：{taskID}")

    # 1、轮询模式查询结果
    print("开始轮询结果")
    resp = APIClient.Common.query_task_info(taskID)
    count = 0
    while True and count < 3:
        if resp.code == ErrorCode.FAILURE:
            count += 1
            continue
        count = 0
        status = resp.data.status
        if status == ApiTaskStatusCancel:
            print("任务已经取消")
            return
        elif status == ApiTaskStatusFailed:
            print("任务执行失败")
            return
        elif status == ApiTaskStatusDoing:
            print("-> 任务正在执行...")
            resp = APIClient.Common.query_task_info(taskID)
        else:
            break
        time.sleep(5)
    if resp.code == ErrorCode.FAILURE:
        print("任务结果查询接口异常")
        return
    print("任务执行成功")

    # 2、下载任务执行结果文件
    print("开始下载任务结果")
    save_dir = APIClient.Common.download_task_result(output_path, taskID)
    print(f"任务执行结果下载成功，文件保存目录是：{save_dir}")


def batch_task_execute(input_path: str, output_path: str):
    print("批量提交任务")
    resp = APIClient.HelixFold3.batch_submit(file_path=input_path) if os.path.isfile(input_path) else \
        APIClient.HelixFold3.batch_submit(file_dir=input_path)
    taskIDs = []
    for r in resp:
        if r.code == ErrorCode.SUCCESS.value:
            taskIDs.append(r.data.task_id)
    print(f"任务数量：{len(resp)} 成功批量提交任务数量：{len(taskIDs)}")
    print(f'任务ID列表：{" ".join([str(task_id) for task_id in taskIDs])}')
    if len(taskIDs) == 0:
        return

    # 1、轮询模式查询结果
    print("开始批量轮询结果")
    resp2 = APIClient.Common.query_task_infos(taskIDs)
    count = 0
    while True and count < 3:
        count = 0
        inactivate = 0
        for r in resp2:
            if r.data.status != ApiTaskStatusDoing:
                inactivate += 1
        if inactivate >= len(taskIDs):
            break
        print(f"-> 剩余运行中任务数量：{len(taskIDs) - inactivate}")
        resp2 = APIClient.Common.query_task_infos(taskIDs)
        time.sleep(5)
    if count >= 3:
        print("任务结果批量查询接口异常")
        return

    # 2、下载任务执行结果文件
    print("开始批量下载任务结果")
    save_dir_list = APIClient.Common.download_task_results(output_path, taskIDs)
    print(f"任务执行结果批量下载成功，文件保存目录列表如下")
    for save_dir in save_dir_list:
        print(f"-> {save_dir}")







