# importing networkx
import networkx as nx
 
# importing matplotlib.pyplot
from matplotlib import pyplot as plt, animation

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

# BFS
graph = {
  '5' : ['3','7'],
  '3' : ['2', '4'],
  '7' : ['8'],
  '2' : [],
  '4' : ['8'],
  '8' : []
}

visited = [] # List to keep track of visited nodes.
queue = []     #Initialize a queue

def bfs(visited, graph, node):
  visited.append(node)
  queue.append(node)

  while queue:
    s = queue.pop(0) 
    print (s, end = " ") 

    for neighbour in graph[s]:
      if neighbour not in visited:
        visited.append(neighbour)
        queue.append(neighbour)

# Driver Code
bfs(visited, graph, '5')

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
    
    fig.suptitle("BFS: [%s"%(plotTitle) + "]", fontweight="bold")
    
    if frame > 0 and frame != len(edge_color_list):
      edge_color_list[frame-1] = "red"
    else:
      edge_color_list[frame] = "red"
    node_color_list[frame] = "grey"
    nx.draw(g, pos=pos, with_labels = True, node_size=1000, edge_color = edge_color_list, node_color=node_color_list)

anim = animation.FuncAnimation(fig, animate, frames=len(linked_edges), interval=1000, repeat=True)
plt.show()