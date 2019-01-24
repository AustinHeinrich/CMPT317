# Austin Heinrich
# awh055
# 11177796
# CMPT 317

   def best_mutator(self, mut_seq):
        """
        Alters a single operator in a sequence, choosing the best alteration
        :param mut_seq - a list of [operator (string), operand (double)]
        :return best_neighbour - the best mutated sequence, closer to the target or as close as the original
        """

        operations = ["ADD", "SUB", "DIV", "MUL", "NOP"]
        neighbour = copy.deepcopy(mut_seq)
        best_neighbour = copy.deepcopy(mut_seq)
        count = 0

        # compute every possible neighbour, choose the best one
        while count < len(mut_seq):
            operations.remove(neighbour[count][0])  # remove the already used operator to avoid repeats
            # print(best_neighbour)

            for an_operation in operations:
                neighbour[count][0] = an_operation

                best_R = self.machine_exec(best_neighbour)  # the best register
                working_R = self.machine_exec(neighbour)    # the current register

                # takes the largest value between R and the target for subtraction reasons
                temp = max(best_R, self.target)
                diff = temp - min(best_R, self.target)

                temp2 = max(working_R, self.target)
                diff2 = temp2 - min(working_R, self.target)

                # compare the difference between the target and the two extant R's, if the neighbour performs worse
                #   than the current best neighbour, it is discarded. However, if it is better than or equal to it
                #   is taken
                if diff2 <= diff:
                    best_neighbour = copy.deepcopy(neighbour)

            neighbour = copy.deepcopy(mut_seq)
            operations = ["ADD", "SUB", "DIV", "MUL", "NOP"]  # restore the full list of operators
            count += 1

        return best_neighbour


        def hill_climbing_search(self, problem, iter_limit):
        """
        Mutates the current best_guess by one operator, but this operator is always the *best* operator to mutate by
            i.e. the operator that gets the sequence closer to the target. If no such operator exists, the current
            best_guess is returned. Forms "hills", points where we can't get to the optimal solution but can get to *a*
            solution --- note that the optimal solution would just be the peak of another "hill"
        :param problem - a Problem object
        :param iter_limit - a timer, the number of times this is allowed to iterate.
        :return: best_guess - the closest we can get to the target, T, within the allotted time or on the current hill
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
                # this line changes an operator so that guess gets closer to the Target
                # takes in best_guess
                guess = problem.best_mutator(best_guess)

                best_R = problem.machine_exec(best_guess)  # the best register
                working_R = problem.machine_exec(guess)    # the current register

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
                        print("Count:", count)
                        return best_guess

        return best_guess
