import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
from pm4py.objects.log.log import EventStream


def apply(file_path, parameters=None):
    if parameters is None:
        parameters = {}

    events = []

    reader = DataFileReader(open(file_path, "rb"), DatumReader())

    for event in reader:
        events.append(event)

    return EventStream(events)
