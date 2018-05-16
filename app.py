import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))



@app.route('/')
def plot():
    import numpy as np
    from bokeh.models import ColumnDataSource, DataRange1d
    from bokeh.models.glyphs import AnnularWedge, Ellipse
    from bokeh.io import curdoc
    import queue
    from bokeh.embed import components
    from bokeh.resources import CDN
    from bokeh.plotting import figure
    from bokeh.transform import linear_cmap
    from bokeh.util.hex import hexbin

    def DFS_visit(node):
        if node.children:
            count = 0
            n_old = None
            for n in node.children:
                if n.seen == False:
                    if count == 0:
                        n.right_bound = n.parent.right_bound
                        for p in node.children:
                            p.range = (p.leaves_subtree / p.parent.leaves_subtree) * p.parent.range
                    else:
                        n.right_bound = n_old.left_bound
                    n.left_bound = n.right_bound + n.range
                    glyph = AnnularWedge(x=10, y=10, inner_radius=(n.level * n.width),
                                         outer_radius=((n.level * n.width) + n.width),
                                         start_angle=n.right_bound, end_angle=n.left_bound, name=n.tags,
                                         fill_color=n.color)
                    plot.add_glyph(source, glyph)
                    n_old = n
                    count += 1
                    DFS_visit(n)
                n.seen = True

    class Node:
        def __init__(self, level, children, leaves_subtree, tags, color):
            self.color = color
            self.tags = tags
            self.level = level
            self.children = children
            self.leaves_subtree = leaves_subtree
            self.width = 1
            self.range = 1
            self.right_bound = 0
            self.left_bound = 0
            self.parent = None
            self.seen = False

    def Set_parent(root):
        if root.children:
            for n in root.children:
                n.parent = root
                Set_parent(n)

    m = Node(3, None, 1, 'm', '#CDE6FF')
    n = Node(3, None, 1, 'n', '#860000')
    l = Node(2, [m], 1, 'l', '#75FFE7')
    f = Node(2, None, 1, 'f', '#191970')
    g = Node(2, None, 1, 'g', '#CD1076')
    h = Node(2, [n], 1, 'h', '#696969')
    i = Node(2, None, 1, 'i', '#83563C')
    j = Node(2, None, 1, 'j', '#F0F8FF')
    k = Node(2, None, 1, 'k', '#7B322C')
    e = Node(1, [l, k, j], 3, 'e', '#7F1AC4')
    b = Node(1, [f], 1, 'b', '#FFFF66')
    c = Node(1, [g, h], 2, 'c', '#FF758D')
    d = Node(1, [i], 1, 'd', '#81E9EF')
    a = Node(0, [b, c, d, e], 7, 'a', '#FF0000')

    def Sunburst(root):
        root.range = np.pi * 2
        root.right_bound = 0
        glyph = Ellipse(x=10, y=10, width=root.width * 2, height=root.width * 2, fill_color=a.color)
        plot.add_glyph(source, glyph)
        DFS_visit(root)

    Set_parent(a)

    source = ColumnDataSource()

    xdr = DataRange1d(start=5, end=15)
    ydr = DataRange1d(start=5, end=15)

    plot = figure(title="Sunburst", x_range=xdr, y_range=ydr, plot_width=650, plot_height=650,
                  h_symmetry=False, v_symmetry=False, min_border=0,
                  tools="pan,wheel_zoom,box_zoom,reset,save,lasso_select,box_select,hover")

    Sunburst(a)

    curdoc().add_root(plot)

    n = 50000
    x = np.random.standard_normal(n)
    y = np.random.standard_normal(n)

    bins = hexbin(x, y, 0.1)

    k = figure(title="Hex Tiles", match_aspect=True, background_fill_color='#440154', plot_width=650, plot_height=650,
               tools='pan,wheel_zoom,box_zoom,reset,save,lasso_select,box_select')
    k.grid.visible = False

    k.hex_tile(q="q", r="r", size=0.1, line_color=None, source=bins,
               fill_color=linear_cmap('counts', 'Viridis256', 0, max(bins.counts)))

    script1, div1 = components(plot)
    script2, div2 = components(k)

    cdn_js = CDN.js_files[0]
    cdn_css = CDN.css_files[0]
    return render_template("plot.html", script1=script1, div1=div1,
                           script2=script2, div2=div2,
                           cdn_js=cdn_js, cdn_css=cdn_css)


@app.route('/')
def index():
    return render_template("index.html")

@app.route("/upload", methods=['POST'])
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

@app.route('/moreinformation', methods=['GET', 'POST'])
def more_information():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('moreinformation.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
