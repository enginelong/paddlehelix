"""
环境初始化工具方法
"""

import os
import sys

from config import auth_config_manager


def init_env():
    # 初始化项目目录及其环境变量
    project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(project_root_path)
    os.environ['PROJECT_ROOT'] = project_root_path

    # 初始化用户身份验证信息
    auth_config = auth_config_manager.load_config()
    auth_config_manager.parse_api_ak_sk_from_auth_config(auth_config)
