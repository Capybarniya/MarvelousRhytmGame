def coords_sum(*coords):
    return tuple(sum(items) for items in zip(*coords))

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])