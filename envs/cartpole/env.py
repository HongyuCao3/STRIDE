import sys, os
import gym
from typing import List, Optional,
from pydantic import BaseModel
from envs.env_helper import BaseEnv


gym_env = gym.make('CartPole-v0')

class State(BaseModel):
    time_step: int
    cur_agent: str
    actions: List[int]
    action_schema: List[tuple]
    textual_descript: str
    
    def is_valid_action(self, action):
        if type(action) == int:
            return action
        else:
            print("Illegal action {}.".format(action))
            return False
        

if __name__ == "__main__":
    pass