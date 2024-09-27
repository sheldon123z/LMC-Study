import grid2op
from grid2op.PlotGrid import PlotMatplot
from grid2op.Action import PlayableAction
from grid2op.Parameters import Parameters

from typing import List, Dict, Any
import matplotlib
import matplotlib.pyplot as plt 

import uuid
import json

from process_message import process_tool_calls, create_message
from tool_map import tool_map
from openai import OpenAI
from registry import env_registry, env_register
from utils.process_json import load_json,save_json

try:
    from lightsim2grid import LightSimBackend
    bk_cls = LightSimBackend
except ImportError as exc:
    print(f"Error: {exc} when importing faster LightSimBackend")
    from grid2op.Backend import PandaPowerBackend
    bk_cls = PandaPowerBackend

# 主流程
if __name__ == "__main__":
    param = Parameters()
    client = OpenAI(
    # api_key="sk-QbYev6PjK70x6wgkje6hnKiN2mnUiIY1zIy4H26RDXkOAluG", # 在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
    # base_url="http://127.0.0.1:9988/v1", #用于moonpalace检测 使用moonpalace先启动检测服务器
    # base_url="https://api.moonshot.cn/v1", # 月之暗面api
    
    api_key = "sk-8e3a75c3f4f54d9c9fd7dd779dcd80a8", # deepseek api
    base_url = "https://api.deepseek.com", #需要修改deepseek的模型
)
    model_moonshot = "moonshot-v1-8k"
    model_deepseek = "deepseek-chat"
    max_iter = 20  # to save time we only assess performance on 30 iterations
    env_name = "l2rpn_case14_sandbox"
    env = grid2op.make(env_name, 
                        action_class=PlayableAction,
                        param=param,
                        backend=bk_cls())

    # 生成一个唯一的环境标识符（如UUID）
    env_id = "test1"   # 只需要这个标识符与环境绑定
    env_register(env_id, env) # 注册环境

    # 创建要发送的消息
    messages = create_message("""请你使用我提供给你的工具,首先画出env_id为"test1"的状态观测图，
                              然后将1号发电机功率提升10Mw，再然后画出当前环境id为'test1'的状态观测图。一共有6个发电机，
                                然后请你再把除了发电机2，3，4以外所有的发电机的功率降低5Mw，请你一次只调控一个发电机，
                                此外注意发电机序号是从0开始的，如果有多个工具调用，
                                请你在每次调用一次工具后都画出当前环境id为'test1'的状态观测图。
                              ，如果有任何一步失败，请你告诉我详细的失败原因是什么,
                              后告知我调用的原因""")

    tools = load_json('tools.json')
    # 调用封装的工具处理函数
    final_response = process_tool_calls(client,tool_map, model_deepseek, tools, messages)
    
    print(f"模型的最终回复：\n{final_response}")

 