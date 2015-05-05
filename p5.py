import json
from collections import namedtuple
import heapq


def start():
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    # List of items that can be in your inventory:
    print Crafting['Items']
    # example: ['bench', 'cart', ..., 'wood', 'wooden_axe', 'wooden_pickaxe']

    # List of items in your initial inventory with amounts:
    print Crafting['Initial']
    # {'coal': 4, 'plank': 1}

    # List of items needed to be in your inventory at the end of the plan:
    # (okay to have more than this; some might be satisfied by initial inventory)
    #print Crafting['Goal']
    # {'stone_pickaxe': 2}

    # Dictionary of crafting recipes:
    print Crafting['Recipes']['craft stone_pickaxe at bench']
    #print Crafting['Recipes'].items
    # example:
    # {	'Produces': {'stone_pickaxe': 1},
    #	'Requires': {'bench': True},
    #	'Consumes': {'cobble': 3, 'stick': 2},
    #	'Time': 1
    # }

    Recipe = namedtuple('Recipe',['name','check','effect','cost'])
    all_recipes = []
    for name,rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    print all_recipes







    t_initial = 'a'
    t_limit = 20
    print "bcccccc"
    edges = {'a': {'b':1,'c':10}, 'b':{'c':1}}
    #print t_graph('a').next()
    #print edges.items()
    print search(t_graph, t_initial, t_is_goal, t_limit, t_heuristic)


def make_checker(rule):
     #this code runs once
	 # do something with rule['Consumes'] and rule['Requires']

    def check(state):
        # this code runs millions of times
        return True # or False

    return check


def make_effector(rule):
    # this code runs once
    # do something with rule['Produces'] and rule['Consumes']
	def effect(state):
		# this code runs millions of times
		return state

	return effect


def search(graph, initial, is_goal, limit, heuristic):
    frontier = PriorityQueue()
    frontier.put(initial, 0)
    came_from = {}
    cost_so_far = {}
    #verbose = {}

    came_from[initial] = None
    cost_so_far[initial] = 0
    #verbose[initial] = ("no_action", initial, 0)

    while not frontier.empty():
        current = frontier.get()

        if is_goal(current):
            break

        neighborhood = graph(current)


        for next in neighborhood:

            name, effect, neighborCost = next
            new_cost = cost_so_far[current] + neighborCost

            if effect not in cost_so_far or new_cost < cost_so_far[effect]:
                cost_so_far[effect] = new_cost
                priority = new_cost + heuristic(effect)
                frontier.put(effect, priority)
                came_from[effect] = current
                #verbose[effect] = next

    current = 'c'
    path = [current]
    total_cost = cost_so_far[current]
    while current != 'a':

        current = came_from[current]
        path.append(current)

    '''
    if is_goal(current):
        plan = []
        #total_cost = cost[u]
        while current:
            plan.append(verbose[current])
            current = came_from[current]
        plan.reverse()
        return 0, plan
    else:
        return 0, []
    '''
	#return cost_so_far, came_from, path
    return total_cost, path




def t_graph(state):
    edges = {'a': {'b':1,'c':10}, 'b':{'c':1}}
    for next_state, cost in edges[state].items():
        yield ((state,next_state), next_state, cost)


def t_is_goal(state):
	return state == 'c'


def t_heuristic(state):
	return 0

#print search(t_graph, t_initial, t_is_goal, t_limit, t_heuristic)




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


if __name__ ==  '__main__':

	start()