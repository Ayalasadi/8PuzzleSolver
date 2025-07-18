import heapq
from typing import Callable, Set, Tuple

class PuzzleState:
    def __init__(self, board: Tuple[str], parent=None, move="", depth=0):
        self.board = board
        self.parent = parent
        self.move = move
        self.depth = depth
        self.blank_index = board.index('b')

    def is_goal(self):
        return self.board == ('1', '2', '3', '4', '5', '6', '7', '8', 'b')
    
    def __lt__(self, other):
        return False #needed for heapq to avoid crash

    def get_neighbors(self):
        neighbors = []
        moves = {
            "Up": -3, "Down": 3, "Left": -1, "Right": 1
        }

        row, col = divmod(self.blank_index, 3)
        for move, delta in moves.items():
            new_blank = self.blank_index + delta
            if (
                0 <= new_blank < 9 and
                not (move == "Left" and col == 0) and
                not (move == "Right" and col == 2)
            ):
                new_board = list(self.board)
                new_board[self.blank_index], new_board[new_blank] = new_board[new_blank], new_board[self.blank_index]
                neighbors.append(PuzzleState(tuple(new_board), self, move, self.depth + 1))
        return neighbors

    def path(self):
        node, result = self, []
        while node:
            result.append(node.board)
            node = node.parent
        return list(reversed(result))

    def __str__(self):
        return ' '.join(self.board)

#search function
def best_first_search(start: PuzzleState, heuristic: Callable[[PuzzleState], int], max_steps: int = 5000):
    frontier = []
    heapq.heappush(frontier, (heuristic(start), start))
    visited: Set[Tuple[str]] = set()
    steps = 0

    while frontier and steps < max_steps:
        _, current = heapq.heappop(frontier)
        steps += 1

        if current.is_goal():
            return current.path(), steps

        visited.add(current.board)

        for neighbor in current.get_neighbors():
            if neighbor.board not in visited:
                heapq.heappush(frontier, (heuristic(neighbor), neighbor))

    return None, steps

#Test block
if __name__ == "__main__":
    start_config = ('1', '2', '3', '4', '5', '6', '7', 'b', '8')
    start = PuzzleState(start_config)

    def heuristic_misplaced(state: PuzzleState) -> int:
        return sum(1 for i, val in enumerate(state.board) if val != 'b' and val != str(i + 1))

    solution, steps = best_first_search(start, heuristic_misplaced)

    if solution:
        print("Solution path:")
        for step in solution:
            print(step)
        print(f"Total steps: {len(solution) - 1}")
        print(f"Nodes explored: {steps}")
    else:
        print("No solution found.")
