class node:
    def __init__(self, state, player_id):
        self.state = state
        self.total_wins = 0
        self.total_playouts = 0

        self.player_id = player_id