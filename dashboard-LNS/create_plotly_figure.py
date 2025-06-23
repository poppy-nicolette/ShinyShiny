#create_plotly_figure()

import networkx as nx
import plotly.graph_objects as go

def create_plotly_figure(G, node_attributes):
    # Identify the largest connected component
    largest_cc = max(nx.connected_components(G), key=len)
    subgraph = G.subgraph(largest_cc).copy()

    # Create a figure and axis
    try:
        pos = nx.forceatlas2_layout(subgraph)
        print("Layout calculation completed.")
    except Exception as e:
        print(f"Error in spring layout calculation: {e}")
        return go.Figure()  # Return an empty figure if layout calculation fails

    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.2, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in subgraph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += (x0, x1, None)
        edge_trace['y'] += (y0, y1, None)

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
            ),
            line_width=2))

    for node in subgraph.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)
        node_trace['marker']['color'] += (subgraph.nodes[node].get('cluster_louvain', 0),)  # Default to 0 if attribute is missing
        node_trace['text'] += (f"Label: {subgraph.nodes[node].get('label', 'N/A')}<br>Cluster: {subgraph.nodes[node].get('cluster_louvain', 0)}<br>Degree: {subgraph.nodes[node].get('degree', 0)}<br>Closeness: {subgraph.nodes[node].get('closeness', 0)}<br>Eigen Centrality: {subgraph.nodes[node].get('eigen_centrality', 0)}",)


    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        annotations=[dict(
                            text="Python code: <a href='https://plotly.com/ipython-notebooks/network-graphs/'> https://plotly.com/ipython-notebooks/network-graphs/</a>",
                            showarrow=False,
                            xref="paper",
                            yref="paper",
                            x=0.005, y=-0.002)],
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)))

    return fig