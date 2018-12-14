import tkinter as tk
from object import *
from score import *

height = 600
width = 800
move_update = 5

def down(event, table, canvas, r=False):
    table.moveObject()
    if r:
        canvas.delete("tableR")
    else:
        canvas.delete("tableL")
    table.drawObject(canvas)

def up(event, table, canvas, r=False):
    table.moveObject(up=True)
    if r:
        canvas.delete("tableR")
    else:
        canvas.delete("tableL")
    table.drawObject(canvas)

def move_ball(canvas, ball, tableL, tableR, scoreL, scoreR):
    ball.moveObject(600, 800, tableL, tableR, scoreL, scoreR)
    canvas.delete("ball")
    ball.drawObject(canvas)
    if ball.start:
        canvas.after(move_update + 495, move_ball, canvas, ball, tableL, tableR, scoreL, scoreR)
        ball.start = False
    else:
        canvas.after(move_update, move_ball, canvas, ball, tableL, tableR, scoreL, scoreR)

def change_frame(frame_name):
    root.winfo_children()[0].destroy()
    new_frame = all_frames[frame_name](root)
    new_frame.pack()

def get_menu_frame(master):
    frame = tk.Frame(master)
    tk.Label(frame, text='Bienvenue sur Pong !', font=("Helvetica", 32)).pack()
    tk.Button(frame, text='Jouer', command=lambda: change_frame('game')).pack()
    tk.Button(frame, text='Quitter', command=root.quit).pack()
    return frame

def get_game_frame(master):
    frame = tk.Frame(master)
    can = tk.Canvas(frame, bg="#ffffff", height=height, width=width)
    can.pack()
    ball = Ball(width / 2 - 10, height / 2 - 10, width / 2 + 10, height / 2 + 10, 1, 1, tag="ball")
    ball.drawObject(can)
    tableL = Table(15, height / 2 - 80, 30, height / 2 + 80, vy=15, tag="tableL")
    tableR = Table(width - 30, height / 2 - 80, width - 15, height / 2 + 80, vy=15, tag="tableR")
    tableL.drawObject(can)
    tableR.drawObject(can)
    scoreL = Score(0)
    scoreR = Score(0)
    scoreL.drawScore(can, height, width)
    scoreR.drawScore(can, height, width, True)
    can.bind_all('<s>', lambda event, table=tableL, canvas=can: down(event, table, canvas))
    can.bind_all('<Down>', lambda event, table=tableR, canvas=can, r=True: down(event, table, canvas, r))
    can.bind_all('<z>', lambda event, table=tableL, canvas=can: up(event, table, canvas))
    can.bind_all('<Up>', lambda event, table=tableR, canvas=can, r=True: up(event, table, canvas, r))
    if ball.start:
        can.after(move_update + 495, move_ball, can, ball, tableL, tableR, scoreL, scoreR)
        ball.start = False
    else:
        can.after(move_update, move_ball, can, ball, tableL, tableR, scoreL, scoreR)
    return frame

root = tk.Tk()
root.title("Projet")
all_frames = {'game': get_game_frame, 'menu': get_menu_frame}
frame = get_menu_frame(root)
frame.pack()
root.mainloop()
