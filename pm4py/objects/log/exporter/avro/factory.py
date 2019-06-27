from pm4py.objects.log.exporter.avro.versions import classic

CLASSIC = "classic"

VERSIONS = {CLASSIC: classic.apply}


def apply(log, file_path, variant=CLASSIC, parameters=None):
    return VERSIONS[variant](log, file_path, parameters=parameters)
