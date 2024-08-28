import sys, os

import argparse
import numpy as np
from datetime import datetime
from env import CartPole
from program_agent import CPAgent
from utils import Logger
from envs.env_helper import get_env_param

def play_through(game, agents, logger,):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--game', type=str, default="cart_pole")
    parser.add_argument('--mdp_known', type=bool, default=True)
    parser.add_argument('--random_param', type=bool, default=True)
    args = parser.parse_args()
    logger_output_path = "envs/cartpole/outputs/"
    os.makedirs(logger_output_path, exist_ok=True)
    now = datetime.now()
    time_string = now.strftime('%Y%m%d%H%M%S')
    logger = Logger(logger_output_path + args.game + "-" + time_string + ".html", verbose=True, writeToFile=False)
    exmps_output_path = "envs/cartpole/prompts/"
    os.makedirs(exmps_output_path, exist_ok=True) 
    exmps_file = exmps_output_path + "cart_pole_exmps_"+time_string+".txt"
    
    ### initialize game and agents ###
    env_param = get_env_param(env_name="tabular_mdp", random_param=args.random_param)
    game = CartPole(env_param=env_param)
    working_memory = {"P":game.P, "R":game.R, "nState":game.nState, "nAction":game.nAction, "epLen":game.epLen,
                      "V": np.zeros((game.epLen,game.nState)),
                      "Q": np.zeros((game.epLen,game.nState,game.nAction)),
                      }
    agent = CPAgent(
        working_memory=working_memory,
        exmps_file=exmps_file
    )
    agents= {"agent": agent}
    play_through(game=game, agents=agents, logger=logger)