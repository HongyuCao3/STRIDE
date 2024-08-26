import sys, os
import gym
from typing import List, Optional
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
        
class CartPole(BaseEnv):
    def __init__(self, env_param):
        self.name = "cart_pole"
        self.required_agents = ["controller"]
        self.env_param = env_param
        
        # TODO: 等待设置具体参数
        
        self.proposal = {0, 1} 
        # agents can make choice in the set
        self.reset()
        
    def get_description(self, agent_role=None):
        assert agent_role == "controller"
        description = "Now you are going to play in a cart pole problem, with "
            # TODO: 设计描述
        return description
    
    def reset(self):
        # TODO: 根据cartpole重置状态
        self.state = State(time_step=1, cur_agent="controller", actions=self.proposal)
        self.is_done = False
    
    def step(self, action):
        # TODO: 根据action更新状态
        pass
    
     
if __name__ == "__main__":
    env = CartPole()
    state = env.state
    print(state.textual_descript)
    
    while not env.is_done:
        action = input("What is your decision\n")
        if env.state.actions == {0,1}:
            # TODO: 获取当前pole的状态
            pass
        state = env.step(action)