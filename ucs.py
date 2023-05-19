# importing networkx
import networkx as nx

# importing matplotlib.pyplot
from matplotlib import pyplot as plt, animation

plt.rcParams["figure.figsize"] = [7.50, 6.50]
plt.rcParams["figure.autolayout"] = True

# Graph
graph = {
    "1": ["2", "3"],
    "2": ["4", "5"],
    "3": ["6"],
    "4": ["5", "7"],
    "5": ["6"],
    "6": ["7"],
    "7": []
}

# cost for each traversal from node to node
cost = {
    ('1', '2'): 2, 
    ('1', '3'): 1, 
    ('2', '4'): 5, ('2', '5'): 3, ('3', '6'): 1, ('4', '5'): 2, ('4', '7'): 4, ('5', '6'): 4, ('6', '7'): 1}

# Visited node list
visited = []

# Data Structure for bfs
queue = []


# parent of each node
parent = {}

# list of sets of con
finalAnswer = []

# Goal Node
goalNode = '7'

def ucs(visited, queue, graph, node, goalNode):
    queue.append([0, node])
    
    # answer for node with minimum cost
    answer = []

    answer.append(10**8)

    while len(queue) != 0:
        # Adds priority by sorting
        queue = sorted(queue)

        s = queue.pop()

        s[0] *= -1

        # count
        count = 0

        if s[1] in goalNode:
            # get the position
            index = goalNode.index(s[1])

            # if a new goal is reached
            if answer[index] == 10**8:
                count += 1

            # if the cost is less
            if answer[index] > s[0]:
                answer[index] = s[0]

            # pop the element
            queue.pop()
            
            # pop last node as it's repeated
            visited.pop()
            
            # append goal node since it's reached
            visited.append(goalNode)
            queue = sorted(queue)
            
            if count == len(goalNode):
                return answer       

        if s[1] not in visited:
            
            for next in graph[s[1]]:
                queue.append(
                    [(s[0] + cost[(s[1], next)]) * -1, next]
                )    
            
            visited.append(s[1])

    return answer

goalNodeReached = ucs(visited, queue, graph, "1", goalNode)

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
            # add graph edges with weights
            g.add_edge(int(key), int(graph[key][i]), weight=cost[(key, graph[key][i])])
            linked_edges.append((int(key), int(graph[key][i])))

addGraphNodes()

# Set position of graph nodes g
pos = nx.spring_layout(g)

edge_color_list = ["grey"] * len(g.edges)
node_color_list = ["lightblue"] * len(g.nodes)
labels = nx.get_edge_attributes(g,'weight')

print(g.edges)

nx.draw(
    g,
    pos=pos,
    with_labels=True,
    node_size=1000,
    edge_color=edge_color_list,
    node_color=node_color_list,
    arrows=True,
    arrowstyle="-|>",
    arrowsize=12,
)
nx.draw_networkx_edge_labels(g, pos=pos, edge_labels=labels)


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
 
    totalEdgeWeight = g.edges[finalAnswer[0]]["weight"]
    
    for i in range(frame):
        totalEdgeWeight = totalEdgeWeight + g.edges[finalAnswer[i]]["weight"]

    fig.suptitle("UCS: [%s" % (plotTitle) + "]\n Total Cost = " + str(totalEdgeWeight) + "\n Goal Node = " + goalNode, fontweight="bold")

    getSet = linked_edges.index(finalAnswer[frame])
    edge_color_list[getSet] = "red"
    node_color_list[list(g.nodes).index(int(visited[frame]))] = "grey"
    
    
    if frame == len(finalAnswer) - 1:
        node_color_list[-1] = "grey"
        fig.suptitle(
            "UCS: [%s" % (plotTitle) + ", " + str(list(g.nodes)[-1]) + "]\n Total Cost = " + str(totalEdgeWeight) + "\n Goal Node = " + goalNode, 
            fontweight="bold",
        )

    
    
    nx.draw(
        g,
        pos=pos,
        with_labels=True,
        node_size=1000,
        edge_color=edge_color_list,
        node_color=node_color_list,
        arrows=True,
        arrowstyle="-|>",
        arrowsize=12
    )
    nx.draw_networkx_edge_labels(g, pos=pos, edge_labels=labels)


anim = animation.FuncAnimation(
    fig, animate, frames=len(finalAnswer), interval=1000, repeat=True
)
plt.show()
