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


def parse():
    trees = Phylo.parse("ncbi-taxonomy.tre", "newick").__next__()

    levels = trees.depths(unit_branch_lengths=True)  # returns a dictionary of pairs (Clade name : depth)

    root = list(levels.keys())[list(levels.values()).index(0)]
    for key in levels.keys():  # loop that finds the name of the root node
        if levels[key] == 0:
            print("found", 0, "at key", key)
            break
    rootnode = Node(root.name, levels[key], root.count_terminals(), root.clades)
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
    return rootnode