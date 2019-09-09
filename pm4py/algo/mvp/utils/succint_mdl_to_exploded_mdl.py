from pm4py.algo.mvp.utils import succint_stream_to_exploded_stream
import pandas as pd


def apply(df):
    stream = df.to_dict('r')

    exploded_stream = succint_stream_to_exploded_stream.apply(stream)

    return pd.DataFrame(exploded_stream)

