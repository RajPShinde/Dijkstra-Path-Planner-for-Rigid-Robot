import sys
# This try-catch is a workaround for Python3 when used with ROS; 
# it is not needed for most platforms
try:
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
except:
    pass

import time
from collections import defaultdict
import math
import pygame

class NodeInfo:
    """
    A class to store index, cost and node information with parent child relations

    ...
    Attributes
    ----------

    cost : int 
        a cost to move from one point to another based on action
    child_node : list
        a list of elements that will contain child node information
    parent_node : list
        a list of elements that will contain parent node information

    Methods
    -------
    None
    """
    def __init__(self, child_node, cost=math.inf):
        """
        Parameters
        ----------
        cost : int 
        a cost to move from one point to another based on action
        child_node : list
            a list of elements that will contain child node information
        parent_node : list
            a list of elements that will contain parent node information
        """

        self.parent_node = None
        self.child_node = child_node
        self.cost = cost

def inside_obstacle(node):
    """
    This function check if the point is inside an obstacle

    Args:
    node: location of a node on map

    Returns:
        True, if not inside obstacles
    
    """
    x = node[0]
    y = node[1]
    # Rectangle bar half plane conditions
    if y<=(8/5)*x+28 and y<=(-37/70)*x+(643/7) and y>=(9/5)*x-141 and y>=(-19/35)*x+(571/7): return 1
    # Ellipse half plane conditions
    if ((x-150)/(40))**2+((y-100)/(20))**2<=1: return 1
    # Non convex half plane conditions
    if y<=13*x-140 and y<=185 and y<=(-7/5)*x+290 and y>=(6/5)*x+30:
        if (y<=x+100 and y<=(-6/5)*x+210):
            f=0
        else:
            return 1
    # Rhombus half plane conditions
    if y<=(3/5)*x-95 and y>=(3/5)*x-125 and y<=(-3/5)*x+175 and y>=(-3/5)*x+145: return 1
    # Circle half plane conditions
    if (x-225)**2+(y-150)**2<=(25)**2: return 1
    return 0

def cart_to_image_convert(cart_x, cart_y):
    """
    This function is used to cart_to_image_convert cartesian to pygame coordinates

    Args:
    :x: x coordinates
    :y: y coordinates

    Returns:
        Will return a tuple with coordinates.
    """
    return (cart_x * 3, (199 - cart_y) * 3)

def draw_map():
    """
    This function is used to draw the basic map of the area

    Args:
    None

    Returns:
        Will return a frame with the map to be shown
    """
    pygame.init()
    size = (300 * 3, 200 * 3) # Map size
    frame = pygame.display.set_mode((300*3, 200*3)) # Scale it for better view
    frame.fill([255,255,255]) # Background fill to white
    pygame.display.set_caption("Dijsktra Animation") # Name for the frame
    frame.fill([255,255,255])
    # Draw the Rhombus shape
    pygame.draw.polygon(frame,[200,100,255],[cart_to_image_convert(225,40),cart_to_image_convert(250,25),cart_to_image_convert(225,10),cart_to_image_convert(200,25)])
    # Draw the non convex shape
    pygame.draw.polygon(frame,[200,100,255],[cart_to_image_convert(25,185),cart_to_image_convert(75,185),cart_to_image_convert(100,150),cart_to_image_convert(75,120),cart_to_image_convert(50,150),cart_to_image_convert(20,120)])
    # Draw the rectangular bar shape
    pygame.draw.polygon(frame,[200,100,255],[cart_to_image_convert(30,76),cart_to_image_convert(100,39),cart_to_image_convert(95,30),cart_to_image_convert(25,68)])
    # Draw the circle shape
    pygame.draw.circle(frame,[200,100,255],(225*3, (199-150)*3), 25*3)
    # Draw the ellipse shape
    pygame.draw.ellipse(frame,[200,100,255],(110*3, (199-120)*3, 80*3, 40*3))
    # Refresh the frame
    pygame.display.flip()
    return frame

