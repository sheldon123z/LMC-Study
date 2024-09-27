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