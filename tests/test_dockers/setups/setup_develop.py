from os.path import dirname, join

from setuptools import setup

import pm4py


def read_file(filename):
    with open(join(dirname(__file__), filename)) as f:
        return f.read()


setup(
    name=pm4py.__name__,
    version=pm4py.__version__,
    description=pm4py.__doc__.strip(),
    long_description=read_file('README'),
    author=pm4py.__author__,
    author_email=pm4py.__author_email__,
    py_modules=[pm4py.__name__],
    include_package_data=True,
    packages=['pm4py', 'pm4py.algo', 'pm4py.algo.discovery', 'pm4py.algo.discovery.dfg',
              'pm4py.algo.discovery.dfg.utils', 'pm4py.algo.discovery.dfg.adapters',
              'pm4py.algo.discovery.dfg.adapters.pandas', 'pm4py.algo.discovery.dfg.versions',
              'pm4py.algo.discovery.alpha', 'pm4py.algo.discovery.alpha.utils', 'pm4py.algo.discovery.alpha.versions',
              'pm4py.algo.discovery.alpha.data_structures', 'pm4py.algo.discovery.causal',
              'pm4py.algo.discovery.causal.versions', 'pm4py.algo.discovery.inductive',
              'pm4py.algo.discovery.inductive.util', 'pm4py.algo.discovery.inductive.versions',
              'pm4py.algo.discovery.inductive.versions.dfg', 'pm4py.algo.discovery.inductive.versions.dfg.util',
              'pm4py.algo.discovery.inductive.versions.dfg.data_structures', 'pm4py.algo.discovery.transition_system',
              'pm4py.algo.discovery.transition_system.util', 'pm4py.algo.discovery.transition_system.versions',
              'pm4py.algo.filtering', 'pm4py.algo.filtering.dfg', 'pm4py.algo.filtering.common',
              'pm4py.algo.filtering.common.timestamp', 'pm4py.algo.filtering.common.attributes',
              'pm4py.algo.filtering.common.end_activities', 'pm4py.algo.filtering.common.start_activities',
              'pm4py.algo.filtering.pandas', 'pm4py.algo.filtering.pandas.cases', 'pm4py.algo.filtering.pandas.paths',
              'pm4py.algo.filtering.pandas.variants', 'pm4py.algo.filtering.pandas.timestamp',
              'pm4py.algo.filtering.pandas.attributes', 'pm4py.algo.filtering.pandas.auto_filter',
              'pm4py.algo.filtering.pandas.end_activities', 'pm4py.algo.filtering.pandas.start_activities',
              'pm4py.algo.filtering.tracelog', 'pm4py.algo.filtering.tracelog.cases',
              'pm4py.algo.filtering.tracelog.paths', 'pm4py.algo.filtering.tracelog.variants',
              'pm4py.algo.filtering.tracelog.timestamp', 'pm4py.algo.filtering.tracelog.attributes',
              'pm4py.algo.filtering.tracelog.auto_filter', 'pm4py.algo.filtering.tracelog.end_activities',
              'pm4py.algo.filtering.tracelog.start_activities', 'pm4py.algo.simulation', 'pm4py.algo.simulation.simple',
              'pm4py.algo.simulation.simple.model', 'pm4py.algo.simulation.simple.model.pandas',
              'pm4py.algo.simulation.simple.model.pandas.versions', 'pm4py.algo.simulation.simple.model.tracelog',
              'pm4py.algo.simulation.simple.model.tracelog.versions', 'pm4py.algo.simulation.simple.filtering',
              'pm4py.algo.simulation.simple.filtering.pandas', 'pm4py.algo.simulation.simple.filtering.pandas.versions',
              'pm4py.algo.simulation.simple.filtering.tracelog',
              'pm4py.algo.simulation.simple.filtering.tracelog.versions', 'pm4py.algo.simulation.playout',
              'pm4py.algo.simulation.playout.versions', 'pm4py.algo.simulation.playout.data_structures',
              'pm4py.algo.conformance', 'pm4py.algo.conformance.alignments',
              'pm4py.algo.conformance.alignments.versions', 'pm4py.algo.conformance.tokenreplay',
              'pm4py.algo.conformance.tokenreplay.versions', 'pm4py.algo.conformance.tokenreplay.diagnostics',
              'pm4py.algo.enhancement', 'pm4py.algo.enhancement.sna', 'pm4py.algo.enhancement.sna.metrics',
              'pm4py.algo.enhancement.sna.metrics.handover', 'pm4py.algo.enhancement.sna.metrics.handover.versions',
              'pm4py.algo.enhancement.sna.metrics.real_handover',
              'pm4py.algo.enhancement.sna.metrics.real_handover.versions',
              'pm4py.algo.enhancement.sna.metrics.similar_activities',
              'pm4py.algo.enhancement.sna.metrics.similar_activities.versions',
              'pm4py.algo.enhancement.sna.transformer', 'pm4py.algo.enhancement.sna.transformer.common',
              'pm4py.algo.enhancement.sna.transformer.pandas', 'pm4py.algo.enhancement.sna.transformer.pandas.versions',
              'pm4py.algo.enhancement.sna.transformer.tracelog',
              'pm4py.algo.enhancement.sna.transformer.tracelog.versions', 'pm4py.util', 'pm4py.objects',
              'pm4py.objects.log', 'pm4py.objects.log.util', 'pm4py.objects.log.adapters',
              'pm4py.objects.log.adapters.pandas', 'pm4py.objects.log.exporter', 'pm4py.objects.log.exporter.csv',
              'pm4py.objects.log.exporter.csv.versions', 'pm4py.objects.log.exporter.xes',
              'pm4py.objects.log.exporter.xes.versions', 'pm4py.objects.log.importer', 'pm4py.objects.log.importer.csv',
              'pm4py.objects.log.importer.csv.versions', 'pm4py.objects.log.importer.xes',
              'pm4py.objects.log.importer.xes.versions', 'pm4py.objects.sna', 'pm4py.objects.petri',
              'pm4py.objects.petri.common', 'pm4py.objects.petri.exporter', 'pm4py.objects.petri.importer',
              'pm4py.objects.conversion', 'pm4py.objects.conversion.log', 'pm4py.objects.conversion.log.versions',
              'pm4py.objects.conversion.process_tree', 'pm4py.objects.conversion.process_tree.versions',
              'pm4py.objects.process_tree', 'pm4py.objects.random_variables', 'pm4py.objects.random_variables.normal',
              'pm4py.objects.random_variables.uniform', 'pm4py.objects.random_variables.constant0',
              'pm4py.objects.random_variables.exponential', 'pm4py.objects.stochastic_petri',
              'pm4py.objects.transition_system', 'pm4py.evaluation', 'pm4py.evaluation.precision',
              'pm4py.evaluation.precision.versions', 'pm4py.evaluation.simplicity',
              'pm4py.evaluation.simplicity.versions', 'pm4py.evaluation.generalization',
              'pm4py.evaluation.generalization.versions', 'pm4py.evaluation.replay_fitness',
              'pm4py.evaluation.replay_fitness.versions', 'pm4py.statistics', 'pm4py.statistics.traces',
              'pm4py.statistics.traces.common', 'pm4py.statistics.traces.pandas', 'pm4py.statistics.traces.tracelog',
              'pm4py.visualization', 'pm4py.visualization.dfg', 'pm4py.visualization.dfg.versions',
              'pm4py.visualization.sna', 'pm4py.visualization.sna.versions', 'pm4py.visualization.common',
              'pm4py.visualization.graphs', 'pm4py.visualization.graphs.util', 'pm4py.visualization.graphs.versions',
              'pm4py.visualization.petrinet', 'pm4py.visualization.petrinet.util',
              'pm4py.visualization.petrinet.common', 'pm4py.visualization.petrinet.versions',
              'pm4py.visualization.process_tree', 'pm4py.visualization.process_tree.versions',
              'pm4py.visualization.transition_system', 'pm4py.visualization.transition_system.util',
              'pm4py.visualization.transition_system.versions', 'tests.documentation_tests'],
    url='http://www.pm4py.org',
    license='GPL 3.0',
    install_requires=[
        'pyvis',
        'networkx>=2.2',
        'matplotlib==2.2.2',
        'numpy',
        'ciso8601',
        'cvxopt',
        'lxml',
        'graphviz',
        'pandas',
        'scipy',
        'scikit-learn'
    ],
    project_urls={
        'Documentation': 'http://pm4py.pads.rwth-aachen.de/documentation/',
        'Source': 'https://github.com/pm4py/pm4py-source',
        'Tracker': 'https://github.com/pm4py/pm4py-source/issues',
    }
)