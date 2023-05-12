# importing networkx
import networkx as nx
 
# importing matplotlib.pyplot
from matplotlib import pyplot as plt, animation

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

# Graph
graph = {
  '5' : ['3','7'],
  '3' : ['2', '4'],
  '7' : ['8'],
  '2' : ['4'],
  '4' : ['8'],
  '8' : ['9'],
  '9' : ['10'],
  '10': []
}

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

def getMidLevelNode(node_with_levels):
  mid = len(node_with_levels)/2 + 1 if (len(node_with_levels)/2) % 2 == 1 else len(node_with_levels)/2
  mid = int(mid)
  midLevelNode = list(node_with_levels.keys())[mid-1]
  
  return midLevelNode

midLevelNode = getMidLevelNode(node_with_levels)
visited = [] # List to keep track of visited nodes on search.
queue = [] # Initialize a queue

parent = {}

def bfs(visited, graph, node):
  visited.append(node)
  queue.append(node)

  while queue:
    s = queue.pop(0)
    print (s, end = " ")
    for next in graph[s]:
      if next not in visited:
        visited.append(next)
        queue.append(next)
        # node: parent format
      parent[next] = s

# Driver Code
bfs(visited, graph, '5')

forward_visited = []
backward_visited = []
forward_queue = []
backward_queue = []

finalNodesForward = []
finalNodesBackward = []

def bidirectional(graph, direction):
  
  ind = 0
  if direction == 'forwards':
    forward_visited.append((list(graph.keys())[0]))
    forward_queue.append(list(graph.keys())[0])
    while forward_queue:
      s = forward_queue.pop(0)
      
      if s == midLevelNode:
        break
      
      for next in graph[s]:
        if next not in forward_visited:
          forward_visited.append(next)
          forward_queue.append(next)
          finalNodesForward.append((int(s), int(next)))
          
          ind = ind + 1
        
        if ind == 1:
          ind = 0
          break
  else:
    
    backward_queue.append((list(graph.keys())[-1]))
    backward_visited.append((list(graph.keys())[-1]))
    while backward_queue:
      s = backward_queue.pop(0)
      
      if s == midLevelNode:
        break
      for parentNode in parent[s]:
        backward_queue.append(parentNode)
        backward_visited.append(parentNode)
        finalNodesBackward.append((int(parentNode), int(s)))

bidirectional(graph, "forwards")
bidirectional(graph, "backwards")

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
      
  forwardNode = ""
  backwardNode = ""
  indexForBackward = 0
  indexForForward = 0
  
  maxLengthForForwardNodes = frame if frame < len(finalNodesForward) else len(finalNodesForward)
  maxLengthForBackwardNodes = frame if frame < len(finalNodesBackward) else len(finalNodesBackward)
  
  # forward nodes
  while(indexForForward < maxLengthForForwardNodes):
    if indexForForward == 0:
      forwardNode = forwardNode + forward_visited[indexForForward]
      node_color_list[list(g.nodes).index(int(forward_visited[indexForForward]))] = "grey"
      edge_color_list[linked_edges.index(finalNodesForward[indexForForward])] = "red"
      indexForForward = indexForForward + 1
      continue
    
    forwardNode = forwardNode + ", " + forward_visited[indexForForward]
    
    # color nodes
    node_color_list[list(g.nodes).index(int(forward_visited[indexForForward]))] = "grey"
    edge_color_list[linked_edges.index(finalNodesForward[indexForForward])] = "red"
    
    # color intersection
    if forward_visited[indexForForward+1] == midLevelNode:
      node_color_list[list(g.nodes).index(int(forward_visited[indexForForward+1]))] = "red"
    
    indexForForward = indexForForward + 1
    
  # backward nodes
  while(indexForBackward < maxLengthForBackwardNodes):
    if indexForBackward == 0:
      backwardNode = backwardNode + backward_visited[indexForBackward]
      node_color_list[list(g.nodes).index(int(backward_visited[indexForBackward]))] = "grey"
      edge_color_list[linked_edges.index(finalNodesBackward[indexForBackward])] = "red"
      indexForBackward = indexForBackward + 1
      continue
    backwardNode = backwardNode + ", " + backward_visited[indexForBackward]
    
    # color nodes
    node_color_list[list(g.nodes).index(int(backward_visited[indexForBackward]))] = "grey"
    edge_color_list[linked_edges.index(finalNodesBackward[indexForBackward])] = "red"
    
    # color intersection
    if backward_visited[indexForBackward] == midLevelNode:
      node_color_list[list(g.nodes).index(int(backward_visited[indexForBackward+1]))] = "red"

    indexForBackward = indexForBackward + 1
  
  # combine the two
  # for i in range(frame):
  #   if i == 0:
  #     plotTitle = plotTitle + forwardNode + ", " + backwardNode
  #     continue
  plotTitle = plotTitle + forwardNode + ", " + backwardNode
  
  fig.suptitle("BIDI: [%s"%(plotTitle) + "]", fontweight="bold")
  
  nx.draw(g, pos=pos, with_labels = True, node_size=1000, edge_color = edge_color_list, node_color=node_color_list)

anim = animation.FuncAnimation(fig, animate, frames=len(finalNodesForward) + len(finalNodesBackward), interval=1000, repeat=True)
plt.show()