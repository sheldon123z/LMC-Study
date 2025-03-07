# tools/grid2op_tools.py
from typing import List, Dict, Any, Optional, Union
from langchain_core.tools import tool
import json
import gc

# 导入全局上下文和操作/观测提供者
from global_context import env_manager
from actions.wrapper import action_factory
from observations.provider import observation_provider

# 存储已创建的动作
action_store = {}

#################################################
# 动作创建工具 - 不执行，仅创建并返回动作ID
#################################################

@tool
def create_gen_set_bus(env_id: str, gen_id: List[int], bus_status: List[int]) -> Dict[str, Any]:
    """
    创建发电机母线设置动作（不执行）。
    
    参数:
    env_id (str): 环境ID
    gen_id (List[int]): 发电机ID列表
    bus_status (List[int]): 母线状态列表，每个整数代表对应操作:
        - 0: 该动作不对这个发电机产生作用
        - -1: 断开该发电机
        - 1: 将该发电机设置到母线1
        - 2: 将该发电机设置到母线2
    
    返回:
    Dict[str, Any]: 包含操作结果的字典，成功时包含action_id
    """
    try:
        action = action_factory.for_env(env_id).gen_set_bus(gen_id, bus_status)
        action_id = f"{env_id}_gen_set_bus_{id(action)}"
        action_store[action_id] = action
        
        return {
            "status": "success",
            "message": "已成功创建发电机母线设置动作，但尚未执行",
            "action_id": action_id,
            "env_id": env_id
        }
    except Exception as e:
        return {
            "status": "failure",
            "message": f"创建发电机母线设置动作失败: {str(e)}"
        }

@tool
def create_load_set_bus(env_id: str, load_id: List[int], bus_status: List[int]) -> Dict[str, Any]:
    """
    创建负荷母线设置动作（不执行）。
    
    参数:
    env_id (str): 环境ID
    load_id (List[int]): 负荷ID列表
    bus_status (List[int]): 母线状态列表
    
    返回:
    Dict[str, Any]: 包含操作结果的字典，成功时包含action_id
    """
    try:
        action = action_factory.for_env(env_id).load_set_bus(load_id, bus_status)
        action_id = f"{env_id}_load_set_bus_{id(action)}"
        action_store[action_id] = action
        
        return {
            "status": "success",
            "message": "已成功创建负荷母线设置动作，但尚未执行",
            "action_id": action_id,
            "env_id": env_id
        }
    except Exception as e:
        return {
            "status": "failure",
            "message": f"创建负荷母线设置动作失败: {str(e)}"
        }

@tool
def create_line_or_set_bus(env_id: str, line_id: List[int], bus_status: List[int]) -> Dict[str, Any]:
    """
    创建线路起始端母线设置动作（不执行）。
    
    参数:
    env_id (str): 环境ID
    line_id (List[int]): 线路ID列表
    bus_status (List[int]): 母线状态列表，每个整数代表对应操作:
        - 0: 该动作不对这个线路端点产生作用
        - -1: 断开该线路端点
        - 1: 将该线路端点设置到母线1
        - 2: 将该线路端点设置到母线2
    
    返回:
    Dict[str, Any]: 包含操作结果的字典，成功时包含action_id
    """
    try:
        action = action_factory.for_env(env_id).line_or_set_bus(line_id, bus_status)
        action_id = f"{env_id}_line_or_set_bus_{id(action)}"
        action_store[action_id] = action
        
        return {
            "status": "success",
            "message": "已成功创建线路起始端母线设置动作，但尚未执行",
            "action_id": action_id,
            "env_id": env_id
        }
    except Exception as e:
        return {
            "status": "failure",
            "message": f"创建线路起始端母线设置动作失败: {str(e)}"
        }

@tool
def create_line_ex_set_bus(env_id: str, line_id: List[int], bus_status: List[int]) -> Dict[str, Any]:
    """
    创建线路终止端母线设置动作（不执行）。
    
    参数:
    env_id (str): 环境ID
    line_id (List[int]): 线路ID列表
    bus_status (List[int]): 母线状态列表，每个整数代表对应操作:
        - 0: 该动作不对这个线路端点产生作用
        - -1: 断开该线路端点
        - 1: 将该线路端点设置到母线1
        - 2: 将该线路端点设置到母线2
    
    返回:
    Dict[str, Any]: 包含操作结果的字典，成功时包含action_id
    """
    try:
        action = action_factory.for_env(env_id).line_ex_set_bus(line_id, bus_status)
        action_id = f"{env_id}_line_ex_set_bus_{id(action)}"
        action_store[action_id] = action
        
        return {
            "status": "success",
            "message": "已成功创建线路终止端母线设置动作，但尚未执行",
            "action_id": action_id,
            "env_id": env_id
        }
    except Exception as e:
        return {
            "status": "failure",
            "message": f"创建线路终止端母线设置动作失败: {str(e)}"
        }

