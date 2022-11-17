import tkinter
from handler import Handler

from cube import Cube

if __name__ == '__main__':
    root = tkinter.Tk()

    WIDTH = 800
    HEIGHT = 1000

    screen = tkinter.Canvas(root, width=WIDTH, height=HEIGHT)
    screen.grid(row=0, column=0, rowspan=1000)

    scroll = tkinter.Scrollbar(root)
    scroll.grid(row=3, column=2, rowspan=10, sticky="nsew")

    output = tkinter.Text(root)
    output.grid(row=3, column=1)

    scroll.config(command=output.yview)
    output.config(yscrollcommand=scroll.set)

    # frame time in milliseconds
    time_label = tkinter.Label(root, text='Frame Time:')
    time_label.grid(row=0, column=1)

    frame_time = tkinter.Entry(root)
    frame_time.grid(row=1, column=1)

    # create cube
    cube = Cube(screen)
    cube.rotate(220, 1)
    cube.rotate(190, 2)
    cube.draw_points()
    cube.draw_edges()

    h = Handler(root, cube, screen, output, frame_time)

    generate_button = tkinter.Button(
        root, text='generate', command=h.handle_generate)
    generate_button.grid(row=2, column=1)

    lock_button = tkinter.Button(root, text='lock', command=h.lock)
    lock_button.grid(row=4, column=1)

    screen.bind('<B1-Motion>', h.motion_handler)
    screen.bind('<Button-1>', h.click_handler)

    root.mainloop()
