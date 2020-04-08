#!/usr/local/bin/python3
#/usr/bin/python3
# Set the path to your python3 above
from pathlib import Path
from board_util import GoBoardUtil
from .sim_util import SimUtil
from .weighting import WeightUtil
from .ucb import run_ucb
import numpy as np

class SimulationPlayer():

    def __init__(self):
        """
        NoGo player that selects moves randomly 
        from the set of legal moves.
        Passe/resigns only at the end of game.

        """
        self.weight_util = WeightUtil(Path('simulation/weights'))
        self.n_sim = 10
    
    def get_move(self, board, color):
        """
        Run one-ply MC simulations to get a move to play.
        """
        
        cboard = board.copy()
        emptyPoints = board.get_empty_points()
        moves = GoBoardUtil.generate_legal_moves(cboard, color)
        
        if not moves:
            return None
        
        C = 0.4  # sqrt(2) is safe, this is more aggressive
        best = None
        best = run_ucb(self, cboard, C, moves, color)
        return best

    def simulate(self, board, move, color):
        cboard = board.copy()
        cboard.play_move(move, color)
        result = SimUtil.probabilitySimulation(cboard, self.weight_util)
        return result
