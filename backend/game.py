from copy import deepcopy
from math import inf
import math
from random import random, randint
import random

MAX = +1
MIN = -1


# La classe ConnectFourBoard représente l'état du jeu
class ConnectFourBoard:
    def __init__(self, board=None, depth=0, piece=MAX):
        self.board = (
            [[0 for _ in range(self.width)] for _ in range(self.height)]
            if board is None
            else board
        )
        self.piece = piece
        self.depth = depth
        self.action = (0, 0)
        self.next_action = (0, 0)
        self.value = 0
        self.alpha = 0
        self.beta = 0
        self.width = 7
        self.height = 6
        self.nbMoves = 0

    def Win_Value(self, piece):
        if piece == MAX:
            return 100
        else:
            return -100

    def heuristicEval1(self, piece):
        """number of potential winning lines"""
        count = 0
        # horizontal
        for row in range(self.height):
            for col in range(self.width - 3):
                nbVide = 0
                nbPiece = 0
                for i in range(4):
                    if self.board[row][col + i] == piece:
                        nbPiece += 1
                    elif self.board[row][col + i] == 0:
                        nbVide += 1

                if nbPiece >= 2 and nbPiece + nbVide == 4:
                    count += 1

        # vertical
        for row in range(self.height - 3):
            for col in range(self.width):
                nbVide = 0
                nbPiece = 0
                for i in range(4):
                    if self.board[row + i][col] == piece:
                        nbPiece += 1
                    elif self.board[row + i][col] == 0:
                        nbVide += 1

                if nbPiece >= 2 and nbPiece + nbVide == 4:
                    count += 1

        # diagonal
        for row in range(self.height - 3):
            for col in range(self.width - 3):
                nbVide = 0
                nbPiece = 0
                for i in range(4):
                    if self.board[row + i][col + i] == piece:
                        nbPiece += 1
                    elif self.board[row + i][col + i] == 0:
                        nbVide += 1

                if nbPiece >= 2 and nbPiece + nbVide == 4:
                    count += 1

        # anti-diagonal
        for row in range(self.height - 3):
            for col in range(3, self.width):
                nbVide = 0
                nbPiece = 0
                for i in range(4):
                    if self.board[row + i][col - i] == piece:
                        nbPiece += 1
                    elif self.board[row + i][col - i] == 0:
                        nbVide += 1

                if nbPiece >= 2 and nbPiece + nbVide == 4:
                    count += 1

        return count

    def heuristicEval2(self, piece):
        """number of potential winning lines - number of potential losing lines"""
        return self.heuristicEval1(piece) - self.heuristicEval1(3 - piece)

    def score_window(self, window):
        if window.count(MAX) == 4:
            return 100
        elif window.count(MAX) == 3 and window.count(0) == 1:
            return 5
        elif window.count(MAX) == 2 and window.count(0) == 2:
            return 2
        elif window.count(MIN) == 2 and window.count(0) == 2:
            return -2
        elif window.count(MIN) == 3 and window.count(0) == 1:
            return -5
        elif window.count(MIN) == 2 and window.count(0) == 2:
            return -2
        # contre attack
        elif window.count(MIN) == 3 and window.count(MAX) == 1:
            return 20
        elif window.count(MIN) == 2 and window.count(MAX) == 1 and window.count(0) == 1:
            return 10
        elif window.count(MIN) == 4:
            return -100
        else:
            return 0

    def getHeuristic(self, piece, heuristic):
        match heuristic:
            case 1:
                return self.heuristicEval1(piece)
            case 2:
                return self.heuristicEval2(piece)

    def getPossibleMoves(self, piece):
        succs = list()
        for j in range(7):
            find = False
            for i in range(5, -1, -1):
                if self.board[i][j] == 0:
                    find = True
                    successor = deepcopy(self)
                    successor.depth = self.depth + 1
                    successor.piece = self.piece * -1
                    successor.action = (i, j)
                    successor.makeMove(i, j, piece)
                    break
            if find:
                succs.append(successor)
        return succs

    def drawBoard(self):
        for i in range(6):
            line = " "
            for j in range(7):
                if self.board[i][j] == MAX:
                    p = "R"
                elif self.board[i][j] == MIN:
                    p = "Y"
                else:
                    p = "_"
                line += p + "  "
            print(line)
        print()

    def makeMove(self, row, col, piece):
        self.board[row][col] = piece

    def win(self, piece):
        # Vérification des diagonales ascendantes
        for row in range(3, 6):
            for col in range(4):
                if all(self.board[row - i][col + i] == piece for i in range(4)):
                    return True
        # Vérification des diagonales descendantes
        for row in range(3, 6):
            for col in range(3, 7):
                if all(self.board[row - i][col - i] == piece for i in range(4)):
                    return True

        # Vérification horizontale
        for row in range(6):
            if self.board[row][3] == piece:
                for col in range(4):
                    if all(self.board[row][col + i] == piece for i in range(4)):
                        return True

        # Vérification verticale
        for col in range(7):
            if self.board[2][col] == piece:
                for row in range(3):
                    if all(self.board[row + i][col] == piece for i in range(4)):
                        return True

        return False

    def matchNul(self):
        for j in range(7):
            if self.board[0][j] == 0:
                return False
        return True

    def gameOver(self, piece):
        return self.win(piece) or self.matchNul()

    def moveInCol(self, col):
        find = False
        if col >= 0 and col <= 6:
            for i in range(5, -1, -1):
                if self.board[i][col] == 0:
                    find = True
                    break
            print(i)
            if find:
                return i
            else:
                return -1
        else:
            return -2


