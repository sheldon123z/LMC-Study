import sys
import os

# 获取当前脚本所在目录的上级目录路径
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 将上级目录路径添加到sys.path
sys.path.append(parent_dir)

import grid2op
from src.utils import get_logger
from grid2op.PlotGrid import PlotMatplot
from grid2op.Action import PlayableAction
from grid2op.Parameters import Parameters
from src.utils.process_json import load_json, save_json
from process_message import process_tool_calls, create_message
from tool_map import tool_map
from openai import OpenAI
from registry import env_registry, env_register

# 设置日志记录器
logger = get_logger(__name__)

try:
    from lightsim2grid import LightSimBackend
    bk_cls = LightSimBackend
    logger.info("成功导入 LightSimBackend 用于更快的后端计算。")
except ImportError as exc:
    logger.warning(f"导入 LightSimBackend 时发生错误：{exc}，将使用 PandaPowerBackend 作为后备方案。")
    from grid2op.Backend import PandaPowerBackend
    bk_cls = PandaPowerBackend

# 主流程
if __name__ == "__main__":
    logger.info("主流程开始执行。")

    # 初始化参数
    param = Parameters()
    logger.info("参数初始化完成。")

    # 初始化OpenAI客户端
    try:
        client = OpenAI(
            api_key="sk-8e3a75c3f4f54d9c9fd7dd779dcd80a8",  # deepseek api
            base_url="https://api.deepseek.com"  # 使用 deepseek 模型
        )
        logger.info("OpenAI 客户端初始化成功，已连接到 DeepSeek API。")
    except Exception as e:
        logger.error(f"OpenAI 客户端初始化失败，错误信息：{e}")
        sys.exit(1)

    # 设置模型和最大迭代次数
    model_moonshot = "moonshot-v1-8k"
    model_deepseek = "deepseek-chat"
    max_iter = 20
    logger.info(f"模型和最大迭代次数设置完成，模型: {model_deepseek}，最大迭代次数: {max_iter}。")

    # 设置环境
    env_name = "l2rpn_case14_sandbox"
    try:
        env = grid2op.make(env_name, action_class=PlayableAction, param=param, backend=bk_cls())
        logger.info(f"环境 '{env_name}' 创建成功，使用后端: {bk_cls.__name__}。")
    except Exception as e:
        logger.error(f"创建环境 '{env_name}' 失败，错误信息：{e}")
        sys.exit(1)

    # 生成唯一环境标识符并注册
    env_id = "test1"
    try:
        env_register(env_id, env)
        logger.info(f"环境 '{env_id}' 注册成功。")
    except Exception as e:
        logger.error(f"注册环境 '{env_id}' 失败，错误信息：{e}")
        sys.exit(1)

    # 创建要发送的消息
    try:
        messages = create_message("""请你使用我提供给你的工具,首先画出env_id为"test1"的状态观测图，一共有6个发电机，编号从0到5
                                  然后将1号发电机功率提升10Mw，再然后画出当前环境id为'test1'的状态观测图。
                                  然后请你再把除了发电机1,2，3，4以外所有的发电机的功率降低5Mw，请你一次只调控一个发电机，
                                  此外如果有多个工具调用，
                                  请你在每次调用一次工具后都画出当前环境id为'test1'的状态观测图。
                                  ，如果有任何一步失败，请你告诉我详细的失败原因是什么,
                                  后告知我调用的原因""")
        logger.info("消息内容创建成功。")
    except Exception as e:
        logger.error(f"创建消息失败，错误信息：{e}")
        sys.exit(1)

    # 加载工具
    try:
        tools = load_json('tools.json')
        logger.info("工具信息加载成功。")
    except Exception as e:
        logger.error(f"加载工具信息失败，错误信息：{e}")
        sys.exit(1)

    # 调用工具处理函数
    try:
        final_response = process_tool_calls(client, tool_map, model_deepseek, tools, messages, temperature=0.15)
        logger.info("工具调用成功，已处理所有工具调用逻辑。")
        logger.info(f"模型的最终回复：\n{final_response}")
    except Exception as e:
        logger.error(f"处理工具调用时发生错误，错误信息：{e}")
        sys.exit(1)