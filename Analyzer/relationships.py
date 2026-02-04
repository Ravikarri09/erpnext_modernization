def analyze_relationships(nodes, edges):
    """
    Analyzes graph relationships.
    """
    adjacency = {}
    for edge in edges:
        source, target = edge
        if source not in adjacency:
            adjacency[source] = []
        adjacency[source].append(target)
    
    return adjacency

def find_orphans(nodes, adjacency):
    orphans = []
    for node in nodes:
        if node not in adjacency:
            orphans.append(node)
    return orphans
