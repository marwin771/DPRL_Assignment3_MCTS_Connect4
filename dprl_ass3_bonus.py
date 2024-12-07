import random
import copy
import math

class ConnectFour:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.current_player = 1  # Player 1 starts

    def play_action(self, col):
        for row in range(self.rows - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.current_player = 3 - self.current_player  # Switch player
                break

    def get_legal_actions(self):
        return [col for col in range(self.cols) if self.board[0][col] == 0]

    def is_terminal(self):
        return self.check_winner() is not None or all(self.board[0][col] != 0 for col in range(self.cols))

    def check_winner(self):
        # Check horizontal, vertical, and diagonal lines for a winner
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if self.board[row][col] != 0 and all(self.board[row][col + i] == self.board[row][col] for i in range(4)):
                    return self.board[row][col]

        for row in range(self.rows - 3):
            for col in range(self.cols):
                if self.board[row][col] != 0 and all(self.board[row + i][col] == self.board[row][col] for i in range(4)):
                    return self.board[row][col]

        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if self.board[row][col] != 0 and all(self.board[row + i][col + i] == self.board[row][col] for i in range(4)):
                    return self.board[row][col]

        for row in range(self.rows - 3):
            for col in range(3, self.cols):
                if self.board[row][col] != 0 and all(self.board[row + i][col - i] == self.board[row][col] for i in range(4)):
                    return self.board[row][col]

        return None

    def get_result(self, player):
        winner = self.check_winner()
        if winner == player:
            return 1  # The player wins
        elif winner is not None:  # Opponent wins
            return -1
        elif all(self.board[0][col] != 0 for col in range(self.cols)):
            return 0  # Draw
        return None  # Game ongoing

    def copy(self):
        return copy.deepcopy(self)

    def print_board(self):
        for row in self.board:
            print(" ".join(str(x) if x != 0 else "." for x in row))
        print()

class Node:
    def __init__(self, game, parent=None, player=None):
        self.game = game
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
        self.player = player

    def is_fully_expanded(self):
        return len(self.children) == len(self.game.get_legal_actions())

    def best_child(self, exploration_weight=1.41):
        return max(self.children, key=lambda child: child.value / (child.visits + 1e-6) + exploration_weight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6)))

    def expand(self):
        untried_actions = [action for action in self.game.get_legal_actions() if action not in [child.game for child in self.children]]
        action = random.choice(untried_actions)
        new_game = self.game.copy()
        new_game.play_action(action)
        child_node = Node(game=new_game, parent=self, player=new_game.current_player)
        self.children.append(child_node)
        return child_node

class MCTS:
    def __init__(self):
        pass

    def search(self, game, iterations=1000):
        root = Node(game=game, player=game.current_player)
        for _ in range(iterations):
            node = self._select(root)
            reward = self.simulate(node)
            self.backpropagate(node, reward)
        return root.best_child(exploration_weight=0).game

    def _select(self, node):
        while not node.game.is_terminal():
            if not node.is_fully_expanded():
                return node.expand()
            else:
                node = node.best_child()
        return node

    def simulate(self, node):
        current_game = node.game.copy()
        current_player = node.player

        while not current_game.is_terminal():
            action = random.choice(current_game.get_legal_actions())
            current_game.play_action(action)

        return current_game.get_result(current_player)

    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            if node.parent is None:  # Root node
                node.value += reward
            else:
                node.value += reward if node.player == node.parent.player else -reward
            node = node.parent

def play_game():
    game = ConnectFour()
    mcts = MCTS()

    while not game.is_terminal():
        game.print_board()
        if game.current_player == 1:
            print("Player 1 (MCTS):")
            game = mcts.search(game, iterations=1000)
        else:
            print("Player 2 (Random):")
            action = random.choice(game.get_legal_actions())
            game.play_action(action)

    game.print_board()
    winner = game.check_winner()
    if winner is None:
        print("It's a draw!")
    else:
        print(f"Player {winner} wins!")

if __name__ == "__main__":
    play_game()
