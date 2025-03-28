# tools/grid2op_tools_mcp.py
"""
按照MCP协议定义Grid2op工具函数的Schema和实现

本模块将Grid2op工具函数按照Model Context Protocol (MCP)协议重新定义，
使其可以与支持MCP协议的大模型API (如OpenAI、Anthropic Claude、MoonshotAI等) 集成使用。

使用方法示例:
```python
# 导入MCP工具定义和映射
from grid2op_tools_mcp import GRID2OP_TOOL_SCHEMAS, GRID2OP_TOOLS_MAPPING

# 创建LLM客户端
client = OpenAI()

# 准备LLM请求
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "你是一个电网操作专家，可以帮助用户执行各种电网操作。"},
        {"role": "user", "content": "请获取test1环境中所有发电机的发电功率，然后增加0号发电机的功率2MW。"}
    ],
    tools=GRID2OP_TOOL_SCHEMAS  # 注册工具函数
)

# 处理LLM返回的工具调用
for tool_call in response.choices[0].message.tool_calls:
    tool_name = tool_call.function.name
    tool_args = json.loads(tool_call.function.arguments)
    
    if tool_name in GRID2OP_TOOLS_MAPPING:
        tool_func = GRID2OP_TOOLS_MAPPING[tool_name]
        result = tool_func(**tool_args)
        print(f"工具 {tool_name} 执行结果: {result}")
```
"""
from typing import List, Dict, Any, Optional, Union
import json
import gc

# 导入全局上下文和操作/观测提供者
from global_context import env_manager
from actions.wrapper import action_factory
from observations.provider import observation_provider

# 存储已创建的动作
action_store = {}

#################################################
# 工具函数实现
#################################################

# 动作创建函数

def create_gen_set_bus(env_id: str, gen_id: List[int], bus_status: List[int]) -> Dict[str, Any]:
    """
    创建发电机母线设置动作（不执行）。
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

def create_load_set_bus(env_id: str, load_id: List[int], bus_status: List[int]) -> Dict[str, Any]:
    """
    创建负荷母线设置动作（不执行）。
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

def create_line_or_set_bus(env_id: str, line_id: List[int], bus_status: List[int]) -> Dict[str, Any]:
    """
    创建线路起始端母线设置动作（不执行）。
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

def create_line_ex_set_bus(env_id: str, line_id: List[int], bus_status: List[int]) -> Dict[str, Any]:
    """
    创建线路终止端母线设置动作（不执行）。
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

def create_storage_set_bus(env_id: str, storage_id: List[int], bus_status: List[int]) -> Dict[str, Any]:
    """
    创建储能设备母线设置动作（不执行）。
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

def create_line_set_status(env_id: str, line_id: List[int], line_status: List[int]) -> Dict[str, Any]:
    """
    创建线路状态设置动作（不执行）。
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

def create_redispatch(env_id: str, gen_id: List[int], amount: List[float]) -> Dict[str, Any]:
    """
    创建发电机重调度动作（不执行）。
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

def create_cancel_redispatch(env_id: str, gen_id: List[int]) -> Dict[str, Any]:
    """
    创建取消发电机重调度的动作（不执行）。
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

def create_curtail(env_id: str, gen_id: List[int], amount: List[float]) -> Dict[str, Any]:
    """
    创建可再生能源发电机限电动作（不执行）。
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

def create_storage_p(env_id: str, storage_id: List[int], amount: List[float]) -> Dict[str, Any]:
    """
    创建储能单元充放电动作（不执行）。
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

# 动作执行函数

def execute_action(action_id: str) -> Dict[str, Any]:
    """
    执行之前创建的动作。
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

def combine_actions(action_ids: List[str]) -> Dict[str, Any]:
    """
    组合多个已创建的动作并返回新的组合动作ID（不执行）。
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

def execute_combined_action(env_id: str, actions_config: Dict[str, List]) -> Dict[str, Any]:
    """
    创建组合动作并立即执行。
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

# 观测获取函数

def get_observation(env_id: str, component: str, element_id: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    获取指定组件的观测数据。
    """
    return observation_provider.get_observation(env_id, component, element_id)

