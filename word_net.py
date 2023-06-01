import pandas as pd
import networkx as nx
from pyvis.network import Network

# Load the data from the CSV file
df = pd.read_csv('./words_nx.csv')

# Create a networkx graph
G = nx.from_pandas_edgelist(df, 'Origen', 'Destino', ['frequency'])

# Get the top 100 words with the highest degree
top_words = sorted(G.degree, key=lambda x: x[1], reverse=True)[:100]

# Create a subgraph with the top words
subgraph = G.subgraph([word for word, _ in top_words])

# Calculate node sizes based on degree
node_sizes = dict(subgraph.degree())
max_degree = max(node_sizes.values())
node_sizes = {node: size / max_degree * 100 for node, size in node_sizes.items()}

# Calculate node degrees for the subgraph
node_degrees = dict(subgraph.degree())

# Calculate edge widths based on node degrees
edge_widths = {(source, target): node_degrees[source] + node_degrees[target] for source, target in subgraph.edges()}

# Normalize edge widths to a reasonable range for visualization
max_width = max(edge_widths.values())
edge_widths = {edge: width / max_width * 10 for edge, width in edge_widths.items()}

# Create a network visualization
network = Network(height="750px", width="100%", notebook=False)

# Add nodes with custom sizes and labels
for node, size in node_sizes.items():
    network.add_node(node, size=size, label=node, title=node, font={'size': size})

# Add edges with custom widths
for edge, width in edge_widths.items():
    source, target = edge
    network.add_edge(source, target, value=width, width=width)

# Set the physics layout of the network
network.barnes_hut(gravity=-17650, central_gravity=0.3)

network.show_buttons(filter_=['physics'])

# Save the network as an HTML file
network.show("network.html")