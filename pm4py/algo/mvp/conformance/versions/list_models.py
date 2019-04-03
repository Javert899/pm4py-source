from pm4py.objects.petri.petrinet import Marking
from pm4py.objects.petri.semantics import is_enabled, weak_execute


def apply(model, df, parameters=None):
    """
    (Off-line) Conformance Checking of database event logs

    Parameters
    -------------
    model
        List of models
    df
        Database event log
    parameters
        Parameters

    Returns
    -------------
    list_booleans
        List of booleans values, one per event, indicating if the execution of the event
        is fit according to the process model or not
    """
    if parameters is None:
        parameters = {}
    ret = []
    current_status = {}

    log = df.to_dict('records')

    for event in log:
        ev_conf, current_status, problems = apply_event(model, event, current_status, parameters=parameters)
        ret.append(ev_conf)
    return ret


def apply_event(model, event, current_status, parameters=None):
    """
    Conformance Checking of an event of a database event log given the models discovered for each perspective

    Parameters
    --------------
    model
        List of models
    event
        Database event
    current_status
        Current status of the execution
    parameters
        Parameters

    Returns
    --------------
    boolean
        Boolean value for event, indicating if the execution of the event is fit
    current_status
        Current status of the process model (updated with the new markings)
    problems
        List of class perspectives for which the replay has had some problem
    """
    if parameters is None:
        parameters = {}

    ret = True
    problems = []

    for attr in event:
        value = event[attr]
        if attr in model and type(value) is str:
            if attr not in current_status:
                current_status[attr] = {}
            if value not in current_status[attr]:
                im = Marking()
                current_status[attr][value] = [model[attr], im]
            activity = event["event_activity"]
            corr_t = [t for t in current_status[attr][value][0].transitions if t.label == activity]
            if len(corr_t) == 1:
                corr_t = corr_t[0]
                new_marking = weak_execute(corr_t, current_status[attr][value][1])
                if not is_enabled(corr_t, current_status[attr][value][0], current_status[attr][value][1]):
                    ret = False
                    problems.append(attr)
                current_status[attr][value][1] = new_marking

    return ret, current_status, problems