def get_topology_snapshot(env_id: str) -> Dict[str, Any]:
    """
    获取电网拓扑结构快照。
    """
    return observation_provider.get_topology_snapshot(env_id)

def get_power_flow_snapshot(env_id: str) -> Dict[str, Any]:
    """
    获取电力潮流快照。
    """
    return observation_provider.get_power_flow_snapshot(env_id)

def get_dispatch_snapshot(env_id: str) -> Dict[str, Any]:
    """
    获取发电机调度快照。
    """
    return observation_provider.get_dispatch_snapshot(env_id)

def get_time_info(env_id: str) -> Dict[str, Any]:
    """
    获取时间相关信息。
    """
    return observation_provider.get_time_info(env_id)

def get_env_parameters(env_id: str) -> Dict[str, Any]:
    """
    获取环境参数。
    """
    return observation_provider.get_env_parameters(env_id)

# 动作清理函数

def clear_actions(env_id: Optional[str] = None) -> Dict[str, Any]:
    """
    清除指定环境或所有环境的已创建动作。
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

#################################################
# 工具函数映射
#################################################

# 将工具名称映射到实际的函数实现
GRID2OP_TOOLS_MAPPING = {
    # 动作创建工具
    "create_gen_set_bus": create_gen_set_bus,
    "create_load_set_bus": create_load_set_bus,
    "create_line_or_set_bus": create_line_or_set_bus,
    "create_line_ex_set_bus": create_line_ex_set_bus,
    "create_storage_set_bus": create_storage_set_bus,
    "create_line_set_status": create_line_set_status,
    "create_redispatch": create_redispatch,
    "create_cancel_redispatch": create_cancel_redispatch,
    "create_curtail": create_curtail,
    "create_storage_p": create_storage_p,
    
    # 动作执行工具
    "execute_action": execute_action,
    "combine_actions": combine_actions,
    "execute_combined_action": execute_combined_action,
    
    # 观测获取工具
    "get_observation": get_observation,
    "get_topology_snapshot": get_topology_snapshot,
    "get_power_flow_snapshot": get_power_flow_snapshot,
    "get_dispatch_snapshot": get_dispatch_snapshot,
    "get_time_info": get_time_info,
    "get_env_parameters": get_env_parameters,
    
    # 动作清理工具
    "clear_actions": clear_actions
}

#################################################
# MCP工具函数Schema定义
#################################################

# 动作创建工具Schema
GRID2OP_TOOL_SCHEMAS = [
    # 动作创建工具
    {
        "type": "function",
        "function": {
            "name": "create_gen_set_bus",
            "description": "创建发电机母线设置动作（不执行）",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    },
                    "gen_id": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "发电机ID列表"
                    },
                    "bus_status": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "母线状态列表，每个整数代表对应操作: 0-不操作, -1-断开, 1-母线1, 2-母线2"
                    }
                },
                "required": ["env_id", "gen_id", "bus_status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_load_set_bus",
            "description": "创建负荷母线设置动作（不执行）",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    },
                    "load_id": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "负荷ID列表"
                    },
                    "bus_status": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "母线状态列表，每个整数代表对应操作: 0-不操作, -1-断开, 1-母线1, 2-母线2"
                    }
                },
                "required": ["env_id", "load_id", "bus_status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_line_or_set_bus",
            "description": "创建线路起始端母线设置动作（不执行）",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    },
                    "line_id": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "线路ID列表"
                    },
                    "bus_status": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "母线状态列表，每个整数代表对应操作: 0-不操作, -1-断开, 1-母线1, 2-母线2"
                    }
                },
                "required": ["env_id", "line_id", "bus_status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_line_ex_set_bus",
            "description": "创建线路终止端母线设置动作（不执行）",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    },
                    "line_id": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "线路ID列表"
                    },
                    "bus_status": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "母线状态列表，每个整数代表对应操作: 0-不操作, -1-断开, 1-母线1, 2-母线2"
                    }
                },
                "required": ["env_id", "line_id", "bus_status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_storage_set_bus",
            "description": "创建储能设备母线设置动作（不执行）",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    },
                    "storage_id": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "储能设备ID列表"
                    },
                    "bus_status": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "母线状态列表，每个整数代表对应操作: 0-不操作, -1-断开, 1-母线1, 2-母线2"
                    }
                },
                "required": ["env_id", "storage_id", "bus_status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_line_set_status",
            "description": "创建线路状态设置动作（不执行）",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    },
                    "line_id": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "线路ID列表"
                    },
                    "line_status": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "线路状态列表: 0-不改变, 1-连接, -1-断开"
                    }
                },
                "required": ["env_id", "line_id", "line_status"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_redispatch",
            "description": "创建发电机重调度动作（不执行）",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    },
                    "gen_id": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "发电机ID列表"
                    },
                    "amount": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "重调度量列表(MW)，正值表示增加发电量，负值表示减少发电量"
                    }
                },
                "required": ["env_id", "gen_id", "amount"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_cancel_redispatch",
            "description": "创建取消发电机重调度的动作（不执行）",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    },
                    "gen_id": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "要取消重调度的发电机ID列表"
                    }
                },
                "required": ["env_id", "gen_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_curtail",
            "description": "创建可再生能源发电机限电动作（不执行）",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    },
                    "gen_id": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "发电机ID列表"
                    },
                    "amount": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "限电比例列表，范围在[0.0, 1.0]之间，1表示不限电，0表示完全限电"
                    }
                },
                "required": ["env_id", "gen_id", "amount"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_storage_p",
            "description": "创建储能单元充放电动作（不执行）",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    },
                    "storage_id": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "储能单元ID列表"
                    },
                    "amount": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "充放电功率列表(MW)，正值表示充电，负值表示放电"
                    }
                },
                "required": ["env_id", "storage_id", "amount"]
            }
        }
    },
    
    # 动作执行工具
    {
        "type": "function",
        "function": {
            "name": "execute_action",
            "description": "执行之前创建的动作",
            "parameters": {
                "type": "object",
                "properties": {
                    "action_id": {
                        "type": "string",
                        "description": "动作ID，由创建动作的工具返回"
                    }
                },
                "required": ["action_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "combine_actions",
            "description": "组合多个已创建的动作并返回新的组合动作ID（不执行）",
            "parameters": {
                "type": "object",
                "properties": {
                    "action_ids": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "要组合的动作ID列表"
                    }
                },
                "required": ["action_ids"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "execute_combined_action",
            "description": "创建组合动作并立即执行",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    },
                    "actions_config": {
                        "type": "object",
                        "description": "动作配置字典，键为动作类型，值为参数列表，例如: {\"gen_set_bus\": [[0, 1], [1, 2]], \"line_set_status\": [[0, 1], [1, -1]]}"
                    }
                },
                "required": ["env_id", "actions_config"]
            }
        }
    },
    
    # 观测获取工具
    {
        "type": "function",
        "function": {
            "name": "get_observation",
            "description": "获取指定组件的观测数据",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    },
                    "component": {
                        "type": "string",
                        "description": "要获取的组件类型，如 'gen_p', 'load_q', 'line_status' 等"
                    },
                    "element_id": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "可选的元素ID列表"
                    }
                },
                "required": ["env_id", "component"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_topology_snapshot",
            "description": "获取电网拓扑结构快照",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    }
                },
                "required": ["env_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_power_flow_snapshot",
            "description": "获取电力潮流快照",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    }
                },
                "required": ["env_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_dispatch_snapshot",
            "description": "获取发电机调度快照",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    }
                },
                "required": ["env_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time_info",
            "description": "获取时间相关信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    }
                },
                "required": ["env_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_env_parameters",
            "description": "获取环境参数",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "环境ID"
                    }
                },
                "required": ["env_id"]
            }
        }
    },
    
    # 动作清理工具
    {
        "type": "function",
        "function": {
            "name": "clear_actions",
            "description": "清除指定环境或所有环境的已创建动作",
            "parameters": {
                "type": "object",
                "properties": {
                    "env_id": {
                        "type": "string",
                        "description": "可选的环境ID，如果提供则只清除该环境的动作"
                    }
                }
            }
        }
    }]