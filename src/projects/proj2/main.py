#!/usr/bin/env python3

################################################################
## DO NOT MODIFY THIS FILE!
##
## If your agent and evaluation function are written correctly,
## then this file will work without issue.
##
## If you would like to run other tests, place it in a
## separate file and run it there.
################################################################

from ...lib.game import Game, RandomAgent
import sys
from . import agent, evaluation


def run_game(args):
    game_type = None
    agents = []

    if args.game == 'discrete_soccer':
        from ...lib.game import discrete_soccer
        game_type = discrete_soccer.DiscreteSoccer()
        my_agent = agent.MinimaxAgent(
            evaluation.soccer,
            alpha_beta_pruning=args.ab_pruning,
            max_depth=args.max_depth
        )
        if args.interactive:
            iagent = discrete_soccer.InteractiveAgent()
            agents = [iagent, my_agent]
        else:
            agents = [my_agent, my_agent]
    elif args.game == 'connect_four':
        from ...lib.game import connect_four
        game_type = connect_four.Connect4()
        my_agent = agent.MinimaxAgent(
            evaluation.connect_four,
            alpha_beta_pruning=args.ab_pruning,
            max_depth=args.max_depth
        )
        if args.interactive:
            iagent = connect_four.InteractiveAgent()
            agents = [iagent, my_agent]
        else:
            agents = [my_agent, my_agent]
    else:
        sys.exit("An invalid game type was provided.")

    game = Game(game_type, agents)
    game.run(play_again='query', speed=0)


def main(cl_args):
    import argparse

    parser = argparse.ArgumentParser(description='Main function for Project 2: Minimax, Alpha-Beta Game Tree Search and Reinforcement Learning.')
    parser.add_argument('--max_depth', type=int, default=5, help='The maximum depth that minimax should search.')
    parser.add_argument('--ab_pruning', action='store_true', help='If included, use alpha-beta pruning.')
    parser.add_argument('--game', type=str, default='discrete_soccer', \
                        help='Game to play. (default: discrete_soccer)\n Options: discrete_soccer, connect_four')
    parser.add_argument('--interactive', action='store_true', default=False, \
                        help='If included, a human player will be able to join the game.')

    args = parser.parse_args(cl_args)

    run_game(args)


if __name__ == '__main__':
    main([])
