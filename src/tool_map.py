from execution_func import *

# 映射工具名称到执行函数对
tool_map = {
    "set_bus": set_bus,
    "line_change_status": line_change_status,
    "plot_layout_by_name":plot_layout_by_name,
    "plot_layout_by_env_id":plot_layout_by_env_id,
    "redispatch":redispatch,
    "curtail":curtail,
    "plot_obs_by_env_id":plot_obs_by_env_id
}