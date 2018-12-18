import tkinter as tk
import time
from decimal import Decimal
from object import *
from score import *
from color import *

root = tk.Tk()
root.title("Projet")

height = 600
width = 800
move_update = 5
players = 2
win_point = tk.IntVar()
win_point.set(2)
winner = '0'
speed = tk.DoubleVar()
speed.set(1.5)
color = 0
colors = [Color("white", "black"),
          Color("black", "white")]
start_time = 0

def change_frame(frame_name):
    root.winfo_children()[0].destroy()
    new_frame = all_frames[frame_name](root)
    new_frame.pack()

def get_menu_frame(master):
    frame = tk.Frame(master)
    tk.Label(frame, text='Bienvenue sur Pong !', font=("Helvetica", 32)).pack()
    tk.Button(frame, text='Jouer', command=lambda: change_frame('game')).pack()
    tk.Button(frame, text='Option', command=lambda: change_frame('option')).pack()
    tk.Button(frame, text='Quitter', command=root.quit).pack()
    return frame

#--------------option frame
def change_color(dir, can, frame):
    global color
    if dir == 'next' and color < len(colors)-1:
        color += 1
    elif dir == 'previous' and color > 0:
        color -= 1
    can = tk.Canvas(frame, bg=colors[color%len(colors)].background, height=100, width=100)
    can.grid(column=1, row=1)
    can.create_rectangle(10, 30, 15, 70, fill=colors[color%len(colors)].foreground, outline=colors[color%len(colors)].foreground)
    can.create_oval(50-4, 50-4, 50+4, 50+4, fill=colors[color%len(colors)].foreground, outline=colors[color%len(colors)].foreground)

def get_option_frame(master):
    frame = tk.Frame(master)
    tk.Label(frame, text='Options pour Pong', font=("Helvetica", 32)).grid(column=0, row=0, columnspan=3)
    can = tk.Canvas(frame, bg=colors[color%len(colors)].background, height=100, width=100)
    can.grid(column=1, row=1)
    can.create_rectangle(10, 30, 15, 70, fill=colors[color%len(colors)].foreground, outline=colors[color%len(colors)].foreground)
    can.create_oval(50-4, 50-4, 50+4, 50+4, fill=colors[color%len(colors)].foreground, outline=colors[color%len(colors)].foreground)
    tk.Button(frame, text='<', command=lambda: change_color('previous', can, frame)).grid(column=0, row=1)
    tk.Button(frame, text='>', command=lambda: change_color('next', can, frame)).grid(column=2, row=1)
    tk.Radiobutton(frame, indicatoron=0, variable=win_point, text="5 points", value=5, state="active").grid(column=0, row=2)
    tk.Radiobutton(frame, indicatoron=0, variable=win_point, text="10 points", value=10, state="normal").grid(column=1, row=2)
    tk.Radiobutton(frame, indicatoron=0, variable=win_point, text="15 points", value=15, state="normal").grid(column=2, row=2)
    tk.Radiobutton(frame, indicatoron=0, variable=speed, text="Vitesse lente", value=1, state="normal").grid(column=0, row=3)
    tk.Radiobutton(frame, indicatoron=0, variable=speed, text="Vitesse moyenne", value=1.5, state="active").grid(column=1, row=3)
    tk.Radiobutton(frame, indicatoron=0, variable=speed, text="Vitesse rapide", value=2, state="normal").grid(column=2, row=3)
    tk.Button(frame, text='Valider et retour au menu', command=lambda: change_frame('menu')).grid(column=0, row=4)
    tk.Button(frame, text='Valider et jouer', command=lambda: change_frame('game')).grid(column=2, row=4)
    return frame

#--------------game frame
def down(event, paddle, canvas):
    paddle.moveObject()
    canvas.delete(paddle.tag)
    paddle.drawObject(canvas)

def up(event, paddle, canvas):
    paddle.moveObject(up=True)
    canvas.delete(paddle.tag)
    paddle.drawObject(canvas)

