# observations/provider.py
from typing import List, Dict, Any, Optional, Union, Tuple
import numpy as np
import grid2op
from global_context import env_manager
from src.utils import get_logger

class ObservationProvider:
    """
    观测数据提供者，用于统一获取 Grid2Op 环境中的各种观测数据。
    """
    
    def __init__(self, env_manager):
        """
        初始化 ObservationProvider。
        
        参数:
        env_manager: 环境管理器实例，用于获取环境和观测
        """
        self.env_manager = env_manager
        self.logger = get_logger(__name__)
    
    def get_observation(self, env_id: str, component: str, element_id: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        统一的观测获取接口
        
        参数:
        env_id (str): 环境ID
        component (str): 要获取的组件类型，如 'gen_p', 'load_q', 'line_status' 等
        element_id (Optional[List[int]]): 可选的元素ID列表
        
        返回:
        Dict[str, Any]: 包含观测结果的字典
        """
        try:
            self.logger.info(f"获取观测数据: env_id={env_id}, component={component}, element_id={element_id}")
            
            # 获取观测对象
            obs = self.env_manager.get_latest_obs(env_id)
            if obs is None:
                self.logger.error(f"无法获取环境 '{env_id}' 的观测数据")
                return {
                    "status": "failure", 
                    "message": f"无法获取环境 '{env_id}' 的观测数据"
                }
            
            # 根据组件类型获取相应数据
            if hasattr(obs, component):
                data = getattr(obs, component)
                
                # 处理元素ID过滤
                if element_id is not None:
                    if isinstance(data, np.ndarray) and data.ndim > 0:
                        data = data[element_id]
                
                # 处理 numpy 数组转换
                if hasattr(data, 'tolist'):
                    data = data.tolist()
                
                self.logger.info(f"成功获取 {component} 数据")
                return {
                    "status": "success",
                    "message": f"成功获取 {component} 数据",
                    "data": data
                }
            else:
                self.logger.error(f"观测对象不包含 {component} 属性")
                return {
                    "status": "failure",
                    "message": f"观测对象不包含 {component} 属性"
                }
        except Exception as e:
            self.logger.error(f"获取观测数据失败: {str(e)}")
            return {
                "status": "failure",
                "message": f"获取观测数据失败: {str(e)}"
            }
    
    def get_multiple_observations(self, env_id: str, components: List[str], element_ids: Optional[Dict[str, List[int]]] = None) -> Dict[str, Any]:
        """
        批量获取多个观测数据
        
        参数:
        env_id (str): 环境ID
        components (List[str]): 要获取的组件类型列表
        element_ids (Optional[Dict[str, List[int]]]): 可选的元素ID字典，键为组件名称，值为元素ID列表
        
        返回:
        Dict[str, Any]: 包含多个观测结果的字典
        """
        try:
            self.logger.info(f"批量获取观测数据: env_id={env_id}, components={components}")
            
            results = {}
            all_success = True
            
            for component in components:
                element_id = element_ids.get(component) if element_ids else None
                result = self.get_observation(env_id, component, element_id)
                results[component] = result
                
                if result["status"] != "success":
                    all_success = False
            
            return {
                "status": "success" if all_success else "partial_success",
                "message": "所有观测数据获取成功" if all_success else "部分观测数据获取失败",
                "results": results
            }
        except Exception as e:
            self.logger.error(f"批量获取观测数据失败: {str(e)}")
            return {
                "status": "failure",
                "message": f"批量获取观测数据失败: {str(e)}"
            }
    
    def get_topology_snapshot(self, env_id: str) -> Dict[str, Any]:
        """
        获取电网拓扑结构快照
        
        参数:
        env_id (str): 环境ID
        
        返回:
        Dict[str, Any]: 包含拓扑结构快照的字典
        """
        try:
            self.logger.info(f"获取拓扑结构快照: env_id={env_id}")
            
            # 获取观测对象
            obs = self.env_manager.get_latest_obs(env_id)
            if obs is None:
                return {
                    "status": "failure", 
                    "message": f"无法获取环境 '{env_id}' 的观测数据"
                }
            
            # 收集拓扑相关信息
            topo_data = {
                "topo_vect": obs.topo_vect.tolist() if hasattr(obs.topo_vect, 'tolist') else obs.topo_vect,
                "line_status": obs.line_status.tolist() if hasattr(obs.line_status, 'tolist') else obs.line_status,
                "timestep_overflow": obs.timestep_overflow.tolist() if hasattr(obs.timestep_overflow, 'tolist') else obs.timestep_overflow,
                "line_or_bus": [int(bus) for bus in obs.line_or_to_subid],
                "line_ex_bus": [int(bus) for bus in obs.line_ex_to_subid],
                "gen_bus": [int(bus) for bus in obs.gen_to_subid],
                "load_bus": [int(bus) for bus in obs.load_to_subid],
            }
            
            # 如果有储能设备
            if hasattr(obs, 'storage_to_subid'):
                topo_data["storage_bus"] = [int(bus) for bus in obs.storage_to_subid]
            
            self.logger.info("成功获取拓扑结构快照")
            return {
                "status": "success",
                "message": "成功获取拓扑结构快照",
                "data": topo_data
            }
        except Exception as e:
            self.logger.error(f"获取拓扑结构快照失败: {str(e)}")
            return {
                "status": "failure",
                "message": f"获取拓扑结构快照失败: {str(e)}"
            }
    
    def get_power_flow_snapshot(self, env_id: str) -> Dict[str, Any]:
        """
        获取电力潮流快照
        
        参数:
        env_id (str): 环境ID
        
        返回:
        Dict[str, Any]: 包含电力潮流快照的字典
        """
        try:
            self.logger.info(f"获取电力潮流快照: env_id={env_id}")
            
            # 获取观测对象
            obs = self.env_manager.get_latest_obs(env_id)
            if obs is None:
                return {
                    "status": "failure", 
                    "message": f"无法获取环境 '{env_id}' 的观测数据"
                }
            
            # 收集电力潮流相关信息
            flow_data = {
                "generators": {
                    "p": obs.gen_p.tolist() if hasattr(obs.gen_p, 'tolist') else obs.gen_p,
                    "q": obs.gen_q.tolist() if hasattr(obs.gen_q, 'tolist') else obs.gen_q,
                    "v": obs.gen_v.tolist() if hasattr(obs.gen_v, 'tolist') else obs.gen_v,
                },
                "loads": {
                    "p": obs.load_p.tolist() if hasattr(obs.load_p, 'tolist') else obs.load_p,
                    "q": obs.load_q.tolist() if hasattr(obs.load_q, 'tolist') else obs.load_q,
                    "v": obs.load_v.tolist() if hasattr(obs.load_v, 'tolist') else obs.load_v,
                },
                "lines": {
                    "p_or": obs.p_or.tolist() if hasattr(obs.p_or, 'tolist') else obs.p_or,
                    "q_or": obs.q_or.tolist() if hasattr(obs.q_or, 'tolist') else obs.q_or,
                    "v_or": obs.v_or.tolist() if hasattr(obs.v_or, 'tolist') else obs.v_or,
                    "a_or": obs.a_or.tolist() if hasattr(obs.a_or, 'tolist') else obs.a_or,
                    "p_ex": obs.p_ex.tolist() if hasattr(obs.p_ex, 'tolist') else obs.p_ex,
                    "q_ex": obs.q_ex.tolist() if hasattr(obs.q_ex, 'tolist') else obs.q_ex,
                    "v_ex": obs.v_ex.tolist() if hasattr(obs.v_ex, 'tolist') else obs.v_ex,
                    "a_ex": obs.a_ex.tolist() if hasattr(obs.a_ex, 'tolist') else obs.a_ex,
                    "rho": obs.rho.tolist() if hasattr(obs.rho, 'tolist') else obs.rho,
                }
            }
            
            # 如果有储能设备
            if hasattr(obs, 'storage_p'):
                flow_data["storage"] = {
                    "p": obs.storage_p.tolist() if hasattr(obs.storage_p, 'tolist') else obs.storage_p,
                    "q": obs.storage_q.tolist() if hasattr(obs.storage_q, 'tolist') else obs.storage_q,
                    "v": obs.storage_v.tolist() if hasattr(obs.storage_v, 'tolist') else obs.storage_v,
                    "charge": obs.storage_charge.tolist() if hasattr(obs.storage_charge, 'tolist') else obs.storage_charge,
                }
            
            self.logger.info("成功获取电力潮流快照")
            return {
                "status": "success",
                "message": "成功获取电力潮流快照",
                "data": flow_data
            }
        except Exception as e:
            self.logger.error(f"获取电力潮流快照失败: {str(e)}")
            return {
                "status": "failure",
                "message": f"获取电力潮流快照失败: {str(e)}"
            }
    
    def get_dispatch_snapshot(self, env_id: str) -> Dict[str, Any]:
        """
        获取发电机调度快照
        
        参数:
        env_id (str): 环境ID
        
        返回:
        Dict[str, Any]: 包含发电机调度快照的字典
        """
        try:
            self.logger.info(f"获取发电机调度快照: env_id={env_id}")
            
            # 获取观测对象
            obs = self.env_manager.get_latest_obs(env_id)
            if obs is None:
                return {
                    "status": "failure", 
                    "message": f"无法获取环境 '{env_id}' 的观测数据"
                }
            
            # 收集发电机调度相关信息
            dispatch_data = {
                "target_dispatch": obs.target_dispatch.tolist() if hasattr(obs.target_dispatch, 'tolist') else obs.target_dispatch,
                "actual_dispatch": obs.actual_dispatch.tolist() if hasattr(obs.actual_dispatch, 'tolist') else obs.actual_dispatch,
            }
            
            # 添加削减相关信息（如果有）
            if hasattr(obs, 'curtailment'):
                dispatch_data["curtailment"] = obs.curtailment.tolist() if hasattr(obs.curtailment, 'tolist') else obs.curtailment
            
            if hasattr(obs, 'curtailment_limit'):
                dispatch_data["curtailment_limit"] = obs.curtailment_limit.tolist() if hasattr(obs.curtailment_limit, 'tolist') else obs.curtailment_limit
            
            if hasattr(obs, 'gen_p_before_curtail'):
                dispatch_data["gen_p_before_curtail"] = obs.gen_p_before_curtail.tolist() if hasattr(obs.gen_p_before_curtail, 'tolist') else obs.gen_p_before_curtail
            
            # 添加发电机余量信息（如果有）
            if hasattr(obs, 'gen_margin_up'):
                dispatch_data["gen_margin_up"] = obs.gen_margin_up.tolist() if hasattr(obs.gen_margin_up, 'tolist') else obs.gen_margin_up
            
            if hasattr(obs, 'gen_margin_down'):
                dispatch_data["gen_margin_down"] = obs.gen_margin_down.tolist() if hasattr(obs.gen_margin_down, 'tolist') else obs.gen_margin_down
            
            self.logger.info("成功获取发电机调度快照")
            return {
                "status": "success",
                "message": "成功获取发电机调度快照",
                "data": dispatch_data
            }
        except Exception as e:
            self.logger.error(f"获取发电机调度快照失败: {str(e)}")
            return {
                "status": "failure",
                "message": f"获取发电机调度快照失败: {str(e)}"
            }
    
    def get_time_info(self, env_id: str) -> Dict[str, Any]:
        """
        获取时间相关信息
        
        参数:
        env_id (str): 环境ID
        
        返回:
        Dict[str, Any]: 包含时间信息的字典
        """
        try:
            self.logger.info(f"获取时间相关信息: env_id={env_id}")
            
            # 获取观测对象
            obs = self.env_manager.get_latest_obs(env_id)
            if obs is None:
                return {
                    "status": "failure", 
                    "message": f"无法获取环境 '{env_id}' 的观测数据"
                }
            
            # 收集时间相关信息
            time_data = {
                "current_step": int(obs.current_step) if hasattr(obs, 'current_step') else None,
                "max_step": int(obs.max_step) if hasattr(obs, 'max_step') else None,
                "delta_time": float(obs.delta_time) if hasattr(obs, 'delta_time') else None,
            }
            
            # 添加日期时间信息（如果有）
            if hasattr(obs, 'year'):
                time_data["date"] = {
                    "year": int(obs.year),
                    "month": int(obs.month),
                    "day": int(obs.day),
                    "hour_of_day": int(obs.hour_of_day),
                    "minute_of_hour": int(obs.minute_of_hour),
                    "day_of_week": int(obs.day_of_week)
                }
            
            self.logger.info("成功获取时间相关信息")
            return {
                "status": "success",
                "message": "成功获取时间相关信息",
                "data": time_data
            }
        except Exception as e:
            self.logger.error(f"获取时间相关信息失败: {str(e)}")
            return {
                "status": "failure",
                "message": f"获取时间相关信息失败: {str(e)}"
            }
    
    def get_env_parameters(self, env_id: str) -> Dict[str, Any]:
        """
        获取环境参数
        
        参数:
        env_id (str): 环境ID
        
        返回:
        Dict[str, Any]: 包含环境参数的字典
        """
        try:
            self.logger.info(f"获取环境参数: env_id={env_id}")
            
            # 获取环境实例
            env = self.env_manager._envs.get(env_id)
            if env is None:
                return {
                    "status": "failure", 
                    "message": f"无法获取环境 '{env_id}' 的实例"
                }
            
            # 收集环境参数
            env_params = {
                "n_gen": env.n_gen,
                "n_load": env.n_load,
                "n_line": env.n_line,
                "n_sub": env.n_sub,
                "n_storage": env.n_storage if hasattr(env, 'n_storage') else 0,
                "thermal_limit": env.get_thermal_limit().tolist() if hasattr(env.get_thermal_limit(), 'tolist') else env.get_thermal_limit(),
                "gen_pmin": env.gen_pmin.tolist() if hasattr(env.gen_pmin, 'tolist') else env.gen_pmin,
                "gen_pmax": env.gen_pmax.tolist() if hasattr(env.gen_pmax, 'tolist') else env.gen_pmax,
                "gen_redispatchable": env.gen_redispatchable.tolist() if hasattr(env.gen_redispatchable, 'tolist') else env.gen_redispatchable,
                "gen_renewable": env.gen_renewable.tolist() if hasattr(env.gen_renewable, 'tolist') else env.gen_renewable,
            }
            
            self.logger.info("成功获取环境参数")
            return {
                "status": "success",
                "message": "成功获取环境参数",
                "data": env_params
            }
        except Exception as e:
            self.logger.error(f"获取环境参数失败: {str(e)}")
            return {
                "status": "failure",
                "message": f"获取环境参数失败: {str(e)}"
            }


# 创建全局 ObservationProvider 实例
observation_provider = ObservationProvider(env_manager)
