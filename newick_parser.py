from Bio import Phylo
import time


t_start = time.time()  # debugging
print(t_start)


class Node:
    def __init__(self, name, level, leaves_subtree, children):
        self.name = name
        self.level = level
        self.leaves_subtree = leaves_subtree
        self.children = children
        self.right_bound = 0
        self.range = 0


trees = Phylo.parse("ncbi-taxonomy.tre", "newick").__next__()

levels = trees.depths(unit_branch_lengths=True)  # returns a dictionary of pairs (Clade name : depth)
dpt = levels.items()

root = list(levels.keys())[list(levels.values()).index(0)]
targetval = 0
for key in levels.keys():  # loop that finds the name of the root node
    if levels[key] == targetval:
        print("found", targetval, "at key", key)
        break
rootnode = Node(root.name, levels[key], root.count_terminals(), root.clades)
print(rootnode.name, rootnode.level, rootnode.leaves_subtree, rootnode.children)
clade_list = trees.find_clades()
names_list = levels.keys()
nodes = []  # this is the list that will contain all nodes

for Clade in clade_list:  # calculates properties and creates nodes
    node_name = Clade.name
    node_children = Clade.clades
    node_leaves = Clade.count_terminals()
    if Clade in names_list:
        node_depth = levels[Clade]
    else:
        node_depth = 0
    nodes.append(Node(node_name, node_depth, node_leaves, node_children))

print(nodes[2].name, nodes[2].children)
level0 = []
levelnot0 = []
for q1 in nodes:
    if q1.level == 0:
        level0.append(q1.name)
    else:
        levelnot0.append(q1.name)
print(level0)
print(len(level0))
print(len(levelnot0))

t_end = time.time()
total_time = t_end - t_start
print("the program took ", total_time, " seconds.")
