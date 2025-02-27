import os
import sys
from typing import List, Dict, Any
import numpy as np
import grid2op
from grid2op.Action import CompleteAction
from grid2op.PlotGrid import PlotMatplot
from registry_object import EnvironmentManager
from src.utils import get_logger


# 初始化日志记录器
logger = get_logger(__name__)

'''
以下内容为Grid2op中各个组件的Action函数实现
'''

# Action
def gen_set_bus_impl(env_manager, env_id: str, gen_id: List[int], bus_status: List[int]) -> Dict[str, Any]:
    """
    在grid2op环境中设置发电机与母线的关联。

    参数:
    env_manager: 环境管理器实例，用于管理和注册环境。
    env_id (str): 环境实例的ID。
    gen_id (List[int]): 发电机ID列表。
    bus_status (List[int]): 发电机与母线状态设置列表，每个整数代表对相应发电机与母线的操作，具体含义如下：
        - 0: 该动作不对这个发电机产生作用。
        - -1: 断开该发电机。
        - 1: 将该发电机设置到母线1。
        - 2: 将该发电机设置到母线2。
        - 3: 将该发电机设置到母线3（grid2op >= 1.10.0）等。

    返回:
    Dict[str, Any]: 包含状态和消息的字典。状态可以是 "success" 或 "failure"，消息描述了操作的结果。

    异常:
    ValueError: 如果环境ID无效或动作是模糊的。
    """
    try:
        logger.info(f"开始执行“发电机母线设置”操作，env_id: {env_id}, gen_id: {gen_id}, bus_status: {bus_status}")
        
        # 获取环境实例
        env = env_manager._envs.get(env_id)
        if env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例。")

        # 创建动作
        act = env.action_space()
        act.gen_set_bus = list(zip(gen_id, bus_status))
        print(act) # 测试用，实装时删除

        # 检查动作是否模糊
        if act.is_ambiguous()[0]:
            ambiguity = act.ambiguous_info()[1]
            raise ValueError(f"动作是模糊的，无法执行。{ambiguity}")
        else:
            # 执行动作并获取新的观察
            obs, _, _, _ = env.step(act)
            
            # 使用 EnvironmentManager 注册新观察
            env_manager.record_observation(env_id, obs)
            
            logger.info(f"成功进行“发电机母线设置”操作。")
            return {
                "status": "success",
                "message": f"成功进行“发电机母线设置”操作。"
            }
    except Exception as e:
        logger.error(f"gen_set_bus_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"gen_set_bus_impl 执行失败: {str(e)}"
        }


def load_set_bus_impl(env_manager, env_id: str, load_id: List[int], bus_status: List[int]) -> Dict[str, Any]:
    """
    在grid2op环境中设置负荷与母线的关联。

    参数:
    env_manager: 环境管理器实例，用于管理和注册环境。
    env_id (str): 环境实例的ID。
    load_id (List[int]): 负荷ID列表。
    bus_status (List[int]): 负荷与母线状态设置列表，每个整数代表对相应负荷与母线的操作，具体含义如下：
        - 0: 该动作不对这个负荷产生作用。
        - -1: 断开该负荷。
        - 1: 将该负荷设置到母线1。
        - 2: 将该负荷设置到母线2。
        - 3: 将该负荷设置到母线3（grid2op >= 1.10.0）等。

    返回:
    Dict[str, Any]: 包含状态和消息的字典。状态可以是 "success" 或 "failure"，消息描述了操作的结果。

    异常:
    ValueError: 如果环境ID无效或动作是模糊的。
    """
    try:
        logger.info(f"开始执行“负载母线设置”操作，env_id: {env_id}, load_id: {load_id}, bus_status: {bus_status}")
        
        # 获取环境实例
        env = env_manager._envs.get(env_id)
        if env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例。")

        # 创建动作
        act = env.action_space()
        act.load_set_bus = list(zip(load_id, bus_status))
        print(act) # 测试用，实装时删除

        # 检查动作是否模糊
        if act.is_ambiguous()[0]:
            ambiguity = act.ambiguous_info()[1]
            raise ValueError(f"动作是模糊的，无法执行。{ambiguity}")
        else:
            # 执行动作并获取新的观察
            obs, _, _, _ = env.step(act)
            
            # 使用 EnvironmentManager 注册新观察
            env_manager.record_observation(env_id, obs)
            
            logger.info(f"成功进行“负载母线设置”操作。")
            return {
                "status": "success",
                "message": f"成功进行“负载母线设置”操作。"
            }
    except Exception as e:
        logger.error(f"load_set_bus_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"load_set_bus_impl 执行失败: {str(e)}"
        }


