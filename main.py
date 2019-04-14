import tkinter
import math
import time
import handler

root = tkinter.Tk()

WIDTH = 800
HEIGHT = 1000

screen = tkinter.Canvas(root, width = WIDTH, height = HEIGHT)
screen.grid(row=0,column=0,rowspan = 1000)

scroll = tkinter.Scrollbar(root)
scroll.grid(row = 3, column = 2,rowspan=10,sticky="nsew")

output = tkinter.Text(root)
output.grid(row = 3, column = 1)

scroll.config(command=output.yview)
output.config(yscrollcommand=scroll.set)

#frame time in milliseconds
time_label = tkinter.Label(root, text = 'Frame Time:')
time_label.grid(row = 0, column = 1)

frame_time = tkinter.Entry(root)
frame_time.grid(row = 1, column = 1)
        
class Node:
    def __init__(self, x ,y ,z,toplevel,clevel):
        self.xyz = [x,y,z]
        self.toplevel = toplevel
        self.clevel = clevel
        self.on = False

    def rotate(self,theta,axis):
        #0 = z axis
        #1 = y axis
        #2 = x axis
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

class Entity:
    def __init__(self,points,edges,offsetx,offsety,size):
        self.points = points
        self.edges = edges
        self.garbage = []
        self.offsetx = offsetx
        self.offsety = offsety
        self.size = size
       

    def rotate(self,theta,axis):
        for p in self.points:
            p.rotate(theta,axis)

    def draw_points(self):
        ox = self.offsetx
        oy = self.offsety
        s = self.size
        for p in self.points:
            colour = ""
            if p.on == True:
                colour = "red"
            self.garbage.append(screen.create_oval(p.xyz[0]+ox-s,p.xyz[1]+oy-s,p.xyz[0]+ox+s,p.xyz[1]+oy+s,fill=colour))
            self.garbage.append(screen.create_text(p.xyz[0]+ox-s,p.xyz[1]+oy-s,text = p.toplevel))
            self.garbage.append(screen.create_text(p.xyz[0]+ox+s,p.xyz[1]+oy+s,text = "c" + str(p.clevel)))
        screen.update()

    def draw_edges(self):
        ox = self.offsetx
        oy = self.offsety
        for e in self.edges:
            p1 = self.points[e[0]].xyz
            p2 = self.points[e[1]].xyz
            
            self.garbage.append(screen.create_line(p1[0]+ox,p1[1]+oy,p2[0]+ox,p2[1]+oy))

    def clear(self):
        screen.delete(*self.garbage)
        self.garbage = []
    
class Cube(Entity):
    def __init__(self,points,edges,offsetx,offsety,size, length, sidep):
        super().__init__(points,edges,offsetx,offsety,size)
        self.length = length
        self.sidep = sidep
        self.slength = length * (sidep - 1)
        self.center = self.slength / 2

        self.clayers = [[],[],[],[]]

    def generate(self):
        #create a 4x4x4 cube
        #generates nodes and edges that link the nodes and saves them
        #if cube is miswired edit this method
        sidep = self.sidep
        l = self.length
        c= self.center
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
                    
                    k = Node(x*l-c,y*l-c,z*l-c, topname,cname)
                    self.clayers[y].append(k)
                    self.points.append(k)
                    

        for i,n in enumerate(self.points):
            for i1,p in enumerate(self.points[i+1:]):
                d = 0
                differences = 0
                for x in range(3):
                    d += math.fabs(n.xyz[x] - p.xyz[x])
                    if math.fabs(n.xyz[x] - p.xyz[x]) != 0:
                        differences += 1

                if differences > 1:
                    continue
                
                if d == -1 * slength or d == slength:
                   
                    self.edges.append([i,i1 + i +1])

            

    def create_frame(self):
        #create the PIC Basic code needed to
        #light up the LED cube based on the schematic in class
        output.delete('1.0', tkinter.END)
        output_text = ''
        try:
            output_text = 'for x=1 to ' + str(int(frame_time.get())//4) + ':\n'
        except:
            return
        for i,layer in enumerate(self.clayers):
            
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

            lol = ''.join(b) + '\n' + ''.join(d) + '\n' + ''.join(c) + ' \n'
            
            
            output_text += '    portb = %' + ''.join(b) + '\n'
            output_text += '    portd = %' + ''.join(d) + '\n'
            output_text += '    portc = %' + ''.join(c) + '\n'
            output_text += '    pause 1\n'
          
            output_text += '\n'
            
            output.insert(tkinter.END, output_text)
            output_text = ''
        output.insert(tkinter.END, '    next x\n')

#create cube
cube = Cube([],[],400,500,15, 150, 4)
cube.generate()
cube.rotate(220,1)
cube.rotate(190,2)
cube.draw_points()
cube.draw_edges()

h = handler.Handler(root,cube,screen)

generate_button = tkinter.Button(root, text='generate', command = cube.create_frame)
generate_button.grid(row = 2, column = 1)

lock_button = tkinter.Button(root, text='lock', command = h.lock)
lock_button.grid(row = 4, column = 1)

screen.bind('<B1-Motion>',h.motion_handler)
screen.bind('<Button-1>',h.click_handler)

root.mainloop()













































































