from Bio import Phylo


class Node:
    def __init__(self, value, name, level, leaves_number):
        self.name = name
        self.level = level
        self.value = value
        self.leaves_number = leaves_number
        self.right_bound = 0
        self.range = 0


trees = Phylo.parse("newick_test.txt", "newick").__next__()
trees.rooted = True

levels = trees.depths(unit_branch_lengths=True)
dpt = levels.items()
print(dpt)
root = list(levels.keys())[list(levels.values()).index(0)]
targetval = 0
for key in levels.keys():
    if levels[key] == targetval:
        print("found", targetval, "at key", key)
root = Node(1, root.name, key, 2)
print(root.name, root.level, root.value)