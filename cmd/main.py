"""
命令行参数解析器
"""
import argparse
import os
import sys

# 同sdk导入时一致 当用户使用命令行工具时 也需要初始化项目目录环境变量、用户身份信息
project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root_path)
os.environ['PROJECT_ROOT'] = project_root_path

from config import auth_config_manager

# 初始化用户身份验证信息
auth_config = auth_config_manager.load_config()
auth_config_manager.parse_api_ak_sk_from_auth_config(auth_config)


def main():
    parser = argparse.ArgumentParser(description="HelixFold3 command-line interface")
    parser.add_argument('input_path', type=str, help="Input file path")
    parser.add_argument('output_path', type=str, help="Output file path")
    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path

    # 将相对路径转换为绝对路径
    absolute_input_path = os.path.abspath(input_path)
    absolute_output_path = os.path.abspath(output_path)

    import command
    command.execute(absolute_input_path, absolute_output_path)


if __name__ == '__main__':
    main()
