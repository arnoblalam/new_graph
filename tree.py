from __future__ import division
from itertools import combinations
import cPickle
from math import log
import csv
from networkx import nx
import pandas as pd
import collections

def deepcopy(obj):
    """Creates a deep copy of an object
    Args:
        obj (any): The object to copy
    Reutns:
        A copy of the object
    """
    return cPickle.loads(cPickle.dumps(obj, -1))
    
def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el
    
def possible_aggregations(t):
    """Returns the possible aggregations of a tree
    Args:
        t (dict): The tree to aggregate (of the form {node_1: {children}}
     Returns:
        The set of possible aggregations of the tree t
     """
    results = set()
    for level, children in t.iteritems():
        x = children | set([level])
        results |= set(combinations(x, 2))
    return results
    
def merge_nodes(t, nodes_to_merge):
    """Merge two nodes together
    Args:
        t (dict): The tree to aggregate
        node_to_merge (tuple): a tuple of form (node_1, node_2) which will be merged
    Returns:
        A copy of t with the two nodes merged
     """
    copy_of_tree = deepcopy(t)
    a, b = nodes_to_merge
    try:
        children_of_a = t[a] - set([b])
        children_of_b = t[b] - set([a])
    except:
        print t
        raise
    combined_children = children_of_a | children_of_b
    for k, v in copy_of_tree.iteritems():
        if (a in v) or (b in v):
            copy_of_tree[k].discard(a)
            copy_of_tree[k].discard(b)
            copy_of_tree[k].add(frozenset(flatten((a, b))))
    copy_of_tree.pop(a, None)
    copy_of_tree.pop(b, None)
    copy_of_tree[frozenset(flatten((a, b)))] = combined_children
    return copy_of_tree
    
def apply_aggregation(t, node_data, f=lambda x, y: x+y):
    """Create the new tree t by applying the aggregations to weights described in node_data
    Args:
        t (dict): The tree to aggregate
        node_data (dict): A dictionary of the form {node: weight...}
        f (function): an aggregation function that takes two parameters x and y
    Returns:
        A new node_data dictionary with the appropriate aggregations applied
    """
    try:
        result = dict()
        for k, v in t.iteritems():
            if type(k) is not frozenset:
                result[k] = node_data[k]
            else:
                intermediate = 0
                for k_ in k:
                    intermediate += node_data[k_]
                result[k] = intermediate
        return result
    except:
        print(t)
        raise
        
def apply_tuple(t, n, f):
    """Internal function for applying aggregation for tupled keys
    """
    if type(t[0]) is not tuple and type(t[1]) is not tuple:
        return f(n[t[0]], n[t[1]])
    elif type(t[0]) is tuple and type(t[1]) is tuple:
        return f(apply_tuple(t[0], n, f), apply_tuple(t[1], n, f))
    elif type(t[0]) is tuple:
        return f(apply_tuple(t[0], n, f), n[t[1]])
    elif type(t[1]) is tuple:
        return f(n[t[0]], apply_tuple(t[1], n, f))
        
def reduce_tree(t):
    """Reduce a tree one time
    Args:
        t (dict): The tree to reduce
    Returns:
        A list of trees obtained by merging one node at a time
    """
    return [merge_nodes(t, x) for x in possible_aggregations(t)]
    
def reduce_n_times(t, n, node_weights, how_many=5, sort_type="maximum"):
    """Reduces a tree n times
    Args:
        t (dict): The tree to reduce (a dictionary of type {node: set([children])}
        n (int): How many times to reduce the tree
        node_weights (dict): A dictionary of the form {node: weight...}
        how_many (int): How 
        sort_type (str): Either maximum or minimum
    Returns:
        A list of trees obtained by aggregating the trees n times
    """
    results = []
    current_batch = [t]
    results += current_batch
    for _ in range(n):
        temp_batch = []
        for t_ in current_batch:
            this_aggregate = reduce_tree(t_)
            for s_ in this_aggregate:
                if s_ not in temp_batch:
                    temp_batch.append(s_)
        reweighted_trees = [apply_aggregation(_t, node_weights) for _t in temp_batch]
        current_batch_entropies = [calculate_H(_t) for _t in reweighted_trees]
        cb = []
        if sort_type == "maximum":
            try:
                entropy_cutoff = sorted(current_batch_entropies, reverse=True)[how_many - 1]
            except IndexError:
                entropy_cutoff = min(current_batch_entropies)
            for k, v in enumerate(current_batch_entropies):
                if v >= entropy_cutoff:
                    cb.append(temp_batch[k])
        elif sort_type == "minimum":
            try:
                entropy_cutoff = sorted(current_batch_entropies)[how_many - 1]
            except IndexError:
                entropy_cutoff = max(current_batch_entropies)
            for k, v in enumerate(current_batch_entropies):
                if v <= entropy_cutoff:
                    cb.append(temp_batch[k])
        results += cb
        current_batch = cb
    return results
    
