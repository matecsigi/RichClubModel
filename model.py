import sys
import networkx as nx
import igraph
from math import *
import random
import numpy
import matplotlib.pyplot as plt

def euclideanRadius(R):
    """Returns the radius corresponding to the parameter value."""
    return sqrt(random.random()*R*R)

def distance(G, node1, node2, beta=1):
    """Calculates the distance between two points in euclidean space."""
    angle1 = G.node[node1]["angle"]
    angle2 = G.node[node2]["angle"]
    r1 = G.node[node1]["radius"]
    r2 = G.node[node2]["radius"]
    x1 = r1*cos(angle1)
    x2 = r2*cos(angle2)
    y1 = r1*sin(angle1)
    y2 = r2*sin(angle2)
    if G.degree(node2) == 0:
        return sqrt(pow(x2-x1,2)+pow(y2-y1,2))
    else:
        return sqrt(pow(x2-x1,2)+pow(y2-y1,2))/sqrt(G.degree(node2))
    

def addNode(G, id, R):
    """Adds a node to the network assigning coordinates to it."""
    G.add_node(id)
    G.node[id]["radius"] = euclideanRadius(R)
    G.node[id]["angle"] = random.uniform(0, 2*pi)

def kClosest(G, id, k):
    """Returns a list of the k closest nodes of the given node."""
    dists = []
    for nodesPresent in range(0, id):
        dists.append(distance(G, id, nodesPresent))
    return numpy.argsort(dists)[0:min(id, k)]

def addMiddleNode(G, node1, node2, id):
    """Add a new node between two nodes"""
    angle1 = G.node[node1]["angle"]
    angle2 = G.node[node2]["angle"]
    r1 = G.node[node1]["radius"]
    r2 = G.node[node2]["radius"]
    x1 = r1*cos(angle1)
    x2 = r2*cos(angle2)
    y1 = r1*sin(angle1)
    y2 = r2*sin(angle2)

    xMiddle, yMiddle = (x1+x2)/2, (y1+y2)/2
    rMiddle = sqrt(xMiddle*xMiddle+yMiddle*yMiddle)
    angleMiddle = atan(yMiddle/xMiddle)

    G.add_node(id)
    G.node[id]["radius"] = rMiddle
    G.node[id]["angle"] = angleMiddle

def saveGML(G, N, limit):
    """Saves the network in a gml format."""
    g = igraph.Graph(directed=False)
    g.add_vertices(G.nodes())
    for node in G.nodes():
        g.vs[node]["radius"] = G.node[node]["radius"]
        g.vs[node]["angle"] = G.node[node]["angle"]
    g.add_edges(G.edges())
    g.save("richclubModel"+"N"+str(N)+"limit"+str(limit)+"rand"+str(random.randrange(1, 100))+".gml")

def saveRichClubDistribution(G, N, limitDistance):
    rc = nx.rich_club_coefficient(G, normalized=True, Q=500)
    plt.plot(rc.keys(),rc.values())
    pdfName = "richclubModel"+"N"+str(N)+"limit"+str(limitDistance)+"rand"+str(random.randrange(1, 100))+"_rich-club"+".pdf"
    plt.savefig(pdfName, format='pdf')
    plt.close()


if __name__=='__main__':

    N = int(sys.argv[1])
    limitDistance = float(sys.argv[2])
    k = 3
    R = 10

    G = nx.Graph()
    currentNodeID = 0

    for t in range(1, N):
        addNode(G, currentNodeID, R)
        
        midNodeID = currentNodeID
        for node in kClosest(G, currentNodeID, k):
            if distance(G, currentNodeID, node) >= limitDistance:
                midNodeID += 1
                addMiddleNode(G, currentNodeID, node, midNodeID)
                G.add_edge(currentNodeID, midNodeID)
                G.add_edge(midNodeID, node)

            else:
                G.add_edge(currentNodeID, node)

        currentNodeID = midNodeID+1
        
    print "nodes: ",G.number_of_nodes()
    print "edges: ", G.number_of_edges()
    saveGML(G, N, limitDistance)
    saveRichClubDistribution(G, N, limitDistance)
