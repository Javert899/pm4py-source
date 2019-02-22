from pm4py.objects.openslex.importer.versions import classic

CLASSIC = "classic"

VERSIONS = {CLASSIC: classic.apply}

def apply(file_path, parameters=None, variant=CLASSIC):
    return VERSIONS[variant](file_path, parameters=parameters)