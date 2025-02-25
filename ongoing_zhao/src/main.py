import sys
import os

# 获取当前脚本所在目录的上级目录路径
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 将上级目录路径添加到sys.path
sys.path.append(parent_dir)

import grid2op
from src.utils import get_logger
from grid2op.PlotGrid import PlotMatplot
from grid2op.Action import PlayableAction
from grid2op.Parameters import Parameters
from src.utils.process_json import load_json, save_json

# 设置日志记录器
logger = get_logger(__name__)


