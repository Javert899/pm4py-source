import tempfile

import pydotplus
import shutil
import os
import sys
import subprocess

from pm4py.algo.mvp.utils import exploded_mdl_to_grouped_stream_old

def apply(df, parameters=None):
    if parameters is None:
        parameters = {}
    image_format = parameters["format"] if "format" in parameters else "png"

    grouped_stream = exploded_mdl_to_grouped_stream_old.apply(df, remove_common=True, include_activity_timest_in_key=True)
    graph = pydotplus.Dot()

    obj_corr = {}

    for event in grouped_stream:
        label_event = event[0] + "\\n(activity=\\n" + event[1] + ")"
        ne = pydotplus.Node(name=label_event, shape="box", style="filled", label=label_event, fillcolor="#FFAAAA")
        graph.add_node(ne)
        for object in grouped_stream[event]:
            item = [(k, v) for k, v in object.items()][0]
            if item not in obj_corr:
                obj_corr[item] = ne
            else:
                e = pydotplus.Edge(src=obj_corr[item], dst=ne, label=item[1]+" (class="+item[0]+")")
                graph.add_edge(e)
                obj_corr[item] = ne
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