import os, getpass

def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")
        key = os.environ.get(var)
        print(f"{key}")
    else:
        key = os.environ.get(var)
        print(f"{var}:{key}")