# Project 2: Minimax, Alpha-Beta Game Tree Search and Reinforcement Learning

In this project, you will complete an agent and an evaluation function
to play a discretized version of soccer.

## Usage

From the root directory, run

    python3 evaluate.py proj2

This will run a version of the game where both players choose actions
randomly. If you would like to play against the agent, run

    python3 evaluate.py proj2 --interactive

For any help on additional commands to use, run

    python3 evaluate.py proj2 --help

## Implementation notes

### The agent

You will be extending the abstract [`Agent`](/src/lib/game/_game.py#L10)
class specified in the game code. You will need to extend the `decide`
method so that it returns the correct action given a GameState.

Because we want our `MinimaxAgent` to be used for many kinds of games,
you can only use the most general information about a game. Each game
extends the [`GameState`](/src/lib/game/_game.py#L135) class; in
particular, we are given the following information:

1. `state.num_players` The number of players in the game
2. `state.current_player` The numeric ID of the player whose turn it
   is at the given state
3. `state.actions` The list of actions available at the moment
4. `state.is_terminal` Whether the current game state is terminal (that is, the game has ended)
5. `state.reward(player_id)` The reward that `player_id` receives, assuming that this is at the end of the game.
6. `state.act(action)` The corresponding GameState that would happen if `action` is performed at `state`

Note that the `GameState` class is immutable -- that is, *updates* to
the game happen by creating an entirely new `GameState` object rather
than destructively updating the existing `GameState`. For example, if
you run

    old_state = copy(state)
    state.act(action)
    old_state != state ## This will evaluate to False

since `state.act` is not destructive, `state` is not changed by
`state.act`. The following code will work:

    new_state = state.act(action)
    new_state != state ## This will evaluate to True

The `GameState` class is implemented as a persistent data structure
using [pyrsistent](https://github.com/tobgu/pyrsistent). That is,
updates to immutable data structures (as copies) are faster than
simple copies, but still relatively slower than mutable updates. For
the purpose of this assignment, you should not have to be too
concerned about the performance of immutable updates.

### The evaluation function

While our Minimax agent is domain-independent, the evaluation function
should be heavily domain-dependent. That is, you should use the
special methods from
the [`SoccerState`](/src/lib/game/discrete_soccer.py#L91) class when
implementing the evaluation function. In particular, you should pay
attention to:

1. `state.ball` Information about the location and state of the soccer ball
2. `state.players` Information about the location and state of each
   player on the field (indexed by the numeric player ID)

There are many helper functions provided in the `SoccerState` class,
so it is worth reading their documentation.
