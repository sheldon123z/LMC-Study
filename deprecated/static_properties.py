from typing import Dict, List, Any
import grid2op
import numpy as np
from src.utils import get_logger
from registry import env_registry


# 初始化日志记录器
logger = get_logger(__name__)


def generator_get_static_properties(env_id: str, gen_id: List[int]) -> Dict:
    """
    获取环境中，指定发电机的静态属性，如最小/最大功率、最大上下调幅度等。

    参数:
    env_id (str): 环境实例的ID。
    gen_id (List[int]): 发电机的ID列表。

    返回:
    Dict: 包含每个发电机静态属性的字典，键是发电机ID，值是包含以下信息的字典：
        - "pmin" (float): 发电机的最小功率。
        - "pmax" (float): 发电机的最大功率。
        - "max_ramp_down" (float): 发电机的最大下调幅度。
        - "max_ramp_up" (float): 发电机的最大上调幅度。
        - "is_redispatchable" (bool): 发电机是否可重新调度。
        - "is_renewable" (bool): 发电机是否为可再生能源。

    异常:
    ValueError: 如果输入的 `gen_id` 列表为空或无效的发电机ID。
    KeyError: 如果无法在环境实例中找到相应的发电机。
    Exception: 任何其他异常。

    日志:
    会记录每次请求的详细信息和错误信息。
    """
    try:
        # 获取环境实例
        env = env_registry.get(env_id)
        if env is None:
            raise ValueError(f"未找到名为 {env_id} 的环境实例。")

        static_properties = {}

        # 获取发电机的静态属性
        logger.info(f"开始获取环境 {env_id} 中发电机的静态属性。")
        for g_id in gen_id:

            static_properties[g_id] = {
                "min_production": env.gen_pmin[g_id],
                "max_production": env.gen_pmax[g_id],
                "max_ramp_down": env.gen_max_ramp_down[g_id],
                "max_ramp_up": env.gen_max_ramp_up[g_id],
                "is_redispatchable": env.gen_redispatchable[g_id],
                "is_renewable": env.gen_renewable[g_id]
            }
        
        logger.info(f"成功获取 {len(gen_id)} 个发电机的静态属性。")
        return static_properties
    
    except ValueError as ve:
        logger.error(f"获取发电机静态属性失败，错误信息: {str(ve)}")
        return {
            "status": "failure",
            "message": str(ve)
        }
    
    except KeyError as ke:
        logger.error(f"获取发电机静态属性失败，错误信息: {str(ke)}")
        return {
            "status": "failure",
            "message": str(ke)
        }
    
    except Exception as e:
        logger.error(f"处理获取发电机静态属性时出错: {str(e)}")
        return {
            "status": "failure",
            "message": f"处理获取发电机静态属性时出错: {str(e)}"
        }


# def load_get_static_properties(env_id: str, load_id: List[int]) -> Dict:



# def powerline_get_static_properties(env_id: str, line_id: List[int]) -> Dict:
    
    

def storage_get_static_properties(env_id: str, storage_id: List[int]) -> Dict:
    """
    获取环境中，指定储能单元的静态属性，如最大储能量、最小储能量、最大功率等。

    参数:
    env_id (str): 环境实例的ID。
    storage_id (List[int]): 储能单元的ID列表。

    返回:
    Dict: 包含每个储能单元静态属性的字典，键是储能单元ID，值是包含以下信息的字典：
        - "max_energy" (float): 储能单元的最大储能，单位为MWh。
        - "min_energy" (float): 储能单元的最小储能，单位为MWh。
        - "max_power_production" (float): 储能单元向电网输出的最大功率，单位为MW。
        - "max_power_absorb" (float): 储能单元从电网吸收的最大功率，单位为MW。
        - "charging_efficiency" (float): 储能单元的充电效率，取值范围为0到1。
        - "discharging_efficiency" (float): 储能单元的放电效率，取值范围为0到1。

    异常:
    ValueError: 如果输入的 `storage_id` 列表为空或无效的储能单元ID。
    KeyError: 如果无法在环境实例中找到相应的储能单元。
    Exception: 任何其他异常。

    日志:
    会记录每次请求的详细信息和错误信息。
    """
    try:
        # 获取环境实例
        env = env_registry.get(env_id)
        if env is None:
            raise ValueError(f"未找到名为 {env_id} 的环境实例。")

        static_properties = {}

        # 获取储能单元的静态属性
        logger.info(f"开始获取环境 {env_id} 中储能单元的静态属性。")
        for s_id in storage_id:

            static_properties[s_id] = {
                "max_energy": env.storage_Emax[s_id],
                "min_energy": env.storage_Emin[s_id],
                "max_power_production": env.storage_max_p_prod[s_id],
                "max_power_absorb": env.storage_max_p_absorb[s_id],
                "charging_efficiency": env.storage_charging_efficiency[s_id],
                "discharging_efficiency": env.storage_discharging_efficiency[s_id]
            }

        logger.info(f"成功获取 {len(storage_id)} 个储能单元的静态属性。")
        return static_properties
    
    except ValueError as ve:
        logger.error(f"获取储能单元静态属性失败，错误信息: {str(ve)}")
        return {
            "status": "failure",
            "message": str(ve)
        }
    
    except KeyError as ke:
        logger.error(f"获取储能单元静态属性失败，错误信息: {str(ke)}")
        return {
            "status": "failure",
            "message": str(ke)
        }
    
    except Exception as e:
        logger.error(f"处理获取储能单元静态属性时出错: {str(e)}")
        return {
            "status": "failure",
            "message": f"处理获取储能单元静态属性时出错: {str(e)}"
        }
    
    
    
# def substation_get_static_properties(env_id: str, substation_id: List[int]) -> Dict:
    
    
