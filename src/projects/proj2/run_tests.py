from lib import cli
from lib.game import Game, RandomAgent, discrete_soccer, connect_four
import sys
import agent, evaluation

import sys

from file_io import save_values
from multiprocessing import Manager, Lock, Process

game_module = {
    'discrete_soccer': discrete_soccer,
    'connect_four': connect_four
}
evaluations = {
    'discrete_soccer': evaluation.soccer,
    'connect_four': evaluation.connect_four
}

def run_main_game(args):
    agents = []

    if not args.game in game_module:
        sys.exit("Invalid game choice! Please choose from among: {}".format(game_module.keys()))

    gm = game_module[args.game]
    evaluation_fn = evaluations[args.game]

    computer_agent = None
    if args.search_method == "minimax":
        computer_agent = agent.MinimaxAgent(
            evaluation_fn,
            args.ab_pruning,
            args.max_depth
        )
    elif args.search_method == "monte_carlo":
        computer_agent = agent.MonteCarloAgent(
            evaluation_fn,
            args.max_playouts
        )
    if computer_agent is None:
        print("Invalid search method")
        exit(0)
    
    agents = [computer_agent, computer_agent]

    game = Game(gm.generator(), agents, display=False)
    
    return game.run(play_again='query', speed=2)

def set_up_game_and_run(search_method,
                        max_depth,
                        ab_pruning,
                        max_playouts,
                        game,
                        interactive,
                        lock):
    import argparse

    parser = argparse.ArgumentParser(description='Main function for Project 2: Minimax, Alpha-Beta, Monte Carlo Game Tree Search and Reinforcement Learning.')
    parser.add_argument('--search_method', type=str, default=search_method,
                        help='Game tree search method to use. (default: minimax)\n Options: minimax, monte_carlo')
    parser.add_argument('--max_depth', type=int, default=max_depth, help='The maximum depth that minimax should search.')
    parser.add_argument('--ab_pruning', action='store_true', default=ab_pruning, help='If included, use alpha-beta pruning.')
    parser.add_argument('--max_playouts', type=int, default=max_playouts, help='The maximum number of playouts that Monte Carlo should perform.')
    parser.add_argument('--game', type=str, default=game, \
                        help='Game to play. (default: discrete_soccer)\n Options: discrete_soccer, connect_four')
    parser.add_argument('--interactive', action='store_true', default=interactive, \
                        help='If included, a human player will be able to join the game.')

    args = parser.parse_args([])

    #Run a game and collect stats
    stat_dictionary = run_main_game(args)

    lock.acquire()
    #Save the statistics into excel spreadsheets
    if (search_method == 'minimax' and ab_pruning==True):
        stat_dictionary["depth"] = max_depth
        save_values(stat_dictionary, "prune")
    elif (search_method == 'minimax' and ab_pruning==False):
        stat_dictionary["depth"] = max_depth
        save_values(stat_dictionary, search_method)
    elif (search_method == 'monte_carlo'):
        stat_dictionary["playouts"] = max_playouts
        save_values(stat_dictionary, search_method)
    lock.release()


search_methods = ['prune', 'monte_carlo']
# search_methods = ['minimax', 'prune', 'monte_carlo']
max_depths = [1, 2, 3, 4]
max_playouts = [10, 25, 50, 75, 100]

num_tests = 25

def main():

    for search_method in search_methods:
        if (search_method == 'minimax'):

            for depth in max_depths:
                with Manager() as manager:
                    all_processes = []
                    lock = manager.Lock()
                    for test in range(0, num_tests):
                        process = Process(target=set_up_game_and_run, args=(
                                            'minimax',
                                            depth,
                                            False, 
                                            1,
                                            'discrete_soccer',
                                            False,
                                            lock
                                         ))
                        all_processes.append(process)
                    
                    #Start all of the subprocesses
                    for process in all_processes:
                        process.start()

                    #Wait for all subprocesses to finish before continuing
                    for process in all_processes:
                        process.join()

        elif search_method == 'prune':
            for depth in max_depths:
                with Manager() as manager:
                    all_processes = []
                    lock = manager.Lock()
                    for test in range(0, num_tests):
                        process = Process(target=set_up_game_and_run, args=(
                                            'minimax',
                                            depth,
                                            True, 
                                            1,
                                            'discrete_soccer',
                                            False,
                                            lock
                                         ))
                        all_processes.append(process)
                    
                    #Start all of the subprocesses
                    for process in all_processes:
                        process.start()

                    #Wait for all subprocesses to finish before continuing
                    for process in all_processes:
                        process.join()
        elif search_method == 'monte_carlo':

            for playout in max_playouts:
                with Manager() as manager:
                    all_processes = []
                    lock = manager.Lock()
                    for test in range(0, num_tests):
                        process = Process(target=set_up_game_and_run, args=(
                                            'monte_carlo',
                                            1,
                                            False, 
                                            playout,
                                            'discrete_soccer',
                                            False,
                                            lock
                                         ))
                        all_processes.append(process)
                    
                    #Start all of the subprocesses
                    for process in all_processes:
                        process.start()

                    #Wait for all subprocesses to finish before continuing
                    for process in all_processes:
                        process.join()

if __name__ == '__main__':
    main()