@tool
def create_storage_set_bus(env_id: str, storage_id: List[int], bus_status: List[int]) -> Dict[str, Any]:
    """
    创建储能设备母线设置动作（不执行）。
    
    参数:
    env_id (str): 环境ID
    storage_id (List[int]): 储能设备ID列表
    bus_status (List[int]): 母线状态列表，每个整数代表对应操作:
        - 0: 该动作不对这个储能设备产生作用
        - -1: 断开该储能设备
        - 1: 将该储能设备设置到母线1
        - 2: 将该储能设备设置到母线2
    
    返回:
    Dict[str, Any]: 包含操作结果的字典，成功时包含action_id
    """
    try:
        action = action_factory.for_env(env_id).storage_set_bus(storage_id, bus_status)
        action_id = f"{env_id}_storage_set_bus_{id(action)}"
        action_store[action_id] = action
        
        return {
            "status": "success",
            "message": "已成功创建储能设备母线设置动作，但尚未执行",
            "action_id": action_id,
            "env_id": env_id
        }
    except Exception as e:
        return {
            "status": "failure",
            "message": f"创建储能设备母线设置动作失败: {str(e)}"
        }

@tool
def create_line_set_status(env_id: str, line_id: List[int], line_status: List[int]) -> Dict[str, Any]:
    """
    创建线路状态设置动作（不执行）。
    
    参数:
    env_id (str): 环境ID
    line_id (List[int]): 线路ID列表
    line_status (List[int]): 线路状态列表:
        - 0: 不改变该线路状态
        - 1: 连接该线路
        - -1: 断开该线路
    
    返回:
    Dict[str, Any]: 包含操作结果的字典，成功时包含action_id
    """
    try:
        action = action_factory.for_env(env_id).line_set_status(line_id, line_status)
        action_id = f"{env_id}_line_set_status_{id(action)}"
        action_store[action_id] = action
        
        return {
            "status": "success",
            "message": "已成功创建线路状态设置动作，但尚未执行",
            "action_id": action_id,
            "env_id": env_id
        }
    except Exception as e:
        return {
            "status": "failure",
            "message": f"创建线路状态设置动作失败: {str(e)}"
        }

@tool
def create_redispatch(env_id: str, gen_id: List[int], amount: List[float]) -> Dict[str, Any]:
    """
    创建发电机重调度动作（不执行）。
    
    参数:
    env_id (str): 环境ID
    gen_id (List[int]): 发电机ID列表
    amount (List[float]): 重调度量列表(MW)，正值表示增加发电量，负值表示减少发电量
    
    返回:
    Dict[str, Any]: 包含操作结果的字典，成功时包含action_id
    """
    try:
        action = action_factory.for_env(env_id).redispatch(gen_id, amount)
        action_id = f"{env_id}_redispatch_{id(action)}"
        action_store[action_id] = action
        
        return {
            "status": "success",
            "message": "已成功创建发电机重调度动作，但尚未执行",
            "action_id": action_id,
            "env_id": env_id
        }
    except Exception as e:
        return {
            "status": "failure",
            "message": f"创建发电机重调度动作失败: {str(e)}"
        }

@tool
def create_cancel_redispatch(env_id: str, gen_id: List[int]) -> Dict[str, Any]:
    """
    创建取消发电机重调度的动作（不执行）。
    
    参数:
    env_id (str): 环境ID
    gen_id (List[int]): 要取消重调度的发电机ID列表
    
    返回:
    Dict[str, Any]: 包含操作结果的字典，成功时包含action_id
    """
    try:
        action = action_factory.for_env(env_id).cancel_redispatch(gen_id)
        action_id = f"{env_id}_cancel_redispatch_{id(action)}"
        action_store[action_id] = action
        
        return {
            "status": "success",
            "message": "已成功创建取消发电机重调度动作，但尚未执行",
            "action_id": action_id,
            "env_id": env_id
        }
    except Exception as e:
        return {
            "status": "failure",
            "message": f"创建取消发电机重调度动作失败: {str(e)}"
        }

