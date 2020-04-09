from gtp_connection import GtpConnection, format_point, point_to_coord
from board_util_nogo import GoBoardUtil, EMPTY, BLACK, WHITE
from simple_board import SimpleGoBoard
from sim_player import SimulationPlayer
from search_player import SearchPlayer
import numpy as np
import random 
import signal

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

class NoGoFlatMC():
    def __init__(self):
        """
        NoGo player that selects moves by flat Monte Carlo Search.
        Resigns only at the end of game.
        Replace this player's algorithm by your own.

        """
        self.name = "NoGo Assignment 4"
        self.version = 0.0
        self.simulation_player = SimulationPlayer()
        self.search_player = SearchPlayer()
        self.best_move = None

    def get_move(self, original_board, color):
        """
        The genmove function using one-ply MC search.
        """
        board = original_board.copy()
        # Pick random move in case we time out
        self.best_move = GoBoardUtil.generate_random_move(board, color)
        # Try to get a move via simulation
        self.best_move = self.simulation_player.get_move(board, color)
        board = original_board.copy()
        # Try to get a perfect move with search
        self.best_move = self.search_player.get_move(board, color)
        return self.best_move

def run():
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnection(NoGoFlatMC(), board)
    con.start_connection()

if __name__=='__main__':
    run()
