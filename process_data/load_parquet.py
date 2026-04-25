import pandas as pd
import fastparquet


def load_parquet_to_dataframe(parquet_file):
    df = pd.read_parquet(parquet_file)

    return df
