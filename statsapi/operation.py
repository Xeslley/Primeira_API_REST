import numpy as np

def op_min(data):
    return min(data)

def op_max(data):
    return max(data)

def op_mean(data):
   return np.mean(data)

def op_median(data):
   return np.median(data)

# def op_mode(data):
#     return np.mod(data)

def op_range(data):
    return op_max(data) - op_min(data)