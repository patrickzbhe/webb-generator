import tkinter
from cube import Cube
from time import time
from math import sqrt

DEFAULT_FRAME_TIME = 500

class App(tkinter.Tk):
    def __init__(self, offsetx=400, offsety=400, size=15, length=150):
        super().__init__()
        self.offsetx = offsetx
        self.offsety = offsety
        self.size = size
        self.length = length

        self.garbage = []
        self.cubes = []
        self.cube_pointer = -1

        self.WIDTH = 800
        self.HEIGHT = 1000

        # handler stuff
        self.mx = self.winfo_pointerx()
        self.my = self.winfo_pointery()
        self.locked = False
        self.last = time()
        self.velx = 0
        self.vely = 0

        self.screen = tkinter.Canvas(
            self, width=self.WIDTH, height=self.HEIGHT)
        self.screen.grid(row=0, column=0, rowspan=1000)

        scroll = tkinter.Scrollbar(self)
        scroll.grid(row=3, column=2, rowspan=8, sticky="nsew")

        self.output = tkinter.Text(self)
        self.output.grid(row=3, column=1)
        self.output.config(yscrollcommand=scroll.set)
        scroll.config(command=self.output.yview)

        # frame time in milliseconds
        time_label = tkinter.Label(self, text='Frame Time:')
        time_label.grid(row=0, column=1)

        self.frame_time_entry = tkinter.Entry(self)
        self.frame_time_entry.grid(row=1, column=1)

        self.new_frame()
        self.render_main_cube()

        self.build_controls()
        lock_button = tkinter.Button(self, text='lock', command=self.lock)
        lock_button.grid(row=4, column=1)

        self.screen.bind('<B1-Motion>', self.motion_handler)
        self.screen.bind('<Button-1>', self.click_handler)

    @property
    def frame_time(self):
        try:
            return int(self.frame_time_entry.get())
        except:
            return DEFAULT_FRAME_TIME

    @property
    def cube(self):
        return self.cubes[self.cube_pointer][0]

    def build_controls(self):
        control_frame = tkinter.Frame(
            self
        )
        control_frame.grid(row=2, column=1)
        generate_button = tkinter.Button(
            control_frame, text='Generate', command=self.generate_basic)
        generate_button.grid(row=2, column=0)
        generate_all_button = tkinter.Button(
            control_frame, text='Generate All', command=self.generate_all_basic)
        generate_all_button.grid(row=2, column=1)
        new_frame_button = tkinter.Button(
            control_frame, text='New Frame', command=self.new_frame)
        new_frame_button.grid(row=2, column=2)
        delete_frame_button = tkinter.Button(
            control_frame, text='Delete Frame', command=self.delete_frame)
        delete_frame_button.grid(row=2, column=3)
        prev_frame_button = tkinter.Button(
            control_frame, text='Prev Frame', command=self.prev_frame)
        prev_frame_button.grid(row=2, column=4)
        next_frame_button = tkinter.Button(
            control_frame, text='Next Frame', command=self.next_frame)
        next_frame_button.grid(row=2, column=5)

    def generate_cube(self):
        cube = Cube()
        cube.rotate(220, 1)
        cube.rotate(190, 2)
        return cube

    def render_main_cube(self):
        self.clear_cube()
        self.render_cube_edges()
        self.render_cube_points()
        self.screen.update()

    def render_cube_points(self):
        ox = self.offsetx
        oy = self.offsety
        s = self.size
        for p in self.cube.points:
            colour = ""
            if p.on == True:
                colour = "red"
            self.garbage.append(self.screen.create_oval(
                p.xyz[0]+ox-s, p.xyz[1]+oy-s, p.xyz[0]+ox+s, p.xyz[1]+oy+s, fill=colour))
            self.garbage.append(self.screen.create_text(
                p.xyz[0]+ox-s, p.xyz[1]+oy-s, text=p.toplevel))
            self.garbage.append(self.screen.create_text(
                p.xyz[0]+ox+s, p.xyz[1]+oy+s, text="c" + str(p.clevel)))

    def render_cube_edges(self):
        ox = self.offsetx
        oy = self.offsety
        for e in self.cube.edges:
            p1 = self.cube.points[e[0]].xyz
            p2 = self.cube.points[e[1]].xyz
            self.garbage.append(self.screen.create_line(
                p1[0]+ox, p1[1]+oy, p2[0]+ox, p2[1]+oy))

    def rotate_cube(self, theta, axis):
        self.cube.rotate(theta, axis)

    def clear_cube(self):
        self.screen.delete(*self.garbage)
        self.garbage = []

    def generate_basic(self):
        self.output.delete('1.0', tkinter.END)
        text = ''
        if self.frame_time:
            text = self.cube.generate_basic(self.frame_time)
        self.output.insert(tkinter.END, text)

    def generate_all_basic(self):
        self.output.delete('1.0', tkinter.END)
        text = '\n'.join([frame[0].generate_basic(frame[1])
                         for frame in self.cubes])
        self.output.insert(tkinter.END, text)

    def lock(self):
        self.locked = not self.locked

    def motion_handler(self, event):
        if self.locked:
            return

        vx = (event.x - self.mx)/25
        vy = (event.y - self.my)/25

        self.velx += vx
        self.vely += vy

        if time() - self.last > 0.026:
            # make sure it doesn't update too fast or else it crashes
            self.rotate_cube(self.velx, 1)
            self.rotate_cube(self.vely, 2)

            self.velx = 0
            self.vely = 0

            self.last = time()

            self.render_main_cube()

        self.mx = event.x
        self.my = event.y
        self.screen.update()

    def click_handler(self, event):
        self.mx = event.x
        self.my = event.y

        for point in self.cube.points:
            if distance(point.xyz, [event.x - self.offsetx, event.y - self.offsety]) < self.size:
                point.on = not point.on
                break

        self.render_main_cube()

    def set_frame_time_text(self, text):
        if not text:
            text = DEFAULT_FRAME_TIME
        text = str(text)
        self.frame_time_entry.delete(0, tkinter.END)
        self.frame_time_entry.insert(0, text)

    def set_frame_time_state(self):
        self.cubes[self.cube_pointer][1] = self.frame_time

    def new_frame(self):
        if self.cubes:
            self.set_frame_time_state()
        cube = self.generate_cube()
        self.cube_pointer += 1
        self.cubes.insert(self.cube_pointer, [cube, DEFAULT_FRAME_TIME])
        self.render_main_cube()
        self.set_frame_time_text(self.cubes[self.cube_pointer][1])

    def delete_frame(self):
        if len(self.cubes) > 0:
            del self.cubes[self.cube_pointer]
            if self.cube_pointer >= len(self.cubes):
                self.cube_pointer -= 1
            self.render_main_cube()
            self.set_frame_time_text(self.cubes[self.cube_pointer][1])

    def next_frame(self):
        self.set_frame_time_state()
        if self.cube_pointer < len(self.cubes) - 1:
            self.cube_pointer += 1
        self.render_main_cube()
        self.set_frame_time_text(self.cubes[self.cube_pointer][1])

    def prev_frame(self):
        self.set_frame_time_state()
        if self.cube_pointer > 0:
            self.cube_pointer -= 1
        self.render_main_cube()
        self.set_frame_time_text(self.cubes[self.cube_pointer][1])


def distance(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
