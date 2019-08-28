from pm4py.algo.mvp.gen_framework.models import model1 as model1_object
from pm4py.visualization.mvp.gen_framework.versions import model1 as model1_visualization
from graphviz import Digraph
from pm4py.visualization.common import gview
from pm4py.visualization.common import save as gsave
import uuid
import tempfile

def apply(model, parameters=None):
    if parameters is None:
        parameters = {}

    if type(model) is model1_object.MVPModel1:
        return model1_visualization.apply(model, parameters=parameters)

def save(gviz, output_file_path):
    """
    Save the diagram

    Parameters
    -----------
    gviz
        GraphViz diagram
    output_file_path
        Path where the GraphViz output should be saved
    """
    gsave.save(gviz, output_file_path)


def view(gviz):
    """
    View the diagram

    Parameters
    -----------
    gviz
        GraphViz diagram
    """
    return gview.view(gviz)
