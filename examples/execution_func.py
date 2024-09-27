import os
import grid2op
from grid2op.PlotGrid import PlotMatplot
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from registry import env_registry
from datetime import datetime
import numpy as np
from src.utils import get_logger

# 初始化日志记录器
logger = get_logger(__name__)

# 定义实现函数
def set_bus_impl(element_indices: List[int], bus_element_index: int, bus_number: int) -> Dict[str, Any]:
    """
    模拟 set_bus 函数的实现，用于设置 grid2op 环境中的总线设置。
    """
    try:
        # 假设在这里与 grid2op 环境进行交互并返回结果
        logger.info(f"开始设置总线。element_indices: {element_indices}, bus_element_index: {bus_element_index}, bus_number: {bus_number}")
        # ... 在这里写交互代码
        return {
            "status": "success",
            "message": f"Bus {bus_number} set for element {bus_element_index}."
        }
    except Exception as e:
        logger.error(f"设置总线时出错: {str(e)}")
        return {
            "status": "failure",
            "message": f"设置总线时出错: {str(e)}"
        }


def set_bus(arguments: Dict[str, Any]) -> Dict[str, Any]:
    try:
        element_indices = arguments["element_indices"]
        bus_element_index = arguments["bus_element_index"]
        bus_number = arguments["bus_number"]
        logger.info(f"接收到设置总线请求。参数: {arguments}")
        result = set_bus_impl(element_indices, bus_element_index, bus_number)
        return result
    except Exception as e:
        logger.error(f"处理set_bus请求时出错: {str(e)}")
        return {
            "status": "failure",
            "message": f"处理set_bus请求时出错: {str(e)}"
        }


def line_change_status_impl(env_id, line_indices: List[int]) -> Dict[str, Any]:
    """
    修改电力线的状态。如果电力线已连接，则尝试断开；如果断开，则尝试连接。
    """
    try:
        # 通过env_id来寻找正确的env    
        env = env_registry.get(env_id)
        if not env:
            raise ValueError(f"环境 ID 为 {env_id} 的环境未找到。")
        
        logger.info(f"开始修改电力线状态。env_id: {env_id}, line_indices: {line_indices}")
        
        # 模拟修改电力线状态
        env.action_space.line_change_status = line_indices
        
        logger.info(f"成功修改电力线状态: {line_indices}")
        return {
            "status": "success",
            "message": f"电力线 {line_indices} 状态已修改。",
        }
    except Exception as e:
        logger.error(f"修改电力线状态时出错: {str(e)}")
        return {
            "status": "failure",
            "message": str(e)
        }


def line_change_status(arguments: Dict[str, Any]) -> Any:
    try:
        env_id = arguments.get("env_id")
        line_indices = arguments.get("line_indices")
        logger.info(f"接收到修改电力线状态请求。参数: {arguments}")
        result = line_change_status_impl(env_id, line_indices)
        return result
    except Exception as e:
        logger.error(f"处理line_change_status请求时出错: {str(e)}")
        return {
            "status": "failure",
            "message": f"处理line_change_status请求时出错: {str(e)}"
        }


def plot_layout_by_name_impl(env_name) -> Dict[str, Any]:
    """
    使用 PlotMatplot 的 plot_layout 方法来绘制电网布局。
    """
    try:
        logger.info(f"开始绘制电网布局，环境名称: {env_name}")
        env = grid2op.make(env_name)
        plot_helper = PlotMatplot(env.observation_space)
        fig_layout = plot_helper.plot_layout()
        fig_layout.savefig('grid_layout.png')
        logger.info("电网布局绘制成功，并保存为 'grid_layout.png'")
        return {
            "status": "success",
            "message": "电网布局绘制成功。",
        }
    except Exception as e:
        logger.error(f"绘制电网布局时出错: {str(e)}")
        return {
            "status": "failure",
            "message": str(e)
        }


def plot_layout_by_name(arguments: Dict[str, Any]) -> Any:
    try:
        env_name = arguments.get("env_name")
        logger.info(f"接收到绘制电网布局请求，环境名称: {env_name}")
        result = plot_layout_by_name_impl(env_name)
        return result
    except Exception as e:
        logger.error(f"处理plot_layout_by_name请求时出错: {str(e)}")
        return {
            "status": "failure",
            "message": f"处理plot_layout_by_name请求时出错: {str(e)}"
        }


def plot_layout_by_env_id_impl(env_id) -> Dict[str, Any]:
    """
    使用 PlotMatplot 的 plot_layout 方法来绘制电网布局。
    """
    try:
        logger.info(f"开始根据环境 ID 绘制电网布局，env_id: {env_id}")
        env = env_registry.get(env_id)
        plot_helper = PlotMatplot(env.observation_space)
        fig_layout = plot_helper.plot_layout()
        fig_layout.savefig('grid_layout.png')
        logger.info("电网布局绘制成功，并保存为 'grid_layout.png'")
        return {
            "status": "success",
            "message": "电网布局绘制成功。",
        }
    except Exception as e:
        logger.error(f"绘制电网布局时出错: {str(e)}")
        return {
            "status": "failure",
            "message": str(e)
        }


def plot_layout_by_env_id(arguments: Dict[str, Any]) -> Any:
    try:
        env_id = arguments.get("env_id")
        logger.info(f"接收到绘制电网布局请求，env_id: {env_id}")
        result = plot_layout_by_env_id_impl(env_id)
        return result
    except Exception as e:
        logger.error(f"处理plot_layout_by_env_id请求时出错: {str(e)}")
        return {
            "status": "failure",
            "message": f"处理plot_layout_by_env_id请求时出错: {str(e)}"
        }


