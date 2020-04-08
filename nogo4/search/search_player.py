from .board_util import GoBoardUtil, BLACK, WHITE, EMPTY
from .transposition_table import TranspositionTable, TTUtil
from .heuristic import statisticaly_evaluate

class SearchPlayer: 

    def __init__(self, board_size=7):
        self.tt = TranspositionTable(board_size)

    def get_move(self, board, color):
        board_copy = board.copy()
        return self.negamax(board_copy)[1]

    def store_table(self):
        self.tt.dump_to_file()

    def negamax(self, board, bbl = [], wbl = [], bneyes = [], wneyes = [], beyes = [], weyes = [],
            weight = None, HeuristicMode = True, SymmetryCheck = True):
        """
        Simple boolean negamax implementation with transposition table optimization

        Returns (true, winning_move) if current player can win with perfect play
        Else returns (false, 0) if current player will lose against perfect play
        Does not prune symmetrically or implement heuristics, simple DFS only.
        Runs full tree instead of using hash table to reduce to a (much smaller) DAG
        """
        # Check transposition table to see whether we have encountered this position
        state_code = self.tt.code(board)
        ret = self.tt.lookup(state_code)
        if ret is not None: 
            return ret
        if SymmetryCheck is True:
            # Check symmetrical equivalents of current board position
            twoD_board = GoBoardUtil.get_twoD_board(board)
            symmetries = TTUtil.symmetries(twoD_board)
            for tdb in symmetries:
                code = self.tt.code_2d(tdb)
                ret = self.tt.lookup(code)
                if ret is not None:
                    return ret
        current_color = board.current_player
        empty_points = list(board.get_empty_points())
        if current_color is BLACK: # Remove known illegal moves
            for pt in bbl:
                if pt in empty_points:
                    empty_points.remove(pt)
        if current_color is WHITE:
            for pt in wbl:
                if pt in empty_points:
                    empty_points.remove(pt)
    
        if len(empty_points) == 0:
            return self.tt.store(state_code, (False, 0))

        if HeuristicMode is True:
            if weight is None:
                [weight, bneyes, wneyes, beyes, weyes] = statisticaly_evaluate(board, current_color)
            ordered_moves = []
            for move in empty_points: # Heuristic check to order moves
                board.fast_play_move(move, current_color)
                (newweight, newbneyes, newwneyes, newbeyes, newweyes) = statisticaly_evaluate(board, current_color, move, 
                                                        weight, list(bneyes), list(wneyes), list(beyes), list(weyes))
                board.undo_move(move, current_color)
                ordered_moves.append((move, newweight, newbneyes, newwneyes, newbeyes, newweyes))
            ordered_moves.sort(key=lambda weighted: -weighted[1])

            for (move, nw, bne, wne, be, we) in ordered_moves:
                try: # Illegal moves will raise ValueError
                    board.play_move(move, current_color)
                    isWin = not self.negamax(board, list(bbl), list(wbl), bne, wne, be, we, -nw)[0]
                    board.undo_move(move, current_color)
                    if isWin:
                        return self.tt.store(state_code, (True, move))
                except ValueError: # Add illegal move to bl so we don't try it again
                    if current_color is BLACK:
                        bbl.append(move)
                    if current_color is WHITE:
                        wbl.append(move)

        else:
            for move in empty_points:
                try: # Illegal moves will raise ValueError
                    board.play_move(move, current_color)
                    isWin = not self.negamax(board, list(bbl), list(wbl))[0]
                    board.undo_move(move, current_color)
                    if isWin:
                        return self.tt.store(state_code, (True, move))
                except ValueError: # Add illegal move to bl so we don't try it again
                    if current_color is BLACK:
                        bbl.append(move)
                    if current_color is WHITE:
                        wbl.append(move)
        
        return self.tt.store(state_code, (False, 0))
