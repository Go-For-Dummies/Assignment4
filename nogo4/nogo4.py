#!/home/mmelley/anaconda3/bin/python3
#/home/mmelley/anaconda3/bin/python3
#Set the path to your python3 above

from pathlib import Path

from gtp_connection import GtpConnection
from board_util import GoBoardUtil, EMPTY, BLACK, WHITE, PASS, MAXSIZE
from simple_board import SimpleGoBoard
from simulation import SimUtil
from weighting import WeightUtil
from ucb import run_ucb
from rr import round_robin

import numpy as np
import random

# Move Selection Policies ###
ROUND_ROBIN = 'rr'
UCB = 'ucb'

MOVE_POLICIES = {
    ROUND_ROBIN, UCB
}
#############################
# Simulation Policies #######
RANDOM = 'random'
PATTERN = 'pattern'

SIMULATION_POLICIES = {
    RANDOM, PATTERN
}
#############################

def undo(board, move):
    board.board[move] = EMPTY
    board.current_player = GoBoardUtil.opponent(board.current_player)

def play_move(board, move, color):
    board.play_move(move, color)

def game_result(board):
    legal_moves = GoBoardUtil.generate_legal_moves(board, board.current_player)
    if not legal_moves:
        result = BLACK if board.current_player == WHITE else WHITE
    else:
        result = None
    return result

class NoGo():
    def __init__(self, move_selection='rr', simulation_policy='random'):
        """
        NoGo player that selects moves by flat Monte Carlo Search.
        Resigns only at the end of game.
        Replace this player's algorithm by your own.

        """
        self.name = "NoGo Assignment 4"
        self.version = 0.0
        self.weight_util = WeightUtil(Path('weights'))
        self._move_selection = move_selection
        self._simulation_policy = simulation_policy
        self.simulations_per_move = 10
        self.n_sim = 10
        self.best_move = None

    @property
    def move_selection(self):
        return self._move_selection

    @property
    def simulation_policy(self):
        return self._simulation_policy

    @move_selection.setter
    def move_selection(self, move_selection):
        if move_selection not in MOVE_POLICIES:
            raise AttributeError(
                'move selection method not implemented: {}'.format(move_selection))
        self._move_selection = move_selection

    @simulation_policy.setter
    def simulation_policy(self, simulation_policy):
        if simulation_policy not in SIMULATION_POLICIES:
            raise AttributeError(
                'simulation policy method not implemented: {}'.format(simulation_policy))
        self._simulation_policy = simulation_policy

    def simulate(self, board, toplay):
        """
        Run a simulated game for a given starting move.
        """
        cboard = board.copy()
        cboard.play_move(move, color)
        if self.simulation_policy == RANDOM:
            result = SimUtil.randomSimulation(cboard)
        elif self.simulation_policy == PATTERN:
            result = SimUtil.probabilitySimulation(cboard, self.weight_util)
        return result

    def policy_moves(self, board):
        empties = board.get_empty_points()
        color = board.current_player
        legal_moves = []
        for move in empties:
            if board.is_legal(move, color):
                legal_moves.append(move)
        gtp_moves = []
        for move in legal_moves:
            coords = point_to_coord(move, board.size)
            gtp_moves.append((format_point(coords), move, 1))
        gtp_moves.sort()
        policy = self.simulation_policy
        if policy == RANDOM:
            w = 1 / len(gtp_moves)
            w = round(w, 3)
            weights = []
            movelist = []
            for item in gtp_moves:
                weights.append(w)
                movelist.append(item[0])
            npweights = np.array(weights)
        elif policy == PATTERN:
            weights = []
            movelist = []
            for item in gtp_moves:
                index = self.weight_util.getindex(board, item[1])
                weight = self.weight_util.getweight(index)
                weights.append(weight)
                movelist.append(item[0])
            npweights = np.array(weights)
            npweights = npweights*(1./npweights.sum())
        else: raise ValueError("Invalid policy type")
        str_weights = []
        for w in npweights:
            str_weights.append(str(round(w, 3)))
        sorted_moves = ' '.join(movelist)
        sorted_weights = ' '.join(str_weights)
        return "{} {}".format(sorted_moves, sorted_weights)

    def get_move(self, board, color):
        """
        Run one-ply MC simulations to get a move to play.
        """
        cboard = board.copy()
        emptyPoints = board.get_empty_points()
        moves = GoBoardUtil.generate_legal_moves(cboard, color)
        if not moves:
            return None
        moves.append(None)
        best = None
        if self.move_selection == UCB:
            C = 0.4  # sqrt(2) is safe, this is more aggressive
            best = run_ucb(self, cboard, C, moves, color)
        elif self.move_selection == ROUND_ROBIN:
            best = round_robin(self, cboard, moves, color)
        return best

def run():
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnection(NoGo(), board)
    con.start_connection()

def point_to_coord(point, boardsize):
    """
    Transform point given as board array index
    to (row, col) coordinate representation.
    Special case: PASS is not transformed
    """
    if point == PASS:
        return PASS
    else:
        NS = boardsize + 1
        return divmod(point, NS)

def format_point(move):
    """
    Return move coordinates as a string such as 'a1', or 'pass'.
    """
    # column_letters = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
    column_letters = "abcdefghjklmnopqrstuvwxyz"
    if move == PASS:
        return "pass"
    row, col = move
    if not 0 <= row < MAXSIZE or not 0 <= col < MAXSIZE:
        raise ValueError
    return column_letters[col - 1]+ str(row)

if __name__=='__main__':
    run()
