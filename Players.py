class Player:
    """Base player class"""
    def __init__(self, symbol):
        self.symbol = symbol

    def get_symbol(self):
        return self.symbol
    
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    """Human subclass with text input in command line"""
    def __init__(self, symbol):
        Player.__init__(self, symbol)
        self.total_nodes_seen = 0

    def clone(self):
        return HumanPlayer(self.symbol)
        
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class AlphaBetaPlayer(Player):
    """Class for Alphabeta AI: implement functions minimax, eval_board, get_successors, get_move
    eval_type: int
        0 for H0, 1 for H1, 2 for H2
    prune: bool
        1 for alpha-beta, 0 otherwise
    max_depth: one move makes the depth of a position to 1, search should not exceed depth
    total_nodes_seen: used to keep track of the number of nodes the algorithm has seearched through
    symbol: X for player 1 and O for player 2
    """
    def __init__(self, symbol, eval_type, prune, max_depth):
        Player.__init__(self, symbol)
        self.eval_type = eval_type
        self.prune = prune
        self.max_depth = int(max_depth) 
        self.max_depth_seen = 0
        self.total_nodes_seen = 0
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'


    def terminal_state(self, board):
        # If either player can make a move, it's not a terminal state
        for c in range(board.cols):
            for r in range(board.rows):
                if board.is_legal_move(c, r, "X") or board.is_legal_move(c, r, "O"):
                    return False 
        return True 


    def terminal_value(self, board):
        # Regardless of X or O, a win is float('inf')
        state = board.count_score(self.symbol) - board.count_score(self.oppSym)
        if state == 0:
            return 0
        elif state > 0:
            return float('inf')
        else:
            return -float('inf')


    def flip_symbol(self, symbol):
        # Short function to flip a symbol
        if symbol == "X":
            return "O"
        else:
            return "X"


    def alphabeta(self, board):

        # Write minimax function here using eval_board and get_successors
        # type:(board) -> (int, int)
        column, row = 0, 0

        startingValue = -float('inf')

        # Replace starting value if there is a higher value
        for position in self.get_successors(board, self.symbol):
            currentValue = self.min_value(position)
            if startingValue < currentValue:
                startingValue = currentValue
                column = position.move[0]
                row = position.move[1]

        # If no higher value is found then use the last highest value
        if startingValue == -float('inf'):
            currentState = self.get_successors(board, self.symbol)[0]
            column = position.move[0]
            row = position.move[1]

        return column, row

    def max_value(self, board, alpha=-float('inf'), beta=float('inf'), depth=0) -> float:

        # Keep track of the number of node seen
        self.total_nodes_seen = self.total_nodes_seen + 1

        # If we've reached a terminal state or max depth
        if self.terminal_state(board):
            return self.terminal_value(board)
        elif depth == self.max_depth:
            return self.eval_board(board)

        startingValue = -float('inf')

        # Recursively find the best value out of all the successors
        for position in self.get_successors(board, self.symbol):
            startingValue = max(startingValue, self.min_value(position, alpha, beta, depth+1))

            if self.prune == '1' and startingValue >= beta:
                return startingValue
            alpha = max(alpha, startingValue)

        return startingValue

    def min_value(self, board, alpha=-float('inf'), beta=float('inf'), depth=0) -> float:

        # Keep track of the number of node seen
        self.total_nodes_seen = self.total_nodes_seen + 1

        # If we've reached a terminal state or max depth
        if self.terminal_state(board):
            return self.terminal_value(board)
        elif depth == self.max_depth:
            return self.eval_board(board)

        startingValue = float('inf')

        # Recursively find the worst value out of all the successors
        for position in self.get_successors(board, self.oppSym):
            startingValue = min(startingValue, self.max_value(position, alpha, beta, depth+1))

            if self.prune == '1' and startingValue <= alpha:
                return startingValue
            beta = min(beta, startingValue)

        return startingValue

    def eval_board(self, board) -> float:
        value = 0

        if self.eval_type == 0: # H0, Piece Difference: Number of your pieces - number of opponent's pieces
            value = board.count_score(self.symbol) - board.count_score(self.Oppsym)
        elif self.eval_type == 1: # H1, Mobility:  Number of your legal moves - number of opponent's legal moves
            value = board.has_legal_moves_remaining(self.symbol) - board.has_legal_moves_remaining(self.Oppsym)
        elif self.eval_type == 2: #H2: Design your own function
            value = board.current_score(self.symbol) + 2

        return value


    def get_successors(self, board, player_symbol) -> list:
        successors = []

        #if there are no more legal moves left for the player, return empty list
        if not board.has_legal_moves_remaining(player_symbol):
            return successors
        
        else:
            #if there are still legal moves left
            #go through the whole board
            for col in range(board.cols):
                for row in range (board.rows):
                    #if move is legal at (col, row)
                    if board.is_legal_move(col, row, player_symbol):
                        #make a clone of the board
                        new_board = board.cloneOBoard()
                        #generate a move on the new board
                        new_board.play_move(col, row, player_symbol)
                        new_board.move = (col, row)
                        #add it to list of possible moves
                        successors.append(new_board)
            return successors


    def get_move(self, board):
        # Write function that returns a move (column, row) here using minimax
        # type:(board) -> (int, int)
        # print(self.alphabeta(board))
        return self.alphabeta(board)

       
        





