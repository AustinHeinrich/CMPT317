# Austin Heinrich
# awh055
# 11177796
# CMPT 317


    def stochastic_mutator(self, mut_seq):
        """
        Alters a single operator in a sequence, choosing a better neighbour from a list of better neighbours
        :param mut_seq - a list of [operator (string), operand (double)]
        :return best_neighbour - the best mutated sequence, closer to the target or as close as the original
        """

        operations = ["ADD", "SUB", "DIV", "MUL", "NOP"]
        neighbour = copy.deepcopy(mut_seq)
        best_neighbour_list = []
        count = 0

        # compute every possible neighbour, choose the best one
        while count < len(mut_seq):
            operations.remove(neighbour[count][0])  # remove the already used operator to avoid repeats
            for an_operation in operations:
                neighbour[count][0] = an_operation

                best_R = self.machine_exec(mut_seq)       # the register for the inputted sequence
                working_R = self.machine_exec(neighbour)  # the current register

                # takes the largest value between R and the target for subtraction reasons
                temp = max(best_R, self.target)
                diff = temp - min(best_R, self.target)

                temp2 = max(working_R, self.target)
                diff2 = temp2 - min(working_R, self.target)

                # compare the difference between the target and the two extant R's, if the neighbour performs worse
                #   than the input sequence, it is discarded. However, if it is better, it is taken and shoved into the
                #   list
                if diff2 < diff:
                    best_neighbour_list.append(neighbour)

            neighbour = copy.deepcopy(mut_seq)
            operations = ["ADD", "SUB", "DIV", "MUL", "NOP"]  # restore the full list of operators
            count += 1

        # make sure the list actually has something! Otherwise, just return the input as best
        if len(best_neighbour_list) > 0:
            best_neighbour = best_neighbour_list[random.randrange(0, len(best_neighbour_list))]
        else:
            best_neighbour = copy.deepcopy(mut_seq)
        return best_neighbour


    def stochastic_hc(self, problem, iter_limit):
        """
        Perform a hill-climb search, but instead of choosing the best neighbour, choose randomly from a list of neighbours
            better than the current sequence.
        :param problem - a Problem object
        :param iter_limit - the number of steps hill-climbing is allowed
        :return best_guess - the closest we can get to the target, T
        """
        # initialize the count and the state
        count = 0
        state = ProblemState(problem.setup(problem.numbers))

        best_guess = state.seq
        print("INITIAL:", str(state.seq) + ", " + str(problem.machine_exec(best_guess)))

        # deepcopy the sequence into problem, allows us to change the sequence within the search
        problem.sequence = copy.deepcopy(state.seq)

        if problem.machine_exec(problem.sequence) == problem.target:
            return best_guess
        else:
            while count < iter_limit:
                count += 1  # a timer
                # this line changes an operator so that guess gets closer to the Target, choosing from a list of better
                #   neighbours
                # takes in best_guess
                guess = problem.stochastic_mutator(best_guess)

                best_R = problem.machine_exec(best_guess)  # the best register
                working_R = problem.machine_exec(guess)  # the current register

                if working_R == problem.target:
                    best_guess = guess
                    # print("Found equal in " + str(count) + ":", best_guess, working_R)
                    break  # break if the target was found before time runs out
                else:
                    # takes the largest value between R and the target for subtraction reasons
                    temp = max(best_R, problem.target)
                    diff = temp - min(best_R, problem.target)

                    temp2 = max(working_R, problem.target)
                    diff2 = temp2 - min(working_R, problem.target)

                    # compare the difference between the target and the two extant R's, if guess has a closer R
                    #   than best_guess, take guess instead
                    if diff2 < diff:
                        best_guess = copy.deepcopy(guess)
                        # print("Found better:", best_guess, working_R)
                    else:
                        # print("Count:", count)
                        return best_guess

        return best_guess
