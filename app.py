from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def plot():
    from bokeh.plotting import figure
    from bokeh.embed import components
    from bokeh.resources import CDN
    p = figure(plot_width=650, plot_height=400)

    p.quad(top=[2, 3, 4], bottom=[1, 2, 3], left=[1, 2, 3],
           right=[1.2, 2.5, 3.7], color="#B3DE69")

    k = figure(plot_width=650, plot_height=400)

    k.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)

    script1, div1 = components(p)
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
