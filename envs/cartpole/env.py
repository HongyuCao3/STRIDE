import sys, os
import numpy as np
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
    def __init__(self, env_param,buckets=(1, 1, 6, 12), n_episodes=1000, min_lr=0.1, min_epsilon=0.1,
                 gamma=1.0, decay=25):
        self.name = "cart_pole"
        self.required_agents = ["controller"]
        self.buckets = buckets  # Discretization buckets
        self.n_episodes = n_episodes  # Number of training episodes
        self.min_lr = min_lr  # Minimum learning rate
        self.min_epsilon = min_epsilon  # Minimum exploration rate
        self.gamma = gamma  # Discount factor
        self.decay = decay  # Decay rate for exploration
        self.Q = np.zeros(self.buckets + (self.env.action_space.n,))  # Initialize Q-table

        # agents can make choice in the set
        self.reset()
        self.description_of_problem_class=description_of_problem_class
        
    def get_description(self, agent_role=None):
        assert agent_role == "controller"
        if self.nState <= 10 and self.nAction <= 10 and self.epLen <= 10:
            P_str = np.array2string(self.P, precision=2, floatmode='fixed')
            R_str = np.array2string(self.R[:,:,0], precision=2, floatmode='fixed')
        else:
            P_str = "stored in working memory. Full matrix is too large to be printed in context history."
            R_str = "stored in working memory. Full matrix is too large to be printed in context history."
        description = "Now you are going to play in a finite-horizon cartpole decision process"
        return description
    
    def discretize(self, obs):
        """Discretize continuous state into discrete buckets."""
        upper_bounds = [
            self.env.observation_space.high[0],
            0.5,
            self.env.observation_space.high[2],
            np.radians(50)
        ]
        lower_bounds = [
            self.env.observation_space.low[0],
            -0.5,
            self.env.observation_space.low[2],
            -np.radians(50)
        ]
        ratios = [(obs[i] + abs(lower_bounds[i])) / (upper_bounds[i] - lower_bounds[i]) for i in range(len(obs))]
        new_obs = [int(round((self.buckets[i] - 1) * ratios[i])) for i in range(len(obs))]
        new_obs = [min(self.buckets[i] - 1, max(0, new_obs[i])) for i in range(len(obs))]
        return tuple(new_obs)
    
    def reset(self):
        # TODO: 根据cartpole重置状态
        self.state = State(time_step=1, cur_agent="controller", actions=self.proposal)
        self.is_done = False
    
    def update_q(self, state, action, reward, new_state, alpha):
        """Update Q-value using the Q-learning update rule."""
        best_q = np.max(self.Q[new_state])
        self.Q[state][action] += alpha * (reward + self.gamma * best_q - self.Q[state][action])

    def get_epsilon(self, t):
        """Calculate decaying epsilon."""
        return max(self.min_epsilon, min(1, 1.0 - np.log10((t + 1) / self.decay)))

    def get_alpha(self, t):
        """Calculate decaying learning rate."""
        return max(self.min_lr, min(0.5, 1.0 - np.log10((t + 1) / self.decay)))
    
     
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