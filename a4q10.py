"""
Austin Heinrich
NSID: awh055
11177796

CMPT Assignment 4 Codebase
Due: 26-Nov-18
"""

import copy
import sys
import time
import random

class ProblemState:
    def __init__(self, board):
        self.board = board
        self.queens = 0  # number of queens on the board, row you are placing queens on
        self.opening = 0  # the best possible opening column
        self.utility = 0  # The utility value of the state

class Problem:
    def __init__(self, size):
        self.size = size  # size of the board, size X size

    def is_terminal(self, state):
        """
        Is the game over?
        :param state: The current working state
        :return: True if the state is terminal and the game is over
        """
        if state.queens == self.size - 1:
            # if the number of queens is at its maximum, game is terminal
            return True
        elif not self.get_actions(state):
            # if there are no legal moves, game is terminal
            return True

        return False

    def is_legal_move(self, col, state):
        """
        Can we perform that move (i.e. placement/turn)?
        :param col: The column where a position would be placed. Note that row is determined by state.queens
        :param state: The current working state
        :return: True if the move is legal
        """

        # Check everything to the left of the proposed position.
        for i in range(state.queens):
            if state.board[col][i] == 1:
                return False

        # Check upwards diagonal to the left of the proposed position.
        if col != 0:
            x = col - 1
            y = state.queens - 1

            while x >= 0 and y >= 0:
                if state.board[x][y] == 1:
                    return False
                x -= 1
                y -= 1

        # Check the downwards diagonal to the left of the proposed position.
        if col < self.size:
            x = col + 1
            y = state.queens - 1
            while x < self.size and y >= 0:
                if state.board[x][y] == 1:
                    return False
                x += 1
                y -= 2

        return True

    def get_actions(self, state):
        """
        Gets a list of actions. Each singular action is an integer that denotes a column, just as queens denotes rows.
        :param state:  The current state of the game
        :return: a list of actions (i.e., moves/placements) that are legal in the given state.
        """

        actions = []

        if state.queens == 0:
            for i in range(self.size):
                actions.append(i)
        else:
            for column in range(self.size):
                if self.is_legal_move(column, state):
                    actions.append(column)

        return actions

    def get_results(self, state, an_act):
        """
        :param state: The current state of the game.
        :param an_act: A singular action, which is to be performed.
        :return: a new game state which is the result of taking the given action in the given state.
        """

        col = an_act
        new_state = ProblemState(copy.deepcopy(state.board))
        new_state.queens = state.queens
        new_state.opening = state.opening

        new_state.board[col][new_state.queens] = 1
        new_state.queens += 1

        return new_state

    def utility_1(self, state):
        """
        Utility function satisfying Version 1.
        :param state: The current working state.
        :return: Returns the final utility of the game, denoting the winner
        """

        if state.queens % 2 == 0:
            util_value = 1
        else:
            util_value = -1

        return util_value

    def utility_2(self, state):
        """
        Utility function satisfying Version 2.
        :param state: The current working state.
        :return: Returns the final utility of the game, denoting the winner
        """

        if state.queens % 2 == 0:
            util_value = -state.queens
        else:
            util_value = state.queens

        return util_value

    def max_value(self, state, ver, is_alphbet, alpha, beta):
        """
        Max's turn.
        :param state: The current working state.
        :param ver: The version of utility being used.
        :param is_alphbet: Whether or not the program uses Alpha-Beta pruning
        :param alpha: The Alpha value
        :param beta: The beta value
        :return: The best utility value
        """
        if self.is_terminal(state):
            # Determine which utility function to use. Defaults to version 1.
            if ver == 1:
                best = self.utility_1(state)
            elif ver == 2:
                best = self.utility_2(state)
            else:
                best = self.utility_1(state)
        else:
            best = -sys.maxsize
            for an_act in self.get_actions(state):
                val = self.min_value(self.get_results(state, an_act), ver, is_alphbet, alpha, beta)
                if val > best:
                    best = val
                if is_alphbet:
                    # If using Alpha-Beta pruning, utilize those functions
                    if best >= beta:
                        return best
                    alpha = max(alpha, best)

        return best

    def min_value(self, state, ver, is_alphbet, alpha, beta):
        """
        Min's turn.
        :param state: The current working state.
        :param ver: The version of utility being used.
        :param is_alphbet: Whether or not the program uses Alpha-Beta pruning
        :param alpha: The Alpha value
        :param beta: The beta value
        :return: The best utility value
        """
        if self.is_terminal(state):
            # Determine which utility function to use. Defaults to version 1.
            if ver == 1:
                best = self.utility_1(state)
            elif ver == 2:
                best = self.utility_2(state)
            else:
                best = self.utility_1(state)
        else:
            best = sys.maxsize
            for an_act in self.get_actions(state):
                val = self.max_value(self.get_results(state, an_act), ver, is_alphbet, alpha, beta)
                if val < best:
                    best = val
                if is_alphbet:
                    # If using Alpha-Beta pruning, utilize those functions.
                    if best <= alpha:
                        return best
                    beta = min(beta, best)

        return best

    def minimax_decision(self, state, ver, is_alphbet, alpha, beta):
        """
        Decides whose turn it is and plays for them.
        :param state: The current working state.
        :param ver: The version of utility being used.
        :param is_alphbet: Whether or not the program uses Alpha-Beta pruning
        :param alpha: The Alpha value
        :param beta: The beta value
        :return: a tuple of the best utility value for a particular action, and the best particular action
        """
        best_action = None
        if ver == 1:
            if self.utility_1(state) > 0:  # Is it Max's Turn?...
                best = -sys.maxsize
                for an_act in self.get_actions(state):
                    val = self.min_value(self.get_results(state, an_act), ver, is_alphbet, alpha, beta)
                    if val > best:
                        best = val
                        best_action = an_act
            else:  # ...or Min's turn?
                best = sys.maxsize
                for an_act in self.get_actions(state):
                    val = self.max_value(self.get_results(state, an_act), ver, is_alphbet, alpha, beta)
                    if val < best:
                        best = val
                        best_action = an_act
        else:  # Defaults to version 2, though if we've gotten to this function *ver* should be either 1 or 2 anyway
            if self.utility_2(state) > 0:  # Is it Max's Turn?...
                best = -sys.maxsize
                for an_act in self.get_actions(state):
                    val = self.min_value(self.get_results(state, an_act), ver, is_alphbet, alpha, beta)
                    if val > best:
                        best = val
                        best_action = an_act
            else:  # ...or Min's turn?
                best = sys.maxsize
                for an_act in self.get_actions(state):
                    val = self.max_value(self.get_results(state, an_act), ver, is_alphbet, alpha, beta)
                    if val < best:
                        best = val
                        best_action = an_act

        return best, best_action

    def solve(self, state, ver, is_alphbet):
        """
        :param state: The current working state.
        :param ver: The version of utility to use.
        :param is_alphbet: True if Alpha-Beta pruning is to be used
        :return: The final utility and the best opening
        """

        util = 0

        while not self.is_terminal(state):

            # Determine the version of utility to use, then determine if Alpha-Beta pruning is used.
            if ver == 1:
                if is_alphbet:
                    # util = self.max_value(state, 1, True, -sys.maxsize, sys.maxsize)
                    util = self.minimax_decision(state, 1, True, -sys.maxsize, sys.maxsize)
                else:
                    # util = self.max_value(state, 1, False, 0, 0)
                    util = self.minimax_decision(state, 1, False, 0, 0)
            elif ver == 2:
                if is_alphbet:
                    # util = self.max_value(state, 2, True, -sys.maxsize, sys.maxsize)
                    util = self.minimax_decision(state, 2, True, -sys.maxsize, sys.maxsize)
                else:
                    # util = self.max_value(state, 2, False, 0, 0)
                    util = self.minimax_decision(state, 2, False, 0, 0)
            else:  # util defaults to 0, though this breaks the program since the next line asks for a tuple
                util = 0

            if state.queens == 0:  # collect the best opening
                state.opening = util[1]
            state = self.get_results(state, util[1])
            state.utility = util[0]

        return state

    def max_value_with_cutoff(self, state, ver, is_alphbet, alpha, beta, depth_lim):
        """
        Max's turn.
        :param state: The current working state.
        :param ver: The version of utility being used.
        :param is_alphbet: Whether or not the program uses Alpha-Beta pruning
        :param alpha: The Alpha value
        :param beta: The beta value
        :param depth_lim
        :return: The best utility value
        """
        if self.is_terminal(state):
            if ver == 1:
                best = self.utility_1(state)
            elif ver == 2:
                best = self.utility_2(state)
            else:
                best = self.utility_1(state)
        elif self.cutoff_test(state, depth_lim):
            # Determine which utility function to use.
            if ver == 1:
                best = self.evaluation(state, 1)
            elif ver == 2:
                best = self.evaluation(state, 2)
            else:
                best = self.evaluation(state, 1)
        else:
            best = -sys.maxsize
            for an_act in self.get_actions(state):
                val = self.min_value_with_cutoff(self.get_results(state, an_act), ver, is_alphbet,
                                                 alpha, beta, depth_lim)
                if val > best:
                    best = val
                if is_alphbet:
                    # If using Alpha-Beta pruning, utilize those functions
                    if best >= beta:
                        return best
                    alpha = max(alpha, best)

        return best

    def min_value_with_cutoff(self, state, ver, is_alphbet, alpha, beta, depth_lim):
        """
        Min's turn.
        :param state: The current working state.
        :param ver: The version of utility being used.
        :param is_alphbet: Whether or not the program uses Alpha-Beta pruning
        :param alpha: The Alpha value
        :param beta: The beta value
        :param depth_lim
        :return: The best utility value
        """
        if self.is_terminal(state):
            if ver == 1:
                best = self.utility_1(state)
            elif ver == 2:
                best = self.utility_2(state)
            else:
                best = self.utility_1(state)
        elif self.cutoff_test(state, depth_lim):
            # Determine which utility function to use.
            if ver == 1:
                best = self.evaluation(state, 1)
            elif ver == 2:
                best = self.evaluation(state, 2)
            else:
                best = self.evaluation(state, 1)
        else:
            best = sys.maxsize
            for an_act in self.get_actions(state):
                val = self.max_value_with_cutoff(self.get_results(state, an_act), ver, is_alphbet,
                                                 alpha, beta, depth_lim)
                if val < best:
                    best = val
                if is_alphbet:
                    # If using Alpha-Beta pruning, utilize those functions.
                    if best <= alpha:
                        return best
                    beta = min(beta, best)

        return best

    def minimax_decision_with_cutoff(self, state, ver, is_alphbet, alpha, beta, depth_lim):
        """
        Decides whose turn it is and plays for them.
        :param state: The current working state.
        :param ver: The version of utility being used.
        :param is_alphbet: Whether or not the program uses Alpha-Beta pruning
        :param alpha: The Alpha value
        :param beta: The beta value
        :param depth_lim:
        :return: a tuple of the best utility value for a particular action, and the best particular action
        """
        best_action = None
        if ver == 1:
            if self.evaluation(state, 1) > 0:  # Is it Max's Turn?...
                best = -sys.maxsize
                for an_act in self.get_actions(state):
                    val = self.min_value_with_cutoff(self.get_results(state, an_act), ver, is_alphbet,
                                                     alpha, beta, depth_lim)
                    if val > best:
                        best = val
                        best_action = an_act
            else:  # ...or Min's turn?
                best = sys.maxsize
                for an_act in self.get_actions(state):
                    val = self.max_value_with_cutoff(self.get_results(state, an_act), ver, is_alphbet,
                                                     alpha, beta, depth_lim)
                    if val < best:
                        best = val
                        best_action = an_act
        else:  # Defaults to version 2, though if we've gotten to this function *ver* should be either 1 or 2 anyway
            if self.evaluation(state, 2) > 0:  # Is it Max's Turn?...
                best = -sys.maxsize
                for an_act in self.get_actions(state):
                    val = self.min_value_with_cutoff(self.get_results(state, an_act), ver, is_alphbet,
                                                     alpha, beta, depth_lim)
                    if val > best:
                        best = val
                        best_action = an_act
            else:  # ...or Min's turn?
                best = sys.maxsize
                for an_act in self.get_actions(state):
                    val = self.max_value_with_cutoff(self.get_results(state, an_act), ver, is_alphbet,
                                                     alpha, beta, depth_lim)
                    if val < best:
                        best = val
                        best_action = an_act

        return best, best_action

    def cutoff_test(self, state, depth_lim):
        """
        Is the search deep enough?
        :param state: The current working state
        :param depth_lim: The depth limit, how deep we are willing to go.
        :return: True if the search should be terminated due to its depth.
        """

        if state.queens >= depth_lim:
            return True

        return False

    def evaluation(self, state, ver):
        """
        Heuristic evalutation function
        :param state: The current working state
        :param ver: The version of utility that is being used
        :return: a utility value
            if ver == 1:
                returns random choice of -1 or 1
            else if ver == 2:
                returns a random integer between the negative and positive number of queens on the board
                does not return a 0
        """
        if ver == 1:
            while True:
                util_value = random.randint(-1, 1)
                if util_value != 0:  # break out of the loop if the utility is not 0, as it should be
                    break
        else:
            if state.queens == 0:
                util_value = 1
            else:
                while True:
                    if state.queens % 2 == 0:
                        util_value = random.randint(0, state.queens)
                    else:
                        util_value = random.randint(-state.queens, 0)
                    if util_value != 0:  # break out of the loop if the utility is not 0, as it should be
                        return util_value

        return util_value

    def solve_with_cutoff(self, state, ver, is_alphbet, depth_lim):
        """
        :param state: The current working state
        :param ver: The version of evaluate to use
        :param is_alphbet: Is alpha-beta pruning enabled?
        :param depth_lim: The depth limit
        :return: A cutoff state.
        """

        while not self.is_terminal(state):
            # break the loop and return if the depth limit has been reached
            if self.cutoff_test(state, depth_lim):
                break

            # Determine the version of utility to use, then determine if Alpha-Beta pruning is used.
            if ver == 1:
                if is_alphbet:
                    # util = self.max_value(state, 1, True, -sys.maxsize, sys.maxsize)
                    util = self.minimax_decision_with_cutoff(state, 1, True, -sys.maxsize, sys.maxsize, depth_lim)
                else:
                    # util = self.max_value(state, 1, False, 0, 0)
                    util = self.minimax_decision_with_cutoff(state, 1, False, 0, 0, depth_lim)
            elif ver == 2:
                if is_alphbet:
                    # util = self.max_value(state, 2, True, -sys.maxsize, sys.maxsize)
                    util = self.minimax_decision_with_cutoff(state, 2, True, -sys.maxsize, sys.maxsize, depth_lim)
                else:
                    # util = self.max_value(state, 2, False, 0, 0)
                    util = self.minimax_decision_with_cutoff(state, 2, False, 0, 0, depth_lim)
            else:  # util defaults to 0, as does the move
                print('error - no proper version')
                util = 0, 0

            if state.queens == 0:  # collect the best opening
                state.opening = util[1]
            state = self.get_results(state, util[1])
            state.utility = util[0]

        return state


