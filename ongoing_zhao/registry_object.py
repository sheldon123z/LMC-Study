import threading
from typing import Any
from contextlib import contextmanager
from collections import defaultdict, deque

class EnvironmentManager:
    def __init__(self):
        self._envs = {}
        self._observations = defaultdict(lambda: deque(maxlen=1000))
        self._lock = threading.RLock()
    
    @contextmanager
    def register_env(self, env_id: str, env: Any):
        """上下文管理方式注册环境"""
        with self._lock:
            if env_id in self._envs:
                raise RuntimeError(f"Environment {env_id} already registered")
            self._envs[env_id] = env
        try:
            yield  # 在此代码块内环境有效
        except Exception as e:
            raise e  # 如果有错误发生，重新抛出
        # 删除 finally 部分，移除自动注销环境
        # finally:
        #     self.deregister_env(env_id)  # 不再自动注销环境

    def deregister_env(self, env_id: str) -> None:
        with self._lock:
            del self._envs[env_id]
            del self._observations[env_id]

    def record_observation(self, env_id: str, obs: Any) -> None:
        with self._lock:
            if env_id not in self._envs:
                raise KeyError(f"Environment {env_id} not found")
            self._observations[env_id].append(obs)

    def get_latest_obs(self, env_id: str) -> Any:
        with self._lock:
            return self._observations[env_id][-1] if self._observations[env_id] else None
