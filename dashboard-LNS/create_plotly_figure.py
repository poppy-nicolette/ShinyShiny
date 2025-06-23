# create_plotly_figure.py

import networkx as nx
import plotly.graph_objects as go

def create_plotly_figure(G, node_attributes, pos):
    # Create a figure and axis
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.2, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
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

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += (x,)
        node_trace['y'] += (y,)
        node_trace['marker']['color'] += (G.nodes[node].get('cluster_louvain', 0),)  # Default to 0 if attribute is missing
        node_trace['text'] += (f"Label: {G.nodes[node].get('label', 'N/A')}<br>Cluster: {G.nodes[node].get('cluster_louvain', 0)}<br>Degree: {G.nodes[node].get('degree', 0)}<br>Closeness: {G.nodes[node].get('closeness', 0)}<br>Eigen Centrality: {G.nodes[node].get('eigen_centrality', 0)}",)

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
