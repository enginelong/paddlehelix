"""
命令行参数解析器
"""
import argparse
import os

from utils import env_util

env_util.init_env()


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
