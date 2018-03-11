
def simulated_annealing(problem, schedule):
    """
        @param: problem: a problem
        @param: schedule: a mapping from time to "temperature"
    """
    # current <- make_node(problem.initial state)
    while True:
        # T <- schedule(t)
        # if T = 0 then return current
        # next <- randomly selected successor of current
        # delta_E <- next.Value - current.Value
        #if delta_E > 0 then current <- next
        # else current <- next only with probability e^(delta_E/T)
        pass
