import math


class Node:
    def __init__(self, x, y, z, toplevel, clevel):
        self.xyz = [x, y, z]
        self.toplevel = toplevel
        self.clevel = clevel
        self.on = False

    def rotate(self, theta, axis):
        # 0 = z axis
        # 1 = y axis
        # 2 = x axis
        if axis == 0:
            n = 0
            k = 1
        elif axis == 1:
            n = 0
            k = 2
        elif axis == 2:
            n = 1
            k = 2

        x = self.xyz[n]
        y = self.xyz[k]

        st = math.sin(math.radians(theta))
        ct = math.cos(math.radians(theta))

        self.xyz[n] = x * ct - y * st
        self.xyz[k] = y * ct + x * st
