import avro.schema
from avro.datafile import DataFileReader, DataFileWriter
from avro.io import DatumReader, DatumWriter
from pm4py.objects.conversion.log import factory as log_conv_factory
import json
from datetime import datetime


def give_type(value):
    if type(value) is str:
        return ["string", "null"]
    if type(value) is datetime:
        return ["long", "null"]
    return None


def transf(k,v,all_attribute_types):
    if all_attribute_types[k] == ["long", "null"]:
        return int(v.timestamp())
    return v


def apply(log, file_path, parameters=None):
    if parameters is None:
        parameters = {}

    schema_dest = file_path.split(".")[0] + ".avsc"
    stream = log_conv_factory.apply(log, variant=log_conv_factory.TO_EVENT_STREAM)

    all_attribute_types = {}

    for event in stream:
        for attr in event:
            if attr not in all_attribute_types:
                this_type = give_type(event[attr])
                all_attribute_types[attr] = this_type

    for attr in event:
        if all_attribute_types[attr] is None:
            del all_attribute_types[attr]

    schema = {}
    schema["namespace"] = "hello"
    schema["type"] = "record"
    schema["name"] = "world"
    schema["fields"] = []

    for attr in all_attribute_types:
        schema["fields"].append({"name": attr, "type": all_attribute_types[attr]})

    F = open(schema_dest, "w")
    F.write(json.dumps(schema))
    F.close()

    schema = avro.schema.Parse(open(schema_dest, "r").read())
    writer = DataFileWriter(open(file_path, "wb"), DatumWriter(), schema)

    for event in stream:
        event_red = dict({k: transf(k,v,all_attribute_types) for k, v in event.items() if k in all_attribute_types})

        writer.append(event_red)

    writer.close()
