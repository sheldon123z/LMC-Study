
import grid2op
from grid2op.PlotGrid import PlotMatplot
import matplotlib.pyplot as plt  # pip install matplotlib
from typing import List, Dict, Any
from registry import env_registry
from datetime import datetime
import numpy as np
import os

# 定义实现函数
def set_bus_impl(element_indices: List[int], bus_element_index: int, bus_number: int) -> Dict[str, Any]:
    """
    模拟 set_bus 函数的实现，用于设置 grid2op 环境中的总线设置。
    """
    # 假设在这里与 grid2op 环境进行交互并返回结果
    # ...在这里写交互代码
    
    return {
        "status": "failure",
        "message": f"Bus settings updated for element {bus_element_index} to bus {bus_number}"
    }

def set_bus(arguments: Dict[str, Any]) -> Dict[str, Any]:
    element_indices = arguments["element_indices"]
    bus_element_index = arguments["bus_element_index"]
    bus_number = arguments["bus_number"]
    
    result = set_bus_impl(element_indices, bus_element_index, bus_number)
    return result


def line_change_status_impl(env_id,line_indices: List[int]) -> Dict[str, Any]:
    """
    修改电力线的状态。如果电力线已连接，则尝试断开；如果断开，则尝试连接。
    
    这里是你编写实际逻辑的地方，调用 grid2op 环境或者其他库来改变电力线状态。
    """
    try:
        # 通过env_id来寻找正确的env    
        env = env_registry.get(env_id)
        if not env:
            raise ValueError(f"Environment with ID {env_id} not found.")
        # line_id_to_change = line_indices
        # print(f"line_indices: {line_indices} \n")
        # action_space = env.action_space
        # change_status = action_space()
        # change_status.line_change_status=line_id_to_change
        
        env.action_space.line_change_status=line_indices
        # 模拟返回值，请在此根据实际调用情况返回相应数据
        return {
            "status": "success",
            "message": f"Powerlines {line_indices} status changed.",
        }
    
    except Exception as e:
        return {
            "status": "failure",
            "message": str(e)
        }

def line_change_status(arguments: Dict[str, Any]) -> Any:
    env_id = arguments.get("env_id")
    line_indices = arguments.get("line_indices")
    result = line_change_status_impl(env_id, line_indices)
    return result


def set_bus_impl(element_indices: List[int], bus_element_index: int, bus_number: int) -> Dict[str, Any]:
    """
    设置电力元件的总线。如果总线编号为 -1，则断开连接。

    这里是你编写实际逻辑的地方，调用 grid2op 环境或者其他库来设置元件的总线。
    """
    # 留出你的代码逻辑部分，例如调用 grid2op
    # 例如：env.action_space.set_bus(...)
    
    # 模拟返回值，请在此根据实际调用情况返回相应数据
    return {
        "status": "success",
        "message": f"Bus {bus_number} set for element {bus_element_index}.",
    }

def set_bus(arguments: Dict[str, Any]) -> Any:
    element_indices = arguments["element_indices"]
    bus_element_index = arguments["bus_element_index"]
    bus_number = arguments["bus_number"]
    result = set_bus_impl(element_indices, bus_element_index, bus_number)
    return result


def plot_layout_by_name_impl(env_name) -> Dict[str, Any]:
    """
    使用 PlotMatplot 的 plot_layout 方法来绘制电网布局。
    """
    try:
        env = grid2op.make(env_name)
        # 创建 PlotMatplot 实例
        plot_helper = PlotMatplot(env.observation_space)
        # 线的id
        line_ids = [int(i) for i in range(env.n_line)]
        # 调用 plot_layout 方法
        fig_layout = plot_helper.plot_layout()
        
        # 可以在这里对绘图对象（fig_layout）做进一步处理，或者保存它
        # 例如，保存为图片:
        fig_layout.savefig('grid_layout.png')
        
        return {
            "status": "success",
            "message": "Grid layout plotted successfully.",
            # "figure": fig_layout
        }
    except Exception as e:
        return {
            "status": "failure",
            "message": str(e)
        }


def plot_layout_by_name(arguments: Dict[str, Any]) -> Any:
    env_name = arguments.get("env_name")
    result = plot_layout_by_name_impl(env_name)
    return result



def plot_layout_by_env_id_impl(env_id) -> Dict[str, Any]:
    """
    使用 PlotMatplot 的 plot_layout 方法来绘制电网布局。
    """
    try:
        # 通过env_id来寻找正确的env    
        env = env_registry.get(env_id)
        
        # 创建 PlotMatplot 实例
        plot_helper = PlotMatplot(env.observation_space)
        # 线的id
        line_ids = [int(i) for i in range(env.n_line)]
        # 调用 plot_layout 方法
        fig_layout = plot_helper.plot_layout()
        
        # 可以在这里对绘图对象（fig_layout）做进一步处理，或者保存它
        # 例如，保存为图片:
        fig_layout.savefig('grid_layout.png')
        
        return {
            "status": "success",
            "message": "Grid layout plotted successfully."
        }
    except Exception as e:
        return {
            "status": "failure",
            "message": str(e)
        }


def plot_layout_by_env_id(arguments: Dict[str, Any]) -> Any:
    env_id = arguments.get("env_id")
    result = plot_layout_by_env_id_impl(env_id)
    return result


