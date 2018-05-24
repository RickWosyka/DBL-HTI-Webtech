from Bio import Phylo


class Node:
    def __init__(self, name, level, leaves_subtree, children):
        self.name = name
        self.level = level
        self.leaves_subtree = leaves_subtree
        self.children = children
        self.right_bound = 0
        self.range = 0


maxDepth = 0
nodes = []
rootnode = 0


def parse(file):
    trees = Phylo.parse(file, "newick").__next__()

    levels = trees.depths(unit_branch_lengths=True)  # returns a dictionary of pairs (Clade name : depth)

    root = list(levels.keys())[list(levels.values()).index(0)]
    for key in levels.keys():  # loop that finds the name of the root node
        if levels[key] == 0:
            break
    global rootnode
    rootnode = Node(root.name, levels[key], root.count_terminals(), root.clades)
    global maxDepth
    maxDepth = max(levels.values())
    clade_list = trees.find_clades()
    names_list = levels.keys()
    global nodes
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
        return


filename = "ncbi-taxonomy.tre"
parse(filename)
print(rootnode.children)
