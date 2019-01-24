# Austin Heinrich
# awh055
# 11177796
# CMPT 317


    def random_search(self, problem, iter_limit):
        """

        :param problem - a Problem object
        :param iter_limit - the amount of times the while-loop will run, functions as a timer
        :return: best_guess - the closest we can get to the target, T, within the allotted time
        """

        # initialize the count and the state
        count = 0
        state = ProblemState(problem.setup(problem.numbers))

        best_guess = state.seq
        print("INITIAL:", str(state.seq) + ", " + str(problem.machine_exec(best_guess)))

        # deepcopy the sequence into problem, allows us to change the sequence within the search
        problem.sequence = copy.deepcopy(state.seq)

        if problem.machine_exec(best_guess) == problem.target:
            return best_guess
        else:
            while count < iter_limit:
                count += 1  # a timer
                guess = problem.mutator(problem.sequence)  # change a random operator

                best_R = problem.machine_exec(best_guess)  # the best register
                working_R = problem.machine_exec(guess)    # the current register

                if working_R == problem.target:
                    best_guess = guess
                    print("Found equal in " + str(count) + ":", best_guess, working_R)
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
                        print("Found better:", best_guess, working_R)

        return best_guess
