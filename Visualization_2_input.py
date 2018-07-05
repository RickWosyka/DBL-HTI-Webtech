from bokeh.models import ColumnDataSource, DataRange1d, HoverTool, TapTool
from bokeh.io import curdoc, show
from bokeh.plotting import figure

xdr = DataRange1d(start=5, end=15)
ydr = DataRange1d(start=5, end=15)
plot = figure(title=None, x_range=xdr, y_range=ydr, plot_width=320, plot_height=300,
              h_symmetry=False, v_symmetry=False, min_border=0,
              tools="pan,wheel_zoom,box_zoom,reset,save")

plot.axis.visible = False
plot.grid.visible = False

plot.add_tools(HoverTool(tooltips=[('Name', '@names'), ('No. of leaves', '@leaves')]))
plot.add_tools(TapTool())

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


def run_foamtree(root):
    set_parent_and_color(root)
    foamtree_root(root)
    curdoc().add_root(plot)
    show(plot)
    reset(root)


def foamtree(node):
    if node.children:
        open_space_left = node.left
        open_space_top = node.top
        open_space_bottom = node.bottom
        open_space_right = node.right
        rgb = (255/ maxDepth)
        for n in node.children:
          n.color = ((255, rgb * n.level, 0))
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
                source = ColumnDataSource(data=dict(names=[root.name], leaves=[root.leaves_subtree]))
                plot.quad(left=n.left, right=n.right, top=n.top,
                             bottom=n.bottom, fill_color=n.color, fill_alpha=0.5,
                             hover_color=n.color, hover_alpha=1.0, name=n.name, source=source,
                             selection_color=n.color, selection_alpha=1.0, selection_line_color='#000000',
                             selection_line_alpha=1.0)
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
    source = ColumnDataSource(data=dict(names=[root.name], leaves=[root.leaves_subtree]))
    plot.quad(left=root.left, right=root.right, top=root.top,
              bottom=root.bottom, fill_color=root.color, fill_alpha=0.5,
              hover_color=root.color, hover_alpha=1.0, name=root.name, source=source,
              selection_color=root.color, selection_alpha=1.0, selection_line_color='#000000',
              selection_line_alpha=1.0)
    foamtree(root)


def set_parent_and_color(root):
    if root.children:
        rgb = (255 / max_depth)
        for n in root.children:
            n.color = (255, rgb * n.level, 0)
            n.parent = root
            set_parent_and_color(n)


def reset(root):
    if root.children:
        for n in root.children:
            n.seen = False
            reset(n)


run_foamtree(rootnode)
