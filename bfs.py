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
  '7' : []
}

# Visited node list
visited = []

# Data Structure for bfs
queue = []
parent = {}

# list of sets of con
finalAnswer = []

def bfs(visited, graph, node):
  visited.append(node)
  queue.append(node)

  while len(queue) != 0:
    s = queue.pop(0)
    
    for next in graph[s]:
      if next not in visited:
        visited.append(next)
        queue.append(next)
        finalAnswer.append((int(s), int(next)))


bfs(visited, graph, '1')

# def makeVistedNodeSet():
#   newVisited = list(visited)
#   for i in range(1, len(newVisited)):
#     finalAnswer.append((int(newVisited[i-1]), int(newVisited[i])))
    
# makeVistedNodeSet()

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

nx.draw(g, pos=pos, with_labels = True, node_size=1000, edge_color = edge_color_list, node_color=node_color_list, arrows=True, arrowstyle= '-|>', arrowsize= 12)

# animate graph
def animate(frame):
    plotTitle = ""
    
    
    if frame == 0:
      for i in range(len(edge_color_list)):
        edge_color_list[i] = "grey"
      for i in range(len(node_color_list)):
        node_color_list[i] = "lightblue"
        
    for i in range(frame + 1 if frame <= len(node_color_list) else -1):
      if i == 0:
        plotTitle = plotTitle + visited[i]
        continue
      plotTitle = plotTitle + ", " + visited[i]
    
    fig.suptitle("BFS: [%s"%(plotTitle) + "]", fontweight="bold")
    
    getSet = linked_edges.index(finalAnswer[frame])
    edge_color_list[getSet] = "red"
    node_color_list[frame if frame < len(node_color_list) else -1] = "grey"
    
    if frame == len(finalAnswer) - 1:
      node_color_list[-1] = "grey"
      fig.suptitle("BFS: [%s"%(plotTitle) + ", " + str(list(g.nodes)[-1]) + "]", fontweight="bold")
      
    nx.draw(g, pos=pos, with_labels = True, node_size=1000, edge_color = edge_color_list, node_color=node_color_list, arrows=True, arrowstyle= '-|>', arrowsize= 12)

anim = animation.FuncAnimation(fig, animate, frames=len(finalAnswer), interval=1000, repeat=True)
plt.show()