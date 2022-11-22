from node import Node
import math


class Cube():
    def __init__(self, length=150, num_sides=4):
        self.points = []
        self.edges = []
        self.length = length
        self.num_sides = num_sides
        self.slength = length * (num_sides - 1)
        self.center = self.slength / 2

        self.c_layers = [[] for _ in range(num_sides)]
        self.generate()

    def rotate(self, theta, axis):
        """Rotate all points in cube"""
        for p in self.points:
            p.rotate(theta, axis)

    def generate(self):
        """Create a NxNxN cube
        generates nodes and edges that link the nodes and saves them
        if cube is miswired edit this method"""
        self.generate_points()
        self.generate_edges()

    def generate_points(self):
        for x in range(self.num_sides):
            for y in range(self.num_sides):
                for z in range(self.num_sides):
                    col_name = y + 4
                    top_num = 0
                    if 1 < z < 4:
                        top_name = 'b'
                    else:
                        top_name = 'd'
                    if z == 3 or z == 1:
                        top_num += 4
                    top_num += x

                    top_name += str(top_num)

                    k = Node(x*self.length-self.center, y*self.length -
                             self.center, z*self.length-self.center, top_name, col_name)
                    self.c_layers[y].append(k)
                    self.points.append(k)

    def generate_edges(self):
        for i, n in enumerate(self.points):
            for i1, p in enumerate(self.points[i+1:]):
                d = 0
                differences = 0
                for x in range(self.num_sides - 1):
                    d += math.fabs(n.xyz[x] - p.xyz[x])
                    if math.fabs(n.xyz[x] - p.xyz[x]) != 0:
                        differences += 1

                if differences > 1:
                    continue

                if d == -1 * self.slength or d == self.slength:
                    self.edges.append([i, i1 + i + 1])

    def generate_basic(self, time):
        """Generate the PIC Basic code needed to
        light up the LED cube based on the schematic in class.
        Loop through all layers and turn on corresponding intersections"""
        output_text = ''
        try:
            output_text = 'for x=1 to ' + str(int(time)//4) + ':\n'
        except:
            return
        for i, layer in enumerate(self.c_layers):
            c = ['0'] * 8
            b = ['0'] * 8
            d = ['0'] * 8

            c[self.num_sides - i - 1] = '1'
            for point in layer:
                if not point.on:
                    continue

                index = 7 - int(point.toplevel[1])
                if point.toplevel[0] == "b":
                    b[index] = '1'
                else:
                    d[index] = '1'

            output_text += f'    portb = %{"".join(b)}\n'
            output_text += f'    portd = %{"".join(d)}\n'
            output_text += f'    portc = %{"".join(c)}\n'
            output_text += '    pause 1\n'
            output_text += '\n'

        output_text += '    next x\n'
        return output_text
