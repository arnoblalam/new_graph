import tree
import math

artificial_tree = {
1:set([2,3,4,5]),
2:set([]),
3:set([6,7]),
4:set([8,9]),
5:set([10,11,12]),
6:set([]),
7:set([]),
8:set([]),
9:set([]),
10:set([]),
11:set([]),
12:set([])
}

artificial_tree_weights ={
1: 100,
2: 20,
3: 50,
4: 200,
5: 10,
6: 30,
7: 20,
8: 30,
9: 150,
10:5,
11:10,
12:13
}

def myAggregationFunction(x, y):
    alpha = 50.0/(x+y)
    z = (x+y)**alpha
    return z
    
results = tree.aggregate(artificial_tree, artificial_tree_weights, 6, 70000, sort_type="maximum", f=myAggregationFunction)


#results = tree.aggregate(artificial_tree, artificial_tree_weights, 6, 70000, sort_type="maximum", f=lambda x,y: (x+y)**1.5)

tree.draw_tree(artificial_tree)