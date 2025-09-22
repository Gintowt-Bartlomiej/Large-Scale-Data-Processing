from typing import List

from lr import base


class LinearRegressionSequential(base.LinearRegression):
    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:
        n = len(X)
        mean_x = sum(X) / n
        mean_y = sum(y) / n

        numerator = sum((X[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        denominator = sum((X[i] - mean_x) ** 2 for i in range(n))

        b1 = numerator / denominator
        b0 = mean_y - b1 * mean_x

        self._coef = [b0, b1]

        return self
