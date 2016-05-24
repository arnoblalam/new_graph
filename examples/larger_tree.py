import tree

artificial_tree = {
1:set([2,3,4]),
2:set([5,6]),
3:set([7,9]),
4:set([10,11,12,13]),
5:set([14,16,17]),
6:set([18,19]),
7:set([20,21,23,24]),
9:set([]),
10:set([26,27]),
11:set([]),
12:set([28,29]),
13:set([]),
14:set([]),
16:set([]),
17:set([]),
18:set([]),
19:set([]),
20:set([]),
21:set([]),
23:set([]),
24:set([]),
26:set([]),
27:set([]),
28:set([]),
29:set([])
}

artificial_tree_weights ={
1: 100,
2: 20,
3: 50,
4: 80,
5: 10,
6: 30,
7: 20,
9: 400,
10:50,
11:30,
12:80,
13:60,
14:20,
16:150,
17:80,
18:40,
19:200,
20:10,
21:130,
23:80,
24:60,
26:260,
27:30,
28:40,
29:10
}

results = tree.aggregate(artificial_tree, artificial_tree_weights, 2, 25)

tree.draw_tree(artificial_tree)