class Queens:
    def __init__(self, size):
        self.size = size
        self.board = [0] * size
        for x in range(size):
            self.board[x] = [0] * size

    def start(self, ver, is_alphbet):
        """
        Begin.
        :param ver: The version of utility being used.
        :param is_alphbet: Whether or not the program uses Alpha-Beta pruning
        :return: A tuple of the solution's Utility value and the time elapsed in seconds
        """
        s_time = time.time()

        prob = Problem(self.size)
        initial_state = ProblemState(self.board)

        # Trivial solutions that don't like the implementation
        if self.size == 1:
            initial_state.board[0] = 1
            initial_state.queens = 1
            initial_state.opening = 0
            initial_state.utility = 1
            fin_time = time.time() - s_time
            return initial_state, fin_time
        elif self.size == 2:
            initial_state.board[0][0] = 1
            initial_state.queens = 1
            initial_state.opening = 0
            initial_state.utility = 1
            fin_time = time.time() - s_time
            return initial_state, fin_time
        elif self.size == 3:
            initial_state.board[1][0] = 1
            initial_state.queens = 1
            initial_state.opening = 1
            initial_state.utility = 1
            fin_time = time.time() - s_time
            return initial_state, fin_time

        solution = prob.solve(initial_state, ver, is_alphbet)
        fin_time = time.time() - s_time

        return solution, fin_time

    def start_depth_cut(self, ver, is_alphbet, cutoff):
        """
        Begin.
        :param ver: The version of utility being used.
        :param is_alphbet: Whether or not the program uses Alpha-Beta pruning
        :param cutoff: Depth at which to cutoff the search.
        :return: A tuple of the solution's Utility value and the time elapsed in seconds
        """
        s_time = time.time()

        prob = Problem(self.size)
        initial_state = ProblemState(self.board)

        # Trivial solutions that don't like the implementation
        if self.size == 1:
            initial_state.board[0] = 1
            initial_state.queens = 1
            initial_state.opening = 0
            initial_state.utility = 1
            fin_time = time.time() - s_time
            return initial_state, fin_time
        elif self.size == 2:
            initial_state.board[0][0] = 1
            initial_state.queens = 1
            initial_state.opening = 0
            initial_state.utility = 1
            fin_time = time.time() - s_time
            return initial_state, fin_time
        elif self.size == 3:
            initial_state.board[1][0] = 1
            initial_state.queens = 1
            initial_state.opening = 1
            initial_state.utility = 1
            fin_time = time.time() - s_time
            return initial_state, fin_time

        solution = prob.solve_with_cutoff(initial_state, ver, is_alphbet, cutoff)
        fin_time = time.time() - s_time

        return solution, fin_time



