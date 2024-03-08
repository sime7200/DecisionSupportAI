import numpy as np
import heapq

#currentState = np.array([0,1,2,3,7,5,4,6,8])
#currentState = np.array([4,3,5,0,1,8,7,2,6])
currentState = np.array([0,5,6,4,2,7,8,1,3])
currentMatrix = currentState.reshape(3, 3)
goalState = np.array([0,1,2,3,4,5,6,7,8])
goalMatrix = goalState.reshape(3, 3)


# Distanza di Manhattan
def h(state, goal):
    dist = 0
    state = np.asarray(state)
    state_matrix = state.reshape(3, 3)
    goal_matrix = goal.reshape(3, 3)

    for i in range(3):
        for j in range(3):
            val = state_matrix[i, j]
            if val != 0:
                goal_position = np.argwhere(goal_matrix == val)[0]
                dist += abs(i - goal_position[0]) + abs(j - goal_position[1])

    return dist


# Restituisce il numero di tessere fuori posto
def h_out_of_place(state, goal):
    state = np.asarray(state).reshape(3, 3)
    goal = np.asarray(goal).reshape(3, 3)

    misplaced_tiles = np.sum(state != goal)
    return misplaced_tiles


# Euristica non utile, per confronti
def h_fake(state, goal):
    return 0


def getNeighbors(cell, array):
    neighbors = []
    state = np.array(array)
    matrixState = state.reshape(3, 3)

    for i,j in enumerate(matrixState):
        for k,l in enumerate(j):
            if l==cell:
                x,y=i,k

    possibleMoves = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]    
    for i,j in possibleMoves:
        # prendo i valori validi
        if 0 <= i < 3 and 0 <= j < 3:
            # escludo la cella che contiene 0
            if(matrixState.item(i,j) != 0):
                neighbors.append(i * 3 + j) # questo ritorna direttamente la cella
    return neighbors


def findZero(arr):
    for i in arr:
        if arr[i] == 0:
            return i


def reconstructPath(finalNode):
    path = []
    while finalNode:
        path.append(finalNode[2])
        finalNode = finalNode[3]
    return path[::-1]



def aStar(initialState, goalState, heuristic=h):
    nodiScoperti = []
    nodiChiusi = set()

    startState = initialState
    startG = 0
    startH = heuristic(initialState, goalState)
    startF = startG + startH
    startNode = (startF, startG, tuple(startState), None)

    heapq.heappush(nodiScoperti, startNode)
    while nodiScoperti:
        currentTuple = heapq.heappop(nodiScoperti)
        _, currentG, currentState, _ = currentTuple
        currentState = np.array(currentState)

        if np.array_equal(currentState, goalState):
            #print("Ancora da aprire:", len(nodiScoperti), "Chiusi:", len(nodiChiusi))
            return reconstructPath(currentTuple)

        currentStateTuple = tuple(currentState)
        if currentStateTuple in nodiChiusi:
            continue

        nodiChiusi.add(currentStateTuple)

        vicini = getNeighbors(0, currentState)
        #print("celle vicino a 0:" + str(ris))
        for neighborCell in vicini: # nel for vado ad aggiungere all'heap e nel while estraggo
            gVal = currentG + 1
            hVal = heuristic(currentState, goalState)
            fVal = gVal + hVal

            neighborState = currentState.copy()
            posZero = findZero(currentState)
            neighborState[neighborCell], neighborState[posZero] = neighborState[posZero], neighborState[neighborCell]
            neighborNode = (fVal, gVal, tuple(neighborState), currentTuple)

            if tuple(neighborState.tolist()) not in nodiChiusi:
                heapq.heappush(nodiScoperti, neighborNode)

    return None






print('\n---INITIAL SITUATION---')
print('\n0 is the empty cell!')
print(currentState.reshape(3, 3))
print("\nSearching...\n")
path = aStar(currentState, goalState)

if path:
    print("\nSolution found!\n")
    for step, state in enumerate(path):
        print(f"Step {step + 1}:", np.asarray(state))
else:
    print("\nNo solution found.")
