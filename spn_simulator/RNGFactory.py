import numpy as np
import random
from statsmodels.distributions.empirical_distribution import ECDF
from scipy.stats import rv_histogram

def get_delay(distribution, delay: int = 0, lmbda: float = 0, a = 0, b = 0, ecdf = ECDF, rv_hist = rv_histogram):

    if distribution == "DET":
        return delay
    
    if distribution == "EXP":
        return np.random.exponential(scale = lmbda)

    if distribution == "NORM":
        return np.random.normal(a,b)

    if distribution == "ECDF":
        rn = random.uniform(0, 1)
        y_idx = min(range(len(ecdf.y)), key=lambda i: abs(ecdf.y[i]-rn))
        return ecdf.x[y_idx]

    if distribution == "SCIPY_HIST":
        return rv_hist.rvs(size = 1)[0]*24 #days to hours