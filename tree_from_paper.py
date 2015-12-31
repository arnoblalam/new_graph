import tree

print("Loading the tree")
test_tree = {
    '1': set(['2', '3']),
    '2': set(['4', '5']),
    '3': set(['6', '7', '8', '9']),
    '4': set(),
    '5': set(),
    '6': set(),
    '7': set(),
    '8': set(),
    '9': set()
    }
    
 
node_weights = {
    '1': 100,
    '2': 50,
    '3': 80,
    '4': 20,
    '5': 50,
    '6': 30,
    '7': 50,
    '8': 100,
    '9': 200
    }

print tree.reduce_n_times(test_tree, 3)