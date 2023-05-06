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

print(g.edges)

# nx.draw(g, pos=pos, with_labels = True, node_size=1000, edge_color = edge_color_list)

# animate graph
def animate(frame):
    plotTitle = ""
    if frame == 0:
        plotTitle = visited[0] + ""
        fig.suptitle("BFS: [%s"%(plotTitle) + "]", fontweight="bold")
        
    for i in range(frame):
        plotTitle = plotTitle + visited[i] + ", "
    
    fig.suptitle("BFS: [%s"%(plotTitle) + "]", fontweight="bold")
    
    edge_color_list[frame] = "red"
    nx.draw(g, pos=pos, with_labels = True, node_size=1000, edge_color = edge_color_list)

anim = animation.FuncAnimation(fig, animate, frames=len(linked_edges), interval=1000)
plt.show()