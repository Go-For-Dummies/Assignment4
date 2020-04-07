import numpy as np

def simulate_move_n_times(player, board, move, toplay):
    """
    Run simulations for a given move.
    """
    wins = 0
    for _ in range(player.n_sim):
        result = player.simulate(board, move, toplay)
        if result == toplay:
            wins += 1
    return wins

def select_best_move(board, moves, moveWins):
    """
    Move select after the search.
    """
    max_child = np.argmax(moveWins)
    return moves[max_child]

def round_robin(player, board, moves, toplay): 
    moveWins = []
    for move in moves:
        wins = simulate_move_n_times(player, board, move, toplay)
        moveWins.append(wins)
    return select_best_move(board, moves, moveWins)
