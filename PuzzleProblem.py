from collections import deque
import queue
import time
class State:
    def __init__(self, tiles):
        self.tiles = tiles
        # self.prev = None

    def copy(self):
        tiles=[]
        for i in range(len(self.tiles)):
            tiles.append([])
            for j in range(len(self.tiles[i])):
                tiles[i].append(self.tiles[i][j])
        return State(tiles)        

    # get all possible valid neighbor states
    def get_neighbor(self):
        N=len(self.tiles)
        neighbors=[]
        row =0
        col=0
        # find blank
        for i in range(N):
            for j in range(N):
                if self.tiles[i][j]==" ":
                    row=i
                    col=j
        
        for [i,j] in [[row-1,col],[row+1,col],[row,col-1],[row,col+1]]:
            if i>=0 and j>=0 and i<N and j<N:
                n=self.copy()

                n.tiles[row][col], n.tiles[i][j]  =  n.tiles[i][j], n.tiles[row][col]
                neighbors.append(n)  
        
        return neighbors
    
    
    def is_goal(self,goal):
        return self.tiles == goal
    

    def __str__(self):
        s = ""
        for row in self.tiles:
            s += " ".join(str(x) for x in row) + "\n"
        return s
    
    def __repr__(self):
        s = ""
        for row in self.tiles:
            s += " ".join(str(x) for x in row) + "\n"
        return s

    def __eq__(self, other):
        return self.tiles == other.tiles

    def __hash__(self):
     return hash(str(self.tiles))
    

# def find_index_2d(nested_array, value):
#     for row, array in enumerate(nested_array):
#         for column in range(len(array)):
#             if array[column] == value:
#                 return (row, column)
    
    
class Node:
    def __init__(self, state: State, parent=None, cost=0, depth=0, hue=0):
        self.state = state
        self.parent = parent
        self.cost = cost
        self.depth = depth
        self.action = []
        self.hue = hue
        


    def path(self):
        node=self
        Path=[]
        while node:
            Path.append(node.state)
            node= node.parent
        return list(reversed(Path))

    def __repr__(self):
        return self.state.__repr__()
    
    
    
class GraphSearch:
    def __init__(self,graph):
        self.graph=graph

    def bfs(self,start,goal):
        start_time=time.time()
        frontier = deque([Node(start)]) 
        explored=[]
        step=1
        while frontier:
            if step==15:
                print ("arrive 15 step")
                break
            frontier_states=[n.state for n in frontier]
            print ("step ",step)
            print("F:",frontier_states,"E:",explored)
            print ("_____________________________________________")
            step+=1
            node = frontier.popleft()
            if node.state==goal:
                end_time=time.time()
                print(f"Total time: {end_time-start_time} seconds")
                return node.path()
            if node.state not in explored:
                explored.append(node.state)
                for (neighbor,cost) in sorted(self.graph[node.state]):
                    if neighbor not in explored and all(n.state !=neighbor for n in frontier):
                        frontier.append(Node(neighbor,parent=node))
        
        print("goal not found")
        return None
    def dfs(self,start,goal):
        start_time=time.time()
        frontier=[Node(start)]
        explored=[]
        step=1
        while frontier:
            if step==15:
                break
            frontier_states=[n.state for n in frontier]
            print ("step ",step)
            print("F:",frontier_states,"E:",explored)
            print ("_____________________________________________")
            step+=1
            node=frontier.pop()
            if node.state==goal:
                end_time=time.time()
                print(f"Total time: {end_time-start_time} seconds")
                return node.path()
            if node.state not in explored:
                explored.append(node.state)
                for (neighbor,cost) in sorted(self.graph[node.state]):
                    if neighbor not in explored and all(n.state!=neighbor for n in frontier):
                        frontier.append(Node(neighbor,parent=node))
        print("goal not found")
        return None
    def ucs(self, start, goal):
        frontier = [Node(start)]
        explored = []
        step = 1

        while frontier:
            frontier.sort(key=lambda n: (n.cost,n.state))
            frontier_states = [(n.state,n.cost) for n in frontier]

            print("step", step)
            print("F:", frontier_states, "E:", explored)
            print("_____________________________________________")
            step += 1

            node = frontier.pop(0)

            if node.state == goal:
                print (f"cost of path = {node.cost}")
                return node.path()

            explored.append(node.state)

            for (neighbor, cost) in sorted(self.graph[node.state]):
                # تكلفة النود الي واصلها + تكلفة الجار
                new_cost = node.cost + cost
                found = False

                # تحقق إن كان الجار موجود في frontier
                for n in frontier:
                    if n.state == neighbor:
                        found = True
                        #
                        if new_cost < n.cost:
                            n.cost = new_cost
                            n.parent = node
                        break

                # لو مش موجود لا في frontier ولا explored
                if not found and neighbor not in explored:
                    frontier.append(Node(neighbor, parent=node, cost=new_cost))

        print("goal not found")
        return None
    def dls(self, start, goal, limit):
        frontier = [Node(start, depth=0)]
        explored = []
        step = 1

        print("Step", step)
        print("Frontier:",[n.state for n in frontier])
        print("Explored:", explored)
        print("-----------------------")

        while frontier:
            node = frontier.pop()
            depth = node.depth
            step += 1

            print("Step", step)
            explored.append(node.state)
            print("Frontier:",[n.state for n in frontier])
            print("Explored:", explored)
            print("-----------------------")

            if node.state == goal:
                print("Goal found!")
                return node.path()

            if depth < limit:
                # نضيف الأبناء للـ frontier
                for (neighbor, cost) in sorted(self.graph[node.state], reverse=True):
                    if neighbor not in explored and all(n.state != neighbor for n in frontier):
                        frontier.append(Node(neighbor, parent=node, depth=depth + 1))
                        print("Step", step)
                        print("Frontier:",[n.state for n in frontier])
                        print("Explored:", explored)
                        print("-----------------------")

        print("Goal not found in this depth limit.")
        return None

    def ids(self, start, goal, max_depth=5):
        for limit in range(max_depth + 1):
            print("\n==============================")
            print(" Depth limit =",limit)
            print("==============================")
            path = self.dls(start, goal, limit)
            if path:
                return path
        return None
    
