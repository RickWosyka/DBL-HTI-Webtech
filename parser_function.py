from Bio import Phylo
import time


class Node:
    def __init__(self, name, level, leaves_subtree, children):
        self.name = name
        self.level = level
        self.leaves_subtree = leaves_subtree
        self.children = children
        self.right_bound = 1
        self.range = 1


maxDepth = 0
nodes = []
rootnode = Node


def Set_parent(root):
    if root.children:
        for n in root.children:
            n.parent = root
            Set_parent(n)


def parse(file):
    # The function that finds the children of a given Node
    def find_children(node, clade):
        if clade is None:
            return []
        subclades = current_clade.clades
        subclade_names = []
        for sub in subclades:
            subclade_names.append(sub.name)
        children = []
        for child_node in nodes:
            if child_node.name in subclade_names:
                children.append(child_node)
        return children

    trees = Phylo.parse(file, "newick").__next__()
    levels = trees.depths(unit_branch_lengths=True)  # returns a dictionary of pairs (Clade : depth)

    root = list(levels.keys())[list(levels.values()).index(0)]
    global maxDepth, current_clade
    maxDepth = max(levels.values())
    clade_list = trees.find_clades()
    names_list = levels.keys()
    global nodes
    nodes = []  # this is the list that will contain all nodes

    # This loop calculates necessary properties and creates proper Nodes
    for Clade in clade_list:
        node_name = Clade.name
        node_leaves = Clade.count_terminals()
        if Clade in names_list:
            node_depth = levels[Clade]
        else:
            node_depth = 0
        nodes.append(Node(node_name, node_depth, node_leaves, []))
        print(Clade.branch_length)
    root_children = []

    # This loop ensures that each Node's children are correct
    for vertex in nodes:
        for cclade in trees.find_clades():
            if cclade.name == vertex.name:
                current_clade = cclade
                break
        vertex.children = find_children(vertex, current_clade)
        if vertex.level == 1:
            root_children.append(vertex)
    global rootnode
    rootnode = Node(root.name, 0, root.count_terminals(), root_children)


filename = "newick_test.nwk"

t0 = time.time()

parse(filename)


t1 = time.time()
t = t1 - t0
print(t)
