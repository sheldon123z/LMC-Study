import os
import grid2op
from grid2op.Action import CompleteAction
from grid2op.PlotGrid import PlotMatplot
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from registry import env_registry
from datetime import datetime
import numpy as np
from src.utils import get_logger
from langchain_core.tools import tool

# 初始化日志记录器
logger = get_logger(__name__)


'''
以下内容为Grid2op中各个组件的Action函数实现
'''
# Action
# Generator
def gen_set_bus_impl (env_id=str, gen_id=List[int], bus_status=List[int]) -> Dict[str, Any]:
    """
    在grid2op环境中设置发电机的母线连接状态。
    

    参数:
    env_id (str): 环境实例的ID。
    gen_id (List[int]): 发电机ID列表。
    bus_status (List[int]): 发电机母线状态设置列表，每个整数代表对相应发电机要执行的操作，具体含义如下：
        - 0: 该动作不对这个线路产生作用。
        - -1: 强制断开母线连接。
        - 1: 连接母线1。
        - 2: 连接母线2。
        - 3及以上: 连接母线3及以上的母线 (grid2op版本>=1.10.0)

    返回:
    Dict[str, Any]: 包含状态和消息的字典。状态可以是 "success" 或 "failure"，消息描述了操作的结果。

    异常:
    ValueError: 如果环境ID无效或动作是模糊的。
    """
    try:
        logger.info(f"开始执行 gen set bus 操作，env_id: {env_id}, gen_id: {gen_id}, bus_status: {bus_status}")
        env = env_registry.get(env_id)
        if env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例。")

        # 修改发电机连接的母线
        act = env.action_space()
        act.gen_set_bus = list(zip(gen_id, bus_status))

        # 判断模糊操作
        if act.is_ambiguous()[0]:
            info = act.ambiguous_info()[1]
            raise ValueError(f"动作是模糊的，无法执行。{info}")
        else:
            obs, reward, done, info = env.step(act)
            logger.info(f"成功进行 gen set bus 操作。")
            return {
                "status": "success",
                "message": f"成功进行 gen set bus 操作。"
            }
    except Exception as e:
        logger.error(f"gen_set_bus_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"gen_set_bus_impl 执行失败: {str(e)}"
        }


def gen_change_bus_impl(env_id=str, gen_id=List[int]) -> Dict[str, Any]:


def redispatch_impl(env_id=str, gen_id=List[int], amount=List[float]) -> Dict[str, Any]:


def curtail_impl(env_id=str, gen_id=List[int], amount=List[float]) -> Dict[str, Any]:

# Load


# Powerline
def line_or_set_bus()


def line_ex_set_bus()


def line_or_change_bus()


def line_ex_change_bus()


def line_set_status_impl(env_id: str, line_id: List[int], line_status: List[int]) -> Dict[str, Any]:
    """
    在grid2op环境中设置输电线路的状态。

    参数:
    env_id (str): 环境实例的ID。
    line_id (List[int]): 输电线路ID列表。
    line_status (List[int]): 输电线路状态设置列表，每个整数代表对相应输电线要执行的操作，具体含义如下：
        - 0: 该动作不对这个线路产生作用。
        - 1: 强制连接该线路。
        - -1: 强制断开该线路。

    返回:
    Dict[str, Any]: 包含状态和消息的字典。状态可以是 "success" 或 "failure"，消息描述了操作的结果。

    异常:
    ValueError: 如果环境ID无效或动作是模糊的。
    """
    try:
        logger.info(f"开始执行 line set status 操作，env_id: {env_id}, line_id: {line_id}, line_status: {line_status}")
        
        # 获取环境实例
        env = env_manager._envs.get(env_id)  # 通过 env_manager 获取环境实例
        if env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例。")

        # 创建动作
        act = env.action_space()
        act.line_set_status = list(zip(line_id, line_status))

        # 检查动作是否模糊
        if act.is_ambiguous()[0]:
            info = act.ambiguous_info()[1]
            raise ValueError(f"动作是模糊的，无法执行。{info}")
        else:
            # 执行动作并获取新的观察
            obs, _, _, _ = env.step(act)
            
            # 使用 EnvironmentManager 注册新观察
            env_manager.record_observation(env_id, obs)  # 新的观察通过 EnvironmentManager 记录
            
            logger.info(f"成功进行 line set status 操作。")
            return {
                "status": "success",
                "message": f"成功进行 line set status 操作。"
            }
    except Exception as e:
        logger.error(f"line_set_status_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"line_set_status_impl 执行失败: {str(e)}"
        }


def line_change_status_impl(env_id: str, line_id: List[int]) -> Dict[str, Any]:
    """
    在grid2op环境中切换输电线路的状态。

    参数:
    env_id (str): 环境实例的ID。
    line_id (List[int]): 要切换状态的输电线路ID列表。

    返回:
    Dict[str, Any]: 包含状态和消息的字典。状态可以是 "success" 或 "failure"，消息描述了操作的结果。

    异常:
    ValueError: 如果环境ID无效或动作是模糊的。
    """
    try:
        logger.info(f"开始执行 line change status 操作，env_id: {env_id}, line_id: {line_id}")
        
        # 获取环境实例
        env = env_manager._envs.get(env_id)  # 通过 EnvironmentManager 获取环境实例
        if env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例。")

        # 创建动作
        act = env.action_space()
        act.line_change_status = line_id

        # 检查动作是否模糊
        if act.is_ambiguous()[0]:
            info = act.ambiguous_info()[1]
            raise ValueError(f"动作是模糊的，无法执行。{info}")
        else:
            # 执行动作并获取新的观察
            obs, _, _, _ = env.step(act)

            # 使用 EnvironmentManager 注册新观察
            env_manager.record_observation(env_id, obs)  # 新的观察通过 EnvironmentManager 记录

            logger.info(f"成功进行 line change status 操作。")
            return {
                "status": "success",
                "message": f"成功进行 line change status 操作。"
            }
    except Exception as e:
        logger.error(f"line_change_status_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"line_change_status_impl 执行失败: {str(e)}"
        }


# Storage Unit


# Substation


'''
以下内容为Grid2op中各个组件的Observation函数实现
'''
# Observation
# Generator


# Load


# Powerline


# Storage Unit


# Substation


