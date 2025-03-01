import os
import numpy

data = {}


def load_numbers():
    """Reads the numbers from the file and loads them into a list."""
    data_path = os.path.join(os.path.dirname(__file__), "data", "input.txt")
    return numpy.loadtxt(data_path, dtype=int).tolist()
