
# Takes a position and a direction representing a line
# and converts it into a cartesion equation.
def vector_line_to_cartesian(p, d, doc=vdoc):
    # If dim = 2:
    # [ 1 ]     [ 2 ]
    # [ 3 ] + t [ 5 ]
    # a = 5 / 2
    # y = a(x + x0) + y0
    #   = ax  + ax0 + y0

    # For dim = 3:
    # Some
    # x = a k + d
    # y = b k + e
    # z = c k + f

