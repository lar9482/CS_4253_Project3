class node:
    def __init__(self, state, player_id):
        self.state = state
        self.total_utility = 0 #Numerator
        self.total_playouts = 1 #Denominator
        self.player_id = player_id

        #Reference to the parent node
        self.parent = None
        
        #References to child nodes.
        self.children = []