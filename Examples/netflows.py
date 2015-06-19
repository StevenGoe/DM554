import networkx as nx
import matplotlib.pyplot as plt

print("Verify that Networkx version is 1.9.1 and above.")
print("Networkx version is: %s" % nx.__version__)

# === Helper functions ===
# Scroll down to network definition

def edges_to_labels(edges, flow_dict={}):
    d = dict()
    for e in edges:
        edge = G.edge[e[0]][e[1]]
        lb   = "%g" % 0
        cap  = ("%g" % edge["capacity"]) if "capacity" in edge else "inf"
        cost = ("%g" % edge["weight"])   if "weight"   in edge else "0"
        sol  = " "
        if e[0] in flow_dict:
            if e[1] in flow_dict[e[0]]:
                sol = "%g" % flow_dict[e[0]][e[1]]
        d[e] = "%s/%s/%s, %s" % (lb, sol, cap, cost)
    return d

def nodes_to_labels(nodes):
    d = dict()
    for n in nodes:
        node = G.node[n]
        bal  = ("%g" % node["demand"]) if "demand" in node else "0"
        d[n] = bal
    return d

def draw_graph(G, flow_dict={}):
    pos = nx.spectral_layout(G)
    nx.draw(G, pos = pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edges_to_labels(G.edges(), flow_dict))
    offset = (0.02, 0.07)
    for p in pos:
        pos[p][0] += offset[0]
        pos[p][1] += offset[1]
    nx.draw_networkx_labels(G, pos, labels=nodes_to_labels(G.nodes()))

    # Show
    #plt.draw()
    # Alternatively, save as file
    plt.savefig("plot-netflows.png")

# === Network definition ===

# Methods:
#G.add_node('a', demand = -5) # demand: balance
#G.add_edge('a', 'b', weight = 3, capacity = 4) # Creates edge with 0/x/capacity, weight

G = nx.DiGraph()
G.add_node('s', demand=-5)
G.add_edge('s','a', capacity=3.0)
G.add_edge('s','b', capacity=1.0)
G.add_edge('a','c', capacity=3.0)
G.add_edge('b','c', capacity=5.0)
G.add_edge('b','d', capacity=4.0)
G.add_edge('d','e', capacity=2.0)
G.add_edge('c','t', capacity=2.0)
G.add_edge('e','t', capacity=3.0)

# === Network drawing ===

# Write this in IPython (without the #)
#%matplotlib inline

draw_graph(G)

# Note: matplotlib draws bolded stubs instead of arrow heads.

# === Solve ===

# --- Max flow ---

flow_value, flow_dict = nx.maximum_flow(G, 's', 't')

print("Max flow value: %g" % flow_value)
print("Max flow solution: %s" % str(flow_dict))

# Alternatively, use Ford-Fulkerson alg:
#flow_dict = nx.ford_fulkerson_flow(G, 's', 't')
#flow_value = nx.cost_of_flow(G, flow_dict)

# --- Min cost flow --- 

#flow_dict = nx.min_cost_flow(G)
#flow_value = nx.cost_of_flow(G, flow_dict)

# --- Max flow min cost ---

#flow_dict = nx.max_flow_min_cost(G, 's', 't')
#flow_value = nx.cost_of_flow(G, flow_dict)

# --- Using simplex ---

#flow_value, flow_dict = nx.network_simplex(G)


# === Draw result with flow ===

draw_graph(G, flow_dict)
