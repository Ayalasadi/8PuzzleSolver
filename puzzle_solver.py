class PuzzleState:
    def __init__(self, board):
        self.board = board
        self.blank_index = board.index('b')

    def is_goal(self):
        return self.board == ('1', '2', '3', '4', '5', '6', '7', '8', 'b')

    def __str__(self):
        return ' '.join(self.board)
