from itertools import combinations

class Node(object):
    """A node of a tree"""

    def __init__(self, name, weight, children):
        """name: The name for the node
        weight (num): The weight on the node
        children (list): A list of child nodes
        """
        self.name = name
        self.weight = weight
        self.children = set(children)
        
    def __repr__(self):
        return "Node(name={}, weight={}, children={})".format(self.name, self.weight, self.children)
    
    def add_node(self, node):
        """node (Node): The node to add
        """
        self.children.add(node)
        
    def possible_aggregations(self):
        """Show the possible aggregations of the current node
        """
        x = self.children | {self} 
        return(combinations(x, 2))
        
    def aggregate(self):
        """Aggregate this node
        """
        possible_aggs = self.possible_aggregations()
        results = set()
        for agg in possible_aggs:
            n = Node(
                    name="(" + str(agg[0].name) + "," + str(agg[1].name) + ")", 
                    weight = agg[0].weight + agg[1].weight,
                    children=agg[0].children|agg[1].children)
            if agg[0].name != self.name and agg[1].name != self.name:
               n = Node(name=self.name, weight=self.weight, children = [n])
            results.add(n)
        return results
        
    @staticmethod
    def tree_aggregate(tree):
        for node in tree:
            