def action_move_left(node):
    """
    This function is an action applied on a node to move left.

    Args:
    node: location of a node on map

    Returns:
        Will return a new node location and cost
    
    """
    cost = 1
    if node[0] > 0 and not inside_obstacle(node):
        return (node[0] - 1, node[1]), cost
    else:
        return None, None
    
def action_move_right(node):
    """
    This function is an action applied on a node to move right

    Args:
    node: location of a node on map

    Returns:
        Will return a new node location and cost
    """
    cost = 1
    if node[0] < 299 and not inside_obstacle(node):
        return (node[0] + 1, node[1]), cost
    else:
        return None, None        

def action_move_up(node):
    """
    This function is an action applied on a node to move up.

    Args:
    node: location of a node on map

    Returns:
        Will return a new node location and cost
    """
    cost = 1
    if node[1] > 0 and not inside_obstacle(node):
        return (node[0], node[1] - 1), cost
    else:
        return None, None

def action_move_down(node):
    """
    This function is an action applied on a node to move down.

    Args:
    node: location of a node on map

    Returns:
        Will return a new node location and cost
    """
    cost = 1
    if node[1] < 199 and not inside_obstacle(node):
        return (node[0], node[1] + 1), cost
    else:
        return None, None

def action_move_up_left(node):
    """
    This function is an action applied on a node to move up left.

    Args:
    node: location of a node on map

    Returns:
        Will return a new node location and cost
    """
    cost = 1.4
    if node[0] > 0 and node[1] > 0 and not inside_obstacle(node):
        return (node[0] - 1, node[1] - 1), cost
    else:
        return None, None

def action_move_up_right(node):
    """
    This function is an action applied on a node to move up right.

    Args:
    node: location of a node on map

    Returns:
        Will return a new node location and cost
    """
    cost = 1.4
    if node[0] < 299 and node[1] > 0 and not inside_obstacle(node):
        return (node[0] + 1, node[1] - 1), cost
    else:
        return None, None

def action_move_down_left(node):
    """
    This function is an action applied on a node to move down left.

    Args:
    node: location of a node on map

    Returns:
        Will return a new node location and cost
    """
    cost = 1.4
    if node[0] > 0 and node[1] < 199 and not inside_obstacle(node):
        return (node[0] - 1, node[1] + 1), cost
    else:
        return None, None

def action_move_down_right(node):
    """
    This function is an action applied on a node to move down right.

    Args:
    node: location of a node on map

    Returns:
        Will return a new node location and cost
    """
    cost = 1.4
    if node[0] < 299 and node[1] < 199 and not inside_obstacle(node):
        return (node[0] + 1, node[1] + 1), cost
    else:
        return None, None

def actions_move(action_type,node):
    """
    This function defines an action set and calls corresponding actions

    Args:
    action_type: string type variable that will give the action input
    node: list of elements that represent a node.

    Returns:
        Will return a new node location and cost
    """
    if action_type == "U":

        return action_move_up(node)
    if action_type == "D":
        return action_move_down(node)
    if action_type == "L":
        return action_move_left(node)
    if action_type == "R":
        return action_move_right(node)
    if action_type == "UL":
        return action_move_up_left(node)
    if action_type == "UR":
        return action_move_up_right(node)
    if action_type == "DL":
        return action_move_down_left(node)
    if action_type == "DR":
        return action_move_down_right(node)
    else:
        return None, None

def my_pop_from_queue(node):
    """
    This is the function to use the list as a priority queue and get min cost

    Args:
    :node: Get the node instance

    Returns:
        Will return the queue node instance with less cost
    """  
    min_a = 0
    for elem in range(len(node)):
        pygame.event.get()
        if node[elem].cost < node[min_a].cost:
            min_a = elem
    return node.pop(min_a)

