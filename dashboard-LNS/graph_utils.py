# graph_utils.py

"""
Contains two functions:
    create_network_graph(nodes_file_path, edges_file_path)
    create_plotly_figure(G)
"""

import networkx as nx
import plotly.graph_objects as go

def create_network_graph(nodes_file_path, edges_file_path):
    import csv

    # Read nodes from CSV
    with open(nodes_file_path, 'r') as nodescsv:
        nodereader = csv.reader(nodescsv)
        nodes = [n for n in nodereader][1:]  # Skip header

    node_attributes = {}

    for n in nodes:
        try:
            node_attributes[n[7]] = {
                'cluster_louvain': int(n[2]) + 1,  # Add 1 to cluster_louvain
                'degree': int(n[4]),
                'closeness': float(n[5]),
                'eigen_centrality': float(n[6]),
                'label':str(n[7])
            }
            #debugging
            #print(f"Node: {n[7]}, Attributes: {node_attributes[n[7]]}")  # Debugging: Print node a
        except (ValueError, IndexError) as e:
            print(f"Error processing node {n}: {e}")

    # Read edges from CSV
    with open(edges_file_path, 'r') as edgescsv:
        edgereader = csv.reader(edgescsv)
        edges = [tuple(e) for e in edgereader][1:]  # Skip header

    # Extract only source and target nodes for edges
    edges2 = [(e[0], e[1]) for e in edges]

    # Initialize graph
    G = nx.Graph()

    #add nodes with attributes
    for node, attrs in node_attributes.items():
        G.add_node(node,**attrs)
        #print(node,attrs)

    #add edges
    G.add_edges_from(edges2)

    # Optionally, you can add edge attributes if needed
    for e in edges:
        G.edges[e[0], e[1]]['weight'] = e[2]
        G.edges[e[0], e[1]]['type'] = e[3]

    #debugging
    #for node, data in G.nodes(data=True):
    #    print(f"graph node: {node}, attributes: {data}")

    return G, node_attributes


