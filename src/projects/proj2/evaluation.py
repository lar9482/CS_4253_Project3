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

    #Total utility
    utility = 0

    #Case where the current player has the ball
    if (state.current_player_obj == state.player_with_ball):

        #Get position of the current's player's goal
        curr_goal = curr_player_goal(state.current_player_obj, state)

        #Get position of current player
        curr_pos = curr_player_pos(state)

        #Get position of other player
        other_pos = other_player_pos(state.current_player_obj, state)

        #Calc distance between current player and its goal
        dis_curr_goal = calculate_distance(
            curr_pos[0],
            curr_goal[0],
            curr_pos[1],
            curr_goal[1]
        )

        #Calc distance between current player and the other player
        dis_curr_other = calculate_distance(
            curr_pos[0],
            other_pos[0],
            curr_pos[1],
            other_pos[1]
        )

        #Take the sum of distance between goal minus the other player
        utility += (dis_curr_goal) - (dis_curr_other)

    #Case where neither player has the ball.
    if (state.objects[0].has_ball == False and state.objects[1].has_ball == False):
        player_pos = curr_player_pos(state)
        dis = calculate_distance(player_pos[0], 
                                 state.objects[2].x,
                                 player_pos[1],
                                 state.objects[2].y)
        utility += 0.5*(1/dis)
    
    if not isinstance(state, discrete_soccer.SoccerState):
        raise ValueError("Evaluation function incompatible with game type.")
    
    return utility

def calculate_distance(x1, x2, y1, y2):
    x_term = (x1 - x2) ** 2
    y_term = (y1 - y2) ** 2

    return math.sqrt(x_term + y_term)

def curr_player_goal(player, state):
    #Case where the current player is on the red team
    if (player.team == 1):
        #Return the blue goal position
        return state.blue_goal_pos
    #Case where the current player is on the blue team
    else:
        #Return the red goal position
        return state.red_goal_pos
    
def other_player_pos(player, state):

    #Case where the current is on the red team
    if (player.team == 1):
        #Return the coords of the playaer on the blue team
        return (state.objects[1].x, state.objects[1].y)
    else:
        #Return the coords of the player on the red team
        return (state.objects[0].x, state.objects[0].y)

def curr_player_pos(state):
    return (state.current_player_obj.x, state.current_player_obj.y)

def connect_four(state, player_id):
    if not isinstance(state, connect_four.Connect4State):
        raise ValueError("Evaluation function incompatible with game type.")
    return 0
