from pm4py.objects.mongodb import parameters
import pymongo
from datetime import datetime

HOSTNAME = parameters.HOSTNAME
PORT = parameters.PORT
DATABASE = parameters.DATABASE
COLLECTION = parameters.COLLECTION


def apply(parameters):
    """
    Retrieves a database log from a MongoDB database

    Parameters
    ------------
    parameters
        Parameters of the algorithm, including: hostname, port, database, collection

    Returns
    ------------
    log
        Database log
    """

    hostname = parameters[HOSTNAME]
    port = parameters[PORT]
    database = parameters[DATABASE]
    collection = parameters[COLLECTION]

    stream = []

    myclient = pymongo.MongoClient("mongodb://localhost:27018/")
    db = myclient["crmEvents"]
    count = 1
    for res in db["crmEvents"].find({"concept:name":{"$exists": True}}):
        event_id = str(count)
        event_activity = res["concept:name"]
        event_timestamp = datetime.fromtimestamp(res["clusterTime"].time)

        for key in res["fullDocument"]:
            stream.append({"event_id": event_id, "event_activity": event_activity, "event_timestamp": event_timestamp, key: res["fullDocument"][key]})

        count = count + 1

    print(stream)