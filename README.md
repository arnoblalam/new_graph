# New Tree Aggregation attempt
## Synopsis

This is a second attempt to programatically generate tree aggregations.

# Requirements

The following non-base libraries are required:

* networkx
* pandas

In addition, for plotting graphviz is required

## Known issues

None as of now

## Using the library

**Please see [tree.html](tree.html) for further documentation**

**Please see [example.py](example.py) for sample code**

The library has three functions that should be run by the user:

* read_tree: Reads a tree from a CSV file
* read_tree_weights: Reads tree weights from a CSV file
* aggregate: Creates aggregations of a tree
* draw_tree: Draws a tree to screen

### read_tree

The `read_tree(filename)` function accepts a filename of a CSV file as an argument.  The file should be of the form

	0,1,2,3,...
	0,0,1,1,0,...
	1,0,0,0,1,...
	2,0,0,0,0,...
	3,0,0,0,0...
	...

where the first row and first column are the node names ("..."" indicates additional nodes).  A 1 in `row i, column j` indicates an edge between the node i and node j (for example, in the above, there is an edge between node 0 and node 1 and another between node 0 and node 2).

It returns a tree of the form:

	{
		0: {1, 2},
	 	1: {3},
	 	2: {}
	 	3: {}
	}

where the tree can be interpreted as:

* Node 0 has children Node 1 and Node 2.
* Node 1 has child Node 3
* Node 2 has no children and 
* Node 3 has no children

### read_tree_weights

The `read_tree_weights(filename)` function accepts a filename of a CSV file as an argument.  The file should be of the form

	0,10
	1,5
	2,4
	3,0
	...

It returns a tree of the form:

	{
		0: 10,
	 	1: 5,
	 	2: 4
	 	3: 0
	 	...
	}

where the tree can be interpreted as:

* Node 0 has weight 10
* Node 1 has weight 5
* Node 2 has weight 4
* Node 3 has weight 0

### aggregate

The `aggregate(t, node_weights, desired_level, how_many, sort_type)` function takes the following arguments:
    t (dict): The tree to reduce (a dictionary of type {node: set([children])}
    node_weights (dict): A dictionary of the form {node: weight...}
    desired_level (int): What level to reduce the tree to
    how_many (int): How many trees to keep after each level of aggregation
    sort_type (str): Either maximum or minimum

It returns a tuple/pair, with the first element in the pair being a list of the "aggregated tree" and the second element being the "resulting weights".  It also outputs a file called `results.csv` that lists each tree_id and entropy.

(`t` and `node_weights` are of the form returned by `read_tree_weights` and `read_tree` so the output of those functions can be used as an input to aggregate).


### draw_tree
The `draw_tree(t)` function takes a tree as an argument and plots the result on screen.

## Sample code

```python
import tree

# load tree from disk
example_tree = tree.read_tree("example_tree.csv")
# load associated weights
example_weights = tree.read_tree_weights("example_tree_weights.csv")
# Aggregate to 2 node trees. Save the reuslting tree and tree_weights in the variables
# resulting_trees, resulting_weights
resulting_trees, resulting_weights = tree.aggregate(
	example_tree, 
	example_weights, 
	desired_level=2, 
	how_many=3, 
	sort_type="maximum")
# Plot the tree with the ID 3
tree.draw_tree(resulting_trees[3])
```