from typing import List
import numpy as np
from lr import base


class LinearRegressionNumpy(base.LinearRegression):
    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:
        X_np = np.array(X)
        y_np = np.array(y)

        mean_x = np.mean(X_np)
        mean_y = np.mean(y_np)

        numerator = np.sum((X_np - mean_x) * (y_np - mean_y))
        denominator = np.sum((X_np - mean_x) ** 2)

        b1 = numerator / denominator
        b0 = mean_y - b1 * mean_x

        self._coef = [b0, b1]

        return self