def redispatch(arguments: Dict[str, Any]) -> Any:
    try:
        env_id = arguments.get("env_id")
        gen_id = arguments.get("gen_id")
        amount = arguments.get("amount")
        logger.info(f"接收到redispatch请求，env_id: {env_id}, gen_id: {gen_id}, amount: {amount}")
        
        # 确保 amount 是一个列表
        if not isinstance(amount, list):
            amount = [amount]
        
        if len(gen_id) > 1 and len(amount) == 1:
            amount = amount * len(gen_id)
        
        result = redispatch_impl(env_id, gen_id, amount)
        return result
    except Exception as e:
        logger.error(f"处理redispatch请求时出错: {str(e)}")
        return {
            "status": "failure",
            "message": f"处理redispatch请求时出错: {str(e)}"
        }


def redispatch_impl(env_id, gen_id: List[int], amount: List[int]) -> Dict[str, Any]:
    try:
        logger.info(f"开始执行redispatch操作，env_id: {env_id}, gen_id: {gen_id}, amount: {amount}")
        env = env_registry.get(env_id)
        if env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例。")
        
        # 检查是否允许进行重分配操作
        if not env.redispatching_unit_commitment_availble:
            raise ValueError("当前环境不允许进行发电机功率重分配操作。")
        
        # 遍历每个发电机，检测是否可进行重分配
        for g_id in gen_id:
            if not env.gen_redispatchable[g_id]:
                raise ValueError(f"发电机 {g_id} 不允许进行功率重分配。")
        
        param = [(g_id, a) for g_id, a in zip(gen_id, amount)]
        action = env.action_space({"redispatch": param})  # 执行功率重分配

        if action.is_ambiguous()[0]:
            info = action.ambiguous_info()[1]
            raise ValueError(f"动作是模糊的，无法执行。{info}")
        else:
            env.step(action)
            logger.info("成功进行发电机功率重分配。")
            return {
                "status": "success",
                "message": "成功进行发电机功率重分配。"
            }
    except Exception as e:
        logger.error(f"redispatch_impl 执行失败: {str(e)}")
        return {
            "status": "failure",
            "message": f"redispatch_impl 执行失败: {str(e)}"
        }


def curtail(arguments: Dict[str, Any]) -> Any:
    try:
        env_id = arguments.get("env_id", "env")
        gen_id = arguments.get("gen_id")
        amount_ratio = arguments.get("amount_ratio")
        logger.info(f"接收到curtail请求，env_id: {env_id}, gen_id: {gen_id}, amount_ratio: {amount_ratio}")
        
        # 确保 gen_id 和 amount_ratio 都被提供
        if gen_id is None or amount_ratio is None:
            raise ValueError("缺少必需的参数: gen_id 或 amount_ratio。")

        if not isinstance(amount_ratio, list):
            amount_ratio = [amount_ratio]

        if len(gen_id) > 1 and len(amount_ratio) == 1:
            amount_ratio = amount_ratio * len(gen_id)

        result = curtail_impl(env_id, gen_id, amount_ratio)
        return result
    except Exception as e:
        logger.error(f"处理curtail请求时出错: {str(e)}")
        return {
            "status": "failure",
            "message": f"处理curtail请求时出错: {str(e)}"
        }


def curtail_impl(env_id, gen_id: List[int], amount_ratio: List[float]) -> Dict[str, Any]:
    try:
        logger.info(f"开始执行curtail操作，env_id: {env_id}, gen_id: {gen_id}, amount_ratio: {amount_ratio}")
        env = env_registry.get(env_id)
        if env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例。")

        param = [(g_id, ratio) for g_id, ratio in zip(gen_id, amount_ratio)]
        action = env.action_space({"curtail": param})

        if action.is_ambiguous()[0]:
            info = action.ambiguous_info()[1]
            raise ValueError(f"动作是模糊的，无法执行。{info}")
        else:
            env.step(action)
            logger.info("成功进行发电削减操作。")
            return {
                "status": "success",
                "message": "成功进行发电削减操作。"
            }
    except Exception as e:
        logger.error(f"curtail_impl 执行失败: {str(e)}")
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
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # 增加到毫秒级时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]  # 精确到毫秒
        filename = f"plot_{timestamp}.png"
        file_path = os.path.join(folder_name, filename)
        
        fig_obs.savefig(file_path)
        logger.info(f"电网观测状态绘制成功，并保存为 {file_path}")
        
        return {
            "status": "success",
            "message": "电网观测状态绘制成功。"
        }
    except Exception as e:
        logger.error(f"绘制电网观测状态时出错: {str(e)}")
        return {
            "status": "failure",
            "message": str(e)
        }

def plot_obs_by_env_id(arguments: Dict[str, Any]) -> Any:
    try:
        env_id = arguments.get("env_id")
        logger.info(f"接收到绘制电网观测状态请求，env_id: {env_id}")
        result = plot_obs_by_env_id_impl(env_id)
        return result
    except Exception as e:
        logger.error(f"处理plot_obs_by_env_id请求时出错: {str(e)}")
        return {
            "status": "failure",
            "message": f"处理plot_obs_by_env_id请求时出错: {str(e)}"
        }