def find_node(point, node):
    """
    This is the function to find the index of a node

    Args:
    :point: coordinates at which the node is present
    :node: Get the node instance

    Returns:
        Will return the index of the point in the node queue
    """  
    for elem in node:
        pygame.event.get()
        if elem.child_node == point:
            return node.index(elem)
        else:
            return None 

def make_path(node, goal):
    """
    This is the function to make path from start to goal

    Args:
    :node: location of a point on map
    :goal: goal points x and y

    Returns:
        WIll return a list with points from start to goal in optimal path
    """    
    p = list()
    p.append(node.child_node)
    parent = node.parent_node
    if parent is None:
        return p
    while parent is not None:
        pygame.event.get()
        p.append(parent.child_node)
        parent = parent.parent_node
    p_rev = list((p))
    p_rev.append(goal)
    return p_rev

def djikstra_search(start, goal):
    """
    This is the Djikstra function that will loop over all locations

    Args:
    :start: initial location of a point robot on map
    :goal: final locatio of a point robot on map

    Returns:
        WIll return the final node that reaches the goal node
    """
    frame = draw_map()
    start_x = start.child_node[0]
    start_y = start.child_node[1]
    # x, y = cart_to_image_convert(start_x, start_y)
    # gx, gy = cart_to_image_convert(goal[0], goal[1])

    # Get coordinates
    x, y = cart_to_image_convert(start_x, start_y)
    gx, gy = cart_to_image_convert(goal[0], goal[1])

    pygame.draw.rect(frame,[255,0,0],[x, y,4,4])
    pygame.draw.rect(frame,[0,255,0],[gx, gy ,4,4])
    pygame.display.flip()

    start_cost = 0
    
    actions_set = ['R', 'D', 'L', 'U', 'UL', 'UR', 'DL', 'DR']
    start = NodeInfo((start_x, start_y), 0)
    current_heap = [start] # Priority Queue with start node

    visited_nodes = defaultdict(list)
    i = 0
    count = 1
    # loop on the current heap
    while current_heap: 
        pygame.event.get()
        # Greedy search on minimum element
        frontier_node = my_pop_from_queue(current_heap)
        if frontier_node.child_node == goal:
            print("Success Dude")
            animate_exploration(start_x,start_y,goal[0],goal[1],frontier_node,visited_nodes,frame)
            return new_node.parent_node

        if frontier_node.child_node not in visited_nodes.values(): # and not inside_obstacle(new_node_location):
            visited_nodes[i] = frontier_node.child_node

        if frontier_node is not None:
            # loop over all child nodes generated from action set
            for action in actions_set:
                pygame.event.get()
                new_node_location, running_cost = actions_move(action, frontier_node.child_node)
                i += 1
                if new_node_location is not None:
                    if new_node_location == goal:
                        print("Success!")
                        animate_exploration(start_x,start_y,goal[0],goal[1],frontier_node,visited_nodes,frame)
                        return new_node.parent_node

                    new_node = NodeInfo(new_node_location, running_cost)

                    new_node.parent_node = frontier_node
                    # Check if visited, append new cost
                    if new_node_location not in visited_nodes.values() and not inside_obstacle(new_node_location):
                        new_node.cost = running_cost + new_node.parent_node.cost
                        if new_node_location not in visited_nodes.values():
                            visited_nodes[i] = new_node_location
                        current_heap.append(new_node)
                    else:
                        # Since visited, update previous cost
                        node_exist_index = find_node(new_node_location, current_heap)
                        if node_exist_index is not None:
                            temp_node = current_heap[node_exist_index]
                            if temp_node.cost > running_cost + new_node.parent_node.cost:
                                temp_node.cost = running_cost + new_node.parent_node.cost
                                temp_node.parent = frontier
                else:
                    continue
        # print(i)
    return None

