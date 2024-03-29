# eightpuzzle.py
# --------------
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


import search
import random
import time
import sys
from optparse import OptionParser

# Module Classes

size = 3

class EightPuzzleState:
    """
    The Eight Puzzle is described in the course textbook on
    page 64.

    This class defines the mechanics of the puzzle itself.  The
    task of recasting this puzzle as a search problem is left to
    the EightPuzzleSearchProblem class.
    """

    def __init__( self, numbers ):
        """
          Constructs a new eight puzzle from an ordering of numbers.

        numbers: a list of integers from 0 to 8 representing an
          instance of the eight puzzle.  0 represents the blank
          space.  Thus, the list

            [1, 0, 2, 3, 4, 5, 6, 7, 8]

          represents the eight puzzle:
            -------------
            | 1 |   | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            ------------

        The configuration of the puzzle is stored in a 2-dimensional
        list (a list of lists) 'cells'.
        """
        self.cells = []
        numbers = numbers[:] # Make a copy so as not to cause side-effects.
        numbers.reverse()
        for row in range(size):
            self.cells.append( [] )
            for col in range(size):
                self.cells[row].append( numbers.pop() )
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col

    def isGoal( self ):
        """
          Checks to see if the puzzle is in its goal state.

            -------------
            |   | 1 | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            -------------

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        True

        >>> EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        False
        """
        current = 0
        for row in range(size):
            for col in range(size):
                if current != self.cells[row][col]:
                    return False
                current += 1
        return True

    def legalMoves( self ):
        """
          Returns a list of legal moves from the current state.

        Moves consist of moving the blank space up, down, left or right.
        These are encoded as 'up', 'down', 'left' and 'right' respectively.

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).legalMoves()
        ['down', 'right']
        """
        moves = []
        row, col = self.blankLocation
        if(row != 0):
            moves.append('up')
        if(row != size - 1):
            moves.append('down')
        if(col != 0):
            moves.append('left')
        if(col != size - 1):
            moves.append('right')
        return moves

    def result(self, move):
        """
          Returns a new eightPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """
        row, col = self.blankLocation
        if(move == 'up'):
            newrow = row - 1
            newcol = col
        elif(move == 'down'):
            newrow = row + 1
            newcol = col
        elif(move == 'left'):
            newrow = row
            newcol = col - 1
        elif(move == 'right'):
            newrow = row
            newcol = col + 1
        else:
            raise "Illegal Move"

        # Create a copy of the current eightPuzzle
        newPuzzle = EightPuzzleState([0 for _ in range(size * size)])
        newPuzzle.cells = [values[:] for values in self.cells]
        # And update it to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two eightPuzzles with the same configuration
          are equal.

          >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]) == \
              EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).result('left')
          True
        """
        for row in range(size):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        lines = []
        horizontalLine = ('-' * (4 * size + 1))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

class EightPuzzleSearchProblem(search.SearchProblem):
    """
      Implementation of a SearchProblem for the  Eight Puzzle domain

      Each state is represented by an instance of an eightPuzzle.
    """
    def __init__(self,puzzle):
        "Creates a new EightPuzzleSearchProblem which stores search information."
        self.expanded = 0
        self.puzzle = puzzle

    def getStartState(self):
        return self.puzzle

    def isGoalState(self,state):
        return state.isGoal()

    def getSuccessors(self,state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        self.expanded += 1
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)

EIGHT_PUZZLE_DATA = [[1, 0, 2, 3, 4, 5, 6, 7, 8],
                     [1, 7, 8, 2, 3, 4, 5, 6, 0],
                     [4, 3, 2, 7, 0, 5, 1, 6, 8],
                     [5, 1, 3, 4, 0, 2, 6, 7, 8],
                     [1, 2, 5, 7, 6, 8, 0, 4, 3],
                     [0, 3, 1, 6, 8, 2, 7, 5, 4]]

def loadEightPuzzle(puzzleNumber):
    """
      puzzleNumber: The number of the eight puzzle to load.

      Returns an eight puzzle object generated from one of the
      provided puzzles in EIGHT_PUZZLE_DATA.

      puzzleNumber can range from 0 to 5.

      >>> print loadEightPuzzle(0)
      -------------
      | 1 |   | 2 |
      -------------
      | 3 | 4 | 5 |
      -------------
      | 6 | 7 | 8 |
      -------------
    """
    return EightPuzzleState(EIGHT_PUZZLE_DATA[puzzleNumber])

def createRandomEightPuzzle(moves=100):
    """
      moves: number of random moves to apply

      Creates a random eight puzzle by applying
      a series of 'moves' random moves to a solved
      puzzle.
    """
    puzzle = EightPuzzleState([i for i in range(size * size)])
    for i in range(moves):
        # Execute a random legal move
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """

    return 0

