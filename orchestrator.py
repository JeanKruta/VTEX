import os
import time

import pandas as pd
from tqdm import tqdm

from retriever.retriever import TFIDFRetriever
from process_data.load_parquet import load_parquet_to_dataframe
from process_data.data_processing import PreprocessingPipeline
from agent_schema.qa_agent import agent_qa
from exporter.exporter import export_df_as_csv
from controller.checkpoint import CheckpointManager
from controller.timeout_manager import TimeoutManager


class Orchestrator:
    def __init__(self, parquet_path, output_path, checkpoint_path, timeout_path):
        self.parquet_path = parquet_path
        self.output_path = output_path
        self.checkpoint_path = checkpoint_path
        self.timeout_path = timeout_path

        self.timeout_manager = TimeoutManager(timeout_path)
        
        self.timeout_indices = []

        self.df = None
        self.pipeline = PreprocessingPipeline()
        self.checkpoint = CheckpointManager(self.checkpoint_path)

    def load_data(self):
        self.df = load_parquet_to_dataframe(self.parquet_path)
        return self.df

    def preprocess(self):
        self.df = self.pipeline.run(self.df)
        return self.df

    def run_inference(self):

        last_index, saved_results = self.checkpoint.load()
        self.timeout_indices = self.timeout_manager.load()

        self.results = saved_results

        print(f"\nRetomando do índice {last_index}...")

        for i, row in tqdm(self.df.iterrows(), total=len(self.df)):

            if i <= last_index:
                continue

            question = row["question"]
            content = row["content"]

            retriever = TFIDFRetriever([content])

            prediction = agent_qa(
                question=question,
                retriever=retriever
            )

            if "TIMEOUT" in prediction:
                item = {
                        "id": i,
                        "row": row.to_dict()
                    }
                self.timeout_indices.append(item)
                self.timeout_manager.save(self.timeout_indices)

            self.results.append({
                "id": i,
                "question": question,
                "prediction": prediction,
                "label": row["data_category_QA"]
            })

            self.checkpoint.save(i, self.results)

            time.sleep(0.2)

        self.df = pd.DataFrame(self.results)
        return self.df

    def reprocess_timeouts(self):
        if not self.timeout_indices:
            return

        print(f"\nReprocessando {len(self.timeout_indices)} timeouts...")

        results_map = {r["id"]: r for r in self.results}

        for item in tqdm(self.timeout_indices):
            i = item["id"]
            row = item["row"]

            question = row["question"]
            content = row["content"]

            retriever = TFIDFRetriever([content])

            prediction = agent_qa(
                question=question,
                retriever=retriever,
                max_retries=3
            )

            results_map[i]["prediction"] = prediction

            time.sleep(0.5)

        self.results = list(results_map.values())

    def export(self):
        export_df_as_csv(self.df, self.output_path)
        return self.df

    def run(self):
        self.load_data()
        self.preprocess()
        self.run_inference()
        self.reprocess_timeouts()
        self.export()

        self.timeout_manager.clear()
        self.checkpoint.clear()

        return self.df