def linear_interpolation(x, p1, p2):
    """Calculates the value between two points using linear interpolation"""
    return p1[1] + ((x-p1[0])*(p2[1]-p1[1]) / (p2[0]-p1[0]))
