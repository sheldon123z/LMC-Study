from typing import *
import json

# 封装消息生成函数
def create_message(content: str) -> List[Dict[str, str]]:
    """
    创建消息。
    """
    # 和模型对话发送信息
    messages = [
        {"role": "system",
         "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手。"},
        {"role": "user", "content": content}  # 用户输入
    ]
    return messages

# 消息处理函数，将大模型的函数调用以及执行进行封装
def process_tool_calls(client, tool_map, llm_model, tools: List[Dict[str, Any]], messages: List[Dict[str, str]]) -> str:
    """
    处理工具调用。

    函数的主要目的是根据工具映射和工具列表中的信息，调用相应的工具对象，并处理返回的结果。
    最后，函数将返回一个字符串，表示处理结果。

    Args:
        client (_type_): 客户端对象，用于与后端服务进行通信。
        tool_map (_type_): 工具映射，将工具名称映射到相应的工具对象。
        tools (List[Dict[str, Any]]): 工具列表，包含要处理的工具调用信息。
        messages (List[Dict[str, str]]): 消息列表，包含与工具调用相关的消息。

    Returns:
        str: 处理结果，表示工具调用是否成功以及相应的结果信息。
    """

    finish_reason = None
    i = 0
    # 向大模型发送指令和工具集合
    model = llm_model
    while finish_reason is None or finish_reason == "tool_calls":
        completion = client.chat.completions.create(
            model= model,
            messages=messages,
            temperature=0.3,
            tools=tools,  # 提交定义好的工具
        )
        # 得到回复后提取finish_reason,并检查是否是工具调用
        choice = completion.choices[0]
        finish_reason = choice.finish_reason
        
        if finish_reason == "tool_calls":  # 判断是否有工具调用
            print(f"函数进行了调用finish_reason={finish_reason} \n")
            messages.append(choice.message)  # 添加工具调用消息到上下文
            for tool_call in choice.message.tool_calls:  # 处理多个工具调用
                tool_call_name = tool_call.function.name
                print(f"执行序号：[{i}] 调用工具名称：{tool_call_name}\n")
                if choice.message.content:
                    print(f"执行序号：[{i}] 模型解释工具调用原因: {choice.message.content}\n")
                tool_call_arguments = json.loads(tool_call.function.arguments)
                print(f"执行序号：[{i}] 函数调用返回参数tool_call_arguments： {tool_call_arguments}\n")
                tool_function = tool_map[tool_call_name]
                
                # 这里将模型给出的函数参数传递到调用的函数中进行函数执行
                print(f"执行序号：[{i}] 正在执行tool_function：{tool_function.__name__}\n")
                tool_result = tool_function(tool_call_arguments)
                print(f"执行序号：[{i}] 执行结果tool_result： {tool_result}\n")
                i+=1 # 显示执行次数
                
                # 判断工具调用的结果并生成消息
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_call_name,
                    "content": json.dumps(tool_result), # <-- 我们约定使用字符串格式向大模型提交工具调用结果，因此在这里使用 json.dumps 将执行结果序列化成字符串
                        })

                # 也可以手动设置其他的原因来遮盖失败的实际问题
                # if tool_result["status"] == "success":
                #     messages.append({
                #         "role": "tool",
                #         "tool_call_id": tool_call.id,
                #         "name": tool_call_name,
                #         "content": json.dumps(tool_result),
                #     })
                # elif tool_result["status"] == "failure":
                #     messages.append({
                #         "role": "tool",
                #         "tool_call_id": tool_call.id,
                #         "name": tool_call_name,
                #         "content": json.dumps({"status": "failure", "message": tool_result["message"]}),
                #     })
                # else:
                #     messages.append({
                #         "role": "tool",
                #         "tool_call_id": tool_call.id,
                #         "name": tool_call_name,
                #         "content": json.dumps({"status": "Unknown", "message": tool_result["message"]}),
                #     })

    # print(choice.message.content)  # 输出模型生成的最终回复
    return choice.message.content