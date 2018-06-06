from Bio import Phylo
import time
from collections import defaultdict


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
    def find_children(node):
        current_clade = namedict[node.name][0]
        namedict[node.name].pop(0)
        subclades = current_clade.clades
        children = []
        for sub in subclades:
            children.append(nodedict[sub.name][0])
            nodedict[sub.name].pop(0)
        node.children = children

    trees = Phylo.parse(file, "newick").__next__()
    levels = trees.depths(unit_branch_lengths=True)  # returns a dictionary of pairs (Clade : depth)

    root = list(levels.keys())[list(levels.values()).index(0)]
    global maxDepth, current_clade
    maxDepth = max(levels.values())
    clade_list = trees.find_clades()
    pairlist = []
    nodepairs = []
    names_list = levels.keys()
    global nodes
    nodes = []  # this is the list that will contain all nodes
    i = 0
    # This loop calculates necessary properties and creates proper Nodes
    for Clade in clade_list:
        node_name = Clade.name
        node_leaves = Clade.count_terminals()
        node_depth = levels[Clade]
        nodes.append(Node(node_name, node_depth, node_leaves, []))
        nodepairs.append((node_name, nodes[i]))
        pairlist.append((Clade.name, Clade))
        i += 1
    root_children = []
    namedict = defaultdict(list)
    nodedict = defaultdict(list)
    for k, v in pairlist:
        namedict[k].append(v)
    for k, v in nodepairs:
        nodedict[k].append(v)
    # This loop ensures that each Node's children are correct
    for vertex in nodes:
        find_children(vertex)
        if vertex.level == 1:
            root_children.append(vertex)
    global rootnode
    rootnode = Node(root.name, 0, root.count_terminals(), root_children)


filename = "ncbi-taxonomy.tre"

t0 = time.time()

parse(filename)


t1 = time.time()
t = t1 - t0
print(t)
