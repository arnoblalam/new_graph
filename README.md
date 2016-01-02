# New Tree Aggregation attempt
## Synopsis

This is a second attempt to programatically generate tree aggregations.

# Requirements

The following non-base libraries are required:

* networkx
* pandas

In addition, for plotting graphviz is required

# Known issues

* Duplicate trees at intermediate levels

For example: If we have start of with the tree `1 -> [2, 3, 4]`, we get the following aggregations:

    (1,2) -> [3, 4]
    (1, 3) -> [2, 4]
    (1, 4) -> [2, 3]
    1 -> [(2, 3), 4]
    1 -> [2, (3, 4)]
    1 -> [(2, 4), 3]

If we aggregate another level, we will get many aggregations, including:

    ((1, 3), 4) -> [2]
    ((1, 4), 3) -> [2]

Note that the first line is from aggregating node (1, 3) with node 4 and the second comes from aggregating node (1,4) with node 3.
However, the resulting trees are the same and have the same entropy.

## Using the library

** Please see tree.html for further documentation **
** Please see example.py for sample code **

The library has three functions that should be run by the user:

* read_tree: Reads a tree from a CSV file
* read_tree_weights: Reads tree weights from a CSV file
* aggregate: Creates aggregations of a tree
* draw_tree: Draws a tree to screen

The `read_tree` function accepts a filename for a CSV file.  The file should be of the form

	0,1,2,3,...
	0,0,1,1,0,...
	1,0,0,0,1,...
	2,0,0,0,0,...
	3,0,0,0,0...
	...

(... indicates additional nodes)
It returns a tree of the form:

	{
		0: {1, 2},
	 	1: {3},
	 	2: {}
	 	3: {}
	}

where the tree can be interpreted as "0 has children 1, 2. 1 has child 3, 2 has no children and 3 has no children".

The `read_tree_weights` function accepts a filename for a CSV file.  The file should be of the form

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

where the tree can be interpreted as "A has children B, C. B has child D, C has no children and D has no children".

The `aggregate` function takes the following arguments:
    t (dict): The tree to reduce (a dictionary of type {node: set([children])}
    node_weights (dict): A dictionary of the form {node: weight...}
    desired_level (int): What level to reduce the tree to
    how_many (int): How many trees to keep after each level of aggregation
    sort_type (str): Either maximum or minimum

`t` and `node_weights` are of the form returned by `read_tree_weights` and `read_tree`.  It returns a tuple/pair, with the first element in the pair being the "aggregated tree" and the second element being the "resulting weights".  It also outputs a file called `results.csv` that lists each tree_id and entropy

The `draw_tree` function takes a tree as an argument and plots the result on screen.