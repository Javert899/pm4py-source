from pm4py.objects.log.importer.avro.versions import classic

CLASSIC = "classic"

VERSIONS = {CLASSIC: classic.apply}


def apply(file_path, variant=CLASSIC, parameters=None):
    if parameters is None:
        parameters = {}

    return VERSIONS[variant](file_path)
