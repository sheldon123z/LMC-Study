from typing import List, Dict, Any, Optional
import numpy as np
import grid2op
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
            
            logger.info("成功进行“发电机母线设置”操作。")
            return {
                "status": "success",
                "message": "成功进行“发电机母线设置”操作。"
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
            
            logger.info("成功进行“负载母线设置”操作。")
            return {
                "status": "success",
                "message": "成功进行“负载母线设置”操作。"
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
            
            logger.info("成功进行“线路输入端母线设置”操作。")
            return {
                "status": "success",
                "message": "成功进行“线路输入端母线设置”操作。"
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
            
            logger.info("成功进行“线路输出端母线设置”操作。")
            return {
                "status": "success",
                "message": "成功进行“线路输出端母线设置”操作。"
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
            
            logger.info("成功进行“储能单元母线设置”操作。")
            return {
                "status": "success",
                "message": "成功进行“储能单元母线设置”操作。"
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
            
            logger.info("成功进行“输电线连接状态设置”操作。")
            return {
                "status": "success",
                "message": "成功进行“输电线连接状态设置”操作。"
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
            
            logger.info("成功进行“发电机重调度”操作。")
            return {
                "status": "success",
                "message": "成功进行“发电机重调度”操作。"
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
            ambiguity = act.is_ambiguous()[1]
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
            
            logger.info("成功进行“储能单元充放电”操作。")
            return {
                "status": "success",
                "message": "成功进行“储能单元充放电”操作。"
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
            
            logger.info("成功进行“限电”操作。")
            return {
                "status": "success",
                "message": "成功进行“限电”操作。"
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
# 1. By Element
def obs_gen_p_impl(env_manager, env_id: str, gen_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中发电机的有功功率输出。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    gen_id (Optional[List[int]]): 可选的发电机ID列表。如果提供，则返回指定发电机的有功功率；
                                如果为None，则返回所有发电机的有功功率。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的发电机有功功率值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if gen_id is None:
            logger.info(f"开始获取所有发电机的有功功率，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定发电机的有功功率，env_id: {env_id}, gen_id: {gen_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据gen_id参数返回相应的数据
        if gen_id is None:
            result = obs.gen_p.tolist() if hasattr(obs.gen_p, 'tolist') else obs.gen_p
            logger.info("成功获取所有发电机的有功功率。")
            return {
                "status": "success",
                "message": "成功获取所有发电机的有功功率。",
                "data": result
            }
        else:
            result = obs.gen_p[gen_id].tolist() if hasattr(obs.gen_p[gen_id], 'tolist') else obs.gen_p[gen_id]
            logger.info("成功获取指定发电机的有功功率。")
            return {
                "status": "success",
                "message": "成功获取指定发电机的有功功率。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_gen_p_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_gen_p_impl 执行失败: {str(e)}"
        }


def obs_gen_q_impl(env_manager, env_id: str, gen_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中发电机的无功功率输出。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    gen_id (Optional[List[int]]): 可选的发电机ID列表。如果提供，则返回指定发电机的无功功率；
                                如果为None，则返回所有发电机的无功功率。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的发电机无功功率值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if gen_id is None:
            logger.info(f"开始获取所有发电机的无功功率，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定发电机的无功功率，env_id: {env_id}, gen_id: {gen_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据gen_id参数返回相应的数据
        if gen_id is None:
            result = obs.gen_q.tolist() if hasattr(obs.gen_q, 'tolist') else obs.gen_q
            logger.info("成功获取所有发电机的无功功率。")
            return {
                "status": "success",
                "message": "成功获取所有发电机的无功功率。",
                "data": result
            }
        else:
            result = obs.gen_q[gen_id].tolist() if hasattr(obs.gen_q[gen_id], 'tolist') else obs.gen_q[gen_id]
            logger.info("成功获取指定发电机的无功功率。")
            return {
                "status": "success",
                "message": "成功获取指定发电机的无功功率。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_gen_q_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_gen_q_impl 执行失败: {str(e)}"
        }


def obs_gen_v_impl(env_manager, env_id: str, gen_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中发电机的电压值。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    gen_id (Optional[List[int]]): 可选的发电机ID列表。如果提供，则返回指定发电机的电压值；
                                如果为None，则返回所有发电机的电压值。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的发电机电压值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if gen_id is None:
            logger.info(f"开始获取所有发电机的电压值，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定发电机的电压值，env_id: {env_id}, gen_id: {gen_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据gen_id参数返回相应的数据
        if gen_id is None:
            result = obs.gen_v.tolist() if hasattr(obs.gen_v, 'tolist') else obs.gen_v
            logger.info("成功获取所有发电机的电压值。")
            return {
                "status": "success",
                "message": "成功获取所有发电机的电压值。",
                "data": result
            }
        else:
            result = obs.gen_v[gen_id].tolist() if hasattr(obs.gen_v[gen_id], 'tolist') else obs.gen_v[gen_id]
            logger.info("成功获取指定发电机的电压值。")
            return {
                "status": "success",
                "message": "成功获取指定发电机的电压值。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_gen_v_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_gen_v_impl 执行失败: {str(e)}"
        }


def obs_gen_theta_impl(env_manager, env_id: str, gen_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中发电机的电压角。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    gen_id (Optional[List[int]]): 可选的发电机ID列表。如果提供，则返回指定发电机的电压角；
                                如果为None，则返回所有发电机的电压角。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的发电机电压角。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if gen_id is None:
            logger.info(f"开始获取所有发电机的电压角，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定发电机的电压角，env_id: {env_id}, gen_id: {gen_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据gen_id参数返回相应的数据
        if gen_id is None:
            result = obs.gen_theta.tolist() if hasattr(obs.gen_theta, 'tolist') else obs.gen_theta
            logger.info("成功获取所有发电机的电压角。")
            return {
                "status": "success",
                "message": "成功获取所有发电机的电压角。",
                "data": result
            }
        else:
            result = obs.gen_theta[gen_id].tolist() if hasattr(obs.gen_theta[gen_id], 'tolist') else obs.gen_theta[gen_id]
            logger.info("成功获取指定发电机的电压角。")
            return {
                "status": "success",
                "message": "成功获取指定发电机的电压角。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_gen_theta_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_gen_theta_impl 执行失败: {str(e)}"
        }


def obs_load_p_impl(env_manager, env_id: str, load_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中负载的有功功率。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    load_id (Optional[List[int]]): 可选的负载ID列表。如果提供，则返回指定负载的有功功率；
                                 如果为None，则返回所有负载的有功功率。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的负载有功功率值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if load_id is None:
            logger.info(f"开始获取所有负载的有功功率，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定负载的有功功率，env_id: {env_id}, load_id: {load_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据load_id参数返回相应的数据
        if load_id is None:
            result = obs.load_p.tolist() if hasattr(obs.load_p, 'tolist') else obs.load_p
            logger.info("成功获取所有负载的有功功率。")
            return {
                "status": "success",
                "message": "成功获取所有负载的有功功率。",
                "data": result
            }
        else:
            result = obs.load_p[load_id].tolist() if hasattr(obs.load_p[load_id], 'tolist') else obs.load_p[load_id]
            logger.info("成功获取指定负载的有功功率。")
            return {
                "status": "success",
                "message": "成功获取指定负载的有功功率。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_load_p_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_load_p_impl 执行失败: {str(e)}"
        }


def obs_load_q_impl(env_manager, env_id: str, load_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中负载的无功功率。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    load_id (Optional[List[int]]): 可选的负载ID列表。如果提供，则返回指定负载的无功功率；
                                 如果为None，则返回所有负载的无功功率。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的负载无功功率值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if load_id is None:
            logger.info(f"开始获取所有负载的无功功率，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定负载的无功功率，env_id: {env_id}, load_id: {load_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据load_id参数返回相应的数据
        if load_id is None:
            result = obs.load_q.tolist() if hasattr(obs.load_q, 'tolist') else obs.load_q
            logger.info("成功获取所有负载的无功功率。")
            return {
                "status": "success",
                "message": "成功获取所有负载的无功功率。",
                "data": result
            }
        else:
            result = obs.load_q[load_id].tolist() if hasattr(obs.load_q[load_id], 'tolist') else obs.load_q[load_id]
            logger.info("成功获取指定负载的无功功率。")
            return {
                "status": "success",
                "message": "成功获取指定负载的无功功率。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_load_q_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_load_q_impl 执行失败: {str(e)}"
        }


def obs_load_v_impl(env_manager, env_id: str, load_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中负载的电压值。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    load_id (Optional[List[int]]): 可选的负载ID列表。如果提供，则返回指定负载的电压值；
                                 如果为None，则返回所有负载的电压值。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的负载电压值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if load_id is None:
            logger.info(f"开始获取所有负载的电压值，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定负载的电压值，env_id: {env_id}, load_id: {load_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据load_id参数返回相应的数据
        if load_id is None:
            result = obs.load_v.tolist() if hasattr(obs.load_v, 'tolist') else obs.load_v
            logger.info("成功获取所有负载的电压值。")
            return {
                "status": "success",
                "message": "成功获取所有负载的电压值。",
                "data": result
            }
        else:
            result = obs.load_v[load_id].tolist() if hasattr(obs.load_v[load_id], 'tolist') else obs.load_v[load_id]
            logger.info("成功获取指定负载的电压值。")
            return {
                "status": "success",
                "message": "成功获取指定负载的电压值。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_load_v_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_load_v_impl 执行失败: {str(e)}"
        }


def obs_load_theta_impl(env_manager, env_id: str, load_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中负载的电压角。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    load_id (Optional[List[int]]): 可选的负载ID列表。如果提供，则返回指定负载的电压角；
                                 如果为None，则返回所有负载的电压角。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的负载电压角。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if load_id is None:
            logger.info(f"开始获取所有负载的电压角，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定负载的电压角，env_id: {env_id}, load_id: {load_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据load_id参数返回相应的数据
        if load_id is None:
            result = obs.load_theta.tolist() if hasattr(obs.load_theta, 'tolist') else obs.load_theta
            logger.info("成功获取所有负载的电压角。")
            return {
                "status": "success",
                "message": "成功获取所有负载的电压角。",
                "data": result
            }
        else:
            result = obs.load_theta[load_id].tolist() if hasattr(obs.load_theta[load_id], 'tolist') else obs.load_theta[load_id]
            logger.info("成功获取指定负载的电压角。")
            return {
                "status": "success",
                "message": "成功获取指定负载的电压角。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_load_theta_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_load_theta_impl 执行失败: {str(e)}"
        }


def obs_p_or_impl(env_manager, env_id: str, line_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中线路起始端（origin）的有功功率。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    line_id (Optional[List[int]]): 可选的线路ID列表。如果提供，则返回指定线路起始端的有功功率；
                                  如果为None，则返回所有线路起始端的有功功率。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的线路起始端有功功率值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if line_id is None:
            logger.info(f"开始获取所有线路起始端的有功功率，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定线路起始端的有功功率，env_id: {env_id}, line_id: {line_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据line_id参数返回相应的数据
        if line_id is None:
            result = obs.p_or.tolist() if hasattr(obs.p_or, 'tolist') else obs.p_or
            logger.info("成功获取所有线路起始端的有功功率。")
            return {
                "status": "success",
                "message": "成功获取所有线路起始端的有功功率。",
                "data": result
            }
        else:
            result = obs.p_or[line_id].tolist() if hasattr(obs.p_or[line_id], 'tolist') else obs.p_or[line_id]
            logger.info("成功获取指定线路起始端的有功功率。")
            return {
                "status": "success",
                "message": "成功获取指定线路起始端的有功功率。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_p_or_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_p_or_impl 执行失败: {str(e)}"
        }


def obs_q_or_impl(env_manager, env_id: str, line_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中线路起始端（origin）的无功功率。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    line_id (Optional[List[int]]): 可选的线路ID列表。如果提供，则返回指定线路起始端的无功功率；
                                  如果为None，则返回所有线路起始端的无功功率。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的线路起始端无功功率值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if line_id is None:
            logger.info(f"开始获取所有线路起始端的无功功率，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定线路起始端的无功功率，env_id: {env_id}, line_id: {line_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据line_id参数返回相应的数据
        if line_id is None:
            result = obs.q_or.tolist() if hasattr(obs.q_or, 'tolist') else obs.q_or
            logger.info("成功获取所有线路起始端的无功功率。")
            return {
                "status": "success",
                "message": "成功获取所有线路起始端的无功功率。",
                "data": result
            }
        else:
            result = obs.q_or[line_id].tolist() if hasattr(obs.q_or[line_id], 'tolist') else obs.q_or[line_id]
            logger.info("成功获取指定线路起始端的无功功率。")
            return {
                "status": "success",
                "message": "成功获取指定线路起始端的无功功率。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_q_or_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_q_or_impl 执行失败: {str(e)}"
        }


def obs_v_or_impl(env_manager, env_id: str, line_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中线路起始端（origin）的电压值。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    line_id (Optional[List[int]]): 可选的线路ID列表。如果提供，则返回指定线路起始端的电压值；
                                  如果为None，则返回所有线路起始端的电压值。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的线路起始端电压值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if line_id is None:
            logger.info(f"开始获取所有线路起始端的电压值，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定线路起始端的电压值，env_id: {env_id}, line_id: {line_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据line_id参数返回相应的数据
        if line_id is None:
            result = obs.v_or.tolist() if hasattr(obs.v_or, 'tolist') else obs.v_or
            logger.info("成功获取所有线路起始端的电压值。")
            return {
                "status": "success",
                "message": "成功获取所有线路起始端的电压值。",
                "data": result
            }
        else:
            result = obs.v_or[line_id].tolist() if hasattr(obs.v_or[line_id], 'tolist') else obs.v_or[line_id]
            logger.info("成功获取指定线路起始端的电压值。")
            return {
                "status": "success",
                "message": "成功获取指定线路起始端的电压值。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_v_or_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_v_or_impl 执行失败: {str(e)}"
        }


def obs_a_or_impl(env_manager, env_id: str, line_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中线路起始端（origin）的电流值。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    line_id (Optional[List[int]]): 可选的线路ID列表。如果提供，则返回指定线路起始端的电流值；
                                  如果为None，则返回所有线路起始端的电流值。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的线路起始端电流值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if line_id is None:
            logger.info(f"开始获取所有线路起始端的电流值，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定线路起始端的电流值，env_id: {env_id}, line_id: {line_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据line_id参数返回相应的数据
        if line_id is None:
            result = obs.a_or.tolist() if hasattr(obs.a_or, 'tolist') else obs.a_or
            logger.info("成功获取所有线路起始端的电流值。")
            return {
                "status": "success",
                "message": "成功获取所有线路起始端的电流值。",
                "data": result
            }
        else:
            result = obs.a_or[line_id].tolist() if hasattr(obs.a_or[line_id], 'tolist') else obs.a_or[line_id]
            logger.info("成功获取指定线路起始端的电流值。")
            return {
                "status": "success",
                "message": "成功获取指定线路起始端的电流值。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_a_or_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_a_or_impl 执行失败: {str(e)}"
        }


def obs_theta_or_impl(env_manager, env_id: str, line_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中线路起始端（origin）的电压角。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    line_id (Optional[List[int]]): 可选的线路ID列表。如果提供，则返回指定线路起始端的电压角；
                                  如果为None，则返回所有线路起始端的电压角。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的线路起始端电压角。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if line_id is None:
            logger.info(f"开始获取所有线路起始端的电压角，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定线路起始端的电压角，env_id: {env_id}, line_id: {line_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据line_id参数返回相应的数据
        if line_id is None:
            result = obs.theta_or.tolist() if hasattr(obs.theta_or, 'tolist') else obs.theta_or
            logger.info("成功获取所有线路起始端的电压角。")
            return {
                "status": "success",
                "message": "成功获取所有线路起始端的电压角。",
                "data": result
            }
        else:
            result = obs.theta_or[line_id].tolist() if hasattr(obs.theta_or[line_id], 'tolist') else obs.theta_or[line_id]
            logger.info("成功获取指定线路起始端的电压角。")
            return {
                "status": "success",
                "message": "成功获取指定线路起始端的电压角。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_theta_or_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_theta_or_impl 执行失败: {str(e)}"
        }


def obs_p_ex_impl(env_manager, env_id: str, line_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中线路终止端（extremity）的有功功率。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    line_id (Optional[List[int]]): 可选的线路ID列表。如果提供，则返回指定线路终止端的有功功率；
                                  如果为None，则返回所有线路终止端的有功功率。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的线路终止端有功功率值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if line_id is None:
            logger.info(f"开始获取所有线路终止端的有功功率，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定线路终止端的有功功率，env_id: {env_id}, line_id: {line_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据line_id参数返回相应的数据
        if line_id is None:
            result = obs.p_ex.tolist() if hasattr(obs.p_ex, 'tolist') else obs.p_ex
            logger.info("成功获取所有线路终止端的有功功率。")
            return {
                "status": "success",
                "message": "成功获取所有线路终止端的有功功率。",
                "data": result
            }
        else:
            result = obs.p_ex[line_id].tolist() if hasattr(obs.p_ex[line_id], 'tolist') else obs.p_ex[line_id]
            logger.info("成功获取指定线路终止端的有功功率。")
            return {
                "status": "success",
                "message": "成功获取指定线路终止端的有功功率。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_p_ex_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_p_ex_impl 执行失败: {str(e)}"
        }


def obs_q_ex_impl(env_manager, env_id: str, line_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中线路终止端（extremity）的无功功率。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    line_id (Optional[List[int]]): 可选的线路ID列表。如果提供，则返回指定线路终止端的无功功率；
                                  如果为None，则返回所有线路终止端的无功功率。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的线路终止端无功功率值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if line_id is None:
            logger.info(f"开始获取所有线路终止端的无功功率，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定线路终止端的无功功率，env_id: {env_id}, line_id: {line_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据line_id参数返回相应的数据
        if line_id is None:
            result = obs.q_ex.tolist() if hasattr(obs.q_ex, 'tolist') else obs.q_ex
            logger.info("成功获取所有线路终止端的无功功率。")
            return {
                "status": "success",
                "message": "成功获取所有线路终止端的无功功率。",
                "data": result
            }
        else:
            result = obs.q_ex[line_id].tolist() if hasattr(obs.q_ex[line_id], 'tolist') else obs.q_ex[line_id]
            logger.info("成功获取指定线路终止端的无功功率。")
            return {
                "status": "success",
                "message": "成功获取指定线路终止端的无功功率。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_q_ex_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_q_ex_impl 执行失败: {str(e)}"
        }


def obs_v_ex_impl(env_manager, env_id: str, line_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中线路终止端（extremity）的电压值。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    line_id (Optional[List[int]]): 可选的线路ID列表。如果提供，则返回指定线路终止端的电压值；
                                  如果为None，则返回所有线路终止端的电压值。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的线路终止端电压值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if line_id is None:
            logger.info(f"开始获取所有线路终止端的电压值，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定线路终止端的电压值，env_id: {env_id}, line_id: {line_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据line_id参数返回相应的数据
        if line_id is None:
            result = obs.v_ex.tolist() if hasattr(obs.v_ex, 'tolist') else obs.v_ex
            logger.info("成功获取所有线路终止端的电压值。")
            return {
                "status": "success",
                "message": "成功获取所有线路终止端的电压值。",
                "data": result
            }
        else:
            result = obs.v_ex[line_id].tolist() if hasattr(obs.v_ex[line_id], 'tolist') else obs.v_ex[line_id]
            logger.info("成功获取指定线路终止端的电压值。")
            return {
                "status": "success",
                "message": "成功获取指定线路终止端的电压值。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_v_ex_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_v_ex_impl 执行失败: {str(e)}"
        }


def obs_a_ex_impl(env_manager, env_id: str, line_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中线路终止端（extremity）的电流值。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    line_id (Optional[List[int]]): 可选的线路ID列表。如果提供，则返回指定线路终止端的电流值；
                                  如果为None，则返回所有线路终止端的电流值。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的线路终止端电流值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if line_id is None:
            logger.info(f"开始获取所有线路终止端的电流值，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定线路终止端的电流值，env_id: {env_id}, line_id: {line_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据line_id参数返回相应的数据
        if line_id is None:
            result = obs.a_ex.tolist() if hasattr(obs.a_ex, 'tolist') else obs.a_ex
            logger.info("成功获取所有线路终止端的电流值。")
            return {
                "status": "success",
                "message": "成功获取所有线路终止端的电流值。",
                "data": result
            }
        else:
            result = obs.a_ex[line_id].tolist() if hasattr(obs.a_ex[line_id], 'tolist') else obs.a_ex[line_id]
            logger.info("成功获取指定线路终止端的电流值。")
            return {
                "status": "success",
                "message": "成功获取指定线路终止端的电流值。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_a_ex_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_a_ex_impl 执行失败: {str(e)}"
        }


def obs_theta_ex_impl(env_manager, env_id: str, line_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中线路终止端（extremity）的电压角。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    line_id (Optional[List[int]]): 可选的线路ID列表。如果提供，则返回指定线路终止端的电压角；
                                  如果为None，则返回所有线路终止端的电压角。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的线路终止端电压角。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if line_id is None:
            logger.info(f"开始获取所有线路终止端的电压角，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定线路终止端的电压角，env_id: {env_id}, line_id: {line_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据line_id参数返回相应的数据
        if line_id is None:
            result = obs.theta_ex.tolist() if hasattr(obs.theta_ex, 'tolist') else obs.theta_ex
            logger.info("成功获取所有线路终止端的电压角。")
            return {
                "status": "success",
                "message": "成功获取所有线路终止端的电压角。",
                "data": result
            }
        else:
            result = obs.theta_ex[line_id].tolist() if hasattr(obs.theta_ex[line_id], 'tolist') else obs.theta_ex[line_id]
            logger.info("成功获取指定线路终止端的电压角。")
            return {
                "status": "success",
                "message": "成功获取指定线路终止端的电压角。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_theta_ex_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_theta_ex_impl 执行失败: {str(e)}"
        }


def obs_rho_impl(env_manager, env_id: str, line_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中线路的容量利用率（rho）。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    line_id (Optional[List[int]]): 可选的线路ID列表。如果提供，则返回指定线路的容量利用率；
                                  如果为None，则返回所有线路的容量利用率。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的线路容量利用率值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if line_id is None:
            logger.info(f"开始获取所有线路的容量利用率，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定线路的容量利用率，env_id: {env_id}, line_id: {line_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据line_id参数返回相应的数据
        if line_id is None:
            result = obs.rho.tolist() if hasattr(obs.rho, 'tolist') else obs.rho
            logger.info("成功获取所有线路的容量利用率。")
            return {
                "status": "success",
                "message": "成功获取所有线路的容量利用率。",
                "data": result
            }
        else:
            result = obs.rho[line_id].tolist() if hasattr(obs.rho[line_id], 'tolist') else obs.rho[line_id]
            logger.info("成功获取指定线路的容量利用率。")
            return {
                "status": "success",
                "message": "成功获取指定线路的容量利用率。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_rho_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_rho_impl 执行失败: {str(e)}"
        }


def obs_line_status_impl(env_manager, env_id: str, line_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中线路的连接状态。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    line_id (Optional[List[int]]): 可选的线路ID列表。如果提供，则返回指定线路的连接状态；
                                  如果为None，则返回所有线路的连接状态。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的线路连接状态（True表示已连接，False表示断开）。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if line_id is None:
            logger.info(f"开始获取所有线路的连接状态，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定线路的连接状态，env_id: {env_id}, line_id: {line_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据line_id参数返回相应的数据
        if line_id is None:
            result = obs.line_status.tolist() if hasattr(obs.line_status, 'tolist') else obs.line_status
            logger.info("成功获取所有线路的连接状态。")
            return {
                "status": "success",
                "message": "成功获取所有线路的连接状态。",
                "data": result
            }
        else:
            result = obs.line_status[line_id].tolist() if hasattr(obs.line_status[line_id], 'tolist') else obs.line_status[line_id]
            logger.info("成功获取指定线路的连接状态。")
            return {
                "status": "success",
                "message": "成功获取指定线路的连接状态。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_line_status_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_line_status_impl 执行失败: {str(e)}"
        }


def obs_timestep_overflow_impl(env_manager, env_id: str, line_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中线路的过载时间步长。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    line_id (Optional[List[int]]): 可选的线路ID列表。如果提供，则返回指定线路的过载时间步长；
                                  如果为None，则返回所有线路的过载时间步长。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的线路过载时间步长值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if line_id is None:
            logger.info(f"开始获取所有线路的过载时间步长，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定线路的过载时间步长，env_id: {env_id}, line_id: {line_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据line_id参数返回相应的数据
        if line_id is None:
            result = obs.timestep_overflow.tolist() if hasattr(obs.timestep_overflow, 'tolist') else obs.timestep_overflow
            logger.info("成功获取所有线路的过载时间步长。")
            return {
                "status": "success",
                "message": "成功获取所有线路的过载时间步长。",
                "data": result
            }
        else:
            result = obs.timestep_overflow[line_id].tolist() if hasattr(obs.timestep_overflow[line_id], 'tolist') else obs.timestep_overflow[line_id]
            logger.info("成功获取指定线路的过载时间步长。")
            return {
                "status": "success",
                "message": "成功获取指定线路的过载时间步长。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_timestep_overflow_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_timestep_overflow_impl 执行失败: {str(e)}"
        }


def obs_time_before_cooldown_line_impl(env_manager, env_id: str, line_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中线路的冷却剩余时间。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    line_id (Optional[List[int]]): 可选的线路ID列表。如果提供，则返回指定线路的冷却剩余时间；
                                  如果为None，则返回所有线路的冷却剩余时间。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的线路冷却剩余时间值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if line_id is None:
            logger.info(f"开始获取所有线路的冷却剩余时间，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定线路的冷却剩余时间，env_id: {env_id}, line_id: {line_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据line_id参数返回相应的数据
        if line_id is None:
            result = obs.time_before_cooldown_line.tolist() if hasattr(obs.time_before_cooldown_line, 'tolist') else obs.time_before_cooldown_line
            logger.info("成功获取所有线路的冷却剩余时间。")
            return {
                "status": "success",
                "message": "成功获取所有线路的冷却剩余时间。",
                "data": result
            }
        else:
            result = obs.time_before_cooldown_line[line_id].tolist() if hasattr(obs.time_before_cooldown_line[line_id], 'tolist') else obs.time_before_cooldown_line[line_id]
            logger.info("成功获取指定线路的冷却剩余时间。")
            return {
                "status": "success",
                "message": "成功获取指定线路的冷却剩余时间。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_time_before_cooldown_line_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_time_before_cooldown_line_impl 执行失败: {str(e)}"
        }


def obs_time_before_cooldown_sub_impl(env_manager, env_id: str, sub_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中变电站的冷却剩余时间。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    sub_id (Optional[List[int]]): 可选的变电站ID列表。如果提供，则返回指定变电站的冷却剩余时间；
                                如果为None，则返回所有变电站的冷却剩余时间。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的变电站冷却剩余时间值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if sub_id is None:
            logger.info(f"开始获取所有变电站的冷却剩余时间，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定变电站的冷却剩余时间，env_id: {env_id}, sub_id: {sub_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据sub_id参数返回相应的数据
        if sub_id is None:
            result = obs.time_before_cooldown_sub.tolist() if hasattr(obs.time_before_cooldown_sub, 'tolist') else obs.time_before_cooldown_sub
            logger.info("成功获取所有变电站的冷却剩余时间。")
            return {
                "status": "success",
                "message": "成功获取所有变电站的冷却剩余时间。",
                "data": result
            }
        else:
            result = obs.time_before_cooldown_sub[sub_id].tolist() if hasattr(obs.time_before_cooldown_sub[sub_id], 'tolist') else obs.time_before_cooldown_sub[sub_id]
            logger.info("成功获取指定变电站的冷却剩余时间。")
            return {
                "status": "success",
                "message": "成功获取指定变电站的冷却剩余时间。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_time_before_cooldown_sub_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_time_before_cooldown_sub_impl 执行失败: {str(e)}"
        }


def obs_time_next_maintenance_impl(env_manager, env_id: str, line_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中线路的下一次维护时间。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    line_id (Optional[List[int]]): 可选的线路ID列表。如果提供，则返回指定线路的下一次维护时间；
                                  如果为None，则返回所有线路的下一次维护时间。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的线路下一次维护时间值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if line_id is None:
            logger.info(f"开始获取所有线路的下一次维护时间，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定线路的下一次维护时间，env_id: {env_id}, line_id: {line_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据line_id参数返回相应的数据
        if line_id is None:
            result = obs.time_next_maintenance.tolist() if hasattr(obs.time_next_maintenance, 'tolist') else obs.time_next_maintenance
            logger.info("成功获取所有线路的下一次维护时间。")
            return {
                "status": "success",
                "message": "成功获取所有线路的下一次维护时间。",
                "data": result
            }
        else:
            result = obs.time_next_maintenance[line_id].tolist() if hasattr(obs.time_next_maintenance[line_id], 'tolist') else obs.time_next_maintenance[line_id]
            logger.info("成功获取指定线路的下一次维护时间。")
            return {
                "status": "success",
                "message": "成功获取指定线路的下一次维护时间。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_time_next_maintenance_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_time_next_maintenance_impl 执行失败: {str(e)}"
        }


def obs_duration_next_maintenance_impl(env_manager, env_id: str, line_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中线路的下一次维护持续时间。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    line_id (Optional[List[int]]): 可选的线路ID列表。如果提供，则返回指定线路的下一次维护持续时间；
                                  如果为None，则返回所有线路的下一次维护持续时间。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的线路下一次维护持续时间值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if line_id is None:
            logger.info(f"开始获取所有线路的下一次维护持续时间，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定线路的下一次维护持续时间，env_id: {env_id}, line_id: {line_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据line_id参数返回相应的数据
        if line_id is None:
            result = obs.duration_next_maintenance.tolist() if hasattr(obs.duration_next_maintenance, 'tolist') else obs.duration_next_maintenance
            logger.info("成功获取所有线路的下一次维护持续时间。")
            return {
                "status": "success",
                "message": "成功获取所有线路的下一次维护持续时间。",
                "data": result
            }
        else:
            result = obs.duration_next_maintenance[line_id].tolist() if hasattr(obs.duration_next_maintenance[line_id], 'tolist') else obs.duration_next_maintenance[line_id]
            logger.info("成功获取指定线路的下一次维护持续时间。")
            return {
                "status": "success",
                "message": "成功获取指定线路的下一次维护持续时间。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_duration_next_maintenance_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_duration_next_maintenance_impl 执行失败: {str(e)}"
        }


def obs_target_dispatch_impl(env_manager, env_id: str, gen_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中发电机的目标调度值。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    gen_id (Optional[List[int]]): 可选的发电机ID列表。如果提供，则返回指定发电机的目标调度值；
                                如果为None，则返回所有发电机的目标调度值。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的发电机目标调度值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if gen_id is None:
            logger.info(f"开始获取所有发电机的目标调度值，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定发电机的目标调度值，env_id: {env_id}, gen_id: {gen_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据gen_id参数返回相应的数据
        if gen_id is None:
            result = obs.target_dispatch.tolist() if hasattr(obs.target_dispatch, 'tolist') else obs.target_dispatch
            logger.info("成功获取所有发电机的目标调度值。")
            return {
                "status": "success",
                "message": "成功获取所有发电机的目标调度值。",
                "data": result
            }
        else:
            result = obs.target_dispatch[gen_id].tolist() if hasattr(obs.target_dispatch[gen_id], 'tolist') else obs.target_dispatch[gen_id]
            logger.info("成功获取指定发电机的目标调度值。")
            return {
                "status": "success",
                "message": "成功获取指定发电机的目标调度值。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_target_dispatch_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_target_dispatch_impl 执行失败: {str(e)}"
        }


def obs_actual_dispatch_impl(env_manager, env_id: str, gen_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中发电机的实际调度值。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    gen_id (Optional[List[int]]): 可选的发电机ID列表。如果提供，则返回指定发电机的实际调度值；
                                如果为None，则返回所有发电机的实际调度值。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的发电机实际调度值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if gen_id is None:
            logger.info(f"开始获取所有发电机的实际调度值，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定发电机的实际调度值，env_id: {env_id}, gen_id: {gen_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据gen_id参数返回相应的数据
        if gen_id is None:
            result = obs.actual_dispatch.tolist() if hasattr(obs.actual_dispatch, 'tolist') else obs.actual_dispatch
            logger.info("成功获取所有发电机的实际调度值。")
            return {
                "status": "success",
                "message": "成功获取所有发电机的实际调度值。",
                "data": result
            }
        else:
            result = obs.actual_dispatch[gen_id].tolist() if hasattr(obs.actual_dispatch[gen_id], 'tolist') else obs.actual_dispatch[gen_id]
            logger.info("成功获取指定发电机的实际调度值。")
            return {
                "status": "success",
                "message": "成功获取指定发电机的实际调度值。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_actual_dispatch_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_actual_dispatch_impl 执行失败: {str(e)}"
        }


def obs_storage_charge_impl(env_manager, env_id: str, storage_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中储能设备的充电状态。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    storage_id (Optional[List[int]]): 可选的储能设备ID列表。如果提供，则返回指定储能设备的充电状态；
                                    如果为None，则返回所有储能设备的充电状态。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的储能设备充电状态。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if storage_id is None:
            logger.info(f"开始获取所有储能设备的充电状态，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定储能设备的充电状态，env_id: {env_id}, storage_id: {storage_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据storage_id参数返回相应的数据
        if storage_id is None:
            result = obs.storage_charge.tolist() if hasattr(obs.storage_charge, 'tolist') else obs.storage_charge
            logger.info("成功获取所有储能设备的充电状态。")
            return {
                "status": "success",
                "message": "成功获取所有储能设备的充电状态。",
                "data": result
            }
        else:
            result = obs.storage_charge[storage_id].tolist() if hasattr(obs.storage_charge[storage_id], 'tolist') else obs.storage_charge[storage_id]
            logger.info("成功获取指定储能设备的充电状态。")
            return {
                "status": "success",
                "message": "成功获取指定储能设备的充电状态。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_storage_charge_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_storage_charge_impl 执行失败: {str(e)}"
        }


def obs_storage_power_target_impl(env_manager, env_id: str, storage_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中储能设备的目标功率值。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    storage_id (Optional[List[int]]): 可选的储能设备ID列表。如果提供，则返回指定储能设备的目标功率值；
                                    如果为None，则返回所有储能设备的目标功率值。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的储能设备目标功率值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if storage_id is None:
            logger.info(f"开始获取所有储能设备的目标功率值，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定储能设备的目标功率值，env_id: {env_id}, storage_id: {storage_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据storage_id参数返回相应的数据
        if storage_id is None:
            result = obs.storage_power_target.tolist() if hasattr(obs.storage_power_target, 'tolist') else obs.storage_power_target
            logger.info("成功获取所有储能设备的目标功率值。")
            return {
                "status": "success",
                "message": "成功获取所有储能设备的目标功率值。",
                "data": result
            }
        else:
            result = obs.storage_power_target[storage_id].tolist() if hasattr(obs.storage_power_target[storage_id], 'tolist') else obs.storage_power_target[storage_id]
            logger.info("成功获取指定储能设备的目标功率值。")
            return {
                "status": "success",
                "message": "成功获取指定储能设备的目标功率值。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_storage_power_target_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_storage_power_target_impl 执行失败: {str(e)}"
        }


def obs_storage_power_impl(env_manager, env_id: str, storage_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中储能设备的实际功率值。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    storage_id (Optional[List[int]]): 可选的储能设备ID列表。如果提供，则返回指定储能设备的实际功率值；
                                    如果为None，则返回所有储能设备的实际功率值。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的储能设备实际功率值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if storage_id is None:
            logger.info(f"开始获取所有储能设备的实际功率值，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定储能设备的实际功率值，env_id: {env_id}, storage_id: {storage_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据storage_id参数返回相应的数据
        if storage_id is None:
            result = obs.storage_power.tolist() if hasattr(obs.storage_power, 'tolist') else obs.storage_power
            logger.info("成功获取所有储能设备的实际功率值。")
            return {
                "status": "success",
                "message": "成功获取所有储能设备的实际功率值。",
                "data": result
            }
        else:
            result = obs.storage_power[storage_id].tolist() if hasattr(obs.storage_power[storage_id], 'tolist') else obs.storage_power[storage_id]
            logger.info("成功获取指定储能设备的实际功率值。")
            return {
                "status": "success",
                "message": "成功获取指定储能设备的实际功率值。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_storage_power_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_storage_power_impl 执行失败: {str(e)}"
        }


def obs_storage_theta_impl(env_manager, env_id: str, storage_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中储能设备的相角值。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    storage_id (Optional[List[int]]): 可选的储能设备ID列表。如果提供，则返回指定储能设备的相角值；
                                    如果为None，则返回所有储能设备的相角值。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的储能设备相角值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if storage_id is None:
            logger.info(f"开始获取所有储能设备的相角值，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定储能设备的相角值，env_id: {env_id}, storage_id: {storage_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据storage_id参数返回相应的数据
        if storage_id is None:
            result = obs.storage_theta.tolist() if hasattr(obs.storage_theta, 'tolist') else obs.storage_theta
            logger.info("成功获取所有储能设备的相角值。")
            return {
                "status": "success",
                "message": "成功获取所有储能设备的相角值。",
                "data": result
            }
        else:
            result = obs.storage_theta[storage_id].tolist() if hasattr(obs.storage_theta[storage_id], 'tolist') else obs.storage_theta[storage_id]
            logger.info("成功获取指定储能设备的相角值。")
            return {
                "status": "success",
                "message": "成功获取指定储能设备的相角值。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_storage_theta_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_storage_theta_impl 执行失败: {str(e)}"
        }


def obs_gen_p_before_curtail_impl(env_manager, env_id: str, gen_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中发电机在削减前的有功功率。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    gen_id (Optional[List[int]]): 可选的发电机ID列表。如果提供，则返回指定发电机在削减前的有功功率；
                                如果为None，则返回所有发电机在削减前的有功功率。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的发电机在削减前的有功功率值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if gen_id is None:
            logger.info(f"开始获取所有发电机在削减前的有功功率，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定发电机在削减前的有功功率，env_id: {env_id}, gen_id: {gen_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据gen_id参数返回相应的数据
        if gen_id is None:
            result = obs.gen_p_before_curtail.tolist() if hasattr(obs.gen_p_before_curtail, 'tolist') else obs.gen_p_before_curtail
            logger.info("成功获取所有发电机在削减前的有功功率。")
            return {
                "status": "success",
                "message": "成功获取所有发电机在削减前的有功功率。",
                "data": result
            }
        else:
            result = obs.gen_p_before_curtail[gen_id].tolist() if hasattr(obs.gen_p_before_curtail[gen_id], 'tolist') else obs.gen_p_before_curtail[gen_id]
            logger.info("成功获取指定发电机在削减前的有功功率。")
            return {
                "status": "success",
                "message": "成功获取指定发电机在削减前的有功功率。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_gen_p_before_curtail_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_gen_p_before_curtail_impl 执行失败: {str(e)}"
        }


def obs_curtailment_mw_impl(env_manager, env_id: str, gen_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中发电机的功率削减量（MW）。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    gen_id (Optional[List[int]]): 可选的发电机ID列表。如果提供，则返回指定发电机的功率削减量；
                                如果为None，则返回所有发电机的功率削减量。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的发电机功率削减量（MW）。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if gen_id is None:
            logger.info(f"开始获取所有发电机的功率削减量，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定发电机的功率削减量，env_id: {env_id}, gen_id: {gen_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据gen_id参数返回相应的数据
        if gen_id is None:
            result = obs.curtailment_mw.tolist() if hasattr(obs.curtailment_mw, 'tolist') else obs.curtailment_mw
            logger.info("成功获取所有发电机的功率削减量。")
            return {
                "status": "success",
                "message": "成功获取所有发电机的功率削减量。",
                "data": result
            }
        else:
            result = obs.curtailment_mw[gen_id].tolist() if hasattr(obs.curtailment_mw[gen_id], 'tolist') else obs.curtailment_mw[gen_id]
            logger.info("成功获取指定发电机的功率削减量。")
            return {
                "status": "success",
                "message": "成功获取指定发电机的功率削减量。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_curtailment_mw_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_curtailment_mw_impl 执行失败: {str(e)}"
        }


def obs_curtailment_impl(env_manager, env_id: str, gen_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中发电机的削减比例（百分比）。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    gen_id (Optional[List[int]]): 可选的发电机ID列表。如果提供，则返回指定发电机的削减比例；
                                如果为None，则返回所有发电机的削减比例。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的发电机削减比例。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if gen_id is None:
            logger.info(f"开始获取所有发电机的削减比例，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定发电机的削减比例，env_id: {env_id}, gen_id: {gen_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据gen_id参数返回相应的数据
        if gen_id is None:
            result = obs.curtailment.tolist() if hasattr(obs.curtailment, 'tolist') else obs.curtailment
            logger.info("成功获取所有发电机的削减比例。")
            return {
                "status": "success",
                "message": "成功获取所有发电机的削减比例。",
                "data": result
            }
        else:
            result = obs.curtailment[gen_id].tolist() if hasattr(obs.curtailment[gen_id], 'tolist') else obs.curtailment[gen_id]
            logger.info("成功获取指定发电机的削减比例。")
            return {
                "status": "success",
                "message": "成功获取指定发电机的削减比例。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_curtailment_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_curtailment_impl 执行失败: {str(e)}"
        }


def obs_curtailment_limit_impl(env_manager, env_id: str, gen_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中发电机的削减限制值。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    gen_id (Optional[List[int]]): 可选的发电机ID列表。如果提供，则返回指定发电机的削减限制值；
                                如果为None，则返回所有发电机的削减限制值。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的发电机削减限制值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if gen_id is None:
            logger.info(f"开始获取所有发电机的削减限制值，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定发电机的削减限制值，env_id: {env_id}, gen_id: {gen_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据gen_id参数返回相应的数据
        if gen_id is None:
            result = obs.curtailment_limit.tolist() if hasattr(obs.curtailment_limit, 'tolist') else obs.curtailment_limit
            logger.info("成功获取所有发电机的削减限制值。")
            return {
                "status": "success",
                "message": "成功获取所有发电机的削减限制值。",
                "data": result
            }
        else:
            result = obs.curtailment_limit[gen_id].tolist() if hasattr(obs.curtailment_limit[gen_id], 'tolist') else obs.curtailment_limit[gen_id]
            logger.info("成功获取指定发电机的削减限制值。")
            return {
                "status": "success",
                "message": "成功获取指定发电机的削减限制值。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_curtailment_limit_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_curtailment_limit_impl 执行失败: {str(e)}"
        }


def obs_gen_margin_up_impl(env_manager, env_id: str, gen_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中发电机的上调余量。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    gen_id (Optional[List[int]]): 可选的发电机ID列表。如果提供，则返回指定发电机的上调余量；
                                如果为None，则返回所有发电机的上调余量。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的发电机上调余量值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if gen_id is None:
            logger.info(f"开始获取所有发电机的上调余量，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定发电机的上调余量，env_id: {env_id}, gen_id: {gen_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据gen_id参数返回相应的数据
        if gen_id is None:
            result = obs.gen_margin_up.tolist() if hasattr(obs.gen_margin_up, 'tolist') else obs.gen_margin_up
            logger.info("成功获取所有发电机的上调余量。")
            return {
                "status": "success",
                "message": "成功获取所有发电机的上调余量。",
                "data": result
            }
        else:
            result = obs.gen_margin_up[gen_id].tolist() if hasattr(obs.gen_margin_up[gen_id], 'tolist') else obs.gen_margin_up[gen_id]
            logger.info("成功获取指定发电机的上调余量。")
            return {
                "status": "success",
                "message": "成功获取指定发电机的上调余量。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_gen_margin_up_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_gen_margin_up_impl 执行失败: {str(e)}"
        }


def obs_gen_margin_down_impl(env_manager, env_id: str, gen_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中发电机的下调余量。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    gen_id (Optional[List[int]]): 可选的发电机ID列表。如果提供，则返回指定发电机的下调余量；
                                如果为None，则返回所有发电机的下调余量。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的发电机下调余量值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if gen_id is None:
            logger.info(f"开始获取所有发电机的下调余量，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定发电机的下调余量，env_id: {env_id}, gen_id: {gen_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据gen_id参数返回相应的数据
        if gen_id is None:
            result = obs.gen_margin_down.tolist() if hasattr(obs.gen_margin_down, 'tolist') else obs.gen_margin_down
            logger.info("成功获取所有发电机的下调余量。")
            return {
                "status": "success",
                "message": "成功获取所有发电机的下调余量。",
                "data": result
            }
        else:
            result = obs.gen_margin_down[gen_id].tolist() if hasattr(obs.gen_margin_down[gen_id], 'tolist') else obs.gen_margin_down[gen_id]
            logger.info("成功获取指定发电机的下调余量。")
            return {
                "status": "success",
                "message": "成功获取指定发电机的下调余量。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_gen_margin_down_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_gen_margin_down_impl 执行失败: {str(e)}"
        }


# 2. Others
def obs_date_time_impl(env_manager, env_id: str) -> Dict[str, Any]:
    """
    获取grid2op环境中当前观测的日期和时间信息。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含观测的日期和时间信息，包括年、月、日、
                  一天中的小时、小时中的分钟以及星期几。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        logger.info(f"开始获取观测的日期和时间信息，env_id: {env_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 创建日期和时间信息字典
        obs_date = {
            'year': obs.year,
            'month': obs.month,
            'day': obs.day,
            'hour_of_day': obs.hour_of_day,
            'minute_of_hour': obs.minute_of_hour,
            'day_of_week': obs.day_of_week
        }
        
        logger.info("成功获取观测的日期和时间信息。")
        return {
            "status": "success",
            "message": "成功获取观测的日期和时间信息。",
            "data": obs_date
        }
    except Exception as e:
        logger.error(f"obs_date_time_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_date_time_impl 执行失败: {str(e)}"
        }


def obs_topo_vect_impl(env_manager, env_id: str, element_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中电网的拓扑结构向量。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    element_id (Optional[List[int]]): 可选的元素ID列表。如果提供，则返回指定元素的拓扑结构信息；
                                    如果为None，则返回整个电网的拓扑结构向量。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的拓扑结构向量。
                  拓扑向量中的每个值代表对应元素连接到的母线编号（1或2）或断开状态（-1）。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if element_id is None:
            logger.info(f"开始获取完整的电网拓扑结构向量，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定元素的拓扑结构信息，env_id: {env_id}, element_id: {element_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 根据element_id参数返回相应的数据
        if element_id is None:
            result = obs.topo_vect.tolist() if hasattr(obs.topo_vect, 'tolist') else obs.topo_vect
            logger.info("成功获取完整的电网拓扑结构向量。")
            return {
                "status": "success",
                "message": "成功获取完整的电网拓扑结构向量。",
                "data": result
            }
        else:
            result = obs.topo_vect[element_id].tolist() if hasattr(obs.topo_vect[element_id], 'tolist') else obs.topo_vect[element_id]
            logger.info("成功获取指定元素的拓扑结构信息。")
            return {
                "status": "success",
                "message": "成功获取指定元素的拓扑结构信息。",
                "data": result
            }
    except Exception as e:
        logger.error(f"obs_topo_vect_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_topo_vect_impl 执行失败: {str(e)}"
        }


def obs_is_alarm_illegal_impl(env_manager, env_id: str) -> Dict[str, Any]:
    """
    获取grid2op环境中当前是否无法发送告警的状态。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据为布尔值，指示当前是否无法发送告警。
                  True表示当前无法发送告警，False表示当前可以发送告警。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    RuntimeError: 如果环境没有配置告警功能。
    """
    try:
        logger.info(f"开始获取当前是否无法发送告警的状态，env_id: {env_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 检查环境是否支持告警功能
        if not hasattr(obs, 'is_alarm_illegal'):
            raise RuntimeError(f"env_id 为 {env_id} 的环境未配置告警功能。")
        
        result = bool(obs.is_alarm_illegal)
        logger.info(f"成功获取当前是否无法发送告警的状态。结果: {result}")
        return {
            "status": "success",
            "message": "成功获取当前是否无法发送告警的状态。",
            "data": result
        }
    except Exception as e:
        logger.error(f"obs_is_alarm_illegal_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_is_alarm_illegal_impl 执行失败: {str(e)}"
        }


def obs_time_since_last_alarm_impl(env_manager, env_id: str) -> Dict[str, Any]:
    """
    获取grid2op环境中自上次发送告警以来经过的时间步数。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据为整数，表示自上次发送告警以来经过的时间步数。
                  如果从未发送过告警，则返回一个很大的值（通常为-1或环境的最大步数）。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    RuntimeError: 如果环境没有配置告警功能。
    """
    try:
        logger.info(f"开始获取自上次发送告警以来经过的时间步数，env_id: {env_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 检查环境是否支持告警功能
        if not hasattr(obs, 'time_since_last_alarm'):
            raise RuntimeError(f"env_id 为 {env_id} 的环境未配置告警功能。")
        
        result = int(obs.time_since_last_alarm)
        logger.info(f"成功获取自上次发送告警以来经过的时间步数。结果: {result}")
        return {
            "status": "success",
            "message": "成功获取自上次发送告警以来经过的时间步数。",
            "data": result
        }
    except Exception as e:
        logger.error(f"obs_time_since_last_alarm_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_time_since_last_alarm_impl 执行失败: {str(e)}"
        }


def obs_last_alarm_impl(env_manager, env_id: str) -> Dict[str, Any]:
    """
    获取grid2op环境中上次发送的告警区域ID列表。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据为整数列表，表示上次告警涉及的区域ID。
                  如果从未发送过告警，则可能返回空列表或者特定的默认值。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    RuntimeError: 如果环境没有配置告警功能。
    """
    try:
        logger.info(f"开始获取上次发送的告警区域ID列表，env_id: {env_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 检查环境是否支持告警功能
        if not hasattr(obs, 'last_alarm'):
            raise RuntimeError(f"env_id 为 {env_id} 的环境未配置告警功能。")
        
        # 转换为列表格式
        result = obs.last_alarm.tolist() if hasattr(obs.last_alarm, 'tolist') else obs.last_alarm
        
        logger.info("成功获取上次发送的告警区域ID列表。")
        return {
            "status": "success",
            "message": "成功获取上次发送的告警区域ID列表。",
            "data": result
        }
    except Exception as e:
        logger.error(f"obs_last_alarm_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_last_alarm_impl 执行失败: {str(e)}"
        }


def obs_attention_budget_impl(env_manager, env_id: str) -> Dict[str, Any]:
    """
    获取grid2op环境中当前的注意力预算值。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据为浮点数或整数，表示当前剩余的注意力预算。
                  注意力预算是用于限制智能体可以发送的告警次数的资源。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    RuntimeError: 如果环境没有配置注意力预算功能。
    """
    try:
        logger.info(f"开始获取当前的注意力预算值，env_id: {env_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 检查环境是否支持注意力预算功能
        if not hasattr(obs, 'attention_budget'):
            raise RuntimeError(f"env_id 为 {env_id} 的环境未配置注意力预算功能。")
        
        result = float(obs.attention_budget)
        logger.info(f"成功获取当前的注意力预算值。结果: {result}")
        return {
            "status": "success",
            "message": "成功获取当前的注意力预算值。",
            "data": result
        }
    except Exception as e:
        logger.error(f"obs_attention_budget_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_attention_budget_impl 执行失败: {str(e)}"
        }


def obs_max_step_impl(env_manager, env_id: str) -> Dict[str, Any]:
    """
    获取grid2op环境中允许的最大步数。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据为整数，表示环境允许的最大步数。
                  这个值表示一个训练或评估场景的总时长。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        logger.info(f"开始获取环境允许的最大步数，env_id: {env_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 检查属性是否存在
        if not hasattr(obs, 'max_step'):
            raise AttributeError(f"env_id 为 {env_id} 的环境没有 max_step 属性。")
        
        result = int(obs.max_step)
        logger.info(f"成功获取环境允许的最大步数。结果: {result}")
        return {
            "status": "success",
            "message": "成功获取环境允许的最大步数。",
            "data": result
        }
    except Exception as e:
        logger.error(f"obs_max_step_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_max_step_impl 执行失败: {str(e)}"
        }


def obs_current_step_impl(env_manager, env_id: str) -> Dict[str, Any]:
    """
    获取grid2op环境中当前已执行的步数。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据为整数，表示当前已执行的步数。
                  初始步为0，随着环境的每一次step()调用而增加。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        logger.info(f"开始获取当前已执行的步数，env_id: {env_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 检查属性是否存在
        if not hasattr(obs, 'current_step'):
            raise AttributeError(f"env_id 为 {env_id} 的环境没有 current_step 属性。")
        
        result = int(obs.current_step)
        logger.info(f"成功获取当前已执行的步数。结果: {result}")
        return {
            "status": "success",
            "message": "成功获取当前已执行的步数。",
            "data": result
        }
    except Exception as e:
        logger.error(f"obs_current_step_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_current_step_impl 执行失败: {str(e)}"
        }


def obs_delta_time_impl(env_manager, env_id: str) -> Dict[str, Any]:
    """
    获取grid2op环境中两次观测之间的时间间隔。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据为整数或浮点数，表示两次观测之间的时间间隔（通常以分钟为单位）。
                  这个值对于理解时序数据和执行时间相关的控制策略非常重要。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        logger.info(f"开始获取两次观测之间的时间间隔，env_id: {env_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 检查属性是否存在
        if not hasattr(obs, 'delta_time'):
            raise AttributeError(f"env_id 为 {env_id} 的环境没有 delta_time 属性。")
        
        result = float(obs.delta_time)
        logger.info(f"成功获取两次观测之间的时间间隔。结果: {result}")
        return {
            "status": "success",
            "message": "成功获取两次观测之间的时间间隔。",
            "data": result
        }
    except Exception as e:
        logger.error(f"obs_delta_time_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_delta_time_impl 执行失败: {str(e)}"
        }


def obs_total_number_of_alert_impl(env_manager, env_id: str, alert_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中已发出的告警总数。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    alert_id (Optional[List[int]]): 可选的告警区域ID列表。如果提供，则返回指定区域的告警总数；
                                  如果为None，则返回所有区域的告警总数。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的告警总数信息。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if alert_id is None:
            logger.info(f"开始获取所有区域的告警总数，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定区域的告警总数，env_id: {env_id}, alert_id: {alert_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 获取告警总数，并根据alert_id返回相应的数据
        total_alerts = obs.total_number_of_alert
        
        # 处理可能的numpy数组类型
        if isinstance(total_alerts, np.ndarray):
            if alert_id is None:
                result = total_alerts.tolist() if hasattr(total_alerts, 'tolist') else total_alerts
                logger.info(f"成功获取所有区域的告警总数。")
            else:
                result = total_alerts[alert_id].tolist() if hasattr(total_alerts[alert_id], 'tolist') else total_alerts[alert_id]
                logger.info(f"成功获取指定区域的告警总数。")
        else:
            # 如果是标量值
            result = int(total_alerts)
            logger.info(f"成功获取告警总数：{result}个。")
        
        return {
            "status": "success",
            "message": "成功获取告警总数。",
            "data": result
        }
    except Exception as e:
        logger.error(f"obs_total_number_of_alert_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_total_number_of_alert_impl 执行失败: {str(e)}"
        }


def obs_was_alert_used_after_attack_impl(env_manager, env_id: str, alert_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中在攻击之后是否使用过告警系统。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    alert_id (Optional[List[int]]): 可选的告警区域ID列表。如果提供，则返回指定区域的告警使用情况；
                                  如果为None，则返回所有区域的告警使用情况。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的告警使用情况信息。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if alert_id is None:
            logger.info(f"开始检查所有区域在攻击之后是否使用过告警系统，env_id: {env_id}")
        else:
            logger.info(f"开始检查指定区域在攻击之后是否使用过告警系统，env_id: {env_id}, alert_id: {alert_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 获取在攻击之后是否使用过告警系统
        alert_usage = obs.was_alert_used_after_attack
        
        # 处理可能的numpy数组类型
        if isinstance(alert_usage, np.ndarray):
            if alert_id is None:
                result = alert_usage.tolist() if hasattr(alert_usage, 'tolist') else alert_usage
                logger.info(f"成功检查所有区域在攻击之后的告警使用情况。")
            else:
                result = alert_usage[alert_id].tolist() if hasattr(alert_usage[alert_id], 'tolist') else alert_usage[alert_id]
                logger.info(f"成功检查指定区域在攻击之后的告警使用情况。")
        else:
            # 如果是标量值
            result = bool(alert_usage)
            logger.info(f"成功检查在攻击之后{'使用过' if result else '未使用过'}告警系统。")
        
        return {
            "status": "success",
            "message": "成功检查在攻击之后是否使用过告警系统。",
            "data": result
        }
    except Exception as e:
        logger.error(f"obs_was_alert_used_after_attack_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_was_alert_used_after_attack_impl 执行失败: {str(e)}"
        }


def obs_attack_under_alert_impl(env_manager, env_id: str, alert_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中当前是否处于告警状态下的攻击。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    alert_id (Optional[List[int]]): 可选的告警区域ID列表。如果提供，则返回指定区域的攻击状态；
                                  如果为None，则返回所有区域的攻击状态。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的攻击状态信息。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if alert_id is None:
            logger.info(f"开始检查所有区域当前是否处于告警状态下的攻击，env_id: {env_id}")
        else:
            logger.info(f"开始检查指定区域当前是否处于告警状态下的攻击，env_id: {env_id}, alert_id: {alert_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 获取当前是否处于告警状态下的攻击
        attack_status = obs.attack_under_alert
        
        # 处理可能的numpy数组类型
        if isinstance(attack_status, np.ndarray):
            if alert_id is None:
                result = attack_status.tolist() if hasattr(attack_status, 'tolist') else attack_status
                logger.info(f"成功检查所有区域当前是否处于告警状态下的攻击。")
            else:
                result = attack_status[alert_id].tolist() if hasattr(attack_status[alert_id], 'tolist') else attack_status[alert_id]
                logger.info(f"成功检查指定区域当前是否处于告警状态下的攻击。")
        else:
            # 如果是标量值
            result = bool(attack_status)
            logger.info(f"成功检查当前{'处于' if result else '不处于'}告警状态下的攻击。")
        
        return {
            "status": "success",
            "message": "成功检查当前是否处于告警状态下的攻击。",
            "data": result
        }
    except Exception as e:
        logger.error(f"obs_attack_under_alert_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_attack_under_alert_impl 执行失败: {str(e)}"
        }


def obs_time_since_last_alert_impl(env_manager, env_id: str, alert_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中自上次告警发出以来经过的时间步数。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    alert_id (Optional[List[int]]): 可选的告警区域ID列表。如果提供，则返回指定区域的时间信息；
                                  如果为None，则返回所有区域的时间信息。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的时间步数信息。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if alert_id is None:
            logger.info(f"开始获取所有区域自上次告警发出以来经过的时间步数，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定区域自上次告警发出以来经过的时间步数，env_id: {env_id}, alert_id: {alert_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 获取自上次告警发出以来经过的时间步数
        time_since_last_alert = obs.time_since_last_alert
        
        # 处理可能的numpy数组类型
        if isinstance(time_since_last_alert, np.ndarray):
            if alert_id is None:
                result = time_since_last_alert.tolist() if hasattr(time_since_last_alert, 'tolist') else time_since_last_alert
                logger.info(f"成功获取所有区域自上次告警发出以来经过的时间步数。")
            else:
                result = time_since_last_alert[alert_id].tolist() if hasattr(time_since_last_alert[alert_id], 'tolist') else time_since_last_alert[alert_id]
                logger.info(f"成功获取指定区域自上次告警发出以来经过的时间步数。")
        else:
            # 如果是标量值
            result = int(time_since_last_alert)
            if result == -1:
                logger.info("成功获取自上次告警发出以来经过的时间步数：从未发出过告警。")
            else:
                logger.info(f"成功获取自上次告警发出以来经过的时间步数：{result}步。")
        
        return {
            "status": "success",
            "message": "成功获取自上次告警发出以来经过的时间步数。",
            "data": result
        }
    except Exception as e:
        logger.error(f"obs_time_since_last_alert_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_time_since_last_alert_impl 执行失败: {str(e)}"
        }


def obs_alert_duration_impl(env_manager, env_id: str, alert_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中告警的持续时间（以时间步为单位）。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    alert_id (Optional[List[int]]): 可选的告警区域ID列表。如果提供，则返回指定区域的告警持续时间；
                                  如果为None，则返回所有区域的告警持续时间。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的告警持续时间信息。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if alert_id is None:
            logger.info(f"开始获取所有区域的告警持续时间，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定区域的告警持续时间，env_id: {env_id}, alert_id: {alert_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 获取告警的持续时间
        alert_duration = obs.alert_duration
        
        # 处理可能的numpy数组类型
        if isinstance(alert_duration, np.ndarray):
            if alert_id is None:
                result = alert_duration.tolist() if hasattr(alert_duration, 'tolist') else alert_duration
                logger.info(f"成功获取所有区域的告警持续时间。")
            else:
                result = alert_duration[alert_id].tolist() if hasattr(alert_duration[alert_id], 'tolist') else alert_duration[alert_id]
                logger.info(f"成功获取指定区域的告警持续时间。")
        else:
            # 如果是标量值
            result = int(alert_duration)
            logger.info(f"成功获取告警的持续时间：{result}步。")
        
        return {
            "status": "success",
            "message": "成功获取告警的持续时间。",
            "data": result
        }
    except Exception as e:
        logger.error(f"obs_alert_duration_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_alert_duration_impl 执行失败: {str(e)}"
        }


def obs_time_since_last_attack_impl(env_manager, env_id: str, alert_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取grid2op环境中自上次攻击以来经过的时间步数。

    参数:
    env_manager: 环境管理器实例，用于管理和获取环境的观测。
    env_id (str): 环境实例的ID。
    alert_id (Optional[List[int]]): 可选的告警区域ID列表。如果提供，则返回指定区域的时间信息；
                                  如果为None，则返回所有区域的时间信息。

    返回:
    Dict[str, Any]: 包含状态、消息和数据的字典。状态可以是 "success" 或 "failure"，
                  消息描述了操作的结果，数据包含所请求的时间步数信息。

    异常:
    ValueError: 如果环境ID无效或无法获取观测。
    """
    try:
        if alert_id is None:
            logger.info(f"开始获取所有区域自上次攻击以来经过的时间步数，env_id: {env_id}")
        else:
            logger.info(f"开始获取指定区域自上次攻击以来经过的时间步数，env_id: {env_id}, alert_id: {alert_id}")
        
        # 获取最新的观测
        obs = env_manager.get_latest_obs(env_id)
        if obs is None:
            raise ValueError(f"无法获取 env_id 为 {env_id} 的环境实例的观测。")
        
        # 获取自上次攻击以来经过的时间步数
        time_since_last_attack = obs.time_since_last_attack
        
        # 处理可能的numpy数组类型
        if isinstance(time_since_last_attack, np.ndarray):
            if alert_id is None:
                result = time_since_last_attack.tolist() if hasattr(time_since_last_attack, 'tolist') else time_since_last_attack
                logger.info(f"成功获取所有区域自上次攻击以来经过的时间步数。")
            else:
                result = time_since_last_attack[alert_id].tolist() if hasattr(time_since_last_attack[alert_id], 'tolist') else time_since_last_attack[alert_id]
                logger.info(f"成功获取指定区域自上次攻击以来经过的时间步数。")
        else:
            # 如果是标量值
            result = int(time_since_last_attack)
            if result == -1:
                logger.info("成功获取自上次攻击以来经过的时间步数：从未发生过攻击。")
            else:
                logger.info(f"成功获取自上次攻击以来经过的时间步数：{result}步。")
        
        return {
            "status": "success",
            "message": "成功获取自上次攻击以来经过的时间步数。",
            "data": result
        }
    except Exception as e:
        logger.error(f"obs_time_since_last_attack_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"obs_time_since_last_attack_impl 执行失败: {str(e)}"
        }

