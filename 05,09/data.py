import numpy as np

def get_data():
    np.random.seed(42)
    class_A = np.random.randn(20, 2) + np.array([2, 2])
    class_B = np.random.randn(20, 2) + np.array([-2, -2])
    class_C = np.random.randn(20, 2) + np.array([2, -2])

    X = np.vstack([class_A, class_B, class_C])
    y = np.array([0]*20 + [1]*20 + [2]*20)  # метки классов

    return X, y
