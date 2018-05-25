import numpy as np
from bokeh.models import ColumnDataSource, DataRange1d
from bokeh.models.glyphs import AnnularWedge
from bokeh.io import curdoc, show
from bokeh.plotting import figure


source = ColumnDataSource()
xdr = DataRange1d(start=5, end=15)
ydr = DataRange1d(start=5, end=15)
plot = figure(title=None, x_range=xdr, y_range=ydr, plot_width=320, plot_height=300,
              h_symmetry=False, v_symmetry=False, min_border=0,
              tools="pan,wheel_zoom,box_zoom,reset,save,lasso_select,box_select,hover")


class Node:
    def __init__(self, level, children, leaves_subtree):
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


def run_sunburst(root):
    set_parent_and_color(root)
    sunburst_root(root)
    curdoc().add_root(plot)
    show(plot)
    reset(root)


def sunburst(node):
    if node.children:
        count = 0
        n_old = None
        for n in node.children:
            if not n.seen:
                if count == 0:
                    n.right_bound = n.parent.right_bound
                    for p in node.children:
                        p.range = (p.leaves_subtree / p.parent.leaves_subtree) * p.parent.range
                else:
                    n.right_bound = n_old.left_bound
                n.left_bound = n.right_bound + n.range
                glyph = AnnularWedge(x=10, y=10, inner_radius=(n.level * n.width),
                                     outer_radius=((n.level * n.width) + n.width),
                                     start_angle=n.right_bound, end_angle=n.left_bound,
                                     fill_color=n.color, line_color='#ffffff', line_width=1, fill_alpha=0.7)
                plot.add_glyph(source, glyph)
                n_old = n
                count += 1
                sunburst(n)
            n.seen = True


def set_parent_and_color(root):
    if root.children:
        rgb = (255 / max_depth)
        for n in root.children:
            n.color = (255, rgb * n.level, 0)
            n.parent = root
            set_parent_and_color(n)


def sunburst_root(root):
    root.range = np.pi * 2
    root.right_bound = 0
    glyph = AnnularWedge(x=10, y=10, inner_radius=0, outer_radius=root.width,
                         start_angle=root.right_bound, end_angle=np.pi * 2,
                         fill_color=root.color, line_alpha=0, fill_alpha=0.7)
    plot.add_glyph(source, glyph)
    sunburst(root)


def reset(root):
    if root.children:
        for n in root.children:
            n.seen = False
            reset(n)


run_sunburst(rootnode)