@tool
def create_curtail(env_id: str, gen_id: List[int], amount: List[float]) -> Dict[str, Any]:
    """
    创建可再生能源发电机限电动作（不执行）。
    
    参数:
    env_id (str): 环境ID
    gen_id (List[int]): 发电机ID列表
    amount (List[float]): 限电比例列表，范围在[0.0, 1.0]之间，1表示不限电，0表示完全限电
    
    返回:
    Dict[str, Any]: 包含操作结果的字典，成功时包含action_id
    """
    try:
        action = action_factory.for_env(env_id).curtail(gen_id, amount)
        action_id = f"{env_id}_curtail_{id(action)}"
        action_store[action_id] = action
        
        return {
            "status": "success",
            "message": "已成功创建发电机限电动作，但尚未执行",
            "action_id": action_id,
            "env_id": env_id
        }
    except Exception as e:
        return {
            "status": "failure",
            "message": f"创建发电机限电动作失败: {str(e)}"
        }

@tool
def create_storage_p(env_id: str, storage_id: List[int], amount: List[float]) -> Dict[str, Any]:
    """
    创建储能单元充放电动作（不执行）。
    
    参数:
    env_id (str): 环境ID
    storage_id (List[int]): 储能单元ID列表
    amount (List[float]): 充放电功率列表(MW)，正值表示充电，负值表示放电
    
    返回:
    Dict[str, Any]: 包含操作结果的字典，成功时包含action_id
    """
    try:
        action = action_factory.for_env(env_id).storage_p(storage_id, amount)
        action_id = f"{env_id}_storage_p_{id(action)}"
        action_store[action_id] = action
        
        return {
            "status": "success",
            "message": "已成功创建储能单元充放电动作，但尚未执行",
            "action_id": action_id,
            "env_id": env_id
        }
    except Exception as e:
        return {
            "status": "failure",
            "message": f"创建储能单元充放电动作失败: {str(e)}"
        }

#################################################
# 动作执行工具
#################################################

@tool
def execute_action(action_id: str) -> Dict[str, Any]:
    """
    执行之前创建的动作。
    
    参数:
    action_id (str): 动作ID，由创建动作的工具返回
    
    返回:
    Dict[str, Any]: 包含执行结果的字典
    """
    try:
        # 从动作存储中获取动作
        action = action_store.get(action_id)
        if action is None:
            return {
                "status": "failure",
                "message": f"找不到ID为 {action_id} 的动作"
            }
        
        # 执行动作
        result = action.execute()
        
        # 移除动作
        del action_store[action_id]
        
        return result
    except Exception as e:
        return {
            "status": "failure",
            "message": f"执行动作失败: {str(e)}"
        }

@tool
def combine_actions(action_ids: List[str]) -> Dict[str, Any]:
    """
    组合多个已创建的动作并返回新的组合动作ID（不执行）。
    
    参数:
    action_ids (List[str]): 要组合的动作ID列表
    
    返回:
    Dict[str, Any]: 包含新组合动作ID的字典
    """
    try:
        if len(action_ids) < 2:
            return {
                "status": "failure",
                "message": "需要至少两个动作ID进行组合"
            }
        
        # 获取第一个动作
        base_action = action_store.get(action_ids[0])
        if base_action is None:
            return {
                "status": "failure",
                "message": f"找不到ID为 {action_ids[0]} 的动作"
            }
        
        env_id = base_action.env_id
        
        # 组合其他动作
        for action_id in action_ids[1:]:
            other_action = action_store.get(action_id)
            if other_action is None:
                return {
                    "status": "failure",
                    "message": f"找不到ID为 {action_id} 的动作"
                }
            
            if other_action.env_id != env_id:
                return {
                    "status": "failure",
                    "message": f"无法组合不同环境的动作: {env_id} 和 {other_action.env_id}"
                }
            
            base_action = base_action.combine(other_action)
        
        # 存储组合动作
        action_id = f"{env_id}_combined_{id(base_action)}"
        action_store[action_id] = base_action
        
        return {
            "status": "success",
            "message": "成功组合动作",
            "action_id": action_id,
            "env_id": env_id
        }
    except Exception as e:
        return {
            "status": "failure",
            "message": f"组合动作失败: {str(e)}"
        }

