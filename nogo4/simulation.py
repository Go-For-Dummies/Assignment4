import random
import numpy as np
from board_util import GoBoardUtil, BLACK, WHITE, PASS
class SimUtil:

    def randomSimulation(board):
        """
        Randomly generates moves and returns the winning color
        when the game is over. 
        """
        timeout = len(board.get_empty_points())
        for i in range(timeout):
            color = board.current_player
            move = GoBoardUtil.generate_random_move(board, color, False)
            if move == PASS:
                return GoBoardUtil.opponent(color)
            board.play_move(move, color)
        print("Error: Played too many moves!)")

    def probabilitySimulation(board, WU):
        """
        Given a WeightUtil object, randomly generates moves according
        to the pattern-based probabilistic and returns the winning
        color when the game is over. Recalculates all patterns after
        every move, could be made more efficient by storing patterns
        and weights and only recalculating patterns that neighbour 
        previous moves.
        """
        timeout = len(board.get_empty_points())
        for i in range(timeout):
            color = board.current_player
            moves = GoBoardUtil.generate_legal_moves(board, color)
            if not moves:
                return GoBoardUtil.opponent(color)
            weights = []
            for move in moves:
                index = WU.getindex(board, move)
                weight = WU.getweight(index)
                weights.append(weight)
            npWeights = np.array(weights)
            # Normalize weights to sum to 1
            npWeights = npWeights*(1./npWeights.sum())
            move = np.random.choice(moves, p=npWeights)
            board.play_move(move, color)
        print("Error: Played too many moves!")
