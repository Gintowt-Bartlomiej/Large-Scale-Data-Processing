"""Script for time measurement experiments on linear regression models."""
import argparse
from typing import List, Tuple, Type
import numpy as np
import matplotlib.pyplot as plt
import os
import json
import time
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + "/.."))
import lr


def get_args() -> argparse.Namespace:
    """Parses script arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--datasets-dir",
        required=True,
        help="Name of directory with generated datasets",
        type=str,
    )
    return parser.parse_args()


def measure_time(model_cls, X, y, repeats=5, num_threads=None, num_processes=None):
    times = []

    for _ in range(repeats):
        if num_threads is not None:
            model = model_cls(num_threads=num_threads)
        elif num_processes is not None:
            model = model_cls(num_processes=num_processes)
        else:
            model = model_cls()

        start_time = time.perf_counter()
        model.fit(X, y)
        end_time = time.perf_counter()
        times.append(end_time - start_time)

    return np.mean(times)


def generate_plots(results, dataset_names, python_version):
    os.makedirs("data", exist_ok=True)

    comparison_filename = f"data/comparison_py{python_version}.png"
    scaling_filename = f"data/scaling_py{python_version}.png"

    plt.figure(figsize=(10, 6))
    for model_name, times in results.items():
        if "2 threads" in model_name or "2 processes" in model_name or "Sequential" in model_name or "Numpy" in model_name:
            plt.plot(dataset_names, times, label=model_name, marker="o")

    plt.xlabel("Dataset")
    plt.ylabel("Time (s)")
    plt.title("Comparison of linear regression implementations speed")
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(comparison_filename)
    plt.close()

    scaling_results = {k: v for k, v in results.items() if "threads" in k or "processes" in k}

    plt.figure(figsize=(10, 6))
    for model_name, times in scaling_results.items():
        plt.plot(dataset_names, times, label=model_name, marker="o")

    plt.xlabel("Dataset")
    plt.ylabel("Time (s)")
    plt.title("Threads/Processes comparison on datasets")
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(scaling_filename)
    plt.close()


def run_experiments(
    models: List[Type[lr.base.LinearRegression]],
    datasets: List[Tuple[List[float], List[float]]],
    dataset_names: List[str],
    python_version: str
):
    results = {}
    thread_process_counts = [2, 4, 8]

    for model_cls in models:
        if "Threads" in model_cls.__name__:
            for count in thread_process_counts:
                model_name = f"{model_cls.__name__} ({count} threads)"
                results[model_name] = []
                for X, y in datasets:
                    avg_time = measure_time(model_cls, X, y, num_threads=count)
                    results[model_name].append(avg_time)

        elif "Process" in model_cls.__name__:
            for count in thread_process_counts:
                model_name = f"{model_cls.__name__} ({count} processes)"
                results[model_name] = []
                for X, y in datasets:
                    avg_time = measure_time(model_cls, X, y, num_processes=count)
                    results[model_name].append(avg_time)

        else:
            model_name = model_cls.__name__
            results[model_name] = []
            for X, y in datasets:
                avg_time = measure_time(model_cls, X, y)
                results[model_name].append(avg_time)

    os.makedirs("data", exist_ok=True)

    json_filename = f"data/time_measurements_py{python_version}.json"
    with open(json_filename, "w") as f:
        json.dump(results, f, indent=4)

    generate_plots(results, dataset_names, python_version)


def main() -> None:
    """Runs script."""
    args = get_args()

    models = [
        lr.LinearRegressionNumpy,
        lr.LinearRegressionProcess,
        lr.LinearRegressionSequential,
        lr.LinearRegressionThreads,
    ]

    datasets = []
    dataset_names = []
    for filename in sorted(os.listdir(args.datasets_dir)):
        if filename.endswith(".txt"):
            file_path = os.path.join(args.datasets_dir, filename)
            data = np.loadtxt(file_path)
            X, y = data[:, 0].tolist(), data[:, 1].tolist()
            datasets.append((X, y))
            dataset_names.append(filename)

    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    run_experiments(models, datasets, dataset_names, python_version)


if __name__ == "__main__":
    main()