def tileMisplacedHeuristic(state, problem = None):
    count = 0
    current = 0
    for row in range(size):
        for col in range(size):
            if current != state.cells[row][col]:
                count += 1
            current += 1
    return count

def manhattanDistance(position1, position2):
    xy1 = position1
    xy2 = position2
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def manhattanDistanceToCorrectPositionHeuristic(state, problem = None):
    coordinates = [(x, y) for x in range(size) for y in range(size)]
    
    total_distance = 0

    current = 0
    for row in range(size):
        for col in range(size):
            if current != state.cells[row][col]:
                total_distance += manhattanDistance(coordinates[state.cells[row][col]], (row, col))
            current += 1

    return total_distance

def outOfColumnRowHeuristic(state, problem = None):
    coordinates = [(x, y) for x in range(size) for y in range(size)]

    outOfRow = 0
    outOfColumn = 0

    current = 0
    for row in range(size):
        for col in range(size):
            if current != state.cells[row][col]:
                if row != coordinates[state.cells[row][col]][0]:
                    outOfRow += 1
                if col != coordinates[state.cells[row][col]][1]:
                    outOfColumn += 1

    return outOfRow + outOfColumn

def euclideanDistanceToCorrectPositionHeuristic(state, problem = None):
    total_distance = 0
    current = 0
    for row in range (size):
        for col in range (size):
            if current != state.cells[row][col] :
                goal_row, goal_col = divmod(state.cells[row][col], 3)
                total_distance += ((row - goal_row) ** 2 + (col - goal_col) ** 2) ** 0.5
            current += 1    
    return total_distance

def swapHeuristic(state, problem):
    coordinates = [(x, y) for x in range(size) for y in range(size)]

    total_cost = 0
    cells2 = [row [:] for row in state.cells]

    for row in range (size):
        for col in range (size):
            x,y = coordinates[cells2[row][col]]
            if (x != row) or (y != col):
                aux = cells2[row][col]
                cells2[row][col] = cells2[x][y]
                cells2[x][y] = aux
                total_cost += 1
    return total_cost

def StalinSort():
    puzzle = createRandomEightPuzzle(100)
    print('A random puzzle:')
    print(puzzle)

    problem = EightPuzzleSearchProblem(puzzle)
    current = 0
    for row in range (size):
        for col in range (size):
            if current != puzzle.cells[row][col]:
                puzzle.cells[row][col] = 0
            else:
                puzzle.cells[row][col] = current
            current += 1  

    print("\nStalin's hand falls upon this puzzle and it now becomes:")
    print(puzzle)

def readCommand(args):
    parser = OptionParser()
    parser.add_option("--heuristic", dest='heuristic', action="store", type="string", default="null")
    parser.add_option("-s", "--size", dest="size", action="store", type="int", default=3)
    parser.add_option("-f", "--function", dest="function", action="store", type="string", default="astar")
    
    options, arg = parser.parse_args(args)

    if len(arg) != 0:
        print("Commands not understood")
        return

    heuristic = None

    if options.heuristic == "manhattan":
        heuristic = manhattanDistanceToCorrectPositionHeuristic
    elif options.heuristic == "euclidian": 
        heuristic = euclideanDistanceToCorrectPositionHeuristic
    elif options.heuristic == "tileMisplaced":
        heuristic = tileMisplacedHeuristic
    elif options.heuristic == "outOfColumnRow":
        heuristic = outOfColumnRowHeuristic
    elif options.heuristic == "swap":
        heuristic = swapHeuristic
    elif options.heuristic == "null":
        heuristic = nullHeuristic
    else:
        print("No such heuristic found")
        return

    func = None
    if options.function == "StalinSort":
        StalinSort()
        return
    elif options.function == "wastar":
        func = search.weightedAStarSearch
    elif options.function == "astar":
        func = search.aStarSearch
    else:
        print("That function doesn't exist")
        return

    global size 
    size = options.size

    runGame(func, heuristic)

def runGame(func, heuristic):
    puzzle = createRandomEightPuzzle(30)
    #puzzle = EightPuzzleState([7, 2, 4, 5, 0, 6, 8, 3, 1])
    # puzzle = EightPuzzleState([8, 7, 6, 5, 4, 3, 2, 1, 0])
    # puzzle = EightPuzzleState([5, 0, 8, 1, 4, 2, 3, 6, 7])
    print(puzzle)
    problem = EightPuzzleSearchProblem(puzzle)
    start = time.time()
    path = func(problem=problem, heuristic=heuristic)
    end = time.time()
    print(end - start)
    print("Expanded nodes: %d" % problem.expanded)
    print('A* found a path of %d moves: %s' % (len(path), str(path)))
    curr = puzzle
    i = 1
    for a in path:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i>1], a))
        print(curr)

        raw_input("Press return for the next state...")   # wait for key stroke
        i += 1

if __name__ == '__main__':
    args = readCommand(sys.argv[1:])