# Grid2op-LLM 电网控制代理

该项目使用大语言模型（LLM）作为控制代理，通过 LangGraph 框架与 Grid2op 电力系统仿真环境进行交互。系统允许大语言模型通过自然语言理解和规划，来执行复杂的电网操作任务。

## 项目概述

Grid2op-LLM 电网控制代理是一个结合了大语言模型和电力系统仿真的项目，旨在探索 AI 在电力系统操作和管理中的应用潜力。该系统可以：

- 使用自然语言解释和执行电网控制指令
- 通过 ReAct（Reasoning and Acting）模式执行多步规划和操作
- 实时获取电网状态并进行分析
- 执行复杂的组合操作，如重调度、线路切换等

## 系统架构

项目由以下几个主要模块组成：

### 1. 全局环境管理

- `global_context.py`：提供全局环境管理器实例
- `registry_object.py`：实现环境注册和管理的核心类

### 2. 日志和工具设施 

- `src/utils/__init__.py`：提供日志记录功能，支持时间戳日志文件

### 3. 电网操作包装器

- `actions/wrapper.py`：提供面向对象的 Grid2op 动作包装器，实现多种电网操作功能

### 4. 观测数据提供者

- `observations/provider.py`：统一获取 Grid2op 环境中各种观测数据的接口

### 5. 工具函数库

- `tools/grid2op_tools.py`：提供给 LLM 使用的工具函数集合，包括：
  - 动作创建工具（不执行）
  - 动作执行工具
  - 观测获取工具
  - 动作清理工具

### 6. LangGraph 集成

项目使用 LangGraph 框架构建 ReAct 代理，实现 LLM 与 Grid2op 环境的交互。

## 工具函数概览

### 动作创建工具

这些工具用于创建不同类型的动作，但不会立即执行：

- `create_gen_set_bus`: 创建发电机母线设置动作
- `create_load_set_bus`: 创建负荷母线设置动作
- `create_line_or_set_bus`: 创建线路起始端母线设置动作
- `create_line_ex_set_bus`: 创建线路终止端母线设置动作
- `create_storage_set_bus`: 创建储能设备母线设置动作
- `create_line_set_status`: 创建线路状态设置动作
- `create_redispatch`: 创建发电机重调度动作
- `create_cancel_redispatch`: 创建取消发电机重调度的动作
- `create_curtail`: 创建可再生能源发电机限电动作
- `create_storage_p`: 创建储能单元充放电动作

### 动作执行工具

这些工具用于执行之前创建的动作：

- `execute_action`: 执行之前创建的动作
- `combine_actions`: 组合多个已创建的动作
- `execute_combined_action`: 创建组合动作并立即执行

### 观测获取工具

这些工具用于获取电网的状态信息：

- `get_observation`: 获取指定组件的观测数据
- `get_topology_snapshot`: 获取电网拓扑结构快照
- `get_power_flow_snapshot`: 获取电力潮流快照
- `get_dispatch_snapshot`: 获取发电机调度快照
- `get_time_info`: 获取时间相关信息
- `get_env_parameters`: 获取环境参数

## 环境管理

环境管理器 (`EnvironmentManager`) 负责：

- 注册和注销环境
- 记录观测数据
- 获取最新的观测
- 线程安全操作

## 安装要求

项目依赖以下主要库：

- grid2op：电力系统仿真环境
- langchain 和 langgraph：大语言模型工具链和图框架
- lightsim2grid：可选的高速后端（推荐）
- 其他依赖：numpy, typing, json 等

## 使用方法

项目的使用流程如下：

1. 创建并注册 Grid2op 环境
2. 配置大语言模型（如 Moonshot 或 OpenAI）
3. 构建 ReAct Agent
4. 与代理进行交互，执行电网操作任务

示例代码（基于`test_function_call.ipynb`）：

```python
# 初始化环境
env = grid2op.make("l2rpn_case14_sandbox")
env_manager.register_env("test1", env)
obs = env.reset()
env_manager.record_observation("test1", obs)

# 配置大语言模型
model = ChatOpenAI(
    model='moonshot-v1-8k', 
    openai_api_key='your_api_key', 
    openai_api_base='https://api.moonshot.cn/v1',
    temperature=0
)

# 配置工具
tools = [
    # 动作创建工具
    create_gen_set_bus,
    create_load_set_bus,
    # ... 其他工具
    
    # 观测获取工具
    get_observation,
    get_topology_snapshot
]

# 创建 ReAct 代理
graph = create_react_agent(model, tools=tools)

# 与代理交互
inputs = {"messages": [("user", """
请执行以下电网操作任务，并描述每一步你的思路：
1. 先获取"test1"环境中所有发电机的当前发电功率。
2. 将0号发电机的发电功率增加2.5MW。
3. 操作完成后，再次获取环境的状态，并分析变化。
""")]}

for s in graph.stream(inputs, stream_mode="values"):
    message = s["messages"][-1]
    if isinstance(message, tuple):
        print(message)
    else:
        message.pretty_print()
```

## 典型应用场景

该系统可以处理的典型任务包括：

1. **电网状态监控**：获取和分析电网中的电力潮流和拓扑结构
2. **发电机调度优化**：通过调整发电机的输出功率，优化系统运行
3. **拓扑结构重构**：通过修改线路和设备的连接状态，改变电网拓扑
4. **应急操作规划**：在面对故障或紧急情况时，规划和执行应急操作
5. **多步操作序列**：执行复杂的多步骤操作序列，以达到特定目标

## 扩展与定制

项目可通过以下方式进行扩展：

1. **添加新工具**：在 `tools/grid2op_tools.py` 中定义新的工具函数
2. **支持更多环境**：扩展系统以支持更多 Grid2op 环境和场景
3. **优化提示工程**：完善与 LLM 的提示工程，提高控制效果
4. **集成前端界面**：为系统添加图形用户界面，方便直观交互

## 项目结构

```
.
├── actions
│   └── wrapper.py          # 动作包装器
├── global_context.py       # 全局环境管理器实例
├── logs                    # 日志目录
├── observations
│   └── provider.py         # 观测数据提供者
├── registry_object.py      # 环境注册和管理类
├── src
│   └── utils
│       └── __init__.py     # 日志工具
├── test_function_call.ipynb # 测试用的主程序
└── tools
    └── grid2op_tools.py    # 工具函数库
```

## 注意事项

- 确保在使用前正确配置 API 密钥和环境设置
- 对于计算密集型任务，建议使用 lightsim2grid 后端以提高性能
- 当前实现主要针对 Grid2op 的 l2rpn_case14_sandbox 环境进行了测试
- 执行某些电网操作可能导致仿真环境中的停电或其他应急事件

## 致谢

本项目基于以下开源技术：
- [Grid2op](https://github.com/rte-france/Grid2op)
- [LangChain](https://github.com/langchain-ai/langchain)
- [LangGraph](https://github.com/langchain-ai/langgraph)

