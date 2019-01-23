# Austin Heinrich
# awh055
# 11177796
# CMPT 317

    def random_guessing(self, problem):
        """
        Generates completely random states, remembering the best one.
        :param problem - a Problem object
        :return best_guess - the closest we can get to the target, T, within the allotted time
        """

        # initialize the count and the state
        count = 0
        state = ProblemState(problem.setup(problem.numbers))

        best_guess = state.seq
        print("INITIAL:",  str(state.seq) + ", " + str(problem.machine_exec(best_guess)))

        if best_guess == problem.target:
            return best_guess
        else:
            while count < 10000000:
                count += 1  # a timer
                guess = problem.setup(prob.numbers)  # get a random sequence

                best_R = problem.machine_exec(best_guess)  # the best register
                working_R = problem.machine_exec(guess)    # the current register

                if working_R == problem.target:
                    best_guess = guess
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
                        best_guess = guess
                        # print("Found better:", best_guess, working_R)

        return best_guess
