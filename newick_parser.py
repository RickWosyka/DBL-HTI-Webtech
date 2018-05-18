from Bio import Phylo
import time


t_start = time.time() #debugging
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


levels = trees.depths(unit_branch_lengths=True) #returns a dictionary of pairs (Clade name, depth)
dpt = levels.items()

root = list(levels.keys())[list(levels.values()).index(0)]
targetval = 0
for key in levels.keys(): #loop that finds the name of the root node
    if levels[key] == targetval:
        print("found", targetval, "at key", key)
        break
rootnode = Node(root.name, levels[key], 2, ["a"])
print(rootnode.name, rootnode.level, rootnode.children)
x = 1
clade_list = trees.find_clades()
names_list = levels.keys()
nc = 0
nodes = []

for Clade in clade_list: #calculates properties and creates nodes
    node_name = Clade.name
    node_children = Clade.clades
    node_leaves = Clade.count_terminals()
    if node_name in names_list:
        node_depth = levels[node_name]
    else:
        node_depth = 0
    nodes[nc] = Node(node_name, node_depth, node_leaves, node_children)

test = Node(1, "testnode", 5, 10, ["test1", "test2"])
print(test.name, test.level, test.children)
print(nodes[0], nodes[1], nodes[2])
t_end = time.time()
print(t_end)
total_time = t_end - t_start
print("the program took ", total_time, " seconds.")
