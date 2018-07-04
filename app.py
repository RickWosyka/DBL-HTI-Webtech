import os
from flask import Flask, render_template, request, redirect, url_for
from Bio import Phylo
from collections import defaultdict

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
rootnode = Node

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
        parse(filename)
        return plot()

# Parser----------------------------------------------------------------------------------------------------------------
def parse(file):
    # The function that finds the children of a given Node
    def find_children(node):
        current_clade = namedict[node.name][0]
        namedict[node.name].pop(0)
        rgb = 255 // maxDepth
        node.color = (255, rgb * node.level, 0)
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
# Parser---------------------------------------------------------------------------------------------------------------|
@app.route("/")
def index():
    return render_template("intro_page.html")

@app.route("/")
def plot():
    import numpy as np
    from bokeh.models import ColumnDataSource, DataRange1d, HoverTool, TapTool
    from bokeh.models.glyphs import AnnularWedge, Quad
    from bokeh.io import curdoc
    from bokeh.embed import components
    from bokeh.resources import CDN
    from bokeh.plotting import figure
    source = ColumnDataSource()
    xdr = DataRange1d(start=5, end=15)
    ydr = DataRange1d(start=5, end=15)
    plot1 = figure(title="Sunburst", x_range=xdr, y_range=ydr, plot_width=650, plot_height=650,
                  h_symmetry=False, v_symmetry=False, min_border=0,
                  tools="pan,wheel_zoom,box_zoom,reset,save")

    plot1.add_tools(HoverTool(tooltips=[('Name', '@names'), ('No. of leaves', '@leaves')]))
    plot1.add_tools(TapTool())

    plot1.axis.visible = False
    plot1.grid.visible = False

    def run_sunburst(root):
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
                    source = ColumnDataSource(data=dict(names=[n.name], leaves=[n.leaves_subtree]))
                    plot1.annular_wedge(x=10, y=10, inner_radius=(n.level * n.width),
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
            for n in root.children:
                n.parent = root
                set_parent_and_color(n)

    def sunburst_root(root):
        root.range = np.pi * 2
        root.right_bound = 0
        source = ColumnDataSource(data=dict(names=[root.name], leaves=[root.leaves_subtree]))
        plot1.annular_wedge(x=10, y=10, inner_radius=0, outer_radius=root.width,
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


    run_sunburst(rootnode)

    # -----------------------------------------------------------------------------------------------------------------
    # Second visualisation:

    source = ColumnDataSource()
    xdr = DataRange1d(start=5, end=15)
    ydr = DataRange1d(start=5, end=15)
    plot2 = figure(title="Foam Tree", x_range=xdr, y_range=ydr, plot_width=650, plot_height=650,
                  h_symmetry=False, v_symmetry=False, min_border=0,
                  tools="pan,wheel_zoom,box_zoom,reset,save,lasso_select,box_select,hover")

    plot2.axis.visible = False
    plot2.grid.visible = False

    def run_foamtree(root):
        foamtree_root(root)
        curdoc().add_root(plot2)
        reset(root)

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


    run_foamtree(rootnode)

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

@app.route('/', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('intro_page.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)