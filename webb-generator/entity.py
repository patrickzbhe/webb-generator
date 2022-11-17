class Entity:
    def __init__(self, screen, points, edges, offsetx, offsety, size):
        self.screen = screen
        self.points = points
        self.edges = edges
        self.garbage = []
        self.offsetx = offsetx
        self.offsety = offsety
        self.size = size

    def rotate(self, theta, axis):
        for p in self.points:
            p.rotate(theta, axis)

    def draw_points(self):
        ox = self.offsetx
        oy = self.offsety
        s = self.size
        for p in self.points:
            colour = ""
            if p.on == True:
                colour = "red"
            self.garbage.append(self.screen.create_oval(
                p.xyz[0]+ox-s, p.xyz[1]+oy-s, p.xyz[0]+ox+s, p.xyz[1]+oy+s, fill=colour))
            self.garbage.append(self.screen.create_text(
                p.xyz[0]+ox-s, p.xyz[1]+oy-s, text=p.toplevel))
            self.garbage.append(self.screen.create_text(
                p.xyz[0]+ox+s, p.xyz[1]+oy+s, text="c" + str(p.clevel)))
        self.screen.update()

    def draw_edges(self):
        ox = self.offsetx
        oy = self.offsety
        for e in self.edges:
            p1 = self.points[e[0]].xyz
            p2 = self.points[e[1]].xyz

            self.garbage.append(self.screen.create_line(
                p1[0]+ox, p1[1]+oy, p2[0]+ox, p2[1]+oy))

    def clear(self):
        self.screen.delete(*self.garbage)
        self.garbage = []