def bfs_solver(start_state :State, goal_state:State):
    """
    Performs a Breadth-First Search to find a solution to the 8-puzzle.
    """
    # The frontier is a queue of nodes to visit
    time_start=time.time()
    frontier = queue.Queue()
    frontier.put(Node(start_state))

    # The explored set stores states we have already visited to avoid cycles
    explored = {start_state}
    
    step = 1
    print("Starting BFS Traversal...")
    print("_____________________________________________")

    while not frontier.empty():
        # Get the next node from the front of the queue
        node = frontier.get()

        # --- Optional: Print the current step for visualization ---
        print(f"Step {step}: Visiting state (Depth: {node.depth})")
        print(node.state)


# Check if we have reached the goal
        if node.state.is_goal(goal_state.tiles):
            time_end=time.time()
            print(f"Total time: {time_end-time_start} seconds")
            print("Goal Found!")
            return node.path()
        # Mark the state as explored
        explored.add(node.state)
        # neighbors (next possible moves)
        for neighbor_state in node.state.get_neighbor():
            # If we haven't seen this state before...
            if neighbor_state not in explored:
                # ...add it to the the frontier
                new_node = Node(neighbor_state, parent=node, depth=node.depth + 1)
                frontier.put(new_node)
        
        step += 1
        print("_____________________________________________")
    
    # If the frontier becomes empty and we haven't found the goal
    print("Goal not found.")
    return None

def dfs_solver(start_state, goal_state):
    """
    performs a depth first search to find a solution to the 8-puzzle
    
    """
    time_start=time.time()
    frontier = [Node(start_state)]
    explored = []
    step=1
    print("Starting DFS Traversal...")
    print("_____________________________________________")
    while frontier:
        node = frontier.pop()
        print(f"Step {step}: Visiting state (Depth: {node.depth})")
        print(node.state)
        if node.state.is_goal(goal_state.tiles):
            time_end=time.time()
            print(f"Total time: {time_end-time_start} seconds")
            print("Goal Found!")
            return node.path()
        
        explored.append(node.state)
        for neighbor_state in node.state.get_neighbor():
            if neighbor_state not in explored and all(n.state!=neighbor_state for n in frontier):
                new_node = Node(neighbor_state, parent=node, depth=node.depth + 1)
                frontier.append(new_node)
        step+=1
        print("_____________________________________________")
    print("Goal not found.")
    return None