@tool
def execute_combined_action(env_id: str, actions_config: Dict[str, List]) -> Dict[str, Any]:
    """
    创建组合动作并立即执行。
    
    参数:
    env_id (str): 环境ID
    actions_config (Dict[str, List]): 动作配置字典，如:
        {
            "gen_set_bus": [[0, 1], [1, 2]],
            "line_set_status": [[0, 1], [1, -1]],
            "redispatch": [[0, 10.0], [1, -5.0]]
        }
    
    返回:
    Dict[str, Any]: 包含执行结果的字典
    """
    try:
        # 创建基础ActionWrapper
        action_wrapper = action_factory.for_env(env_id)
        
        # 根据配置添加各类动作
        for action_type, action_params in actions_config.items():
            if hasattr(action_wrapper, action_type):
                # 检查参数格式
                if not isinstance(action_params, list) or len(action_params) == 0:
                    return {
                        "status": "failure",
                        "message": f"动作 {action_type} 的参数格式不正确"
                    }
                
                # 如果参数是嵌套列表 [[id1, val1], [id2, val2], ...]
                if isinstance(action_params[0], list) and len(action_params[0]) == 2:
                    ids, values = zip(*action_params)
                    method = getattr(action_wrapper, action_type)
                    method(list(ids), list(values))
                else:
                    # 其他参数格式，直接传入
                    return {
                        "status": "failure",
                        "message": f"动作 {action_type} 的参数格式必须为 [[id1, val1], [id2, val2], ...]"
                    }
            else:
                return {
                    "status": "failure",
                    "message": f"不支持的动作类型: {action_type}"
                }
        
        # 执行组合动作
        return action_wrapper.execute()
    except Exception as e:
        return {
            "status": "failure",
            "message": f"组合动作执行失败: {str(e)}"
        }

#################################################
# 观测获取工具
#################################################

@tool
def get_observation(env_id: str, component: str, element_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取指定组件的观测数据。
    
    参数:
    env_id (str): 环境ID
    component (str): 要获取的组件类型，如 'gen_p', 'load_q', 'line_status' 等
    element_id (Optional[List[int]]): 可选的元素ID列表
    
    返回:
    Dict[str, Any]: 包含观测结果的字典
    """
    return observation_provider.get_observation(env_id, component, element_id)

@tool
def get_topology_snapshot(env_id: str) -> Dict[str, Any]:
    """
    获取电网拓扑结构快照。
    
    参数:
    env_id (str): 环境ID
    
    返回:
    Dict[str, Any]: 包含拓扑结构快照的字典
    """
    return observation_provider.get_topology_snapshot(env_id)

@tool
def get_power_flow_snapshot(env_id: str) -> Dict[str, Any]:
    """
    获取电力潮流快照。
    
    参数:
    env_id (str): 环境ID
    
    返回:
    Dict[str, Any]: 包含电力潮流快照的字典
    """
    return observation_provider.get_power_flow_snapshot(env_id)

@tool
def get_dispatch_snapshot(env_id: str) -> Dict[str, Any]:
    """
    获取发电机调度快照。
    
    参数:
    env_id (str): 环境ID
    
    返回:
    Dict[str, Any]: 包含发电机调度快照的字典
    """
    return observation_provider.get_dispatch_snapshot(env_id)

@tool
def get_time_info(env_id: str) -> Dict[str, Any]:
    """
    获取时间相关信息。
    
    参数:
    env_id (str): 环境ID
    
    返回:
    Dict[str, Any]: 包含时间信息的字典
    """
    return observation_provider.get_time_info(env_id)

@tool
def get_env_parameters(env_id: str) -> Dict[str, Any]:
    """
    获取环境参数。
    
    参数:
    env_id (str): 环境ID
    
    返回:
    Dict[str, Any]: 包含环境参数的字典
    """
    return observation_provider.get_env_parameters(env_id)

#################################################
# 动作清理工具
#################################################

@tool
def clear_actions(env_id: Optional[str] = None) -> Dict[str, Any]:
    """
    清除指定环境或所有环境的已创建动作。
    
    参数:
    env_id (Optional[str]): 可选的环境ID，如果提供则只清除该环境的动作
    
    返回:
    Dict[str, Any]: 包含清除结果的字典
    """
    try:
        global action_store
        
        before_count = len(action_store)
        
        if env_id:
            # 清除指定环境的动作
            action_store = {k: v for k, v in action_store.items() if not k.startswith(f"{env_id}_")}
            after_count = len(action_store)
            cleared_count = before_count - after_count
            
            return {
                "status": "success",
                "message": f"已清除环境 '{env_id}' 的 {cleared_count} 个动作"
            }
        else:
            # 清除所有动作
            action_store.clear()
            
            return {
                "status": "success",
                "message": f"已清除所有环境的 {before_count} 个动作"
            }
    except Exception as e:
        return {
            "status": "failure",
            "message": f"清除动作失败: {str(e)}"
        }
