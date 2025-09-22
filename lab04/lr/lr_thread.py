from typing import List
import threading
from lr import base


class LinearRegressionThreads(base.LinearRegression):
    def __init__(self, num_threads = 4):
        super().__init__()
        self.num_threads = num_threads

    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:
        n = len(X)
        mean_x = sum(X) / n
        mean_y = sum(y) / n

        batch_size = n // self.num_threads

        results = {"numerator": 0, "denominator": 0}
        lock = threading.Lock()

        def compute_partial(start, end):
            num = sum((X[i] - mean_x) * (y[i] - mean_y) for i in range(start, end))
            denom = sum((X[i] - mean_x) ** 2 for i in range(start, end))
            with lock:
                results["numerator"] += num
                results["denominator"] += denom

        threads = []
        for i in range(self.num_threads):
            start = i * batch_size
            end = n if i == self.num_threads - 1 else (i + 1) * batch_size
            t = threading.Thread(target=compute_partial, args=(start, end))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        b1 = results["numerator"] / results["denominator"]
        b0 = mean_y - b1 * mean_x

        self._coef = [b0, b1]

        return self
