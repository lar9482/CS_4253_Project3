#!/usr/bin/env python3

import pygame
## We will use persistent data structures because we want fast
## immutable game states
from pyrsistent import m, v, pmap, PRecord
import time

from timeit import default_timer as timer

class Agent:
    def __init__(self):
        pass

    def decide(self, state):
        """Main decision function for the agent. Returns the action that the
        agent decides for the current player to perform.

        Note that the available actions at a given GameState is
        accessed via `state.actions`.

        :param GameState state: The current state of the game.
        :returns action: The desired action that the player will perform.

        """
        raise NotImplementedError

    def learn(self, states, player_id):
        """Optional function. In the special case that the agent has an
        evaluation function that it is actively learning, this
        function exists as a way of 'retrospectively' learning.

        For now, ignore this function.

        :param states: List of states that the game went through,
                       where states[0] is the initial state.
        """
        pass


class Game:
    def __init__(self, game_type, agents, display=True):
        self.game_type = game_type
        self.agents = list(agents)
        self.display = display
        if display:
            pygame.init()
            self.screen = pygame.display.set_mode((672, 480))

    def run(self, play_again='query', speed=2):
        # while True:
        #     self._run_round(speed)
        #     if not play_again or play_again == 'query' and not self._play_again():
        #         break
        stat_dictionary = self._run_round(speed)
        
        return stat_dictionary


    def _run_round(self, speed):
        state = self.game_type.init(self.agents)
        states = [state]
        i = -1
        self._draw_state(state)


        stat_dictionary = {}
        stat_dictionary["red_team_moves"] = 0
        stat_dictionary["blue_team_moves"] = 0
        stat_dictionary["total_moves"] = 0
        stat_dictionary["won"] = ""
        stat_dictionary["time"] = 0

        red_team_moves = 0
        blue_team_moves = 0
        repeated = False
        start_time = timer()

        iteration_threshold = 1000

        if speed == 2:
            turn_wait = 0
            round_wait = 10
        elif speed == 1:
            turn_wait = 50
            round_wait = 100
        else:
            turn_wait = 500
            round_wait = 1000
        while not state.is_terminal:
            new_state = None
            i = (i + 1) % len(self.agents)
            while new_state == None:
                start_t = int(round(time.time() * 1000))
                agent = self.agents[i]
                action = agent.decide(state)
                new_state = state.act(action)
                if not new_state:
                    print("Invalid action performed!")
            self._draw_state(new_state)
            if new_state in states:
                stat_dictionary["red_team_moves"] = red_team_moves
                stat_dictionary["blue_team_moves"] = blue_team_moves
                stat_dictionary["total_moves"] = red_team_moves+blue_team_moves
                stat_dictionary["won"] = "draw"
                stat_dictionary["time"] = timer() - start_time
                repeated = True
                print("State has been repeated! Therefore, game is over.")
                break

            if (red_team_moves+blue_team_moves >= iteration_threshold):
                stat_dictionary["red_team_moves"] = red_team_moves
                stat_dictionary["blue_team_moves"] = blue_team_moves
                stat_dictionary["total_moves"] = red_team_moves+blue_team_moves
                stat_dictionary["won"] = "exhausted"
                stat_dictionary["time"] = timer() - start_time
                repeated = True
                print("1000 calcuated. Terminate game")
                break

            states += [new_state]
            state = new_state
            end_t = int(round(time.time() * 1000))
            wait_time = turn_wait - (end_t - start_t)
            # while True:
            #     pygame.event.clear()
            #     event = pygame.event.wait()
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_SPACE:
            #             break
            if wait_time > 0 and self.display:
                pygame.time.wait(wait_time)

            if (state.objects[state.current_player].team == 1): 
                red_team_moves += 1
            
            if (state.objects[state.current_player].team == 2):
                blue_team_moves += 1 

        if (not repeated):
            stat_dictionary["red_team_moves"] = red_team_moves
            stat_dictionary["blue_team_moves"] = blue_team_moves
            stat_dictionary["total_moves"] = red_team_moves+blue_team_moves
            stat_dictionary["won"] = str(state.is_terminal)
            stat_dictionary["time"] = timer() - start_time
            print('Finished game')

        for player_id, agent in enumerate(self.agents):
            agent.learn(states, player_id)

        pygame.time.wait(round_wait)

        return stat_dictionary

    def _draw_state(self, state):
        if self.display:
            surf = state.draw()
            # surf = pygame.transform.scale(surf, (672, 480))
            self.screen.blit(surf, (0, 0))
            pygame.display.flip()

    def _play_again(self):
        font = pygame.font.SysFont("monospace", 32)
        font.set_bold(True)
        label = font.render("play again? (y/n)", 1, (255, 255, 255))
        window = (self.screen.get_width()/2 - 200, self.screen.get_height()/2 - 30, 400, 60)
        window_b = (window[0]-4, window[1]-4, window[2]+8, window[3]+8)
        pygame.draw.rect(self.screen, (255, 255, 255), window_b)
        pygame.draw.rect(self.screen, (0, 0, 0), window)
        self.screen.blit(label, (window[0]+18, window[1]+7))
        pygame.display.flip()
        while True:
            pygame.event.clear()
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                if event.key == pygame.K_n:
                    return False

class GameType:
    """A helper class that initializes the game state. Used as a class
    since the game type might have parameters."""
    def __init__(self):
        pass

    def init(self, agents):
        pass


class GameState(PRecord):
    """A recording of the current state of a game. The game state performs
    several functions: it contains information about the current game
    state, but also contains code for running the game via the "act"
    method. This enables the Game class to run the game in real time
    while also allowing agents to look into the future.

    When writing your agent, it should only access the functions given
    in this class.

    """

    @property
    def num_players(self):
        """Returns the number of players in the game."""
        pass

    @property
    def current_player(self):
        """Returns the ID of the current player of the game."""
        pass

    @property
    def is_terminal(self):
        """True if the game state is at a terminal node."""
        raise NotImplementedError

    @property
    def actions(self):
        """Returns the list of actions available at this state."""
        raise NotImplementedError

    def reward(self, player_id):
        """Returns the reward that the player receives at the end of the
        game.

        :param int player_id: The player id.
        :return: The reward for `player_id` if the state is terminal;
                 None otherwise.
        """
        raise NotImplementedError

    def act(self, action):
        """Returns the resultant GameState object when performing `action` in
        the current state. Since the GameState keeps track of the
        current player, there is no need to pass which player is
        performing the action.

        For further emphasis, note that this function is NOT
        DESTRUCTIVE! It returns a *new* game state for which `action`
        has been performed without changing anything in the current
        GameState object.

        You might be worried that this method will be
        inefficient. However, this class has been implemented as a
        *persistent* data structure using pyrsistent, which means that
        it has several memory- and time-based optimizations that make
        copying efficient. It will be worse than destructive updates,
        but significantly better than deep copying.

        :param Action action: The action to perform
        :return: A new GameState where action has been performed, or
                 None if the action is invalid.

        """
        raise NotImplementedError

    def _action_is_valid(self, action):
        if self.is_terminal:
            print("""ERROR: Player tried to perform an action in a terminal state. Make sure that you are performing actions solely in non-terminal states.""")
            return None

        if not action in self.actions:
            print("""ERROR: Player tried to perform an illegal action. Make sure that you only perform actions available in `state.actions`.

Action: {}
Allowed actions: {}""".format(action, self.actions))
            return None
        return self

    def draw(self):
        """Used internally for visualizing the state of the game in the Game
        class.

        :returns: A pygame.Surface image of the current game state.
        """
        raise NotImplementedError
