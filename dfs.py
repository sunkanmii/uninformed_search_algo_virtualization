# importing networkx
import networkx as nx
 
# importing matplotlib.pyplot
from matplotlib import pyplot as plt, animation

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

# DFS
graph = {
  '5' : ['3','7'],
  '3' : ['2', '4'],
  '7' : ['8'],
  '2' : [],
  '4' : ['8'],
  '8' : []
}

# Using a Python dictionary to act as an adjacency list
visited = [] # Set to keep track of visited nodes of graph.

def dfs(visited, graph, node):  #function for dfs 
  if node not in visited:
    print (node)
    visited.append(node)
    for neighbour in graph[node]:
      dfs(visited, graph, neighbour)
print("Following is the Depth-First Search")
dfs(visited, graph, '5')

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
      node_color_list[i] = "lightblue"
      
  for i in range(frame+1):
    if i == 0:
      plotTitle = plotTitle + visited[i]
      continue
    plotTitle = plotTitle + ", " + visited[i]
  
  # set figure title
  fig.suptitle("BFS: [%s"%(plotTitle) + "]", fontweight="bold")
  
  if finalAnswer[frame] not in linked_edges and frame < len(finalAnswer):
    i = 1
    finalAnswer[frame] = (list(finalAnswer[frame])[1], list(finalAnswer[frame])[0])
    
    if finalAnswer[frame] not in linked_edges:
      finalAnswer[frame] = (list(finalAnswer[frame])[1], list(finalAnswer[frame])[0])
      while finalAnswer[frame] not in linked_edges and i < frame:
        finalAnswer[frame] = (list(finalAnswer[frame-i])[0], list(finalAnswer[frame])[1])
        i = i + 1
  
  edge_color_list[linked_edges.index(finalAnswer[frame])] = "red"
  
  
  node_color_list[list(g.nodes).index(int(visited[frame]))] = "grey"
  if frame == len(finalAnswer) - 1:
    node_color_list[list(g.nodes).index(int(visited[frame+1]))] = "grey"
    fig.suptitle("BFS: [%s"%(plotTitle + ", " + visited[frame+1]) + "]", fontweight="bold")
    
  
  nx.draw(g, pos=pos, with_labels = True, node_size=1000, edge_color = edge_color_list, node_color=node_color_list)

anim = animation.FuncAnimation(fig, animate, frames=len(finalAnswer), interval=1000, repeat=True)
plt.show()

