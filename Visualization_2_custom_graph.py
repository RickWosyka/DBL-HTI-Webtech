from bokeh.models import ColumnDataSource, DataRange1d
from bokeh.models.glyphs import Quad
from bokeh.io import curdoc, show
from bokeh.plotting import figure

source = ColumnDataSource()
xdr = DataRange1d(start=5, end=15)
ydr = DataRange1d(start=5, end=15)
plot = figure(title=None, x_range=xdr, y_range=ydr, plot_width=320, plot_height=300,
              h_symmetry=False, v_symmetry=False, min_border=0,
              tools="pan,wheel_zoom,box_zoom,reset,save,lasso_select,box_select,hover")


class Node:
    def __init__(self, level, children, leaves_subtree, color):
        self.color = color
        self.level = level
        self.children = children
        self.leaves_subtree = leaves_subtree
        self.width = 1
        self.range = 1
        self.right_bound = 0
        self.left_bound = 0
        self.parent = None
        self.seen = False
        self.top = 0
        self.bottom = 0
        self.right = 0
        self.left = 0
        self.area = 0


m = Node(3, None,         1, '#CDE6FF')
t = Node(3, None,         1, '#860000')
q = Node(2, [m],          1, '#75FFE7')
f = Node(2, None,         1, '#191970')
g = Node(2, None,         1, '#CD1076')
h = Node(2, [t],          1, '#696969')
i = Node(2, None,         1, '#83563C')
j = Node(2, None,         1, '#F0F8FF')
k = Node(2, None,         1, '#7B322C')
e = Node(1, [q, k, j],    3, '#7F1AC4')
b = Node(1, [f],          1, '#FFFF66')
c = Node(1, [g, h],       2, '#FF758D')
d = Node(1, [i],          1, '#81E9EF')
a = Node(0, [b, c, d, e], 7, '#FF0000')


#b_b = Node(2, None, 1, (80, 236, 255))
#b_a = Node(2, None, 1, (40, 60, 150))
#e = Node(1, None, 1, (255, 50, 50))
#d = Node(1, None, 1, (50, 50, 255))#
#c = Node(1, None, 1, (50, 255, 255))#
#b = Node(1, [b_a, b_b], 2, (255, 255, 50))
#a = Node(0, [b, c, d, e], 5, (255, 0, 255))


def run_foamtree():
    set_parent(a)
    foamtree_root(a)
    curdoc().add_root(plot)
    show(plot)
    reset(a)


def foamtree(node):
    if node.children:
        open_space_left = node.left
        open_space_top = node.top
        open_space_bottom = node.bottom
        open_space_right = node.right
        for n in node.children:
            if not n.seen:
                n.area = (n.leaves_subtree / n.parent.leaves_subtree) * n.parent.area
                if (open_space_right - open_space_left) >= (open_space_top - open_space_bottom):
                    n.top = open_space_top
                    n.bottom = open_space_bottom
                    n.left = open_space_left
                    n.right = (n.area / (n.top - n.bottom)) + n.left
                    on_width = True
                else:
                    n.top = open_space_top
                    n.left = open_space_left
                    n.right = open_space_right
                    n.bottom = -(n.area / (n.right - n.left)) + n.top
                    on_width = False
                glyph = Quad(left=n.left, right=n.right, top=n.top,
                             bottom=n.bottom, fill_color=n.color, fill_alpha=0.5)
                plot.add_glyph(source, glyph)
                if on_width:
                    open_space_left = n.right
                else:
                    open_space_top = n.bottom
                foamtree(n)
            n.seen = True


def foamtree_root(root):
    root.top = 14
    root.bottom = 6
    root.left = 6
    root.right = 14
    root.area = (root.top - root.bottom) * (root.right - root.left)
    glyph = Quad(left=root.left, right=root.right, top=root.top,
                 bottom=root.bottom, fill_color=root.color, fill_alpha=0.5)
    plot.add_glyph(source, glyph)
    foamtree(root)


def set_parent(root):
    if root.children:
        for n in root.children:
            n.parent = root
            set_parent(n)


def reset(root):
    if root.children:
        for n in root.children:
            n.seen = False
            reset(n)


run_foamtree()
