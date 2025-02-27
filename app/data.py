import numpy

data = {}


def load_numbers():
    """Reads the numbers from the file and loads them into a list."""
    return numpy.loadtxt("data/input.txt", dtype=int).tolist()
