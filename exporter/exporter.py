import os
import pandas as pd


def export_df_as_csv(df, output_path, filename="results_complete.csv"):
    os.makedirs(output_path, exist_ok=True)

    full_path = os.path.join(output_path, filename)

    df.to_csv(full_path, index=False)
