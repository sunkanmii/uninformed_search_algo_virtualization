# importing networkx
import networkx as nx
 
# importing matplotlib.pyplot
from matplotlib import pyplot as plt, animation

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

# Graph
graph = {
  '1' : ['2','3'],
  '2' : ['4', '5'],
  '3' : ['6'],
  '4' : ['5'],
  '5' : ['6'],
  '6' : ['7'],
  '7' : ['4'],
  '8' : ['7']
}

# Using a Python dictionary to act as an adjacency list
visited = [] # Set to keep track of visited nodes of graph.
node_with_levels = {}

def getNodeLevels():
  # level starts from zero
  level = 0
  for node in graph:
    if node not in node_with_levels:
      node_with_levels[node] = level
    for next in graph[node]:
      level = node_with_levels[node] + 1
      if next not in node_with_levels:
        node_with_levels[next] = level
              
getNodeLevels()

foundNodeList = []

#function for dls with start and goal node
def dls(visited, graph, node, goal_node, foundGoalNode, limit):   
  if node not in visited:
    print (node)
    visited.append(node)
    if goal_node == node:
      foundNodeList.append(True)
    for next in graph[node]:
      if len(foundNodeList) != 0:
        continue
      if int(node_with_levels[next]) == limit+1:
        continue
      dls(visited, graph, next, goal_node, foundGoalNode, limit)
        
    # Limit
    
limit = 3


# Iterative Deepening Search Python
def iterDeepSearch(src, target, maxDepth):
  # Repeatedly depth-limit search till the
  # maximum depth
  for i in range(maxDepth+1):
    if (len(foundNodeList) == 0):
      visited.clear()
      dls(visited, graph, src, target, False, i)
    else:
      break
  if len(foundNodeList) != 0:
    return True
  return False

# Node we're looking for
end_node = '6'
foundNode = iterDeepSearch(list(graph.keys())[0], end_node, limit)

# list of set
finalAnswer = []

def makeVistedNodeSet():
  newVisited = list(visited)
  for i in range(1, len(newVisited)):
    finalAnswer.append((int(newVisited[i-1]), int(newVisited[i])))

makeVistedNodeSet()

fig = plt.figure()
g = nx.Graph()

linked_edges = []

def addGraphNodes():
  for key in graph:
    for i in range(len(graph[key])):
      g.add_edge(int(key), int(graph[key][i]))
      linked_edges.append((int(key), int(graph[key][i])))

addGraphNodes()

# Set position of graph nodes g
pos = nx.spring_layout(g)

edge_color_list = ["grey"]*len(g.edges)
node_color_list = ["lightblue"]*len(g.nodes)

print(g.edges)

nx.draw(g, pos=pos, with_labels = True, node_size=1000, edge_color = edge_color_list, node_color=node_color_list)

# animate graph
def animate(frame):
  plotTitle = ""
  
  if frame == 0:
    for i in range(len(edge_color_list)):
      edge_color_list[i] = "grey"
    for i in range(len(node_color_list)):
      node_color_list[i] = "lightblue"
      
  for i in range(frame+1):
    if i == 0:
      plotTitle = plotTitle + visited[i]
      continue
    plotTitle = plotTitle + ", " + visited[i]
  
  # set figure title
  fig.suptitle("Iter Deepening Search(\nLevel Limit - " + str(limit) + " \nGoal Node: "+ end_node + " ): [%s"%(plotTitle) + "]", fontweight="bold")
  
  if finalAnswer[frame] not in linked_edges and frame < len(finalAnswer):
    i = 1
    finalAnswer[frame] = (list(finalAnswer[frame])[1], list(finalAnswer[frame])[0])
    
    if finalAnswer[frame] not in linked_edges:
      finalAnswer[frame] = (list(finalAnswer[frame])[1], list(finalAnswer[frame])[0])
      while finalAnswer[frame] not in linked_edges and i <= frame:
        finalAnswer[frame] = (list(finalAnswer[frame-i])[0], list(finalAnswer[frame])[1])
        i = i + 1
  
  edge_color_list[linked_edges.index(finalAnswer[frame])] = "red"
  
  indexOfNodeInGraph = list(g.nodes).index(int(visited[frame])) 
  
  node_color_list[indexOfNodeInGraph] = "grey"
  
  if frame == len(finalAnswer) - 1:
    # node_color_list[list(g.nodes).index(int(visited[frame+1]))] = "grey"
    fig.suptitle("Iter Deepening Search (\nLevel Limit - " + str(limit) + " \nGoal Node: "+ end_node + " ): [%s"%(plotTitle + ", " + visited[frame+1]) + "]", fontweight="bold")
  
  if list(g.nodes)[list(g.nodes).index(int(visited[frame]))] == int(end_node) and foundNode:
    node_color_list[list(g.nodes).index(int(visited[frame]))] = "red"
    edge_color_list[linked_edges.index(finalAnswer[frame])] = "red"
    
    
  if frame == len(finalAnswer) - 1 and foundNode and list(g.nodes)[list(g.nodes).index(int(visited[frame+1]))] == int(end_node):
    node_color_list[list(g.nodes).index(int(visited[frame+1]))] = "red"
    edge_color_list[linked_edges.index(finalAnswer[frame])+1] = "red"
    # reset what was set
    edge_color_list[linked_edges.index(finalAnswer[frame])] = "grey"
    node_color_list[indexOfNodeInGraph] = "grey"
  
  nx.draw(g, pos=pos, with_labels = True, node_size=1000, edge_color = edge_color_list, node_color=node_color_list)

anim = animation.FuncAnimation(fig, animate, frames=len(finalAnswer), interval=1000, repeat=True)
plt.show()