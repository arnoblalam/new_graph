from itertools import combinations, chain, imap
import collections
import cPickle
import networkx as nx

def deepcopy(obj):
    return cPickle.loads(cPickle.dumps(obj, -1))
    
def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

def possible_aggregations(t):
    results = set()
    for level, children in t.iteritems():
        x = children | set([level])
        results |= set(combinations(x, 2))
    return results
    
def merge_nodes(t, nodes_to_merge):
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
            copy_of_tree[k].add((a, b))
    copy_of_tree.pop(a, None)
    copy_of_tree.pop(b, None)
    copy_of_tree[(a, b)] = combined_children
    return copy_of_tree
    
def apply_aggregation(t, node_data, f=lambda x, y: x+y):
    """Create the new tree t by applying the aggregations to weights described in node_data"""
    try:
        result = dict()
        for k, v in t.iteritems():
            if type(k) is not tuple:
                result[k] = node_data[k]
            else:
                result[k] = apply_tuple(k, node_data, f)
        return result
    except:
        print(t)
        raise
        
def apply_tuple(t, n, f):
    if type(t[0]) is not tuple and type(t[1]) is not tuple:
        return f(n[t[0]], n[t[1]])
    elif type(t[0]) is tuple and type(t[1]) is tuple:
        return f(apply_tuple(t[0], n, f), apply_tuple(t[1], n, f))
    elif type(t[0]) is tuple:
        return f(apply_tuple(t[0], n, f), n[t[1]])
    elif type(t[1]) is tuple:
        return f(n[t[0]], apply_tuple(t[1], n, f))
        
def reduce_tree(t):
    return [merge_nodes(t, x) for x in possible_aggregations(t)]
    
def reduce_n_times(t, n):
    results = set()
    current_batch = reduce_tree(t)
    for x in current_batch:
        results.add(str(x))
    for _ in range(1, n):
        temp = []
        for tree in current_batch:
            temp += reduce_tree(tree)
            for x in temp:
                results.add(str(x))
        current_batch = temp
    results_ = [eval(x) for x in results]
    return results_
    
def read_matrix(filename):
    