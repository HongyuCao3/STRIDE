import sys, os
import gym
from typing import List, Optional
from pydantic import BaseModel
from envs.env_helper import BaseEnv


gym_env = gym.make('CartPole-v0')

description_of_problem_class="""The CartPole problem is a classic reinforcement learning task where the goal is to balance a pole on a moving cart by applying forces to the cart. The challenge is to keep the pole upright by preventing it from falling over or moving outside of a predefined boundary.

Components:
State Space $S$: ${s = (x, \dot{x}, \theta, \dot{\theta})}$, where $x$ is the cart position, $\dot{x}$ is the cart velocity, $\theta$ is the pole angle, and $\dot{\theta}$ is the pole's angular velocity.
Action Space $A$: ${a_{0}, a_{1}}$, where $a_{0}$ represents applying a force to the left, and $a_{1}$ represents applying a force to the right.
Transition Dynamics: The state transitions are governed by the physics of the cart-pole system, which is influenced by the applied action. The transitions are typically modeled by differential equations that describe the motion of the cart and pole.
Reward: The agent typically receives a reward of +1 for every time step the pole remains upright and within bounds. If the pole falls over or the cart moves out of bounds, the episode ends, and no further rewards are received.
Horizon length $H$: The episode continues until the pole falls, the cart goes out of bounds, or a maximum number of time steps is reached.

Interaction protocol:
For each time step $h=0,1,2,\dots,H$:
- Agent observes the current state $s_h = (x_h, \dot{x}_h, \theta_h, \dot{\theta}_h)$.
- Agent takes an action $a_h \in A$ (applying force to the cart).
- The state transitions to $s_{h+1}$ based on the physical dynamics of the system.
- Agent receives a reward of +1 for keeping the pole balanced.

Goal of the agent:
Maximize the cumulative reward, which corresponds to keeping the pole balanced for as many time steps as possible.
"""

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
        self.description_of_problem_class=description_of_problem_class
        
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