class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

    def expand(self, successors):
        for successor in successors:
            child_node = Node(successor, parent=self)
            self.children.append(child_node)

    def ucb1(self, total_visits):
        if self.visits == 0:
            return math.inf
        exploitation = self.value / self.visits
        exploration = math.sqrt(2 * math.log(total_visits) / self.visits)
        return exploitation + exploration

    def select_child(self):
        total_visits = sum(child.visits for child in self.children)
        best_child = max(self.children, key=lambda child: child.ucb1(total_visits))
        return best_child


class Play:
    depth_limit = 1

    @staticmethod
    def humanTurn(state, play_col):
        error = 0
        play_row = state.moveInCol(play_col)
        if play_row == -1:
            error = 1
        return play_row, error

    @staticmethod
    def computerTurn(state, algorithm=1, heuristic=2):
        if algorithm == 1:
            next_action = Play.MonteCarloTreeSearch(state)
            print(next_action)
            return next_action

        elif algorithm == 2:
            next_action, _ = Play.MinimaxAlphaBetaPruning(
                state, Play.depth_limit, -inf, +inf, MAX, 2
            )
            return next_action

    @staticmethod
    def playrandom(state):
        play_row = -1
        while play_row == -1:
            play_col = randint(0, 6)
            play_row = state.moveInCol(play_col)

        return play_row, play_col

    @staticmethod
    def play(state, Turn):
        if Turn == MAX:
            play_row, play_col = Play.computerTurn(state, algorithm=1)
        else:
            play_row, play_col = Play.computerTurn(state, algorithm=2)

        return play_col, play_row

    @staticmethod
    def MinimaxAlphaBetaPruning(
        state, depth_limit, alpha=-inf, beta=+inf, piece=MAX, heuristicSelection=1
    ):
        if state.depth < depth_limit:
            if piece == MAX:
                state.value = -inf
                state.alpha = -inf
                state.beta = +inf
                for successor in state.getPossibleMoves(piece):
                    next_action, next_value = Play.MinimaxAlphaBetaPruning(
                        successor,
                        depth_limit,
                        state.alpha,
                        state.beta,
                        MIN,
                        heuristicSelection,
                    )
                    if state.value < next_value:
                        state.value = next_value
                        state.next_action = next_action
                    state.alpha = max(state.value, alpha)
                    if state.value >= beta:
                        if state.depth == 0:
                            return state.next_action, state.value
                        else:
                            return state.action, state.value
            else:
                state.value = inf
                state.alpha = -inf
                state.beta = inf
                for successor in state.getPossibleMoves(piece):
                    next_action, next_value = Play.MinimaxAlphaBetaPruning(
                        successor,
                        depth_limit,
                        state.alpha,
                        state.beta,
                        MAX,
                        heuristicSelection,
                    )
                    if state.value > next_value:
                        state.value = next_value
                        state.next_action = next_action
                    state.beta = min(state.value, beta)
                    if state.value <= alpha:
                        if state.depth == 0:
                            return state.next_action, state.value
                        else:
                            return state.action, state.value
        if state.gameOver(state.piece):
            if state.matchNul():
                state.value = 0
            else:
                state.value = state.Win_Value(state.piece)
        else:
            state.value = state.getHeuristic(state.piece, heuristicSelection)
        if state.depth == 0:
            return state.next_action, state.value
        else:
            return state.action, state.value

    # MonteCarloTreeSearch
    @staticmethod
    def MonteCarloTreeSearch(root_state, num_simulations=1000):
        root = Node(root_state)

        for _ in range(num_simulations):
            node = root
            state = deepcopy(root_state)  # Create a deepcopy for simulation

            # Selection: Traverse the tree using UCB1 until reaching an unvisited node or a terminal node.
            while not state.gameOver(state.piece):
                if not node.children:
                    break  # If leaf node is reached, break out
                node = node.select_child()
                action = node.state.action
                state.makeMove(action[0], action[1], state.piece)
                state.piece *= -1

            # Expansion: If the node is unvisited and not terminal, expand it.
            if not node.children and not state.gameOver(state.piece):
                successors = state.getPossibleMoves(state.piece)
                node.expand(successors)
                node = node.select_child()
                action = node.state.action
                state.makeMove(action[0], action[1], state.piece)
                state.piece *= -1

            # Simulation: Simulate random play from the current state until reaching a terminal state.
            while not state.gameOver(state.piece):
                successors = state.getPossibleMoves(state.piece)
                if not successors:
                    break
                random_successor = random.choice(successors)
                state = deepcopy(random_successor)
                state.piece *= -1

            # Backpropagation: Update values and visit counts
            result = state.heuristicEval1(
                state.piece
            )  # Use a heuristic to evaluate the leaf node
            Play.backpropagate(node, result)

        best_action_node = max(root.children, key=lambda child: child.visits)
        return best_action_node.state.action

    @staticmethod
    def backpropagate(node, result):
        while node:
            node.visits += 1
            node.value += result
            node = node.parent
