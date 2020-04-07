import re
from board_util import GoBoardUtil, BLACK, WHITE, EMPTY, BORDER

class WeightUtil:

    def __init__(self, file):

        file1 = open(str(file), 'r')
        weightlist = file1.readlines()
        self.weightdict = {}
        for line in weightlist:
            splitline = re.split(" ", line)
            index, weight = splitline
            self.weightdict[index] = weight

    def getweight(self, index):
        """
        Takes a base 4 index string and returns a float weight for that move
        """
        indexb10 = str(int(index, 4))
        return float(self.weightdict[indexb10])

    def getindex(self, board, move):
        """
        Takes a move on a board and produces an index for use with the weight file
        """
        index = ''
        index = index + str(board.board[move + board.NS + 1]) # Bottom Right
        index = index + str(board.board[move + board.NS]) # Bottom
        index = index + str(board.board[move + board.size]) # Bottom Left
        index = index + str(board.board[move + 1]) # Right
        index = index + str(board.board[move - 1]) # Left
        index = index + str(board.board[move - board.size]) # Top Right
        index = index + str(board.board[move - board.NS]) # Top
        index = index + str(board.board[move - board.NS - 1]) # Diagonal Top Left
        if board.current_player == WHITE: # Swap 1's and 2's if player is not black
            # This could be done much more efficiently by doing a little arithetic up top, but less readable
            invert_index = index.replace("1", "b")
            invert_index = invert_index.replace("2", "1")
            invert_index = invert_index.replace("b", "2")
            return invert_index
        return index

