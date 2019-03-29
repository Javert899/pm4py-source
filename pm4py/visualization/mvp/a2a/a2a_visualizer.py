import os
import shutil
import subprocess
import sys
import tempfile

import pydotplus


def apply(mvp, parameters=None):
    if parameters is None:
        parameters = {}
    image_format = parameters["format"] if "format" in parameters else "png"

    act_corr = {}

    graph = pydotplus.Dot()

    for index, perspective in enumerate(mvp):
        for n1 in mvp[perspective].dfg_matrix:
            if n1 not in act_corr:
                label = n1
                ne = pydotplus.Node(name=label, shape="box", style="filled", label=label,
                                    fillcolor="#AAAAFF")
                graph.add_node(ne)
                act_corr[n1] = ne
            for n2 in mvp[perspective].dfg_matrix[n1]:
                if n2 not in act_corr:
                    label = n2
                    ne = pydotplus.Node(name=label, shape="box", style="filled", label=label,
                                        fillcolor="#AAAAFF")
                    graph.add_node(ne)
                    act_corr[n2] = ne
                e = pydotplus.Edge(src=act_corr[n1], dst=act_corr[n2],
                                   label=perspective + " (" + str(mvp[perspective].dfg_matrix[n1][n2]) + ")",
                                   color=mvp[perspective].default_edges_color[0],
                                   fontcolor=mvp[perspective].default_edges_color[0])
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
