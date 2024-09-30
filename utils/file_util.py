"""
文件操作工具方法
"""

import json
import os
import shutil
from datetime import datetime
from typing import Any
from urllib.parse import urlparse

import requests


def download_file(save_dir: str, filename: str, url: str = "") -> str:
    """
    下载文件
    :param save_dir: 保存目录
    :param filename: 下载文件名
    :param url: 下载URL
    :return: 文件保存路径 download_dir + '/' + filename
    """
    try:
        create_directories(save_dir)
    except RuntimeError:
        return ""
    path = ""
    try:
        # 发起 GET 请求，stream=True 表示流式下载
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 检查请求是否成功

        # 打开目标文件进行写入
        path = "".join([save_dir, '/', filename])
        with open(path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):  # 按块读取内容
                if chunk:  # 确保块不为空
                    file.write(chunk)  # 写入文件

        print(f"-> 文件 {filename} 已成功下载到: {path}")

    except requests.exceptions.RequestException as e:
        print(f"文件 {filename} 下载失败: {e}")
    return path


def parse_filename_from_url(url: str) -> str:
    # 解析 URL
    parsed_url = urlparse(url)

    # 获取路径部分
    path = parsed_url.path

    # 提取文件名
    filename = os.path.basename(path)

    return filename


def clear_dir(target_dir: str) -> bool:
    """
    清空该目录，目录存在则清空目录中所有文件/文件夹；目录不存在则新建目录
    :param target_dir: 目标目录路径
    :return: True 表示操作成功；False 表示操作异常
    """
    try:
        # 检查目录是否存在
        if os.path.exists(target_dir):
            # 清空目录中的所有文件和子目录
            for filename in os.listdir(target_dir):
                file_path = os.path.join(target_dir, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # 删除文件或符号链接
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # 递归删除子目录
        else:
            # 如果目录不存在，则创建
            os.makedirs(target_dir)
        return True
    except Exception as e:
        print(f"清空目录时出现异常: {e}")
        return False


def parse_json_from_file(file_path: str) -> dict[str, Any]:
    """
    读取文件，将内容解析成json对象

    :param file_path: JSON 文件的路径
    :return: 解析后的 JSON 数据（字典）
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"文件内容不是有效的 JSON: {file_path}")
        return {}
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return {}


def parse_json_list_from_file(file_path: str) -> list[dict[str, Any]]:
    """
    读取文件，将内容解析成列表，每个元素是一个json对象

    :param file_path: JSON 文件的路径
    :return: 解析后的 JSON 列表（列表）
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 确保读取的数据是列表
        if isinstance(data, list):
            return data
        else:
            print(f"文件内容不是有效的 JSON 列表: {file_path}")
            return []
    except FileNotFoundError:
        print(f"文件未找到: {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"文件内容不是有效的 JSON: {file_path}")
        return []
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return []


def check_json_type(file_path: str) -> str:
    """
    判断 JSON 文件内部是列表还是字典。

    :param file_path: JSON 文件路径
    :return: 返回 'list' 如果是列表，返回 'dict' 如果是字典，返回 'invalid' 如果格式不正确
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)  # 解析 JSON 文件

            if isinstance(data, list):
                return 'list'  # 如果是列表
            elif isinstance(data, dict):
                return 'dict'  # 如果是字典
            else:
                return 'invalid'  # 既不是列表也不是字典
    except json.JSONDecodeError:
        return 'invalid'  # JSON 格式错误
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return 'invalid'  # 其他异常情况


def create_directories(dir_path: str):
    """创建多级目录，如果目录已存在则不做任何操作."""
    try:
        if os.path.exists(dir_path):
            return
        os.makedirs(dir_path, exist_ok=True)  # exist_ok=True 允许目录已存在
    except Exception as e:
        print(f"创建目录 {dir_path} 时出错: {e}")
        raise RuntimeError(f"创建目录时出错: {e}")


def generate_directory_name() -> str:
    """生成目录名，格式为 'batch-download-timestamp'."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # 获取当前时间戳
    directory_name = f"batch-download-{timestamp}"  # 生成目录名
    return directory_name


def assemble_file_path(path: str) -> str:
    """
    装配绝对路径
    :param path: 文件相对路径
    :return: 文件绝对路径
    """
    return os.path.join(os.getenv("PROJECT_ROOT"), path)