def move_ball(canvas, ball, paddles, scores):
    global winner
    won = False
    ball.moveObject(600, 800, paddles, scores)
    canvas.delete("ball")
    ball.drawObject(canvas)
    if ball.start:
        for score in scores:
            if score.value == win_point.get():
                won = True
                break
        if won == False:
            canvas.delete("score")
            for score in scores:
                if (scores.index(score) + 1) % 2 == 0:
                    score.drawScore(canvas, height, width, True)
                else:
                    score.drawScore(canvas, height, width)
            canvas.after(move_update + 495, move_ball, canvas, ball, paddles, scores)
            ball.start = False
        else:
            winner = str(scores.index(score) + 1)
            canvas.unbind_all('<s>')
            canvas.unbind_all('<Down>')
            canvas.unbind_all('<z>')
            canvas.unbind_all('<Up>')
            scores.clear()
            paddles.clear()
            change_frame('end')
    else:
        canvas.after(move_update, move_ball, canvas, ball, paddles, scores)

def get_game_frame(master):
    global start_time
    start_time = time.time()
    frame = tk.Frame(master)
    canvas = tk.Canvas(frame, bg=colors[color%len(colors)].background, height=height, width=width)
    canvas.pack()
    ball = Ball(width / 2 - 10, height / 2 - 10, width / 2 + 10, height / 2 + 10, speed.get(), speed.get(), color=colors[color%len(colors)].foreground, outline=colors[color%len(colors)].foreground, tag="ball")
    ball.drawObject(canvas)
    paddles = []
    scores = []
    for i in range(players):
        if i == 0:
            paddles.append(Paddle(15, height / 2 - 80, 30, height / 2 + 80, vy=15, color=colors[color%len(colors)].foreground, outline=colors[color%len(colors)].foreground, tag="paddleL"))
            canvas.bind_all('<s>', lambda event, paddle=paddles[0], canvas=canvas: down(event, paddle, canvas))
            canvas.bind_all('<z>', lambda event, paddle=paddles[0], canvas=canvas: up(event, paddle, canvas))
        if i == 1:
            paddles.append(Paddle(width - 30, height / 2 - 80, width - 15, height / 2 + 80, vy=15, color=colors[color%len(colors)].foreground, outline=colors[color%len(colors)].foreground, tag="paddleR"))
            canvas.bind_all('<Down>', lambda event, paddle=paddles[1], canvas=canvas: down(event, paddle, canvas))
            canvas.bind_all('<Up>', lambda event, paddle=paddles[1], canvas=canvas: up(event, paddle, canvas))
        paddles[i].drawObject(canvas)
        scores.append(Score(0, color=colors[color%len(colors)].foreground))
        if (i + 1) % 2 == 0:
            scores[i].drawScore(canvas, height, width, True)
        else:
            scores[i].drawScore(canvas, height, width)
    ball.start = False
    canvas.after(move_update + 495, move_ball, canvas, ball, paddles, scores)
    return frame

def get_end_frame(master):
    global winner
    elapsed_time = round(Decimal(time.time() + 80 - start_time), 2)
    end_time = ''
    frame = tk.Frame(master)
    if elapsed_time >= 60:
        end_time = str(elapsed_time // 60) + " minute(s) et " + str(elapsed_time % 60) + " seconde(s)"
    else:
        end_time = str(elapsed_time) + " seconde(s)"
    wins = "J" + winner + " gagne !"
    winner = '0'
    canvas = tk.Canvas(frame, bg=colors[color%len(colors)].background, height=height, width=width)
    canvas.grid(column=0, row=0, columnspan=2)
    canvas.create_text(width/2, height/2, text=wins, font=("Helvetica", 32), fill=colors[color%len(colors)].foreground)
    canvas.create_text(width/2, height/2 + 50, text=end_time, font=("Helvetica", 25), fill=colors[color%len(colors)].foreground)
    tk.Button(frame, text='Retour au menu', command=lambda: change_frame('menu')).grid(column=0, row=1)
    tk.Button(frame, text='Rejouer', command=lambda: change_frame('game')).grid(column=1, row=1)
    return frame

all_frames = {'game': get_game_frame, 'option': get_option_frame, 'menu': get_menu_frame, 'end': get_end_frame}
frame = get_menu_frame(root)
frame.pack()
root.mainloop()
