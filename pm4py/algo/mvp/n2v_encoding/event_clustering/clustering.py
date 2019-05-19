from pm4py.algo.mvp.n2v_encoding import encode

def apply(df, parameters=None):
    if parameters is None:
        parameters = {}

    encoding = parameters["encoding"] if "encoding" in parameters else encode.from_df(df, parameters=parameters)

    