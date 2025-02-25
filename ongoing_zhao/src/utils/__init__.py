"""
 Modified by Xiaodong Zheng
"""
import logging
import os
import sys
from datetime import datetime

def get_logger(name):
    # 生成带有时间戳的日志文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_directory = "logs" # 本行为新增内容，用于指定日志文件所在的目录
    log_filename = f"logs/实验_{timestamp}.log"
    
    # 以下内容为新增
    # 检查日志文件夹是否存在，如果不存在则创建
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    # 新增内容结束

    # 检查是否已经有了 FileHandler，以防止重复配置
    if not logging.getLogger().hasHandlers():
        # 配置日志记录器
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s] [%(name)s] [%(filename)s(%(lineno)d)] [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler(log_filename),  # 日志文件带时间戳
                logging.StreamHandler()             # 控制台输出
            ]
        )
    
    return logging.getLogger(name)

# 使用 get_logger 函数创建 logger 实例
logger = get_logger(__name__)

# 测试日志输出
logger.info("这是带时间戳的日志文件测试信息。")