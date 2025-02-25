import json
import os

def load_json(file_path):
    """
    加载 JSON 文件并将其转化为 Python 数据结构（通常是 dict 或 list）。
    
    :param file_path: JSON 文件的路径
    :return: 返回加载后的 Python 数据结构（dict 或 list）
    :raises: FileNotFoundError 如果文件不存在，或 ValueError 如果解析失败
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件 {file_path} 不存在。")
    
    with open(file_path, 'r', encoding='utf-8') as json_file:
        try:
            data = json.load(json_file)
            return data
        except json.JSONDecodeError as e:
            raise ValueError(f"解析 JSON 文件失败：{e}")

def save_json(data, file_path):
    """
    将 Python 数据结构保存为 JSON 文件。
    
    :param data: Python 数据结构（通常是 dict 或 list）
    :param file_path: 保存 JSON 文件的路径
    :raises: TypeError 如果数据不是可序列化为 JSON 的类型
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except TypeError as e:
        raise ValueError(f"无法将数据保存为 JSON 格式：{e}")