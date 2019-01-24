"""
Austin Heinrich
NSID: awh055
11177796

CMPT 317 Assignment 3 Question 4
Due: 29-Oct-2018
"""
import copy
import time


class Variable:
    def __init__(self, cur_value, domain):
        """
        A variable with a current value and a list of domains
        :param cur_value: initialized to None. When it has a value, the domains list is empty
        :param domain: set of possible values, empty when a variable is filled
        """
        self.cur_value = cur_value
        self.domain = domain


class ProblemState:
    def __init__(self, variables, consistent):
        """
        :param variables: a dict that stores variables, indexed by their location in the matrix.
        :param consistent: a boolean flag that declares the state's consistency. True for consistent.
        """
        self.variables = variables
        self.consistent = consistent

    def is_consistent(self):
        """
        :return: True if the state is consistent
        """
        return self.consistent

    def to_string(self, sq_size):
        for i in range(sq_size):
            for j in range(sq_size):
                print(str(self.variables[(i, j)].cur_value) + ", ", end='')
            print("")


class Problem:
    def __init__(self, latin_sq, square_size):
        self.latin_sq = latin_sq
        self.sq_size = square_size

    def is_goal(self, state):
        """
        Checks if the state is a goal state i.e. a complete Latin Square
        :param state: the current working state
        :return: True if the state is a Latin Square, else False
        """

        # can't have an unfilled variable
        # x = {i, j}
        for a_key in state.variables:
            if state.variables.get(a_key).cur_value == 0:
                return False

        # if the state is inconsistent, it is not a solution
        if not state.is_consistent():
            print("here!")
            return False

        possible_values = set(range(1, self.sq_size + 1))  # {1, 2, 3, ... N}
        # iterate through all columns and rows, making sure they match the possible values
        for i in range(self.sq_size):
            col = set(state.variables[(i, j)].cur_value for j in range(self.sq_size))
            if possible_values != col:
                return False
            row = set(state.variables[(j, i)].cur_value for j in range(self.sq_size))
            if possible_values != row:
                return False

        return True

    def get_actions(self, state):
        """
        Gets a set of possible actions for the next blank
        :param state: the current state
        :return: actions - a set of possible actions
        """

        if state.is_consistent() is False:
            return {}  # prevent an inconsistent state from generating (inconsistent) children
        else:
            for i in range(self.sq_size):
                for j in range(self.sq_size):
                    if state.variables[(i, j)].cur_value == 0:
                        actions = state.variables[(i, j)].domain  # {1, 2, 3, ... N}
                        return actions

        return {}  # no actions available, empty domain or no actions possible or something went wrong

    def results(self, state, act):
        """
        Return a new state action with the next unassigned variable assigned
        :param state: the current state
        :param act: a possible action
        :return: a new state
        """

        new_state = state

        for i in range(self.sq_size):
            for j in range(self.sq_size):
                if new_state.variables[(i, j)].cur_value == 0:
                    new_state.variables[(i, j)].cur_value = act
                    for k in range(self.sq_size):

                        # remove the act from the domain of each unassigned variable in the row
                        # note that it won't remove an act from an assigned variable... since they have an empty domain
                        #  already
                        if act in new_state.variables[(i, k)].domain:
                            new_state.variables[(i, k)].domain.remove(act)
                            if len(new_state.variables[(i, k)].domain) == 0 \
                                    and new_state.variables[(i, k)].cur_value == 0:
                                # print('here!')
                                new_state.consistency = False

                        # remove the act from the domain of each unassigned variable in the column
                        if act in new_state.variables[(k, j)].domain:
                            new_state.variables[(k, j)].domain.remove(act)
                            if len(new_state.variables[(k, j)].domain) == 0 \
                                    and new_state.variables[(k, j)].cur_value == 0:
                                # print('here!')
                                new_state.consistency = False
                    break
            else:  # continue if an unassigned variable has not been found
                continue
            break

        return new_state

    def restrict_domain(self, a_state, acts, coords):
        """
        Returns a domain with restricted values removed --- that is, values that cannot be place in the blank
        :param acts: a set of possible actions at that square
        :param coords: the coordinates of a blank, a tuple
        :return: restricted_domain
        """

        col = set(self.latin_sq[coords[0]])  # get the column the blank exists on
        row = set(self.latin_sq[x][coords[1]] for x in range(self.sq_size))  # get the row the blank exists on

        restricted_domain = acts - col
        restricted_domain = restricted_domain - row
        if len(restricted_domain) == 0:
            a_state.consistent = False

        return set(restricted_domain)

    def initial_state(self):
        """
        Assigns variables that are initially assigned, blanks are left as 0 and should be referred to as unassigned
        Assigned domains have an empty domain, likewise unassigned variables have an occupied, restricted domain
        :param latin_sq: a given latin square, list[][]
        :return: a new state object, with initial variables assigned
        """
        state = ProblemState(dict(), True)

        actions = set(range(1, self.sq_size + 1))
        for i in range(self.sq_size):
            for j in range(self.sq_size):
                if self.latin_sq[i][j] != 0:
                    # Variable = {x, {0}}
                    state.variables[(i, j)] = Variable(self.latin_sq[i][j], {None})
                else:
                    # Variable = {0, {1, 2, 3, ... N}}
                    state.variables[(i, j)] = Variable(self.latin_sq[i][j], set(self.restrict_domain(state, actions, (i, j))))

        return state


