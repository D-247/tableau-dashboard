import networkx as nx
import matplotlib.pyplot as plt

def build_poset_Zn_multiplication(n):
    elements = list(range(n))
    G = nx.DiGraph()

    # Define the partial order: a <= b if a = a * b mod n or a == b
    for a in elements:
        for b in elements:
            if a != b and (a == (a * b) % n):
                G.add_edge(a, b)

    # Remove transitive edges to make Hasse diagram
    H = nx.transitive_reduction(G)
    return H

def draw_lattice_Zn(n):
    G = build_poset_Zn_multiplication(n)

    # Print covering projections
    print(f"\nCovering Relations in Z{n} (a = ab or a = b):\n")

    for u, v in G.edges():
        print(f"{u} < {v} is a covering relation")

    # Upper and lower covering projections
    print("\nLower Covering Projections:")
    for node in G.nodes():
        lowers = list(G.predecessors(node))
        if lowers:
            print(f"{node} covers: {', '.join(map(str, lowers))}")
        else:
            print(f"{node} covers: None")

    print("\nUpper Covering Projections:")
    for node in G.nodes():
        uppers = list(G.successors(node))
        if uppers:
            print(f"{node} is covered by: {', '.join(map(str, uppers))}")
        else:
            print(f"{node} is covered by: None")

    # Assign levels for vertical layout
    levels = {}
    for node in nx.topological_sort(G):
        preds = list(G.predecessors(node))
        if not preds:
            levels[node] = 0
        else:
            levels[node] = max(levels[p] for p in preds) + 1

    # Position nodes by level
    pos = {}
    level_nodes = {}
    for node, level in levels.items():
        level_nodes.setdefault(level, []).append(node)

    for level, nodes in level_nodes.items():
        width = len(nodes)
        for i, node in enumerate(nodes):
            pos[node] = (i - width / 2, level)

    plt.figure(figsize=(6, 5))
    nx.draw(G, pos, labels={n: str(n) for n in G.nodes()},
            with_labels=True, node_color='lightblue', node_size=1200,
            font_size=14, font_weight='bold', arrows=False)

    # Draw edges manually
    for u, v in G.edges():
        plt.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], 'k')

    plt.title(f"Lattice Diagram of Z{n} (a = ab or a = b)", fontsize=14)
    plt.axis('off')
    plt.show()

draw_lattice_Zn(16)
