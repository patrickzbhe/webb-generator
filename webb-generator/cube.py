from entity import Entity
from node import Node
import math
import tkinter


class Cube(Entity):
    def __init__(self, screen, offsetx=400, offsety=500, size=15, length=150, sidep=4, points=[], edges=[]):
        super().__init__(screen, points, edges, offsetx, offsety, size)
        self.length = length
        self.sidep = sidep
        self.slength = length * (sidep - 1)
        self.center = self.slength / 2

        self.clayers = [[], [], [], []]
        self.generate()

    def generate(self):
        # create a 4x4x4 cube
        # generates nodes and edges that link the nodes and saves them
        # if cube is miswired edit this method
        sidep = self.sidep
        l = self.length
        c = self.center
        slength = self.slength

        for x in range(sidep):
            for y in range(sidep):
                for z in range(sidep):
                    cname = y + 4
                    topname = ''
                    topnum = 0
                    if 1 < z < 4:
                        topname += 'b'
                    else:
                        topname += 'd'
                    if z == 3 or z == 1:
                        topnum += 4
                    topnum += x

                    topname += str(topnum)

                    k = Node(x*l-c, y*l-c, z*l-c, topname, cname)
                    self.clayers[y].append(k)
                    self.points.append(k)

        for i, n in enumerate(self.points):
            for i1, p in enumerate(self.points[i+1:]):
                d = 0
                differences = 0
                for x in range(3):
                    d += math.fabs(n.xyz[x] - p.xyz[x])
                    if math.fabs(n.xyz[x] - p.xyz[x]) != 0:
                        differences += 1

                if differences > 1:
                    continue

                if d == -1 * slength or d == slength:

                    self.edges.append([i, i1 + i + 1])

    def generate_basic(self, time):
        # create the PIC Basic code needed to
        # light up the LED cube based on the schematic in class
        output_text = ''
        try:
            output_text = 'for x=1 to ' + str(int(time)//4) + ':\n'
        except:
            return
        for i, layer in enumerate(self.clayers):
            c = ['0'] * 8
            b = ['0'] * 8
            d = ['0'] * 8

            c[3 - i] = '1'

            for point in layer:
                if not point.on:
                    continue

                tlevel = point.toplevel
                index = 7 - int(tlevel[1])

                if tlevel[0] == "b":
                    b[index] = '1'
                else:
                    d[index] = '1'

            output_text += '    portb = %' + ''.join(b) + '\n'
            output_text += '    portd = %' + ''.join(d) + '\n'
            output_text += '    portc = %' + ''.join(c) + '\n'
            output_text += '    pause 1\n'

            output_text += '\n'

        output_text += '    next x\n'
        return output_text