class TreeSearch:
    def __init__(self):
        pass

    def depth_first(self, square, size):
        """
        Performs a depth first search of the problem
        :param square: A Latin Square
        :param size: the side length of said Latin Square
        :return: True if a solution is found, else False
        """

        nodes = 0
        s_time = time.time()
        front_size = 0

        prob = Problem(square, size)
        initial_state = prob.initial_state()
        frontier = [initial_state]

        if prob.is_goal(initial_state):  # immediate solution
            t = time.time() - start_time
            print("Time:", str(t) + "s")
            print("Nodes Checked:", nodes)
            return True

        while len(frontier) > 0:
            last = frontier.pop()  # pop the last node in the frontier (maintaining LIFO)

            if prob.is_goal(last):  # check for solution
                last.to_string(prob.sq_size)
                t = time.time() - s_time
                print("Time:", str(t) + "s")
                print("Nodes Checked:", nodes)
                print("Max Frontier Size:", front_size)
                return True

            nodes += 1  # increment nodes checked

            for x in range(prob.sq_size):
                for y in range(prob.sq_size):
                    if last.variables[(x, y)].cur_value == 0:
                        actions = prob.get_actions(last)
                        for an_act in actions:
                            new_state = prob.results(copy.deepcopy(last), an_act)
                            frontier.append(new_state)
                            front_size = max(len(frontier), front_size)

            if (time.time() - s_time) >= 10.0:
                break

        print("Failure.")
        t = time.time() - s_time
        print("Time:", str(t) + "s")
        print("Nodes Checked:", nodes)
        print("Max Frontier Size:", front_size)
        return False


fin = 'LatinSquares.txt'
print("Data Set:", fin)

# Generate a list of all Latin Squares, as well as the number of squares and their sizes
# L = list of latin squares
# size = the size of the respective latin square i.e. use L[p] and size[p], where p is the problem number
file_data = []
L = []
size = []
counting_size = 0
with open(fin) as f:
    number_of_problems = f.readline().split()
    number_of_problems = int(number_of_problems[0])
    for p in range(number_of_problems):
        file_data.clear()  # clear the running list of all file data
        size.append(int(f.readline().split()[0]))
        for i in range(size[p]):
            square = f.readline().split()
            file_data.append(square)  # store a square into a single list
        L.append(copy.deepcopy(file_data))  # store the square data in a list of squares
        f.readline()

f.close()
# Convert everything to Integer, '_' becomes 0
# Get the number of blanks in each problem
count = []
for x in range(len(L)):
    count.append(0)
    for y in range(len(L[x])):
        for z in range(len(L[x][y])):
            if L[x][y][z] == '_':
                L[x][y][z] = 0
                count[x] += 1
            L[x][y][z] = int(L[x][y][z])

timeo = 0
for x in range(number_of_problems):
    start_time = time.time()
    search = TreeSearch()
    solve = search.depth_first(L[x], size[x])
    if solve:
        print("")
    else:
        print("")
    timeo += (time.time() - start_time)
    # if timeo >= 10
        # print("\n\nTime's Up")
        # break
