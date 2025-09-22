from typing import List
import multiprocessing
from lr import base


class LinearRegressionProcess(base.LinearRegression):
    def __init__(self, num_processes = 4):
        super().__init__()
        self.num_processes = num_processes

    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:
        n = len(X)
        mean_x = sum(X) / n
        mean_y = sum(y) / n
        
        batch_size = n // self.num_processes

        def compute_partial(start, end, queue):
            num = sum((X[i] - mean_x) * (y[i] - mean_y) for i in range(start, end))
            denom = sum((X[i] - mean_x) ** 2 for i in range(start, end))
            queue.put((num, denom))

        queue = multiprocessing.Queue()
        processes = []

        for i in range(self.num_processes):
            start = i * batch_size
            end = n if i == self.num_processes - 1 else (i + 1) * batch_size
            p = multiprocessing.Process(target=compute_partial, args=(start, end, queue))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

        numerator = 0
        denominator = 0
        while not queue.empty():
            num, denom = queue.get()
            numerator += num
            denominator += denom

        b1 = numerator / denominator
        b0 = mean_y - b1 * mean_x

        self._coef = [b0, b1]

        return self
