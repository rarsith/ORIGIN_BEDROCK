from pymongo import MongoClient
import networkx as nx
import matplotlib.pyplot as plt

# Step 1: Set Up MongoDB Connection
client = MongoClient('mongodb://localhost:27017/')
db = client['Origin_Celestis']
collection = db['New_Era']

# Step 2: Fetch Data
documents = list(collection.find())

# Step 3: Construct Tree Structure
G = nx.DiGraph()

for doc in documents:
    G.add_node(doc['_id'], label=doc.get('entry_name', ''))
    if 'visual_children' in doc and doc['visual_children']:
        for child_id in doc['visual_children']:
            G.add_edge(doc['_id'], child_id)


# Step 4: Visualize the Tree
def draw_tree(graph):
    pos = nx.spring_layout(graph)  # or use any other layout you prefer
    labels = nx.get_node_attributes(graph, 'label')

    plt.figure(figsize=(12, 8))
    nx.draw(graph, pos, with_labels=True, labels=labels, node_size=3000, node_color='lightblue', font_size=10,
            font_weight='bold', arrows=True)
    plt.show()


draw_tree(G)