# Austin Heinrich
# awh055
# 11177796
# CMPT 317

def random_restart_hc(self, problem, iter_limit, restart_limit):
       """
       This search strategy repeats hill climbing search multiple times, taking the best answer out of all searches.
       :param problem - a Problem object
       :param iter_limit - the number of times a steps hill-climbing is allowed
       :param restart_limit - the number of times hill-climbing restarts
       :return best_guess - the closest we can get to the target, T
       """

       # initialize to a hill climbing solution
       best_guess = self.hill_climbing_search(problem, iter_limit)
       print("INITIAL:", str(best_guess) + ", " + str(problem.machine_exec(best_guess)))

       while restart_limit > 0:
           guess = self.hill_climbing_search(problem, iter_limit)

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
                   return best_guess

           restart_limit -= 1  # decrement the number of restarts remaining

       return best_guess
