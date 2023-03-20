#!/usr/bin/env python3

import math, random
from lib.game import discrete_soccer, connect_four


#The main evaluation function that is used in the soccer game
def soccer(state, player_id):
    #Case where a win/loss is detected in the game
    if (state.is_terminal != None):
        #If the winning team did not belong to the "current" player
        #Indicating the player who just played won the game
        if (state.is_terminal != state.objects[player_id].team):
            return 10
        
        #If the winning team does belong to the current player.
        #Indicating that the player who just played lost the game
        elif (state.is_terminal == state.objects[player_id].team):
             return -10

    #Case where the current player has the ball
    elif (state.objects[player_id] == state.player_with_ball):
        #Get position of the current's player's goal
        curr_goal = curr_player_goal(state.objects[player_id], state)

        #Get position of current player
        curr_pos = curr_player_pos(state, player_id)

        #Get position of other player
        other_pos = other_player_pos(state.objects[player_id], state)

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
        #Calc distance between other player and the current player's goal
        dis_other_goal = calculate_distance(
            other_pos[0],
            curr_goal[0],
            other_pos[1],
            curr_goal[1]
        )

        #If the other player is not inbetween the current player and its goal.
        #Basically, the current player is free to go to its goal.
        if (dis_other_goal > dis_curr_other):
            #Return the minimum distance between current player and goal
            return (5/dis_curr_goal)
        else:
            #Else, take the other player into account
            return 0.75*((5/dis_curr_goal) - (dis_curr_goal))


    #Case where neither player has the ball.
    elif (state.objects[0].has_ball == False and state.objects[1].has_ball == False):
        player_pos = curr_player_pos(state, player_id)

        #Calculate distance between the current player's position and the ball's position
        dis = calculate_distance(player_pos[0], 
                                 state.objects[2].x,
                                 player_pos[1],
                                 state.objects[2].y)
        #Try to minimize the distance between current player and the ball
        return 0.5*(1/dis)
    
    #Case where the other player has the ball.
    elif (state.objects[get_other_player_id(player_id)].has_ball):
        #Get position of current player
        curr_pos = curr_player_pos(state, player_id)

        #Calculating the id of the other player.
        other_id = get_other_player_id(player_id)

        #Get position of other player
        other_pos = other_player_pos(state.objects[player_id], state)

        #Get position of the other player's goal.
        other_goal_pos = curr_player_goal(state.objects[other_id], state)
        
        #Calculating the midpoint position between the other player and its goal.
        midpoint_x = (other_pos[0] + other_goal_pos[0]) / 2
        midpoint_y = (other_pos[1] + other_goal_pos[1]) / 2

        #Calculate the distance between the current player
        #and the midpoint.
        dis_curr_midpoint = calculate_distance(
                                curr_pos[0],
                                midpoint_x,
                                curr_pos[1],
                                midpoint_y
                            )
        if (dis_curr_midpoint == 0):
            return 0.5
        
        return 0.25*(1/dis_curr_midpoint)

    # if not isinstance(state, discrete_soccer.SoccerState):
    #     raise ValueError("Evaluation function incompatible with game type.")

def calculate_distance(x1, x2, y1, y2):
    x_term = (x1 - x2) ** 2
    y_term = (y1 - y2) ** 2

    return math.sqrt(x_term + y_term)

def curr_player_goal(player, state):
    #Case where the current player is on the red team
    if (player.team == 1):
        #Return the blue goal position
        return state.red_goal_pos
    #Case where the current player is on the blue team
    else:
        #Return the red goal position
        return state.blue_goal_pos
    
def other_player_pos(player, state):

    #Case where the current player is on the red team
    if (player.team == 1):
        #Return the coords of the playaer on the blue team
        return (state.objects[1].x, state.objects[1].y)
    
    #Case where the current player is on the blue team
    else:
        #Return the coords of the player on the red team
        return (state.objects[0].x, state.objects[0].y)

def curr_player_pos(state, player_id):
    return (state.objects[player_id].x, state.objects[player_id].y)

def get_other_player_id(player_id):
    if (player_id == 0):
        return 1
    else:
        return 0


################################################################################################
#Unused function below
################################################################################################

def connect_four(state, player_id):
    if not isinstance(state, connect_four.Connect4State):
        raise ValueError("Evaluation function incompatible with game type.")
    return 0
