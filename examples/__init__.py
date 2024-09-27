"""
 Modified by Xiaodong Zheng
"""
import logging
import os
import sys

def get_logger(name):
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(name)s] [%(filename)s(%(lineno)d)] [%(levelname)s] %(message)s",
                        handlers=[logging.FileHandler('app.log'), logging.StreamHandler()])
    return logging.getLogger(name)


logger = logging.getLogger(__name__)