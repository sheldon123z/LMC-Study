import os
import sys
from typing import List, Dict, Any, Optional
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
            ambiguity = act.is_ambiguous()[1]
            raise ValueError(f"动作是模糊的，无法执行。{ambiguity}")
        else:
            # 执行动作并记录新状态
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
            ambiguity = act.is_ambiguous()[1]
            raise ValueError(f"动作是模糊的，无法执行。{ambiguity}")
        else:
            # 执行动作并记录新状态
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
            ambiguity = act.is_ambiguous()[1]
            raise ValueError(f"动作是模糊的，无法执行。{ambiguity}")
        else:
            # 执行动作并记录新状态
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
            ambiguity = act.is_ambiguous()[1]
            raise ValueError(f"动作是模糊的，无法执行。{ambiguity}")
        else:
            # 执行动作并记录新状态
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
            ambiguity = act.is_ambiguous()[1]
            raise ValueError(f"动作是模糊的，无法执行。{ambiguity}")
        else:
            # 执行动作并记录新状态
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
            ambiguity = act.is_ambiguous()[1]
            raise ValueError(f"动作是模糊的，无法执行。{ambiguity}")
        else:
            # 执行动作并记录新状态
            obs, _, _, _ = env.step(act)
            
            # 使用 EnvironmentManager 注册新观察
            env_manager.record_observation(env_id, obs)
            
            logger.info(f"成功进行“输电线连接状态设置”操作。")
            return {
                "status": "success",
                "message": f"成功进行“输电线连接状态设置”操作。"
            }
    except Exception as e:
        logger.error(f"line_set_status_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"line_set_status_impl 执行失败: {str(e)}"
        }


def redispatch_impl(env_manager, env_id: str, gen_id: List[int], amount: List[float]) -> Dict[str, Any]:
    """
    在grid2op环境中设置发电机的重调度量。

    参数:
    env_manager: 环境管理器实例，用于管理和注册环境。
    env_id (str): 环境实例的ID。
    gen_id (List[int]): 发电机ID列表。
    amount (List[float]): 每个发电机对应的重调度量（MW），正值表示增加发电量，负值表示减少发电量。

    返回:
    Dict[str, Any]: 包含状态和消息的字典。状态可以是 "success" 或 "failure"，消息描述了操作的结果。

    异常:
    ValueError: 如果环境ID无效或动作是模糊的。
    """
    try:
        logger.info(f"开始执行 redispatch 操作，env_id: {env_id}, gen_id: {gen_id}, amount: {amount}")
        
        # 获取环境实例
        env = env_manager._envs.get(env_id)
        if env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例。")

        # 检查发电机是否可重调度（后续可考虑是否在函数调用中，结合静态参数验证进行验证）
        # non_redispatchable_gens = []
        # for gen in gen_id:
        #     if not env.gen_redispatchable[gen]:
        #         non_redispatchable_gens.append(gen)

        # if non_redispatchable_gens:
        #     raise ValueError(f"发电机 {non_redispatchable_gens} 不可重调度。")

        # 创建动作
        act = env.action_space()
        act.redispatch = list(zip(gen_id, amount))
        print(act)  # 测试用，实装时删除

        # 检查动作是否模糊
        if act.is_ambiguous()[0]:
            ambiguity = act.is_ambiguous()[1]
            raise ValueError(f"动作是模糊的，无法执行。{ambiguity}")
        else:
            # 执行动作并获取新的观察
            obs, _, _, _ = env.step(act)
            
            # 使用 EnvironmentManager 注册新观察
            env_manager.record_observation(env_id, obs)
            
            logger.info(f"成功进行“发电机重调度”操作。")
            return {
                "status": "success",
                "message": f"成功进行“发电机重调度”操作。"
            }
    except Exception as e:
        logger.error(f"redispatch_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"redispatch_impl 执行失败: {str(e)}"
        }

        
def cancel_redispatch_impl(env_manager, env_id: str, gen_id: List[int]) -> Dict[str, Any]:
    """
    取消指定发电机的重调度指令，将其目标调度值重置为0。

    参数:
    env_manager: 环境管理器实例，用于管理环境状态
    env_id (str): 环境实例的ID
    gen_id (List[int]): 要取消调度的发电机ID列表

    返回:
    Dict[str, Any]: 包含操作状态和消息的字典
    
    异常:
    ValueError: 如果环境ID无效或动作是模糊的。
    """
    try:
        logger.info(f"开始取消重调度操作，env_id: {env_id}, gen_id: {gen_id}")

        # 获取环境实例
        env = env_manager._envs.get(env_id)
        if env is None:
            raise ValueError(f"环境ID '{env_id}' 不存在")

        # 获取最新观测数据
        latest_obs = env_manager.get_latest_obs(env_id)
        if latest_obs is None:
            raise ValueError(f"无法获取环境 '{env_id}' 的观测数据")

        # 获取当前调度值并检查有效性
        gen_id_arr = np.array(gen_id)
        target_dispatch = latest_obs.target_dispatch[gen_id_arr]
        if np.all(target_dispatch == 0):
            raise ValueError("指定的发电机未进行重调度")

        # 创建动作
        act = env.action_space()
        deltas = -target_dispatch  # 计算反向delta值
        act.redispatch = list(zip(gen_id, deltas.tolist()))
        print(act)  # 测试用，实装时删除

        # 检查动作是否模糊
        if act.is_ambiguous()[0]:
            ambiguity_info = act.is_ambiguous()[1]
            raise ValueError(f"动作是模糊的，无法执行。{ambiguity}")

        # 执行动作并记录新状态
        new_obs, _, _, _ = env.step(act)
        
        # 使用 EnvironmentManager 注册新观察
        env_manager.record_observation(env_id, new_obs)

        logger.info(f"成功取消发电机 {gen_id} 的调度指令")
        return {
            "status": "success",
            "message": f"成功取消发电机 {gen_id} 的调度指令",
        }

    except Exception as e:
        logger.error(f"取消重调度失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"取消重调度失败: {str(e)}"
        }


