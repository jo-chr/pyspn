import numpy as np

#np.random.seed(1337)

def get_delay(distribution, delay: int = 0, lmbda: float = 0, a = 0, b = 0):
    
    if distribution == "DET":
        return delay
    
    if distribution == "EXP":
        return np.random.exponential(scale = lmbda)

    if distribution == "NORM":
        return np.random.normal(a,b)
        
    
    
