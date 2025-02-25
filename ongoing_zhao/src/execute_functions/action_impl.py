import numpy as np
import grid2op
from grid2op.Action import CompleteAction

def propertygen_set_bus(env_id='env', method=None, gen_id=None, busbars=None):
    """
    根据指定的方法修改Grid2Op环境中发电机的母线分配。
    
    Parameters:
    env_id (str): Grid2Op环境的ID，默认为'env'。
    method (str): 选择修改母线的方式，支持 "full_vector"、"index"、"list" 和 "dict"。
    gen_id (list, optional): 发电机ID的列表，用于 "index" 和 "list" 方法。
    busbars (list/dict): 母线分配信息，可以是完整的数组、元组列表或字典，视 method 而定。
    
    Returns:
    res (ndarray): 修改后的发电机母线设置。
    """
    # 加载环境
    env = grid2op.make(env_id, test=True, action_class=CompleteAction)

    # 创建一个动作空间
    act = env.action_space()

    # 根据不同的method处理母线分配
    if method == "full_vector":
        if isinstance(busbars, list) and len(busbars) == act.n_gen:
            # 完整的母线数组
            act.gen_set_bus = np.array(busbars, dtype=int)
        else:
            raise ValueError("full_vector method requires a full array matching the number of generators.")
    
    elif method == "index":
        if isinstance(busbars, list) and len(gen_id) == len(busbars):
            # 根据发电机ID修改母线
            busbar_vector = np.zeros(act.n_gen, dtype=int)
            for i, gen in enumerate(gen_id):
                busbar_vector[gen] = busbars[i]
            act.gen_set_bus = busbar_vector
        else:
            raise ValueError("index method requires both gen_id and busbars to be lists of the same length.")
    
    elif method == "list":
        if isinstance(busbars, list) and all(isinstance(i, tuple) for i in busbars):
            # 元组列表形式
            act.gen_set_bus = busbars
        else:
            raise ValueError("list method requires a list of tuples (gen_id, busbar).")
    
    elif method == "dict":
        if isinstance(busbars, dict):
            # 字典形式
            act.gen_set_bus = busbars
        else:
            raise ValueError("dict method requires a dictionary mapping generator names to busbars.")
    
    else:
        raise ValueError("Invalid method. Choose from 'full_vector', 'index', 'list', or 'dict'.")

    # 返回修改后的母线分配
    res = act.gen_set_bus
    return res

# 示例调用：

# 使用 full_vector 方法
env_id = "educ_case14_storage"
method = "full_vector"
busbars = [1, 2, 3, 0]
print(propertygen_set_bus(env_id=env_id, method=method, busbars=busbars))

# 使用 index 方法
method = "index"
gen_id = [0, 1]
busbars = [1, 2]
print(propertygen_set_bus(env_id=env_id, method=method, gen_id=gen_id, busbars=busbars))

# 使用 list 方法
method = "list"
busbars = [(0, -1), (1, 2)]
print(propertygen_set_bus(env_id=env_id, method=method, busbars=busbars))

# 使用 dict 方法
method = "dict"
busbars = {"gen_1_0": 2}
print(propertygen_set_bus(env_id=env_id, method=method, busbars=busbars))