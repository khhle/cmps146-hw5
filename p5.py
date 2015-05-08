import sys
import time
import json
from collections import namedtuple
import heapq


def convert_to_tuple(inventory,items):
    state = []

    for next in items:
        if next in inventory:
            state.append(inventory[next])
        else:
            state.append(0)
    return tuple(state)


def make_item_index_list(items):
    index_list = {}
    index = 0
    for next in items:
        index_list[next] = index
        index += 1
    return index_list


def graph(state):
    for r in all_recipes:
        if r.check(state):
            #print str(r.name) + ' ' + str(r.effect(state))
            yield (r.name, r.effect(state), r.cost)


def make_checker(rule):
     #this code runs once
	 # do something with rule['Consumes'] and rule['Requires']
    consumes = {}
    requires = {}

    if 'Consumes' in rule:
        consumes = rule['Consumes']
        print consumes
    if 'Requires' in rule:
        requires = rule['Requires']


    def check(state):
        # this code runs millions of times
        for next in consumes:
            index = items_index_list[next]
            if consumes[next] > state[index]:
                return False

        for next in requires:
            index = items_index_list[next]
            if requires[next] > state[index]:
                return False

        return True # or False

    return check


def make_effector(rule):

    # this code runs once
    # do something with rule['Produces'] and rule['Consumes']

    consumes = {}
    produces = {}

    if 'Consumes' in rule:
        consumes = rule['Consumes']
    if 'Produces' in rule:
        produces = rule['Produces']



    def effect(state):
        # this code runs millions of times
        next_state = list(state)

        for item in produces:
            next_state[items_index_list[item]] += produces[item]

        for item in consumes:
            next_state[items_index_list[item]] -= consumes[item]

        return tuple(next_state)

    return effect


def is_goal(current_state):
    goal_state = convert_to_tuple(goal,items)
    for i in range(0, len(goal_state)):
        if current_state[i] < goal_state[i]:
            return False
    return True

def heuristic(state,last_state):

    #limit non consumable item to 1
    for item in non_consumables:
        index = items_index_list[non_consumables[item]]
        if state[index] > goal_state[index] and state[index] > 1:
            return sys.maxint


    #coal limit
    if state[8] > 1 and state[8] > goal_state[8]:
        return sys.maxint

    #ore limit
    if state[2] > 1 and state[2] > goal_state[2]:
        return sys.maxint

    #ingot limit
    if state[5] > 6 and state[5] > goal_state[5]:
        return sys.maxint

    #plank limit
    if state[9] > 4 and state[9] > goal_state[9]:
        return sys.maxint

    #stick limit
    if state[11] > 4 and state[11] > goal_state[11]:
        return sys.maxint

    #wood limit
    if state[14] > 1 and state[14] > goal_state[14]:
        return sys.maxint

    #cobble limit
    if state[3] > 8 and state[3] > goal_state[3]:
        return sys.maxint

    return 0


def search(graph, initial, is_goal, limit, heuristic):
    frontier = PriorityQueue()
    frontier.put(initial, 0)
    came_from = {}
    cost_so_far = {}
    visited = {}

    came_from[initial] = None
    cost_so_far[initial] = 0
    visited[initial] = ("Start", initial, 0)
    i = 0


    t_start = time.time()
    t_deadline = t_start + THINK_DURATION


    while not frontier.empty() and i < limit:
        current = frontier.get()

        if is_goal(current):
            break

        neighborhood = graph(current)

        for next in neighborhood:
            name, effect, neighborCost = next
            new_cost = cost_so_far[current] + neighborCost

            if effect not in cost_so_far or new_cost < cost_so_far[effect]:
                cost_so_far[effect] = new_cost
                priority = new_cost + heuristic(effect,current)
                frontier.put(effect, priority)
                came_from[effect] = current
                visited[effect] = next

        t_now = time.time()
        if t_now > t_deadline:
            print "Time out!!!"
            break

    if not is_goal(current):
        return 0,[]

    print '\nFinish within: ' + str(t_now - t_start) + ' seconds.'
    plan = []
    total_cost = cost_so_far[current]
    while current:
        plan.append(visited[current])
        current = came_from[current]
    plan.reverse()
    return total_cost, plan










#Helper class for search function
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


THINK_DURATION = 30
all_recipes = []
items_index_list = {}
items = []
consumables = {}
non_consumables = {}
inventory = {}
goal = {}
initial_state = []
goal_state = []

#def start():
with open('Crafting.json') as f:
    Crafting = json.load(f)


Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []
for name,rule in Crafting['Recipes'].items():
    #print rule
    checker = make_checker(rule)
    effector = make_effector(rule)
    recipe = Recipe(name, checker, effector, rule['Time'])
    all_recipes.append(recipe)

print "Recipes"  + str(all_recipes)



# List of items that can be in your inventory:
items = Crafting['Items']
print "Items: " + str(items)

#List of all non_consumable items
temp = 0
for i in [0, 1, 4, 6, 7, 12, 13, 15, 16]:
    non_consumables[temp] = items[i]
    temp += 1
print 'Non Consumables: ' + str(non_consumables)

#List of all consumable items
temp = 0
for i in [2, 3, 5, 8, 9, 10, 11, 14]:
    consumables[temp] = items[i]
    temp += 1
print 'Consumables: ' + str(consumables)


# List of items in your initial inventory with amounts:
inventory =  Crafting['Initial']
print "Inventory: " + str(inventory)

# List of items needed to be in your inventory at the end of the plan:
goal = Crafting['Goal']
print "Goal" + str(goal)

goal_state = convert_to_tuple(goal,items)

#keep track of items by index number
items_index_list = make_item_index_list(items)
#print items_index_list

initial_state = convert_to_tuple(inventory,items)
print "Initial state" + str(initial_state)



total_cost = 0
path = []
total_cost, path = search(graph, initial_state, is_goal, 1000000, heuristic)
print "Total cost: " + str(total_cost)
print "Path: " + str(path)








