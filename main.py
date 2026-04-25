from orchestrator import Orchestrator


def main():
    output_path = "./output"
    checkpoint_path = "./temp/temp_checkpoint.json"
    timeout_path = "./temp/temp_timeout.json"
    

    orchestrator = Orchestrator(
        parquet_path="./input/0000.parquet",
        output_path=output_path,
        checkpoint_path=checkpoint_path,
        timeout_path=timeout_path
    )

    df_results = orchestrator.run()

    print(df_results.head())


if __name__ == "__main__":
    main()