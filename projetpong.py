import tkinter as tk
height = 600
width = 800

def movingR(can, obj, direction):
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

def moveBall(can, balle, vx, vy):
    bx1, by1, bx2, by2 = can.coords(balle)
    can.delete(balle)
    can.create_oval(bx1 + vx, by1 + vy, bx2 + vx, by2 + vy, fill="black")

def touch(can, objleft, objright):
    ax1, ay1, ax2, ay2 = can.coords(objleft)
    bx1, by1, bx2, by2 = can.coords(objright)
    if ay2 - ay1 <= by2 - by1:
        ay1, by1 = by1, ay1
        ay2, by2 = by2, ay2

    if ax2 >= bx1 and (ay1 <= by2-5 and by1+5 <= ay2):
        return True
    else:
        return False

def isDead(can, balle):
    bx1, by1, bx2, by2 = can.coords(balle)
    if by2 >= height or by1 <= 0:
        return False
    if bx1 <= 0 or bx2 >= width:
        return True

def change_frame(frame_name):
    children = root.winfo_children()
    frame = children[0]
    frame.destroy()
    frame_function = usine_de_frames[frame_name]
    new_frame = frame_function(root)
    new_frame.pack()

def get_menu_frame(master):
    frame = tk.Frame(master)
    tk.Label(frame, text='Menu', font=("Helvetica", 16)).pack()
    tk.Button(frame, text='Jouer', command=lambda: change_frame('jeu')).pack()
    tk.Button(frame, text='Quitter', command=root.quit).pack()
    return frame

def get_game_frame(master):
    frame = tk.Frame(master)
    can = tk.Canvas(frame, bg="#ffffff", height=height, width=width)
    can.pack()
    balle = can.create_oval(width / 2 - 10, height / 2 - 10, width / 2 + 10, height / 2 + 10, fill="black")

    raquette1 = can.create_rectangle(15, height / 2 - 80, 30, height / 2 + 80, fill="black")
    raquette2 = can.create_rectangle(width - 30, height / 2 - 80, width - 15, height / 2 + 80, fill="black")
    but1 = can.create_rectangle(0, 0, 10, height, fill="red", outline="red")
    but2 = can.create_rectangle(width - 10, 0, width, height, fill="red", outline="red")

    vx = -0.20
    vy = 0.10

    moveBall(can, balle, vx, vy)
    #if touch(can, raquette1, balle) or touch(can, balle, raquette2):
    #    vx = -vx
    #if isDead(can, balle):
    #    vx = 0
    #    vy = 0
    #else:
    #    vy = -vy

    can.bind_all('<s>', downA)
    can.bind_all('<Down>', downB)
    can.bind_all('<z>', upA)
    can.bind_all('<Up>', upB)
    return frame

root = tk.Tk()
root.title("Projet")
usine_de_frames = {'jeu': get_game_frame, 'menu': get_menu_frame}
frame = get_menu_frame(root)
frame.pack()
root.mainloop()
