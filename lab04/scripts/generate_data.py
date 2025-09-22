"""Script for generation of artificial datasets."""
import argparse
from typing import List
from typing import Tuple
import os
import numpy as np
import pickle


def get_args() -> argparse.Namespace:
    """Parses script arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num-samples",
        required=True,
        help="Number of samples to generate",
        type=int,
    )
    parser.add_argument(
        "--out-dir",
        required=True,
        help="Name of directory to save generated data",
        type=str,
    )

    return parser.parse_args()


def generate_data(num_samples: int) -> Tuple[List[float], List[float]]:
    """Generated X, y with given number of data samples."""
    np.random.seed(42)
    X = np.random.uniform(-10, 10, num_samples)
    y = 2 * X + 5 + np.random.normal(0, 1, num_samples)
    return X.tolist(), y.tolist()


def main() -> None:
    """Runs script."""
    args = get_args()
    num_samples = args.num_samples
    out_dir = args.out_dir

    os.makedirs(out_dir, exist_ok=True)
    X, y = generate_data(num_samples)

    output_file = os.path.join(out_dir, f"{num_samples}.txt")

    with open(output_file, "w") as f:
        for x_val, y_val in zip(X, y):
            f.write(f"{x_val} {y_val}\n")


if __name__ == "__main__":
    main()
