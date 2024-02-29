# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from collections import defaultdict
import random

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def dfs_rec(problem, v, l, moves, done):
    l[v[0]] = True

    if problem.isGoalState(v[0]):
        done[0] = True
        moves.insert(0, v[1])
        return
    
    for w in problem.getSuccessors(v[0]):
        if done[0]:
            break
        if w[0] not in l.keys():
            dfs_rec(problem, w, l, moves, done)

    moves.insert(0, v[1])

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    
    "*** YOUR CODE HERE ***"
    
    moves = []
    s = []
    l = {}

    done = [False]

    l[problem.getStartState()] = True

    for v in problem.getSuccessors(problem.getStartState()):
        dfs_rec(problem, v, l, moves, done)
        if done[0]:
            break

    return moves

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    moves = []
    queue = []
    l = {}
    parent = {}
    directions = {}
    goal = None

    l[problem.getStartState()] = True
    queue.append(problem.getStartState())

    parent[problem.getStartState()] = None
    directions[problem.getStartState()] = None

    while queue:
        v = queue.pop(0)
        if problem.isGoalState(v):
            goal = v
            break
        for w in problem.getSuccessors(v):
            if w[0] not in l.keys():
                l[w[0]] = True
                parent[w[0]] = v
                queue.append(w[0])
                directions[w[0]] = w[1]

    while parent[goal]:
        moves.insert(0, directions[goal])
        goal = parent[goal]

    return moves

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    moves = []
    queue = util.PriorityQueue()
    explored = []
    cost = {}
    cost[problem.getStartState()] = 0
    queue.push(problem.getStartState(), 0)
    parent = {}
    goal = None

    while not queue.isEmpty():
        v = queue.pop()
        cost_v = cost[v]

        if problem.isGoalState(v):
            goal = v
            break

        if v not in explored:
            explored.append(v)

            for w in problem.getSuccessors(v):
                cost_w = cost_v + w[2]
                if (w[0] not in cost.keys()) or (cost[w[0]] > cost_w):
                    cost[w[0]] = cost_w
                    parent[w[0]] = (v, w[1])
                    queue.push(w[0], cost_w)

    while goal != problem.getStartState():
        v = parent[goal]
        moves.insert(0, v[1])
        goal = v[0]

    return moves

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    openSet = util.PriorityQueue()
    cameFrom = {}

    gScore = defaultdict(lambda: float('inf'))
    gScore[problem.getStartState()] = 0

    fScore = defaultdict(lambda: float('inf'))
    fScore[problem.getStartState()] = heuristic(problem.getStartState(), problem)

    openSet.push(problem.getStartState(), fScore[problem.getStartState()])

    goal = None
    moves = []

    while not openSet.isEmpty():
        current = openSet.pop()

        if problem.isGoalState(current):
            goal = current
            break
    
        for neighbour in problem.getSuccessors(current):
            tentativeGScore = gScore[current] + neighbour[2]

            if tentativeGScore < gScore[neighbour[0]]:
                cameFrom[neighbour[0]] = (current, neighbour[1])
                gScore[neighbour[0]] = tentativeGScore
                fScore[neighbour[0]] = tentativeGScore + heuristic(neighbour[0], problem)
                openSet.update(neighbour[0], fScore[neighbour[0]])

    while goal != problem.getStartState():
            v = cameFrom[goal]
            moves.insert(0, v[1])
            goal = v[0]

    return moves

def fScoreFunc(g, h, w):
    if g < h:
        return g + h
    else:
        return (g + (2 * w - 1) * h) / w

def weightedAStarSearch(problem, weight = 1.5, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    openSet = util.PriorityQueue()
    cameFrom = {}

    gScore = defaultdict(lambda: float('inf'))
    gScore[problem.getStartState()] = 0

    fScore = defaultdict(lambda: float('inf'))
    fScore[problem.getStartState()] = fScoreFunc(0, heuristic(problem.getStartState(), problem), weight)

    openSet.push(problem.getStartState(), fScore[problem.getStartState()])

    goal = None
    moves = []

    while not openSet.isEmpty():
        current = openSet.pop()

        if problem.isGoalState(current):
            goal = current
            break
    
        for neighbour in problem.getSuccessors(current):
            tentativeGScore = gScore[current] + neighbour[2]

            if tentativeGScore < gScore[neighbour[0]]:
                cameFrom[neighbour[0]] = (current, neighbour[1])
                gScore[neighbour[0]] = tentativeGScore
                fScore[neighbour[0]] = fScoreFunc(tentativeGScore, heuristic(neighbour[0], problem), weight)
                openSet.update(neighbour[0], fScore[neighbour[0]])

    while goal != problem.getStartState():
            v = cameFrom[goal]
            moves.insert(0, v[1])
            goal = v[0]

    return moves

def randomSearch(problem):
    stack = util.Stack()
    stack.push(problem.getStartState())
    visited = []
    visited.append(problem.getStartState())
    cameFrom = {}
    moves = []
    goal = None
    while not stack.isEmpty():
        currentState = stack.pop()
        if problem.isGoalState(currentState):
            goal = currentState
            break
        
        successors = problem.getSuccessors(currentState)
        next = random.choice(successors)
        successors.remove(next)

        while next[0] in visited:
            if len(successors) == 0:
                break
            next = random.choice(successors)
            successors.remove(next)

        if next[0] not in visited:
            cameFrom[next[0]] = (currentState, next[1])
            stack.push(next[0])
            visited.append(next[0])

    if goal == None:
        return []

    while goal != problem.getStartState():
        v = cameFrom[goal]
        moves.insert(0, v[1])
        goal = v[0]

    return moves


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
wastar = weightedAStarSearch
rs = randomSearch