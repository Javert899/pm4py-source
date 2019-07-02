import pyarrow as pa
import pyarrow.parquet as pq
import os
import shutil


def apply(df, path, parameters=None):
    """
    Exports a dataframe to a Parquet file

    Parameters
    ------------
    df
        Dataframe
    path
        Path
    parameters
        Possible parameters of the algorithm
    """
    if parameters is None:
        parameters = {}

    compression = parameters["compression"] if "compression" in parameters else "snappy"
    partition_cols = parameters["partition_cols"] if "partition_cols" in parameters else None

    df.columns = [x.replace(":", "AAA") for x in df.columns]
    if partition_cols is not None:
        partition_cols = [x.replace(":", "AAA") for x in partition_cols]
    df = pa.Table.from_pandas(df)

    if partition_cols is not None:
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        pq.write_to_dataset(df, path, compression=compression, partition_cols=partition_cols)
    else:
        pq.write_table(df, path, compression=compression)


def export_to_dataset(df, path, parameters=None):
    if parameters is None:
        parameters = {}

    compression = parameters["compression"] if "compression" in parameters else "snappy"
    partition_cols = parameters["partition_cols"] if "partition_cols" in parameters else None

    df.columns = [x.replace(":", "AAA") for x in df.columns]

    df = pa.Table.from_pandas(df)
    pq.write_to_dataset(df, root_path=path, compression=compression, partition_cols=partition_cols)
