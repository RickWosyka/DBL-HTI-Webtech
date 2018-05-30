import os
from flask import Flask, render_template, request, redirect, url_for
from Bio import Phylo

app = Flask(__name__)


class Node:
    def __init__(self, name, level, leaves_subtree, children):
        self.color = None
        self.name = name
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

maxDepth = 0
nodes = []
rootnode = Node("placeholder", -1, -1, None)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/", methods=['POST'])
def upload():
    target = os.path.join(APP_ROOT, 'data/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        return render_template("completed_upload.html")

# Parser:
def parse(file):
    trees = Phylo.parse(file, "newick").__next__()

    levels = trees.depths(unit_branch_lengths=True)  # returns a dictionary of pairs (Clade name : depth)

    root = list(levels.keys())[list(levels.values()).index(0)]
    for key in levels.keys():  # loop that finds the name of the root node
        if levels[key] == 0:
            break
    global rootnode
    rootnode = Node(root.name, levels[key], root.count_terminals(), root.clades)
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
# Parser

@app.route("/")
def plot():
    import numpy as np
    from bokeh.models import ColumnDataSource, DataRange1d
    from bokeh.models.glyphs import AnnularWedge, Quad
    from bokeh.io import curdoc
    from bokeh.embed import components
    from bokeh.resources import CDN
    from bokeh.plotting import figure

    source = ColumnDataSource()
    xdr = DataRange1d(start=5, end=15)
    ydr = DataRange1d(start=5, end=15)
    plot1 = figure(title=None, x_range=xdr, y_range=ydr, plot_width=650, plot_height=650,
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

    m = Node(3, None, 1)
    t = Node(3, None, 1)
    r = Node(2, [m], 1)
    f = Node(2, None, 1)
    g = Node(2, None, 1)
    h = Node(2, [t], 1)
    i = Node(2, None, 1)
    j = Node(2, None, 1)
    k = Node(2, None, 1)
    e = Node(1, [r, k, j], 3)
    b = Node(1, [f], 1)
    c = Node(1, [g, h], 2)
    d = Node(1, [i], 1)
    a = Node(0, [b, c, d, e], 7)

    def run(root):
        set_parent_and_color(root)
        sunburst_root(root)
        curdoc().add_root(plot1)
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
                    plot1.add_glyph(source, glyph)
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
        glyph = AnnularWedge(x=10, y=10, inner_radius=0, outer_radius=root.width,
                             start_angle=root.right_bound, end_angle=np.pi * 2,
                             fill_color=root.color, line_alpha=0, fill_alpha=0.7)
        plot1.add_glyph(source, glyph)
        sunburst(root)

    def reset(root):
        if root.children:
            for n in root.children:
                n.seen = False
                reset(n)

    run(a)

    # -----------------------------------------------------------------------------------------------------------------
    # Second visualisation:

    source = ColumnDataSource()
    xdr = DataRange1d(start=5, end=15)
    ydr = DataRange1d(start=5, end=15)
    plot2 = figure(title=None, x_range=xdr, y_range=ydr, plot_width=650, plot_height=650,
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



    # b_b = Node(2, None, 1, (80, 236, 255))
    # b_a = Node(2, None, 1, (40, 60, 150))
    # e = Node(1, None, 1, (255, 50, 50))
    # d = Node(1, None, 1, (50, 50, 255))#
    # c = Node(1, None, 1, (50, 255, 255))#
    # b = Node(1, [b_a, b_b], 2, (255, 255, 50))
    # a = Node(0, [b, c, d, e], 5, (255, 0, 255))

    def run_foamtree():
        set_parent(a)
        foamtree_root(a)
        curdoc().add_root(plot2)
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
                    plot2.add_glyph(source, glyph)
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
        plot2.add_glyph(source, glyph)
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

    script1, div1 = components(plot1)
    script2, div2 = components(plot2)

    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    return render_template("plot.html", script1=script1, div1=div1,
                           script2=script2, div2=div2,
                           cdn_css=cdn_css, cdn_js=cdn_js)


# Link to more information page:
@app.route('/moreinformation', methods=['GET', 'POST'])
def more_information():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('moreinformation.html')


# Link back to home page:
@app.route('/', methods=['GET', 'POST'])
def backtohomepage():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)