def dls_solver(start_state, goal_state, limit):
    """
    performs a depth limited search to find a solution to the 8-puzzle
    
    """
    time_start=time.time()
    frontier = [Node(start_state, depth=0)]
    explored = []
    step = 1

    print("Starting DLS Traversal...")
    print("_____________________________________________")
    while frontier:
        node = frontier.pop()
        depth = node.depth
        print(f"Step {step}: Visiting state (Depth: {node.depth})")
        print(node.state)
        explored.append(node.state)
        if node.state.is_goal(goal_state.tiles):
            time_end=time.time()
            print(f"Total time: {time_end-time_start} seconds")
            print("Goal Found!")
            return node.path()

        if depth < limit:
            for neighbor_state in node.state.get_neighbor():
                if neighbor_state not in explored:
                    
                    new_node = Node(neighbor_state, parent=node, depth=depth + 1)
                    frontier.append(new_node)
        step += 1
        print("_____________________________________________")

    print("Goal not found in this depth limit.")
    return None

def ids_solver(start_state, goal_state, max_depth):
    """
    performs an iterative deepening search to find a solution to the 8-puzzle
    
    """
    for limit in range(max_depth + 1):
        print("\n==============================")
        print(" Depth limit =",limit)
        print("==============================")
        path = dls_solver(start_state, goal_state, limit)
        if path:
            return path
    return None
def h1(state, goal):
    count = 0
    for i in range(3):
        for j in range(3):
            # مقارنة العنصر في الحالة الحالية مع العنصر في الحالة الهدف
            if state[i][j] != goal[i][j]:
                count += 1
    return count
def h2(state, goal):
    count = 0
    for i in range(3):
        for j in range(3):
        # i,j position in current state   
            for r in range(3):
                for c in range(3):
                    # r,c position in goal state
                    # بنبحث عن العنصر الموجود في الحالة الحالية مكانه وين في الحالة الهدف
                    if goal[r][c]==state[i][j]:
                        # الصف غلط
                        if i!=r:
                            count+=1
                        # العمود غلط
                        if j!=c:
                            count+=1
    return count
def gbfs_solver(start_state: State, goal_state:State , heuristic='h2'):
    time_start=time.time()
    frontier = [Node(start_state)]
    explored = []
    step = 1

    while frontier:
        
        
        if heuristic=='h1':
            frontier.sort(key=lambda n: h1(n.state.tiles, goal_state.tiles))
            
        else:
            frontier.sort(key=lambda n: h2(n.state.tiles, goal_state.tiles))

        print("Step", step)
        print("Frontier:", [n.state.tiles for n in frontier])
        print("Explored:", [s.tiles for s in explored])
        print("-----------------------------------")
        step += 1
        
        node = frontier.pop(0)
        explored.append(node.state)
        max_frontier=0
        if len(frontier)>max_frontier:
            max_frontier=len(frontier)

        if node.state.is_goal(goal_state.tiles):
            print("Goal Found!")
            number_of_explored=len(explored)
            time_end=time.time()
            print(f"Max size of frontier: {max_frontier}")
            print(f"Number of explored nodes: {number_of_explored}")
            print(f"Total time: {time_end-time_start} seconds")
            return node.path()


        for neighbor_state in node.state.get_neighbor():
            if neighbor_state not in explored and all(n.state != neighbor_state for n in frontier):
                frontier.append(Node(neighbor_state, parent=node))

    print("Goal not found.")
    return None

def a_start_solver(start_state:State , goal_state:State,heuristic='h1'):
    frontier=[Node(start_state)]
    explored=[]
    step=1
    while frontier:
        node=frontier.pop(0)
        if heuristic == 'h1':
            h_val = h1(node.state.tiles, goal_state.tiles)
            # f(n)=g(n)+h(n)
            frontier.sort(key=lambda n: n.depth + h_val)
        else:
            h_val = h2(node.state.tiles, goal_state.tiles)
            # f(n)=g(n)+h(n)
            frontier.sort(key=lambda n: n.depth + h_val)


        print ("Step",step)
        print("===================================")
        print(f"Current Node: {node.state.tiles}")
        print(f"g(n) = {node.depth}")
        print(f"h(n) = {h_val}")
        print(f"f(n) = {node.depth + h_val}")
        print("Frontier:",[n.state.tiles for n in frontier])
        print("Explored:", [s.tiles for s in explored])
        print("===================================")
        step += 1

        explored.append(node.state)
        if node.state.is_goal(goal_state.tiles):
            print("Goal Found!")
            return node.path()
        for neighbor_state in node.state.get_neighbor():
            if neighbor_state not in explored and all(n.state!=neighbor_state for n in frontier):
                frontier.append(Node(neighbor_state,parent=node,depth=node.depth+1 , hue=h1(neighbor_state.tiles, goal_state.tiles)))
    print ("Goal not found.")
    return None

