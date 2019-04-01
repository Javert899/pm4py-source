from pm4py.objects.mongodb import parameters
from pm4py.objects.mongodb.versions import classic

CLASSIC = "classic"

VERSIONS = {CLASSIC: classic.apply}

HOSTNAME = parameters.HOSTNAME
PORT = parameters.PORT
DATABASE = parameters.DATABASE
COLLECTION = parameters.COLLECTION

DEFAULT_HOSTNAME = parameters.DEFAULT_HOSTNAME
DEFAULT_PORT = parameters.DEFAULT_PORT
DEFAULT_DATABASE = parameters.DEFAULT_DATABASE
DEFAULT_COLLECTION = parameters.DEFAULT_COLLECTION


def apply(variant=CLASSIC, parameters=None):
    """
    Retrieves a database log from a MongoDB database

    Parameters
    ------------
    variant
        Variant of the algorithm to use
    parameters
        Parameters of the algorithm, including: hostname, port, database, collection

    Returns
    ------------
    log
        Database log
    """
    if parameters is None:
        parameters = {}

    parameters[HOSTNAME] = parameters[HOSTNAME] if HOSTNAME in parameters else DEFAULT_HOSTNAME
    parameters[PORT] = parameters[PORT] if PORT in parameters else DEFAULT_PORT
    parameters[DATABASE] = parameters[DATABASE] if DATABASE in parameters else DEFAULT_DATABASE
    parameters[COLLECTION] = parameters[COLLECTION] if COLLECTION in parameters else DEFAULT_COLLECTION

    return VERSIONS[variant](parameters)
