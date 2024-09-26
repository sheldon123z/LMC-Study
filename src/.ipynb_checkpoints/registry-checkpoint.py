# 在脚本的顶层定义 env_registry 作为全局变量
env_registry = {}

# 函数中引用该全局变量
def env_register(env_id, env):
    global env_registry  # 声明使用全局变量
    env_registry[env_id] = env