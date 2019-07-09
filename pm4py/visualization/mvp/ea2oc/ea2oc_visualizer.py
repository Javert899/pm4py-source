import tempfile

import pydotplus
import shutil
import os
import sys
import subprocess

import networkx as nx


def apply(encoding, parameters=None):
    if parameters is None:
        parameters = {}
    image_format = parameters["format"] if "format" in parameters else "png"

    graph0 = encoding["graph"]
    graph = pydotplus.Dot()

    nodes = {}

    for node in graph0.nodes:
        node_label = str(node)

        if "event=" in node_label:
            n = pydotplus.Node(name=node_label, shape="box", style="filled", label=node_label, fillcolor="#FF0000")
        elif "object=" in node_label:
            n = pydotplus.Node(name=node_label, shape="box", style="filled", label=node_label, fillcolor="#FFFFFF")
        elif "ACTIVITY=" in node_label:
            n = pydotplus.Node(name=node_label, shape="box", style="filled", label=node_label, fillcolor="#00FF00")
        else:
            n = pydotplus.Node(name=node_label, shape="box", style="filled", label=node_label, fillcolor="#5555FF")
        graph.add_node(n)

        nodes[node_label] = n
    for edge in graph0.edges:
        source = str(edge[0])
        target = str(edge[1])

        if "event=" in target:
            (source, target) = (target, source)
        elif "object=" in target and not "event=" in source:
            (source, target) = (target, source)

        e = pydotplus.Edge(src=nodes[source], dst=nodes[target])
        graph.add_edge(e)

    file_name = tempfile.NamedTemporaryFile(suffix='.' + image_format)
    file_name.close()
    graph.write(file_name.name, format=image_format)

    return file_name


def view(figure):
    """
    View on the screen a figure that has been rendered

    Parameters
    ----------
    figure
        figure
    """
    try:
        filename = figure.name
        figure = filename
    except AttributeError:
        # continue without problems, a proper path has been provided
        pass

    is_ipynb = False

    try:
        get_ipython()
        is_ipynb = True
    except NameError:
        pass

    if is_ipynb:
        from IPython.display import Image
        return Image(open(figure, "rb").read())
    else:
        if sys.platform.startswith('darwin'):
            subprocess.call(('open', figure))
        elif os.name == 'nt':  # For Windows
            os.startfile(figure)
        elif os.name == 'posix':  # For Linux, Mac, etc.
            subprocess.call(('xdg-open', figure))


def save(figure, output_file_path):
    """
    Save a figure that has been rendered

    Parameters
    -----------
    figure
        figure
    output_file_path
        Path where the figure should be saved
    """
    try:
        filename = figure.name
        figure = filename
    except AttributeError:
        # continue without problems, a proper path has been provided
        pass

    shutil.copyfile(figure, output_file_path)