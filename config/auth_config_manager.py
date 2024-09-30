"""
配置文件加载工具方法
"""
import os
import threading

import yaml

# 定义配置文件路径
_auth_config_path = os.path.join(os.getenv("PROJECT_ROOT"), "config/auth.yaml")

# 获取互斥锁
_auth_config_lock = threading.Lock()
_ak_sk_lock = threading.Lock()

# 定义全局配置变量
auth_config = {}
_ak, _sk = "", ""

# 定义ak, sk缺失提示信息
_missing_sk_sk_message = """
        未配置用户身份验证信息AK、SK，可以采用以下两种方式配置：
            1、在config/auth.yaml中配置如下信息
                credentials:
                    paddlehelix_api_ak: "xxx"
                    paddlehelix_api_sk: "xxx"
            2、配置环境变量
                export PADDLEHELIX_API_AK="your_access_key"
                export PADDLEHELIX_API_SK="your_secret_key"
    """


def load_config(file_path: str = _auth_config_path) -> dict:
    """
    从配置文件中加载用户AK、SK
    :param file_path:
    :return: 配置信息字典
    """
    global auth_config
    if len(auth_config) > 0:
        return auth_config
    with _auth_config_lock:
        if len(auth_config) > 0:
            return auth_config
        with open(file_path, 'r') as file:
            auth_config = yaml.safe_load(file)
    return auth_config


def parse_api_ak_sk_from_auth_config(config: dict) -> tuple[str, str]:
    """
    获取用户AK、SK，如果不存在配置文件中，则尝试从环境变量加载，建议使用环境变量的方式存储AK、SK
    :return: AK、SK二元组
    """
    global _ak, _sk
    if len(_ak) > 0 and len(_sk) > 0:
        return _ak, _sk
    with _ak_sk_lock:
        if len(_ak) > 0 and len(_sk) > 0:
            return _ak, _sk
        if len(config) <= 0:
            _ak, _sk = os.getenv("PADDLEHELIX_API_AK", ""), os.getenv("PADDLEHELIX_API_SK", "")
        else:
            if "credentials" in config:
                ak_sk_dict = config.get("credentials", {})
                if len(ak_sk_dict) > 0:
                    if "paddlehelix_api_ak" in ak_sk_dict:
                        _ak = ak_sk_dict.get("paddlehelix_api_ak", "")
                    if "paddlehelix_api_sk" in ak_sk_dict:
                        _sk = ak_sk_dict.get("paddlehelix_api_sk", "")
    assert len(_ak) > 0 and len(_sk) > 0, _missing_sk_sk_message
    return _ak, _sk

