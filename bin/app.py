from flask import Flask, render_template, request
import matplotlib.pyplot as plt

from matplotlib.collections import PolyCollection
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(
    __name__,
    instance_relative_config=False,
    template_folder="templates"
)

def polygon_under_graph(x, y):
    """
    Construct the vertex list which defines the polygon filling the space under
    the (x, y) line graph. This assumes x is in ascending order.
    """
    return [(x[0], 0.), *zip(x, y), (x[-1], 0.)]

def create_graph():
    filename = 'demo'

    # random but consistant data
    lst = [2,9,4,6,4]
    x = np.linspace(float(min(lst)), float(max(lst)), 5)
    lambdas = range(1, 5)

    # clear buffer
    plt.clf()
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # Plot a basic polygon.
    # verts[i] is a list of (x, y) pairs defining polygon i.
    gamma = np.vectorize(math.gamma)
    verts = [polygon_under_graph(x, l**x * np.exp(-l) / gamma(x + 1))
            for l in lambdas]
    facecolors = plt.colormaps['viridis_r'](np.linspace(0, 1, len(verts)))

    poly = PolyCollection(verts, facecolors=facecolors, alpha=.7)
    ax.add_collection3d(poly, zs=lambdas, zdir='y')

    ax.set(xlim=(0, 5), ylim=(1, 5), zlim=(0, 0.35),
        xlabel='x', ylabel=r'$\lambda$', zlabel='probability')
    plt.savefig(f'static/img/{filename}.png')

@app.route('/', methods=['GET'])
def getIndex():
    create_graph()
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5000, debug = True)