def storage_p_impl(env_manager, env_id: str, storage_id: List[int], amount: List[float]) -> Dict[str, Any]:
    """
    在grid2op环境中设置储能单元的充放电功率。

    参数:
    env_manager: 环境管理器实例，用于管理和注册环境。
    env_id (str): 环境实例的ID。
    storage_id (List[int]): 储能单元ID列表。
    amount (List[float]): 每个储能单元对应的充放电功率(MW)，正值表示充电(从电网吸收能量)，
                          负值表示放电(向电网释放能量)。

    返回:
    Dict[str, Any]: 包含状态和消息的字典。状态可以是 "success" 或 "failure"，消息描述了操作的结果。

    异常:
    ValueError: 如果环境ID无效或动作是模糊的。
    """
    try:
        logger.info(f"开始执行 storage_p 操作，env_id: {env_id}, storage_id: {storage_id}, amount: {amount}")
        
        # 获取环境实例
        env = env_manager._envs.get(env_id)
        if env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例。")
        
        # 创建动作
        act = env.action_space()
        act.storage_p = list(zip(storage_id, amount))
        print(act)  # 测试用，实装时删除
        
        # 检查动作是否模糊
        if act.is_ambiguous()[0]:
            ambiguity = act.is_ambiguous()[1]
            raise ValueError(f"动作是模糊的，无法执行。{ambiguity}")
        else:
            # 执行动作并获取新的观察
            obs, _, _, _ = env.step(act)
            
            # 使用 EnvironmentManager 注册新观察
            env_manager.record_observation(env_id, obs)
            
            logger.info(f"成功进行“储能单元充放电”操作。")
            return {
                "status": "success",
                "message": f"成功进行“储能单元充放电”操作。"
            }
    except Exception as e:
        logger.error(f"storage_p_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"storage_p_impl 执行失败: {str(e)}"
        }


def curtail_impl(env_manager, env_id: str, gen_id: List[int], amount: List[float]) -> Dict[str, Any]:
    """
    在grid2op环境中设置可再生能源发电机的限电量。

    参数:
    env_manager: 环境管理器实例，用于管理和注册环境。
    env_id (str): 环境实例的ID。
    gen_id (List[int]): 发电机ID列表。
    amount (List[float]): 每个发电机对应的限电百分比，范围在[0.0, 1.0]之间，1表示不限电，0表示完全限电。

    返回:
    Dict[str, Any]: 包含状态和消息的字典。状态可以是 "success" 或 "failure"，消息描述了操作的结果。

    异常:
    ValueError: 如果环境ID无效或动作是模糊的。
    """
    try:
        logger.info(f"开始执行 curtail 操作，env_id: {env_id}, gen_id: {gen_id}, amount: {amount}")
        
        # 获取环境实例
        env = env_manager._envs.get(env_id)
        if env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例。")
        
        # 检查发电机是否是可再生能源（可以执行限电操作）
        # non_renewable_gens = []
        # for gen in gen_id:
        #     if not env.gen_renewable[gen]:
        #         non_renewable_gens.append(gen)
        
        # if non_renewable_gens:
        #     raise ValueError(f"发电机 {non_renewable_gens} 不是可再生能源，不能执行限电操作。")
        
        # 创建动作
        act = env.action_space()
        act.curtail = list(zip(gen_id, amount))
        print(act)  # 测试用，实装时删除
        
        # 检查动作是否模糊
        if act.is_ambiguous()[0]:
            ambiguity = act.is_ambiguous()[1]
            raise ValueError(f"动作是模糊的，无法执行。{ambiguity}")
        else:
            # 执行动作并获取新的观察
            obs, _, _, _ = env.step(act)
            
            # 使用 EnvironmentManager 注册新观察
            env_manager.record_observation(env_id, obs)
            
            logger.info(f"成功进行“限电”操作。")
            return {
                "status": "success",
                "message": f"成功进行“限电”操作。"
            }
    except Exception as e:
        logger.error(f"curtail_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"curtail_impl 执行失败: {str(e)}"
        }


'''
以下内容为Grid2op中各个组件的Observation函数实现
'''

# Observation
'''待完成'''
