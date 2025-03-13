import copy
from typing import Dict, Literal, Any
import json

from gymnasium import Env
from gymnasium.spaces import Discrete, MultiDiscrete, Box

import grid2op
from grid2op.gym_compat import GymEnv, BoxGymObsSpace, DiscreteActSpace, BoxGymActSpace, MultiDiscreteActSpace
from lightsim2grid import LightSimBackend


class Grid2opEnvWrapper(Env):
    def __init__(self,
                 env_config: Dict[Literal["backend_cls",
                                          "backend_options",
                                          "env_name",
                                          "env_is_test",
                                          "obs_attr_to_keep",
                                          "act_type",
                                          "act_attr_to_keep"],
                                  Any] = None):
        super().__init__()
        if env_config is None:
            env_config = {}

        # handle the backend
        backend_cls = LightSimBackend
        if "backend_cls" in env_config:
            backend_cls = env_config["backend_cls"]
        backend_options = {}
        if "backend_options" in env_config:
            backend_options = env_config["backend_options"]
        backend = backend_cls(**backend_options)

        # create the grid2op environment
        env_name = "l2rpn_case14_sandbox"
        if "env_name" in env_config:
            env_name = env_config["env_name"]
        if "env_is_test" in env_config:
            is_test = bool(env_config["env_is_test"])
        else:
            is_test = False
        self._g2op_env = grid2op.make(env_name, backend=backend, test=is_test)
        # NB by default this might be really slow (when the environment is reset)
        # see https://grid2op.readthedocs.io/en/latest/data_pipeline.html for maybe 10x speed ups !
        # TODO customize reward or action_class for example !

        # create the gym env (from grid2op)
        self._gym_env = GymEnv(self._g2op_env)

        # customize observation space
        obs_attr_to_keep = ["rho", "p_or", "gen_p", "load_p"]
        if "obs_attr_to_keep" in env_config:
            obs_attr_to_keep = copy.deepcopy(env_config["obs_attr_to_keep"])
        self._gym_env.observation_space.close()
        self._gym_env.observation_space = BoxGymObsSpace(self._g2op_env.observation_space,
                                                         attr_to_keep=obs_attr_to_keep
                                                         )
        # export observation space for the Grid2opEnv
        self.observation_space = Box(shape=self._gym_env.observation_space.shape,
                                     low=self._gym_env.observation_space.low,
                                     high=self._gym_env.observation_space.high)

        # customize the action space
        act_type = "discrete"
        if "act_type" in env_config:
            act_type = env_config["act_type"]

        self._gym_env.action_space.close()
        if act_type == "discrete":
            # user wants a discrete action space
            act_attr_to_keep =  ["set_line_status_simple", "set_bus"]
            if "act_attr_to_keep" in env_config:
                act_attr_to_keep = copy.deepcopy(env_config["act_attr_to_keep"])
            self._gym_env.action_space = DiscreteActSpace(self._g2op_env.action_space,
                                                          attr_to_keep=act_attr_to_keep)
            self.action_space = Discrete(self._gym_env.action_space.n)
        elif act_type == "box":
            # user wants continuous action space
            act_attr_to_keep =  ["redispatch", "set_storage", "curtail"]
            if "act_attr_to_keep" in env_config:
                act_attr_to_keep = copy.deepcopy(env_config["act_attr_to_keep"])
            self._gym_env.action_space = BoxGymActSpace(self._g2op_env.action_space,
                                                        attr_to_keep=act_attr_to_keep)
            self.action_space = Box(shape=self._gym_env.action_space.shape,
                                    low=self._gym_env.action_space.low,
                                    high=self._gym_env.action_space.high)
        elif act_type == "multi_discrete":
            # user wants a multi-discrete action space
            act_attr_to_keep = ["one_line_set", "one_sub_set"]
            if "act_attr_to_keep" in env_config:
                act_attr_to_keep = copy.deepcopy(env_config["act_attr_to_keep"])
            self._gym_env.action_space = MultiDiscreteActSpace(self._g2op_env.action_space,
                                                               attr_to_keep=act_attr_to_keep)
            self.action_space = MultiDiscrete(self._gym_env.action_space.nvec)
        else:
            raise NotImplementedError(f"action type '{act_type}' is not currently supported.")
            
            
    def reset(self, seed=None, options=None):
        # use default _gym_env (from grid2op.gym_compat module)
        # NB: here you can also specify "default options" when you reset, for example:
        # - limiting the duration of the episode "max step"
        # - starting at different steps  "init ts"
        # - study difficult scenario   "time serie id"
        # - specify an initial state of your grid "init state"
        return self._gym_env.reset(seed=seed, options=options)
        
    def step(self, action):
        # use default _gym_env (from grid2op.gym_compat module)
        return self._gym_env.step(action)
        


from stable_baselines3 import PPO
'''
env_config = {"env_name": "l2rpn_idf_2023",
               "env_is_test": True,
               "act_type": "box",
              }
'''
gym_env = Grid2opEnvWrapper()
sb3_algo = PPO("MlpPolicy", gym_env, verbose=0)

sb3_algo.learn(total_timesteps=1024)


from grid2op.Agent import BaseAgent
from grid2op.Runner import Runner

class Grid2opAgentWrapper(BaseAgent):
    def __init__(self,
                 gym_env: Grid2opEnvWrapper,
                 trained_agent: PPO):
        self.gym_env = gym_env
        BaseAgent.__init__(self, gym_env._gym_env.init_env.action_space)
        self.trained_agent = trained_agent
        
    def act(self, obs, reward, done):
        # you can customize it here to call the NN policy `trained_agent`
        # only in some cases, depending on the observation for example
        gym_obs = self.gym_env._gym_env.observation_space.to_gym(obs)
        gym_act, _states = self.trained_agent.predict(gym_obs, deterministic=True)
        grid2op_act = self.gym_env._gym_env.action_space.from_gym(gym_act)
        return grid2op_act
    
    def seed(self, seed):
        # implement the seed function
        if seed is None:
            return
        seed_int = int(seed)
        if seed_int != seed:
            raise RuntimeError("Seed must be convertible to an integer")
        self.trained_agent.set_random_seed(seed_int)


my_agent = Grid2opAgentWrapper(gym_env, sb3_algo)
runner = Runner(**gym_env._g2op_env.get_params_for_runner(),
                agentClass=None,
                agentInstance=my_agent)

nb_episode_test = 2
seeds_test_env = (0, 1)    # same size as nb_episode_test
seeds_test_agent = (3, 4)  # same size as nb_episode_test
ts_ep_test =  (0, 1)       # same size as nb_episode_test
res = runner.run(nb_episode=nb_episode_test,
                 env_seeds=seeds_test_env,
                 agent_seeds=seeds_test_agent,
                 episode_id=ts_ep_test,
                 add_detailed_output=True
                 )
for _, chron_id, cum_reward, nb_time_step, max_ts, _ in res:
    msg_tmp = "\tFor chronics with id {}\n".format(chron_id)
    msg_tmp += "\t\t - cumulative reward: {:.6f}\n".format(cum_reward)
    msg_tmp += "\t\t - number of time steps completed: {:.0f} / {:.0f}".format(nb_time_step, max_ts)
    print(msg_tmp)