def main():
    print("=== General Search System ===")
    print("Choose data type:")
    print("1. Graph search")
    print("2. 8-Puzzle search")

    choice = input("Enter your choice (1 or 2): ")
    if choice == '1':
        print("Graph search selected.")
        graph={
                "S": [("A",2),("C",4)],
                "A": [("B",8),("C",15),("D",5)],
                "C": [("A",15),("B",2),("D",2)],
                "B": [("A",8),("C",2),("D",8),("T",8)],
                "D":[("A",5),("B",8),("C",2),("T",11)],
                "T":[]
            }   
        start = input("Enter start node: ")
        goal = input("Enter goal node: ")
        print("Choose search algorithm:")
        print("1. BFS")
        print("2. DFS")
        print("3. UCS")
        print("4. IDS")
        algo_choice = input("Enter your choice (1-4): ")
        
        search = GraphSearch(graph)
        
        if algo_choice == '1':
            path = search.bfs(start, goal)
            print("Path found by BFS:", path)
        elif algo_choice == '2':
            path = search.dfs(start, goal)
            print("Path found by DFS:", path)
        elif algo_choice == '3':
            path = search.ucs(start, goal)
            print("Path found by UCS:", path)
        elif algo_choice == '4':
            max_depth = int(input("Enter max depth for IDS: "))
            path = search.ids(start, goal, max_depth)
            print("Path found by IDS:", path)
        else:
            print("Invalid choice.")
    
    elif choice == '2':
        print("8-Puzzle search selected.")
        # Define start and goal states here or take input
        state = [[1, 2, 3],
                 [4, " ", 6],
                 [7, 5, 8]]
        
        goal_state = [[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, " "]]
        
        start_state = State(state)
        goal_state = State(goal_state)
        
        print("Choose search algorithm:")
        print("1. BFS")
        print("2. DFS")
        print("3. IDS")
        print("4. GBFS")
        print("5. A* Search")
        algo_choice = input("Enter your choice (1 or 5): ")
        
        if algo_choice == '1':
            solution_path = bfs_solver(start_state, goal_state)
            if solution_path:
                print("\n--- Solution Path ---")
                for i, state in enumerate(solution_path):
                    if i == 15:
                        print("stop printing after 15 moves")
                        break
                    print(f"Move #{i}:")
                    print(state)
            else:
                print("\n--- No Solution Found ---")        
        elif algo_choice == '2':
            solution_path = dfs_solver(start_state, goal_state)
            if solution_path:
                print("\n--- Solution Path ---")
                for i, state in enumerate(solution_path):
                    if i == 15:
                        print("stop printing after 15 moves")
                        break
                    print(f"Move #{i}:")
                    print(state)
            else:
                print("\n--- No Solution Found ---")   
        elif algo_choice == '3':
            max_depth = int(input("Enter max depth for IDS: "))
            solution_path = ids_solver(start_state, goal_state, max_depth)
            if solution_path:
                print("\n--- Solution Path ---")
                for i, state in enumerate(solution_path):
                    if i == 15:
                        print("stop printing after 15 moves")
                        break
                    print(f"Move #{i}:")
                    print(state)
            else:
                print("\n--- No Solution Found ---")  
        elif algo_choice == '4':
            print("siii")
            solution_path = gbfs_solver(start_state, goal_state)
            if solution_path:
                print("\n--- Solution Path ---")
                for i, state in enumerate(solution_path):
                    if i == 15:
                        print("stop printing after 15 moves")
                        break
                    print(f"Move #{i}:")
                    print(state)  
        elif algo_choice == '5':
            solution_path = a_start_solver(start_state, goal_state)
            if solution_path:
                print ("\n--- Solution Path ---")
                for i, state in enumerate(solution_path):
                  if i==15:
                      print ("stop printing after 15 moves")
                      break
                  print (f"Move {i}:")
                  print (state)                          
if __name__ == "__main__":
    main()        