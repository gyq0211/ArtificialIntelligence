import random

print ("please enter the state of the pancake, as a list of numbers separated with space such as 1 2 3 4 5:")

# state is a tuple that keeps track of 
# 1. self: visited node,
# 2. state: a list that shows where the pancakes are,
# 3. spt: the backward cost, 
# 4. before: list of panckaes before next flipping
class State:
    def __init__(self, state, spt, before):
        self.state = state
        # We add 1 to spt, to show that we made a flip
        self.backward = spt + 1
        # Calling the forward cost, using gap hueristic
        self.forward = heuristic(state)
        # What the paancakes would look like after the flip
        self.before = before + [state]  # The list of the pancake order made before


def heuristic(s):
    # Shows the total number of gaps 
    h = 0
    # For the range ofthe input 
    for i in range(len(s) - 1):
        # Check whether there is a size gap between pancakes
        if abs(s[i] - s[i + 1]) > 1:
            # If so add 1 to total number of gpas 
            h += 1
    return h


# Store the visited nodes
visited = []
# List of the initial input 
initial = [int(x) for x in raw_input().split()]
###### The following line are for creating random tests ######
#list1 = [1, 2, 3, 4, 5]
#initial = random.sample(list1, 5)
##### End of random tests ######

# store the frontier
frontier = [(0, initial, State(initial, 0, []))]


var = 1
while var == 1:
    # Poping the first element of the frontier
    frt = frontier.pop(0)
    #### We didn't use these explicitly, but it was for debugging puposes #####
    nodes = frt[0]
    curr = frt[1]  # the current list of these pancake
    state = frt[2]
    #### End of debugging section #####
    ############## Astar algorithm - beginning #####################
    # once you have more than 1 pancake the Astar would make sense
    # if we have more than 1 pancake, for the number ofpanckaes +1 
    for i in range(2, len(initial)+1):  # table should also be one pancake
        next = curr[i - 1::-1] + curr[i:]  # flip the pancake
        cost = state.backward + state.forward # estimate the cost of the pancake
        if next not in frontier:  # check if the node is in the frontier
            # if it is in the frontier, generate the new state to add to the frontier
            frontier.append((cost, next, State(next, state.backward, state.before)))
        # if next is frontier and the total cost is higheer then it would be replaced
        elif next in frontier and frontier[1][0] > cost:
            frontier.pop(1)  # pop off the 'next state'
            # replace child in the frontier with new chil
            frontier.append((cost, next, State(next, state.backward, state.before)))
    
    if frt[1] == sorted(initial): #If we have the right order 
        print("The initial state is the first line,")
        # the first line will be the initial state
        print("and it will take the following " + str(len(state.before) - 1) + " flips:")
        for i in range(len(state.before)):
            print(state.before[i])
        break
     ############## Astar algorithm - End ####################### 
