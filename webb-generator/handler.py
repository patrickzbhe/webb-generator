import time
import math
import tkinter


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


class Handler:
    def __init__(self, root, cube, screen, output, frame_time):
        self.mx = root.winfo_pointerx()
        self.my = root.winfo_pointery()

        self.cube = cube
        self.screen = screen
        self.output = output
        self.frame_time = frame_time

        self.velx = 0
        self.vely = 0

        self.last = time.time()

        self.locked = False

    def click_handler(self, event):
        self.mx = event.x
        self.my = event.y

        for point in self.cube.points:
            if distance(point.xyz, [event.x - self.cube.offsetx, event.y - self.cube.offsety]) < self.cube.size:
                point.on = not point.on
                break

        self.screen.delete("all")
        self.cube.draw_edges()
        self.cube.draw_points()

        self.screen.update()

    def lock(self):
        self.locked = not self.locked

    def motion_handler(self, event):
        if self.locked:
            return

        vx = (event.x - self.mx)/25
        vy = (event.y - self.my)/25

        self.velx += vx
        self.vely += vy

        if time.time() - self.last > 0.026:
            # make sure it doesn't update too fast or else it crashes
            self.cube.rotate(self.velx, 1)
            self.cube.rotate(self.vely, 2)

            self.velx = 0
            self.vely = 0

            self.last = time.time()

            self.cube.clear()
            self.cube.draw_edges()
            self.cube.draw_points()

        self.mx = event.x
        self.my = event.y

        self.screen.update()

    def handle_generate(self):
        self.output.delete('1.0', tkinter.END)
        text = self.cube.generate_basic(self.frame_time.get())
        self.output.insert(tkinter.END, text)
