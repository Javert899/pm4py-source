from pm4py.algo.other.anchors.interface.anchor_classification import AnchorClassification
from sklearn.linear_model import PassiveAggressiveClassifier
from pm4py.util.anchors import anchor_tabular
from pm4py.objects.log.util import get_log_representation
from pm4py.objects.log.log import EventLog
import sklearn.ensemble


class ClassicAnchorClassification(AnchorClassification):
    def __init__(self, log, target, classes, parameters=None):
        """
        Initialize the Anchors classification

        Parameters
        ------------
        log
            Log
        target
            Numerical target of the classification
        classes
            Classes (of the classification)
        parameters
            Parameters of the algorithm

        Returns
        ------------
        anchors
            Anchors classifier
        """
        if parameters is None:
            parameters = {}

        self.parameters = parameters

        self.log = log
        self.data, self.feature_names, self.str_tr_attr, self.str_ev_attr, self.num_tr_attr, self.num_ev_attr = get_log_representation.get_default_representation_with_attribute_names(
            self.log)
        self.target = target
        self.classes = classes

        AnchorClassification.__init__(self, self.log, target, classes, parameters=None)

    def train(self):
        """
        Train the anchors classifier (underlying is random forest classifier)
        """
        self.classifier = sklearn.ensemble.RandomForestClassifier(n_estimators=50)
        self.explainer = anchor_tabular.AnchorTabularExplainer(self.classes, self.feature_names, self.data,
                                                               categorical_names={})
        self.explainer.fit(self.data, self.feature_names, self.data, self.feature_names)
        self.classifier.fit(self.explainer.encoder.transform(self.data), self.target)

    def predict(self, trace):
        """
        Predict using the underlying classifier

        Parameters
        -------------
        trace
            Trace

        Returns
        --------------
        prediction
            Predicted target class
        """
        log = EventLog()
        log.append(trace)
        data, feature_names = get_log_representation.get_representation(log, self.str_tr_attr, self.str_ev_attr,
                                                                        self.num_tr_attr, self.num_ev_attr,
                                                                        feature_names=self.feature_names)

        prediction = self.classifier.predict(data)[0]
        return self.classes[prediction]

    def explain(self, trace, threshold=0.95):
        """
        Provides explanation of the given decision

        Parameters
        -------------
        trace
            Trace
        threshold
            Threshold of the decision explanation
        """
        log = EventLog()
        log.append(trace)
        data, feature_names = get_log_representation.get_representation(log, self.str_tr_attr, self.str_ev_attr,
                                                                        self.num_tr_attr, self.num_ev_attr,
                                                                        feature_names=self.feature_names)

        exp = self.explainer.explain_instance(data[0], self.classifier.predict, threshold=0.95)

        return ' AND '.join(exp.names())
