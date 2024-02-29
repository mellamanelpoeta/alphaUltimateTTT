# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/MCTS/MCTS.ipynb.

# %% auto 0
__all__ = ['MCTS']

# %% ../nbs/MCTS/MCTS.ipynb 4
from .Node import Node
import numpy as np

# %% ../nbs/MCTS/MCTS.ipynb 5
#Copyright 2024 Gerardo Guerrero

class MCTS:
    def __init__(self, game, args):
        self.game = game
        self.args = args

    def search(self, state):
        root = Node(self.game, self.args, state)

        for search in range(self.args['num_simulations']):
            node = root

            #Walkdown the tree until a leaf node is reached
            # Select
            # the most promising node
            while node.is_fully_expanded():
                node = node.select()

            # if a leaf node is reached
            # Expand
            if not node.is_terminal():
                node = node.expand()

            value = node.simulate(self.game.next_symbol)
            # Backpropagate the value
            node.backpropagate(value)

        action_probs = np.zeros(81)
        for child in root.children:
            action_probs[child.action] = child.visits
        action_probs /= np.sum(action_probs)
        return action_probs
