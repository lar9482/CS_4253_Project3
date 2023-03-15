#!/usr/bin/env python3

import math, random
from lib.game import discrete_soccer, connect_four

def soccer(state, player_id):
    # TODO: Implement this function!
    #
    # The soccer evaluation function *must* look into the game state
    # when running. It will then return a number, where the larger the
    # number, the better the expected reward (or lower bound reward)
    # will be.
    #
    # For a good evaluation function, you will need to
    # SoccerState-specific information. The file
    # `src/lib/game/discrete_soccer.py` provides a description of all
    # useful SoccerState properties.
    
    #Case where neither player has the ball.
    if (state.objects[0].has_ball == False and state.objects[1].has_ball == False):
        dis = calculate_distance(state.current_player_obj, state.objects[2])
        return (1/dis)
        

    if not isinstance(state, discrete_soccer.SoccerState):
        raise ValueError("Evaluation function incompatible with game type.")
    
    return 10

def calculate_distance(object1, object2):
    x_term = (object1.x - object2.x) ** 2
    y_term = (object1.y - object2.y) ** 2

    return math.sqrt(x_term + y_term)

def connect_four(state, player_id):
    if not isinstance(state, connect_four.Connect4State):
        raise ValueError("Evaluation function incompatible with game type.")
    return 0