def line_or_set_bus_impl(env_manager, env_id: str, line_id: List[int], bus_status: List[int]) -> Dict[str, Any]:
    """
    在grid2op环境中设置输电线路的电流输入端与母线的关联。

    参数:
    env_manager: 环境管理器实例，用于管理和注册环境。
    env_id (str): 环境实例的ID。
    line_id (List[int]): 输电线路ID列表。
    bus_status (List[int]): 发电机与母线状态设置列表，每个整数代表对相应发电机与母线的操作，具体含义如下：
        - 0: 该动作不对这个发电机产生作用。
        - -1: 断开该发电机。
        - 1: 将该发电机设置到母线1。
        - 2: 将该发电机设置到母线2。
        - 3: 将该发电机设置到母线3（grid2op >= 1.10.0）等。

    返回:
    Dict[str, Any]: 包含状态和消息的字典。状态可以是 "success" 或 "failure"，消息描述了操作的结果。

    异常:
    ValueError: 如果环境ID无效或动作是模糊的。
    """
    try:
        logger.info(f"开始执行“线路输入端母线设置”操作，env_id: {env_id}, line_id: {line_id}, bus_status: {bus_status}")
        
        # 获取环境实例
        env = env_manager._envs.get(env_id)
        if env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例。")

        # 创建动作
        act = env.action_space()
        act.line_or_set_bus = list(zip(line_id, bus_status))
        print(act) # 测试用，实装时删除

        # 检查动作是否模糊
        if act.is_ambiguous()[0]:
            ambiguity = act.ambiguous_info()[1]
            raise ValueError(f"动作是模糊的，无法执行。{ambiguity}")
        else:
            # 执行动作并获取新的观察
            obs, _, _, _ = env.step(act)
            
            # 使用 EnvironmentManager 注册新观察
            env_manager.record_observation(env_id, obs)
            
            logger.info(f"成功进行“线路输入端母线设置”操作。")
            return {
                "status": "success",
                "message": f"成功进行“线路输入端母线设置”操作。"
            }
    except Exception as e:
        logger.error(f"line_or_set_bus_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"line_or_set_bus_impl 执行失败: {str(e)}"
        }


def line_ex_set_bus_impl(env_manager, env_id: str, line_id: List[int], bus_status: List[int]) -> Dict[str, Any]:
    """
    在grid2op环境中设置输电线路的电流输出端与母线的关联。

    参数:
    env_manager: 环境管理器实例，用于管理和注册环境。
    env_id (str): 环境实例的ID。
    line_id (List[int]): 输电线路ID列表。
    bus_status (List[int]): 发电机与母线状态设置列表，每个整数代表对相应发电机与母线的操作，具体含义如下：
        - 0: 该动作不对这个发电机产生作用。
        - -1: 断开该发电机。
        - 1: 将该发电机设置到母线1。
        - 2: 将该发电机设置到母线2。
        - 3: 将该发电机设置到母线3（grid2op >= 1.10.0）等。

    返回:
    Dict[str, Any]: 包含状态和消息的字典。状态可以是 "success" 或 "failure"，消息描述了操作的结果。

    异常:
    ValueError: 如果环境ID无效或动作是模糊的。
    """
    try:
        logger.info(f"开始执行“线路输出端母线设置”操作，env_id: {env_id}, line_id: {line_id}, bus_status: {bus_status}")
        
        # 获取环境实例
        env = env_manager._envs.get(env_id)
        if env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例。")

        # 创建动作
        act = env.action_space()
        act.line_ex_set_bus = list(zip(line_id, bus_status))
        print(act) # 测试用，实装时删除

        # 检查动作是否模糊
        if act.is_ambiguous()[0]:
            ambiguity = act.ambiguous_info()[1]
            raise ValueError(f"动作是模糊的，无法执行。{ambiguity}")
        else:
            # 执行动作并获取新的观察
            obs, _, _, _ = env.step(act)
            
            # 使用 EnvironmentManager 注册新观察
            env_manager.record_observation(env_id, obs)
            
            logger.info(f"成功进行“线路输出端母线设置”操作。")
            return {
                "status": "success",
                "message": f"成功进行“线路输出端母线设置”操作。"
            }
    except Exception as e:
        logger.error(f"line_ex_set_bus_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"line_ex_set_bus_impl 执行失败: {str(e)}"
        }