def calculate_H(n):
    """Given node weights, calculates the entropy
    Args:
        n (dict): A dictionary of the form {node: weight...}
    Returns:
        The entropy of the tree"""
    total = sum(n.itervalues())
    weights =  [wi/total for wi in n.itervalues()]
    return -sum([wi*log(wi, 2) for wi in weights])
    
def calculate_S(n):
    """Given a node weight, calculates the normalized entropy (entropy divided by log of number of nodes)
    Args:
        n (dict): A dictionary of the form {node: weight...}
    Returns:
        The relative entropy of the tree
    """
    return calculate_H(n)/log(len(n), 2)
    
def aggregate(t, node_weights, desired_level, how_many=5, sort_type="maximum"):
    """Reduces a tree n times
    Args:
        t (dict): The tree to reduce (a dictionary of type {node: set([children])}
        node_weights (dict): A dictionary of the form {node: weight...}
        desired_level (int): What level to reduce the tree to
        how_many (int): How many trees to keep after each level of aggregation
        sort_type (str): Either maximum or minimum
    Returns:
        A list of trees obtained by aggregating the trees n times
    Side Effects:
            Creates a file called results.csv
    """
    #global results
    results = []
    h = []
    s = []
    n_ = []
    if desired_level < 2:
        raise Exception("Tree must have at least two levels")
    elif desired_level >= len(t):
        results = [t]
    else:
        n = len(t) - desired_level
        reduced_trees = reduce_n_times(t, n, node_weights, how_many, sort_type)
        results = [apply_aggregation(_t, node_weights) for _t in reduced_trees]
    with open('results.csv', 'w') as csvfile:
        fieldnames = ['tree id', 'number of nodes', 'entropy', 'normalized entropy']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        for tree_id, t in enumerate(results):
            h.append(calculate_H(t))
            s.append(calculate_S(t))
            n_.append(len(t))
            writer.writerow({'tree id': tree_id, 'number of nodes': len(t), 'entropy': calculate_H(t), 'normalized entropy': calculate_S(t)})
    return pd.DataFrame({"tree_structure": reduced_trees, "weights": results, 
        "nodes": n, "entropy": h, "normalized_entropy": s, "nodes": n_})
    
def draw_tree(t):
    """Plot a tree
    Args:
        t (dict): The tree to plot (a dictionary of the form {node: children})
    Returns:
        None
    Side Effects:
       Outputs the tree to screen     
    """
    G = nx.DiGraph(t)
    pos=nx.graphviz_layout(G,prog='dot')
    nx.draw(G,pos,with_labels=True,arrows=False)
    
def read_tree(filename):
    """Read a tree from a matrix (csv file
    Args:
        filename (csv file): The CSV file containing tree data in adjacency list format
    """
    input_data = pd.read_csv(filename, index_col=0)
    G = nx.DiGraph(input_data.values)
    x = nx.to_dict_of_dicts(G)
    r = {}
    for k in x:
        r[k] = set(x[k].keys())
    return r
    
def read_tree_weights(filename):
    """Read a tree from a matrix (csv file
    Args:
        filename (csv file): The CSV file containing tree data in adjacency list format
    Returns:
        A dictionary of the form {node_name: weight}
    """
    node_weights = {}
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            node_weights[int(row[0])] = float(row[1])
    return node_weights