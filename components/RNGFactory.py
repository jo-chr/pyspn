import scipy as sp

def get_delay(distribution, a=0.0, b=1.0, c=0.0, d=0.0):

    if distribution == "det":
        return a
    
    if distribution == "uniform":
        return abs(sp.stats.uniform.rvs(a, b))

    if distribution == "norm":
        return abs(sp.stats.norm.rvs(a, b))

    if distribution == "uniform":
        return abs(sp.stats.uniform.rvs(a, b))

    if distribution == "cauchy":
        return abs(sp.stats.cauchy.rvs(a, b))

    if distribution == "triang":
        return abs(sp.stats.triang.rvs(a, b, c))

    if distribution == "expon":
        return abs(sp.stats.expon.rvs(a, b))

    if distribution == "weibull_min":
        return abs(sp.stats.weibull_min.rvs(a, b, c))

    if distribution == "weibull_max":
        return abs(sp.stats.weibull_max.rvs(a, b, c))

    if distribution == "lognorm":
        return abs(sp.stats.lognorm.rvs(a, b, c))

    if distribution == "gamma":
        return abs(sp.stats.gamma.rvs(a, b, c))

    if distribution == "poisson":
        return abs(sp.stats.poisson.rvs(a, b))
    
    if distribution == "exponpow":
        return abs(sp.stats.exponpow.rvs(a, b, c))
