import numpy as np
from bokeh.models import ColumnDataSource, DataRange1d, HoverTool, TapTool
from bokeh.io import curdoc, show
from bokeh.plotting import figure

xdr = DataRange1d(start=5, end=15)
ydr = DataRange1d(start=5, end=15)
plot = figure(title=None, x_range=xdr, y_range=ydr, plot_width=320, plot_height=300,
              h_symmetry=False, v_symmetry=False, min_border=0,
              tools="pan,wheel_zoom,box_zoom,reset,save,lasso_select")

plot.axis.visible = False
plot.grid.visible = False

plot.add_tools(HoverTool(tooltips=[('Name', '@names'), ('No. of leaves', '@leaves')]))
plot.add_tools(TapTool())

class Node:
    def __init__(self, level, children, leaves_subtree, name):
        self.color = (255, 0, 0)
        self.level = level
        self.children = children
        self.leaves_subtree = leaves_subtree
        self.width = 1
        self.range = 1
        self.right_bound = 0
        self.left_bound = 0
        self.parent = None
        self.seen = False
        self.name = name


m = Node(3, None,         1, "m")
t = Node(3, None,         1, "t")
r = Node(2, [m],          1, "r")
f = Node(2, None,         1, "f")
g = Node(2, None,         1, "g")
h = Node(2, [t],          1, "h")
i = Node(2, None,         1, "i")
j = Node(2, None,         1, "j")
k = Node(2, None,         1, "k")
e = Node(1, [r, k, j],    3, "e")
b = Node(1, [f],          1, "b")
c = Node(1, [g, h],       2, "c")
d = Node(1, [i],          1, "d")
a = Node(0, [b, c, d, e], 7, "a")


def run(root):
    set_parent_and_color(root)
    sunburst_root(root)
    curdoc().add_root(plot)
    show(plot)
    reset(root)


def sunburst(node):
    if node.children:
        count = 0
        n_old = None
        maxDepth = 4
        rgb = (255/ maxDepth)
        for n in node.children:
            n.color = ((255, rgb * n.level, 0))
            if not n.seen:
                if count == 0:
                    n.right_bound = n.parent.right_bound
                    for p in node.children:
                        p.range = (p.leaves_subtree / p.parent.leaves_subtree) * p.parent.range
                else:
                    n.right_bound = n_old.left_bound
                n.left_bound = n.right_bound + n.range
                source = ColumnDataSource(data=dict(names=[n.name], leaves=[n.leaves_subtree]))
                plot.annular_wedge(x=10, y=10, inner_radius=(n.level * n.width),
                                     outer_radius=((n.level * n.width) + n.width),
                                     start_angle=n.right_bound, end_angle=n.left_bound,
                                     fill_color=n.color, line_color='#ffffff', line_width=1, fill_alpha=0.5,
                                     hover_color=n.color, hover_alpha=1.0, name=n.name, source=source,
                                     selection_color=n.color, selection_alpha=1.0, selection_line_color='#000000',
                                     selection_line_alpha=1.0)
                n_old = n
                count += 1
                sunburst(n)
            n.seen = True


def set_parent_and_color(root):
    if root.children:
        max_depth = 4
        rgb = (255 / max_depth)
        for n in root.children:
            n.color = (255, rgb * n.level, 0)
            n.parent = root
            set_parent_and_color(n)


def sunburst_root(root):
    root.range = np.pi * 2
    root.right_bound = 0
    source = ColumnDataSource(data=dict(names=[root.name], leaves=[root.leaves_subtree]))
    plot.annular_wedge(x=10, y=10, inner_radius=0, outer_radius=root.width,
                       start_angle=root.right_bound, end_angle=np.pi * 2,
                       fill_color=root.color, line_color='#ffffff', line_width=1, fill_alpha=0.5,
                       hover_color=root.color, hover_alpha=1.0, name=root.name, source=source,
                       selection_color=root.color, selection_alpha=1.0, selection_line_color='#000000',
                       selection_line_alpha=1.0)
    sunburst(root)


def reset(root):
    if root.children:
        for n in root.children:
            n.seen = False
            reset(n)


run(a)
