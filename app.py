from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def plot():
    import numpy as np
    from bokeh.models import ColumnDataSource, DataRange1d, Plot, LinearAxis, Grid
    from bokeh.models.glyphs import AnnularWedge, Ellipse
    from bokeh.io import curdoc
    import queue
    from bokeh.plotting import figure
    from bokeh.embed import components
    from bokeh.resources import CDN

    class Node:
        def __init__(self, level, children, leaves_subtree):
            self.level = level
            self.children = children
            self.leaves_subtree = leaves_subtree
            self.width = 1
            self.range = 1
            self.right_bound = 0
            self.left_bound = self.right_bound + self.range
            self.parent = None

    def Set_parent(root):
        if root.children:
            for n in root.children:
                n.parent = root
                Set_parent(n)

    def Sunburst(root):
        root.range = np.pi * 2
        root.right_bound = 0
        glyph = Ellipse(x=10, y=10, width=root.width * 2, height=root.width * 2)
        plot.add_glyph(source, glyph)
        DFS_visit(root)

    def DFS_visit(node):
        if node.children:
            count = 0
            n_old = None
            for n in node.children:
                if count == 0:
                    n.right_bound = n.parent.right_bound
                    for n in node.children:
                        n.range = (n.leaves_subtree / n.parent.leaves_subtree) * n.parent.range
                else:
                    n.right_bound = n_old.left_bound
                n.left_bound = n.right_bound + n.range
                glyph = AnnularWedge(x=10, y=10, inner_radius=(n.level * n.width),
                                     outer_radius=((n.level * n.width) + n.width),
                                     start_angle=n.right_bound, end_angle=(n.right_bound + n.range))
                plot.add_glyph(source, glyph)
                n_old = n
                count += 1
                DFS_visit(n)

    m = Node(3, None, 1)
    n = Node(3, None, 1)
    l = Node(2, [m], 1)
    f = Node(2, None, 1)
    g = Node(2, None, 1)
    h = Node(2, [n], 1)
    i = Node(2, None, 1)
    j = Node(2, None, 1)
    k = Node(2, None, 1)
    e = Node(1, [l, k, j], 3)
    b = Node(1, [f], 1)
    c = Node(1, [g, h], 2)
    d = Node(1, [i], 1)
    a = Node(0, [b, c, d, e], 7)

    Set_parent(a)

    source = ColumnDataSource()

    xdr = DataRange1d(start=5, end=15)
    ydr = DataRange1d(start=5, end=15)

    plot = Plot(title=None, x_range=xdr, y_range=ydr, plot_width=650, plot_height=400,
                h_symmetry=False, v_symmetry=False, min_border=0, toolbar_location=None)

    Sunburst(a)

    xaxis = LinearAxis()
    plot.add_layout(xaxis, 'below')

    yaxis = LinearAxis()
    plot.add_layout(yaxis, 'left')

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))

    curdoc().add_root(plot)

    k = figure(plot_width=650, plot_height=400)

    k.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)

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


if __name__ == '__main__':
    app.run(port=5000, debug=True)
