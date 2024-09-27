import os
import ast
import json
from typing import Any

def get_python_files(directory):
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def get_functions_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        source = file.read()
    parsed_ast = ast.parse(source, filename=file_path)
    functions = []
    for node in ast.walk(parsed_ast):
        if isinstance(node, ast.FunctionDef):
            functions.append(node)
    return functions

def get_function_info(func_node):
    func_name = func_node.name
    docstring = ast.get_docstring(func_node) or "No description available."
    parameters = []
    for arg in func_node.args.args:
        param_name = arg.arg
        # 获取类型注解
        if arg.annotation:
            param_type = ast.unparse(arg.annotation)
        else:
            param_type = "Any"
        parameters.append({
            "name": param_name,
            "annotation": param_type
        })
    return {
        "name": func_name,
        "description": docstring.strip(),
        "parameters": parameters
    }

def map_type(annotation):
    type_mappings = {
        'int': 'integer',
        'float': 'number',
        'str': 'string',
        'bool': 'boolean',
        'list': 'array',
        'dict': 'object',
        'Any': 'any'
    }
    # 简化处理复杂类型
    if annotation in type_mappings:
        return type_mappings[annotation]
    else:
        return 'any'

def generate_tool_description(func_info):
    tool = {
        "name": func_info["name"],
        "description": func_info["description"],
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }

    for param in func_info["parameters"]:
        param_name = param["name"]
        param_type = map_type(param["annotation"])

        param_description = {
            "type": param_type,
            "description": f"Parameter '{param_name}' of type {param_type}"
        }

        tool["parameters"]["properties"][param_name] = param_description
        tool["parameters"]["required"].append(param_name)

    return tool

def generate_tools_from_files(python_files):
    tools = []
    for file_path in python_files:
        functions = get_functions_from_file(file_path)
        for func_node in functions:
            if func_node.name.startswith('_'):
                continue  # 跳过私有函数
            func_info = get_function_info(func_node)
            tool_description = generate_tool_description(func_info)
            tools.append(tool_description)
    return tools

if __name__ == "__main__":
    directory = './grid2op/Action'  # 替换为您的目录路径
    python_files = get_python_files(directory)
    tools = generate_tools_from_files(python_files)
    with open('tools_from_directory.json', 'w', encoding='utf-8') as f:
        json.dump(tools, f, ensure_ascii=False, indent=4)