"""
# Horizontal test
arr = [[0, 1, 0], [1, 0, 0], [0, 0, 0]]
sta = ProblemState(arr)
prob = Problem(4)
sta.queens = 2
print("Horiz 1 (false):", prob.is_legal_move(0, sta))  # should be false

# Diagonal Test 1
arr = [[1, 0, 0], [0, 1, 0], [0, 0, 0]]
sta = ProblemState(arr)
prob = Problem(4)
sta.queens = 2
print("Diag 1 (false):", prob.is_legal_move(2, sta))  # should be false

# Diagonal Test 2
arr = [[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]]
sta = ProblemState(arr)
prob = Problem(4)
sta.queens = 2
print('Diag 2 (false):', prob.is_legal_move(0, sta))  # should be false

# Actions Test
print("Actions (empty):", prob.get_actions(sta))
arr = [[0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
sta = ProblemState(arr)
prob = Problem(4)
sta.queens = 1
print("Actions 2 ([3]):", prob.get_actions(sta))

arr = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]]
sta = ProblemState(arr)
prob = Problem(4)
sta.queens = 1
print("Actions 3 ([0, 1]):", prob.get_actions(sta))

# Terminal Test
arr = [[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]]
sta = ProblemState(arr)
prob = Problem(4)
sta.queens = 2
print('Terminal 1 (true):', prob.is_terminal(sta))

arr = [[0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 1, 0, 0]]
sta = ProblemState(arr)
prob = Problem(4)
sta.queens = 4
print('Terminal 2 (true):', prob.is_terminal(sta))

arr = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]]
sta = ProblemState(arr)
prob = Problem(4)
sta.queens = 1
print('Terminal 3 (false):', prob.is_terminal(sta))

# Results Test
arr = [[0, 0, 0], [0, 0, 0], [1, 0, 0]]
sta = ProblemState(arr)
prob = Problem(3)
sta.queens = 1
print('                          ', sta.board)
print('Results 1 (compare above):', prob.get_results(sta, 0).board)

arr = [[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]]
sta = ProblemState(arr)
prob = Problem(4)
sta.queens = 2
print('                          ', sta.board)
print('Results 2 (compare above):', prob.get_results(sta, 2).board)

# Utility Test
arr = [[0, 0, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 1, 0, 0]]
sta = ProblemState(arr)
prob = Problem(4)
sta.queens = 4
print('Utility 1  (1):', prob.utility(sta))

arr = [[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]]
sta = ProblemState(arr)
prob = Problem(4)
sta.queens = 2
print('Utility 2  (1):', prob.utility(sta))

arr = [[1, 0, 0, 0], [0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
sta = ProblemState(arr)
prob = Problem(4)
sta.queens = 3
print('Utility 2 (-1):', prob.utility(sta))
"""