def redispatch(arguments: Dict[str, Any]) -> Any:
    env_id = arguments.get("env_id")
    gen_id = arguments.get("gen_id")
    amount = arguments.get("amount")

    # 确保 amount 是一个列表
    if not isinstance(amount, list):
        amount = [amount]
    
    if len(gen_id) > 1 and len(amount) == 1:
        amount = amount * len(gen_id)
        
    # 调用实际的 redispatch_impl 函数
    result = redispatch_impl(env_id, gen_id, amount)
    return result

def redispatch_impl(env_id, gen_id: List[int], amount: List[int]) -> Dict[str, Any]:
    try:
        env = env_registry.get(env_id)
        if env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例.")

        # 检查是否允许进行重分配操作
        if not env.redispatching_unit_commitment_availble:
            raise ValueError("当前环境不允许进行发电机功率重分配操作。")
        # 遍历每个发电机，检测是否可进行重分配
        for g_id in gen_id:
            if not env.gen_redispatchable[g_id]:
                raise ValueError(f"发电机 {g_id} 不允许进行功率重分配。")

        # 进行功率重分配操作
        param = [(g_id, a) for g_id, a in zip(gen_id, amount)]
        action = env.action_space({"redispatch": param})  # 执行功率重分配

        if action.is_ambiguous()[0]:
            info = action.ambiguous_info()[1]
            raise ValueError(f"动作是模糊的，无法执行。{info}")
        else:
            env.step(action)  # 执行动作
            return {
                "status": "success",
                "message": "成功进行电机功率重分配。"
            }
    except Exception as e:
        return {
            "status": "failure",
            "message": str(e)
        }
def curtail(arguments: Dict[str, Any]) -> Any:
    # 获取传入的参数
    env_id = arguments.get("env_id", "env")  # 如果没有提供 env_id，使用默认 "env"
    gen_id = arguments.get("gen_id")
    amount_ratio = arguments.get("amount_ratio")
    
    # 确保 gen_id 和 amount_ratio 都被提供
    if gen_id is None or amount_ratio is None:
        return {
            "status": "failure",
            "message": "缺少必需的参数: gen_id 或 amount_ratio."
        }

    # 确保 amount_ratio 是一个列表
    if not isinstance(amount_ratio, list):
        amount_ratio = [amount_ratio]

    # 如果 gen_id 有多个，而 amount_ratio 只有一个，将其扩展为与 gen_id 数量一致
    if len(gen_id) > 1 and len(amount_ratio) == 1:
        amount_ratio = amount_ratio * len(gen_id)
    
    # 检查 gen_id 和 amount_ratio 的长度是否匹配
    if len(gen_id) != len(amount_ratio):
        return {
            "status": "failure",
            "message": "gen_id 和 amount_ratio 的长度不匹配."
        }
    
    # 调用实际的 curtail 执行函数
    try:
        result = curtail_impl(env_id, gen_id, amount_ratio)
    except Exception as e:
        return {
            "status": "failure",
            "message": f"执行curtail操作时出错: {str(e)}"
        }
    
    return result       

def curtail_impl(env_id, gen_id: List[int], amount_ratio: List[float]) -> Dict[str, Any]:
    try:
        # 从 env_registry 中获取对应的环境
        env = env_registry.get(env_id)
        if env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例.")
        
        # 将 gen_id 和 amount_ratio 配对，并将削减操作传递给 action_space
        param = [(g_id, ratio) for g_id, ratio in zip(gen_id, amount_ratio)]
        action = env.action_space({"curtail": param})  # 执行削减操作
        if action.is_ambiguous()[0]:
            info = action.ambiguous_info()[1]
            raise ValueError(f"动作是模糊的，无法执行。{info}")
        else:
            env.step(action)  # 执行动作
            return {
                "status": "success",
                "message": "成功进行发电削减操作."
            }
    except Exception as e:
        return {
            "status": "failure",
            "message": f"curtail_impl 执行失败: {str(e)}"
        }



def plot_obs_by_env_id_impl(env_id) -> Dict[str, Any]:
    """
    使用 PlotMatplot 的 plot_obs 方法来绘制电网的观测状态。
    """
    try:
        # 通过env_id来寻找正确的env    
        env = env_registry.get(env_id)
        
        if env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例。")

        # 获取当前环境的观测值，不需要调用 reset
        obs = env.get_obs()

        # 创建 PlotMatplot 实例
        plot_helper = PlotMatplot(env.observation_space)
        
        # 调用 plot_obs 方法，显示线的功率信息和负载的电压信息
        fig_obs = plot_helper.plot_obs(obs, line_info="p", load_info="v")
        
        # 保存图片
        folder_name = "images"
        # 如果文件夹不存在，则创建文件夹
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"plot_{timestamp}.png"
        file_path = os.path.join(folder_name, filename)
        fig_obs.savefig(file_path)
        
        return {
            "status": "success",
            "message": "成功绘制电网观测状态."
        }
    except Exception as e:
        return {
            "status": "failure",
            "message": str(e)
        }


def plot_obs_by_env_id(arguments: Dict[str, Any]) -> Any:
    env_id = arguments.get("env_id")
    result = plot_obs_by_env_id_impl(env_id)
    return result