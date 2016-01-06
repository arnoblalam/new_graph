import tree

print "Reading tree"
example_tree = tree.read_tree("example_tree.csv")
example_weights = tree.read_tree_weights("example_tree_weights.csv")

print "Aggregating"
results = tree.aggregate(
	example_tree, 
	example_weights, 
	desired_level=2, 
	how_many=3, 
	sort_type="maximum")


print "Drawing tree with tree ID 3"
tree.draw_tree(results.iloc[3]["tree_structure"])