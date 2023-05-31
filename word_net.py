import pandas as pd
from pyvis.network import Network
import random

# Create a sample dataframe with 50,000 edges
n = 50000
data = {
    'Source': [f'Word_{i}' for i in range(n)],
    'Target': [f'Word_{i+1}' for i in range(n)],
    'Weight': [random.randint(1, 10) for _ in range(n)]
}

df = pd.DataFrame(data)

# Create a network visualization
network = Network(height="750px", width="100%", notebook=False)

# Get the top 50 words with the highest degree
top_words = df['Source'].value_counts().nlargest(50).index.tolist()

# Add nodes
network.add_nodes(top_words)

# Add edges
filtered_df = df[df['Source'].isin(top_words) & df['Target'].isin(top_words)]
edges = zip(filtered_df['Source'], filtered_df['Target'], filtered_df['Weight'])
for source, target, weight in edges:
    network.add_edge(source, target, value=weight)

# Set the physics layout of the network
network.barnes_hut()

# Save the network as an HTML file
network.set_options(
    """
    const options = {
  "nodes": {
    "borderWidth": null,
    "borderWidthSelected": null,
    "opacity": null,
    "font": {
      "size": 81
    },
    "size": 117
  },
  "edges": {
    "color": {
      "inherit": true
    },
    "selfReferenceSize": null,
    "selfReference": {
      "angle": 0.7853981633974483
    },
    "smooth": {
      "forceDirection": "none"
    }
  },
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -80000,
      "springLength": 250,
      "springConstant": 0.001
    },
    "minVelocity": 0.75
  }
}
    """
)
network.show("network.html")