def storage_set_bus_impl(env_manager, env_id: str, storage_id: List[int], bus_status: List[int]) -> Dict[str, Any]:
    """
    在grid2op环境中设置储能设备与母线的关联。

    参数:
    env_manager: 环境管理器实例，用于管理和注册环境。
    env_id (str): 环境实例的ID。
    storage_id (List[int]): 储能设备ID列表。
    bus_status (List[int]): 发电机与母线状态设置列表，每个整数代表对相应发电机与母线的操作，具体含义如下：
        - 0: 该动作不对这个发电机产生作用。
        - -1: 断开该发电机。
        - 1: 将该发电机设置到母线1。
        - 2: 将该发电机设置到母线2。
        - 3: 将该发电机设置到母线3（grid2op >= 1.10.0）等。

    返回:
    Dict[str, Any]: 包含状态和消息的字典。状态可以是 "success" 或 "failure"，消息描述了操作的结果。

    异常:
    ValueError: 如果环境ID无效或动作是模糊的。
    """
    try:
        logger.info(f"开始执行“储能单元母线设置”操作，env_id: {env_id}, storage_id: {storage_id}, bus_status: {bus_status}")
        
        # 获取环境实例
        env = env_manager._envs.get(env_id)
        if env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例。")

        # 创建动作
        act = env.action_space()
        act.storage_set_bus = list(zip(storage_id, bus_status))
        print(act) # 测试用，实装时删除

        # 检查动作是否模糊
        if act.is_ambiguous()[0]:
            ambiguity = act.ambiguous_info()[1]
            raise ValueError(f"动作是模糊的，无法执行。{ambiguity}")
        else:
            # 执行动作并获取新的观察
            obs, _, _, _ = env.step(act)
            
            # 使用 EnvironmentManager 注册新观察
            env_manager.record_observation(env_id, obs)
            
            logger.info(f"成功进行“储能单元母线设置”操作。")
            return {
                "status": "success",
                "message": f"成功进行“储能单元母线设置”操作。"
            }
    except Exception as e:
        logger.error(f"storage_set_bus_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"storage_set_bus_impl 执行失败: {str(e)}"
        }


def line_set_status_impl(env_manager, env_id: str, line_id: List[int], line_status: List[int]) -> Dict[str, Any]:
    """
    在grid2op环境中设置输电线路的状态。

    参数:
    env_manager: 环境管理器实例，用于管理和注册环境。
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
        print(act) # 测试用，实装时删除

        # 检查动作是否模糊
        if act.is_ambiguous()[0]:
            ambiguity = act.ambiguous_info()[1]
            raise ValueError(f"动作是模糊的，无法执行。{ambiguity}")
        else:
            # 执行动作并获取新的观察
            obs, _, _, _ = env.step(act)
            
            # 使用 EnvironmentManager 注册新观察
            env_manager.record_observation(env_id, obs)
            
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

'''
def redispatch_impl(env_manager, env_id: str, gen_id: List[int], amount: List[float]) -> Dict[str, Any]:


def storage_p_impl(env_manager, env_id: str, storage_id: List[int], amount: List[float]) -> Dict[str, Any]:
    
    
def curtail_mw_impl(env_manager, env_id: str, gen_id: List[int], amount: List[float]) -> Dict[str, Any]:
'''

'''
以下内容为Grid2op中各个组件的Observation函数实现
'''
# Observation
# Generator


# Load


# Powerline


# Storage Unit


# Substation


