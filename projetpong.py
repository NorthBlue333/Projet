import tkinter as tk
height = 600
width = 800

root = tk.Tk()
root.title("Test")
can = tk.Canvas(root, bg="#ffffff", height=height, width=width)
can.pack()
root.update_idletasks()

balle = can.create_oval(width / 2 - 10, height / 2 - 10, width / 2 + 10, height / 2 + 10, fill="black")
raquette1 = can.create_rectangle(10, height / 2 - 80, 30, height / 2 + 80, fill="black")
raquette2 = can.create_rectangle(width - 30, height / 2 - 80, width - 10, height / 2 + 80, fill="black")

def movingR(obj, direction):
    if direction == "down":
        dir = 15
    else:
        dir = -15
    can.move(obj, 0, dir)

def downA(event):
    movingR(raquette1, "down")

def downB(event):
    movingR(raquette2, "down")

def upA(event):
    movingR(raquette1, "up")

def upB(event):
    movingR(raquette2, "up")

can.bind_all('<s>', downA)
can.bind_all('<Down>', downB)
can.bind_all('<z>', upA)
can.bind_all('<Up>', upB)

def touch(objleft, objright):
    ax1, ay1, ax2, ay2 = can.coords(objleft)
    bx1, by1, bx2, by2 = can.coords(objright)
    if ay2 - ay1 <= by2 - by1:
        ay1, by1 = by1, ay1
        ay2, by2 = by2, ay2

    if ax2 >= bx1 and (ay1 <= by1 and by2 <= ay2):
        return True
    else:
        return False

vx = -0.20
vy = 0.10

while True:
    can.move(balle, vx, vy)

    if touch(raquette1, balle) or touch(balle, raquette2):
        vx = -vx
    if by2 >= height or by1 <= 0:
        vy = -vy
    can.update()
root.mainloop()
