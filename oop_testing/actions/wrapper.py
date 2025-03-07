# actions/wrapper.py
from typing import List, Dict, Any, Optional, Union, Tuple
import numpy as np
import grid2op
from grid2op.Action import BaseAction
from global_context import env_manager
from src.utils import get_logger

class ActionWrapper:
    """
    Grid2op动作的面向对象包装器，用于组合多种操作并执行。
    """
    
    def __init__(self, env_manager, env_id: str):
        """
        初始化ActionWrapper。
        
        参数:
        env_manager: 环境管理器实例，用于管理和注册环境
        env_id (str): 环境实例的ID
        """
        self.env_manager = env_manager
        self.env_id = env_id
        
        # 获取环境实例
        self.env = env_manager._envs.get(env_id)
        if self.env is None:
            raise ValueError(f"无法找到 env_id 为 {env_id} 的环境实例。")
            
        # 创建一个新的动作
        self.action = self.env.action_space()
        
        # 设置日志
        self.logger = get_logger(__name__)
    
    def gen_set_bus(self, gen_id: List[int], bus_status: List[int]) -> 'ActionWrapper':
        """
        设置发电机与母线的连接状态。
        
        参数:
        gen_id (List[int]): 发电机ID列表
        bus_status (List[int]): 母线状态列表，每个整数代表对应的操作:
            - 0: 该动作不对这个发电机产生作用
            - -1: 断开该发电机
            - 1: 将该发电机设置到母线1
            - 2: 将该发电机设置到母线2
            - 3: 将该发电机设置到母线3(grid2op >= 1.10.0)等
            
        返回:
        ActionWrapper: 返回自身，支持链式调用
        """
        self.action.gen_set_bus = list(zip(gen_id, bus_status))
        self.logger.info(f"已添加发电机母线设置操作: gen_id={gen_id}, bus_status={bus_status}")
        return self
    
    def load_set_bus(self, load_id: List[int], bus_status: List[int]) -> 'ActionWrapper':
        """
        设置负荷与母线的连接状态。
        
        参数:
        load_id (List[int]): 负荷ID列表
        bus_status (List[int]): 母线状态列表
            
        返回:
        ActionWrapper: 返回自身，支持链式调用
        """
        self.action.load_set_bus = list(zip(load_id, bus_status))
        self.logger.info(f"已添加负荷母线设置操作: load_id={load_id}, bus_status={bus_status}")
        return self
    
    def line_or_set_bus(self, line_id: List[int], bus_status: List[int]) -> 'ActionWrapper':
        """
        设置输电线路起始端与母线的连接状态。
        
        参数:
        line_id (List[int]): 线路ID列表
        bus_status (List[int]): 母线状态列表
            
        返回:
        ActionWrapper: 返回自身，支持链式调用
        """
        self.action.line_or_set_bus = list(zip(line_id, bus_status))
        self.logger.info(f"已添加线路起始端母线设置操作: line_id={line_id}, bus_status={bus_status}")
        return self
    
    def line_ex_set_bus(self, line_id: List[int], bus_status: List[int]) -> 'ActionWrapper':
        """
        设置输电线路终止端与母线的连接状态。
        
        参数:
        line_id (List[int]): 线路ID列表
        bus_status (List[int]): 母线状态列表
            
        返回:
        ActionWrapper: 返回自身，支持链式调用
        """
        self.action.line_ex_set_bus = list(zip(line_id, bus_status))
        self.logger.info(f"已添加线路终止端母线设置操作: line_id={line_id}, bus_status={bus_status}")
        return self
    
    def storage_set_bus(self, storage_id: List[int], bus_status: List[int]) -> 'ActionWrapper':
        """
        设置储能设备与母线的连接状态。
        
        参数:
        storage_id (List[int]): 储能设备ID列表
        bus_status (List[int]): 母线状态列表
            
        返回:
        ActionWrapper: 返回自身，支持链式调用
        """
        self.action.storage_set_bus = list(zip(storage_id, bus_status))
        self.logger.info(f"已添加储能设备母线设置操作: storage_id={storage_id}, bus_status={bus_status}")
        return self
    
    def line_set_status(self, line_id: List[int], line_status: List[int]) -> 'ActionWrapper':
        """
        设置输电线路的连接状态。
        
        参数:
        line_id (List[int]): 线路ID列表
        line_status (List[int]): 线路状态列表:
            - 0: 不改变该线路状态
            - 1: 连接该线路
            - -1: 断开该线路
            
        返回:
        ActionWrapper: 返回自身，支持链式调用
        """
        self.action.line_set_status = list(zip(line_id, line_status))
        self.logger.info(f"已添加线路状态设置操作: line_id={line_id}, line_status={line_status}")
        return self
    
    def redispatch(self, gen_id: List[int], amount: List[float]) -> 'ActionWrapper':
        """
        设置发电机的重调度量。
        
        参数:
        gen_id (List[int]): 发电机ID列表
        amount (List[float]): 重调度量列表(MW)，正值表示增加发电量，负值表示减少发电量
            
        返回:
        ActionWrapper: 返回自身，支持链式调用
        """
        self.action.redispatch = list(zip(gen_id, amount))
        self.logger.info(f"已添加发电机重调度操作: gen_id={gen_id}, amount={amount}")
        return self
    
    def cancel_redispatch(self, gen_id: List[int]) -> 'ActionWrapper':
        """
        取消指定发电机的重调度。
        
        参数:
        gen_id (List[int]): 要取消重调度的发电机ID列表
            
        返回:
        ActionWrapper: 返回自身，支持链式调用
        """
        # 获取最新观测
        obs = self.env_manager.get_latest_obs(self.env_id)
        if obs is None:
            raise ValueError(f"无法获取环境 '{self.env_id}' 的观测数据")
            
        # 获取当前调度值并计算反向delta值
        gen_id_arr = np.array(gen_id)
        target_dispatch = obs.target_dispatch[gen_id_arr]
        deltas = -target_dispatch  # 计算反向delta值
        
        # 设置重调度
        self.action.redispatch = list(zip(gen_id, deltas.tolist()))
        self.logger.info(f"已添加取消发电机重调度操作: gen_id={gen_id}")
        return self
    
    def storage_p(self, storage_id: List[int], amount: List[float]) -> 'ActionWrapper':
        """
        设置储能单元的充放电功率。
        
        参数:
        storage_id (List[int]): 储能单元ID列表
        amount (List[float]): 充放电功率列表(MW)，正值表示充电，负值表示放电
            
        返回:
        ActionWrapper: 返回自身，支持链式调用
        """
        self.action.storage_p = list(zip(storage_id, amount))
        self.logger.info(f"已添加储能单元充放电操作: storage_id={storage_id}, amount={amount}")
        return self
    
    def curtail(self, gen_id: List[int], amount: List[float]) -> 'ActionWrapper':
        """
        设置可再生能源发电机的限电量。
        
        参数:
        gen_id (List[int]): 发电机ID列表
        amount (List[float]): 限电比例列表，范围在[0.0, 1.0]之间，1表示不限电，0表示完全限电
            
        返回:
        ActionWrapper: 返回自身，支持链式调用
        """
        self.action.curtail = list(zip(gen_id, amount))
        self.logger.info(f"已添加发电机限电操作: gen_id={gen_id}, amount={amount}")
        return self
    
    def combine(self, other_action: Union[BaseAction, 'ActionWrapper']) -> 'ActionWrapper':
        """
        将当前动作与另一个动作组合。
        
        参数:
        other_action: 另一个动作，可以是Grid2op的BaseAction或ActionWrapper
            
        返回:
        ActionWrapper: 返回自身，支持链式调用
        """
        if isinstance(other_action, ActionWrapper):
            # 如果是ActionWrapper，获取其内部的BaseAction
            other_action = other_action.get_action()
            
        # 使用Grid2op动作的组合功能
        self.action += other_action
        self.logger.info("已组合两个动作")
        return self
    
    def __add__(self, other: Union[BaseAction, 'ActionWrapper']) -> 'ActionWrapper':
        """
        重载+运算符，用于组合动作。
        
        参数:
        other: 另一个动作，可以是Grid2op的BaseAction或ActionWrapper
            
        返回:
        ActionWrapper: 新的动作包装器，包含组合后的动作
        """
        # 创建一个新的ActionWrapper
        result = ActionWrapper(self.env_manager, self.env_id)
        
        # 复制当前动作
        result.action = self.action
        
        # 组合另一个动作
        return result.combine(other)
    
    def get_action(self) -> BaseAction:
        """
        获取内部的Grid2op动作对象。
        
        返回:
        BaseAction: Grid2op的动作对象
        """
        return self.action
    
    def is_ambiguous(self) -> Tuple[bool, str]:
        """
        检查动作是否模糊。
        
        返回:
        Tuple[bool, str]: 是否模糊的标志和详细信息
        """
        return self.action.is_ambiguous()
    
    def execute(self) -> Dict[str, Any]:
        """
        执行动作并返回结果。
        
        返回:
        Dict[str, Any]: 包含执行结果的字典
        """
        try:
            # 检查动作是否模糊
            is_ambiguous, ambiguity_msg = self.action.is_ambiguous()
            if is_ambiguous:
                raise ValueError(f"动作是模糊的，无法执行: {ambiguity_msg}")
                
            # 输出动作内容(用于调试)
            self.logger.debug(f"执行动作: {self.action}")
                
            # 执行动作
            obs, reward, done, info = self.env.step(self.action)
                
            # 使用环境管理器注册新观察
            self.env_manager.record_observation(self.env_id, obs)
                
            # 返回执行结果
            self.logger.info("动作执行成功")
            return {
                "status": "success",
                "message": "动作执行成功",
                "observation": obs,
                "reward": reward,
                "done": done,
                "info": info
            }
        except Exception as e:
            self.logger.error(f"动作执行失败: {str(e)}")
            return {
                "status": "failure",
                "message": f"动作执行失败: {str(e)}"
            }


class ActionFactory:
    """
    用于创建ActionWrapper实例的工厂类。
    """
    
    def __init__(self, env_manager):
        """
        初始化ActionFactory。
        
        参数:
        env_manager: 环境管理器实例
        """
        self.env_manager = env_manager
    
    def for_env(self, env_id: str) -> ActionWrapper:
        """
        为指定环境创建一个ActionWrapper实例。
        
        参数:
        env_id (str): 环境实例的ID
            
        返回:
        ActionWrapper: 新创建的动作包装器
        """
        return ActionWrapper(self.env_manager, env_id)

# 创建全局 ActionFactory 实例
action_factory = ActionFactory(env_manager)