def animate_exploration(xs,ys,goal_x,goal_y,frontier_node,visited_nodes,frame):
    """
    This is the animate function

    Args:
    :xs: start x coordinate
    :ys: start y coordinate
    :goal_x: goal x coordinate
    :goal_y: goal y coordinate
    :frontier_node: frontier node that reaches just before the goal
    :visited_nodes: dictionary of all visited nodes
    :frame: frame to be used in pygame

    Returns:
        WIll show the animation accordingly. To quit, user needs to use onscreen buttons
    """
    p = list()
    p.append(frontier_node.child_node)
    parent = frontier_node.parent_node
    final_cost = frontier_node.cost
    if parent is None:
        return p
    while parent is not None:
        p.append(parent.child_node)
        parent = parent.parent_node
    p_rev = list((p))
    p_rev.append((goal_x, goal_y))
    frontier_node = p_rev
    new_list = []
    for item in visited_nodes.values():
        new_list.append(item)
    visited_nodes = new_list
    # Create the visualisation to start on visited nodes
    for i in range(0,len(visited_nodes)):
        # print(i)
        pygame.event.get()
        pygame.event.get()
        pygame.draw.rect(frame,[0,0,255],[(visited_nodes[i][0])*3,(199-visited_nodes[i][1])*3,0.8,0.8])
        pygame.time.wait(1)
        pygame.display.flip()
    pygame.draw.rect(frame,[255,0,0],[(goal_x)*3,(199-goal_y)*3,4,4])

    # Create the path
    count = 0
    while count < len(frontier_node):
        pygame.event.get()
        pygame.event.get()
        pygame.draw.rect(frame,[255,0,0],[(goal_x)*3,(199-goal_y)*3,4,4])
        # print(frontier_node[count])
        (goal_x,goal_y)=frontier_node[count] #[goal_x][goal_y]
        pygame.time.wait(10)
        pygame.display.flip()
        count += 1
    pygame.draw.rect(frame,[255,0,0],[(goal_x)*3,(199-goal_y)*3,4,4])
    print("Done!")
    print("The final cost to reach the goal is: " + str(final_cost))
    print("Press x on graph to exit code.")
    flag = True
    while flag:
        pygame.event.get()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                flag = False
    

def main():
    """
    This is the main function

    Args:
    None

    Returns:
        Will complete the execution of the code
    """
    tic = time.time()
    print("Enter the start and goal coordinates-")
    print("start_x, start_y, goal_x, goal_y: (eg: 5 5 140 14)")
    coordinate_points = [int(x) for x in input().split()]
    if len(coordinate_points) != 4:
        print("Please input start(2) and goal(2) - 4 points: ")
        main()
    # print(coordinate_points, coordinate_points[0], coordinate_points[1])
    start_x = coordinate_points[0]
    start_y = coordinate_points[1]
    goal_x = coordinate_points[2]
    goal_y = coordinate_points[3]
    start_node = NodeInfo((start_x, start_y), 0)
    goal_node = (goal_x, goal_y)
    # print(start_x, start_y, goal_node[0], goal_node[1])

    if goal_node > (300, 200) or (start_x, start_y) > (300,200):
        print("Outside map of the robot. Please try again.")
        main()
    elif inside_obstacle((start_x, start_y)):
        print("Start node inside obstacle. Please try again.")
        main()
    elif (start_x, start_y) < (0, 0) or goal_node < (0, 0):
        print("Outside the map of robot. Please try again.")
        main()    
    elif start_x == goal_node[0] and start_y == goal_node[1]:
        print("Start node is equal to goal node. Please try again.")
        main()
    elif inside_obstacle(goal_node):
        print("Inside goal")
        print("Please try again.")
        main()
    else:
        print("Starting exploration...")
        final_goal_parent = djikstra_search(start_node, goal_node)
        if final_goal_parent is not None:
            nodes_list = make_path(final_goal_parent, goal_node)
            print("The list of coordinates to start position")
            print(nodes_list)

    toc = time.time() # Compute time
    print("Time to compute is " + str((toc-tic)/60) + " mins")

main()