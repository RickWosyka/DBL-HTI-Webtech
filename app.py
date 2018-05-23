import os
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


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



@app.route('/')
def plot():
    import numpy as np
    import bokeh as bok
    from bokeh.models import ColumnDataSource, DataRange1d
    from bokeh.models.glyphs import AnnularWedge, Ellipse, Quad
    from bokeh.io import curdoc
    from bokeh.embed import components
    from bokeh.resources import CDN
    from bokeh.plotting import figure

    def DFS_visit(node):
        if node.children:
            maxDepth = 4
            count = 0
            n_old = None
            rgb = (255 / maxDepth)
            for n in node.children:
                n.color = (255, rgb * n.level, 0)
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
                                         start_angle=n.right_bound, end_angle=n.left_bound, fill_color=n.color,
                                         line_color='#ffffff', line_width=1, fill_alpha=0.7)
                    plot.add_glyph(source, glyph)
                    n_old = n
                    count += 1
                    DFS_visit(n)
                n.seen = True

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

    def Set_parent(root):
        if root.children:
            for n in root.children:
                n.parent = root
                Set_parent(n)

    m = Node(3, None, 1, None)
    n = Node(3, None, 1, None)
    l = Node(2, [m], 1, None)
    f = Node(2, None, 1, None)
    g = Node(2, None, 1, None)
    h = Node(2, [n], 1, None)
    i = Node(2, None, 1, None)
    j = Node(2, None, 1, None)
    k = Node(2, None, 1, None)
    e = Node(1, [l, k, j], 3, None)
    b = Node(1, [f], 1, None)
    c = Node(1, [g, h], 2, None)
    d = Node(1, [i], 1, None)
    a = Node(0, [b, c, d, e], 7, (255, 0, 0))

    def Sunburst(root):
        root.range = np.pi * 2
        root.right_bound = 0
        glyph = AnnularWedge(x=10, y=10, inner_radius=0, outer_radius=(root.width),
                         start_angle=n.right_bound, end_angle=np.pi * 2, fill_color=root.color, line_alpha=0,
                         fill_alpha=0.7)
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

    # -----------------------------------------------------------------------------------------------------------------
    # Second visualisation:

    source = ColumnDataSource()
    open_space_top = 0
    open_space_bottom = 0
    open_space_left = 0
    open_space_right = 0

    m = Node(3, None, 1, '#CDE6FF')
    p = Node(3, None, 1, '#860000')
    l = Node(2, [m], 1, '#75FFE7')
    f = Node(2, None, 1, '#191970')
    g = Node(2, None, 1, '#CD1076')
    h = Node(2, [p], 1, '#696969')
    i = Node(2, None, 1, '#83563C')
    j = Node(2, None, 1, '#F0F8FF')
    k = Node(2, None, 1, '#7B322C')
    e = Node(1, [l, k, j], 3, '#7F1AC4')
    b = Node(1, [f], 1, '#FFFF66')
    c = Node(1, [g, h], 2, '#FF758D')
    d = Node(1, [i], 1, '#81E9EF')
    a = Node(0, [b, c, d, e], 7, '#FF0000')

    def foamtree(node):
        if node.children:
            global open_space_left
            global open_space_top
            global open_space_bottom
            global open_space_right
            on_width = False
            maxDepth = 3
            rgb = (255 / maxDepth)
            for n in node.children:
                n.color = (255, rgb * n.level, 0)
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
                    glyph = Quad(left=n.left, right=n.right, top=n.top, bottom=n.bottom, fill_color=n.color,
                                 fill_alpha=0.5)
                    bok.models.plots.plot.add_glyph(source, glyph)
                    if on_width:
                        open_space_left = n.right
                    else:
                        open_space_top = n.bottom
                    foamtree(n)
                n.seen = True

    def foamroot(root):
        global open_space_left
        global open_space_top
        global open_space_bottom
        global open_space_right
        root.top = 14
        root.bottom = 6
        root.left = 6
        root.right = 14
        root.area = (root.top - root.bottom) * (root.right - root.left)
        root.color = (255, 0, 0)
        open_space_top = root.top
        open_space_bottom = root.bottom
        open_space_left = root.left
        open_space_right = root.right
        glyph = Quad(left=root.left, right=root.right, top=root.top, bottom=root.bottom, fill_color=root.color,
                     fill_alpha=0.5)
        bok.models.plots.plot.add_glyph(source, glyph)
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

    def run():
        xdr = DataRange1d(start=5, end=15)
        ydr = DataRange1d(start=5, end=15)

        bok.models.plots.plot = figure(title="Foam tree", x_range=xdr, y_range=ydr, plot_width=650, plot_height=650,
                                       h_symmetry=False, v_symmetry=False, min_border=0,
                                       tools="pan,wheel_zoom,box_zoom,reset,save,lasso_select,box_select,hover")

        set_parent(a)
        foamroot(a)

        curdoc().add_root(bok.models.plots.plot)

        reset(a)

    run()

    script1, div1 = components(plot)
    script2, div2 = components(bok.models.plots.plot)

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