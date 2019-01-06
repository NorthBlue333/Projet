import tkinter as tk
import time
import random
from decimal import Decimal
import copy
from object import *
from score import *
from color import *

root = tk.Tk()
root.title("Projet")

height = 600
width = 800
paddlew = 15
paddleh = 160
paddlespeed = 30
grid_pad = 15
move_update = 5
players = tk.IntVar()
players.set(2)
win_point = tk.IntVar()
win_point.set(5)
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
    can = tk.Canvas(frame, bg=colors[color].background, height=100, width=100)
    can.grid(column=1, row=1)
    can.create_rectangle(10, 30, 15, 70, fill=colors[color].foreground, outline=colors[color].foreground)
    can.create_oval(50-4, 50-4, 50+4, 50+4, fill=colors[color].foreground, outline=colors[color].foreground)

def get_option_frame(master):
    frame = tk.Frame(master)
    tk.Label(frame, text='Options du Pong', font=("Helvetica", 32)).grid(column=0, row=0, columnspan=3, padx=3*grid_pad, pady=grid_pad)
    can = tk.Canvas(frame, bg=colors[color].background, height=100, width=100)
    can.grid(column=1, row=1, padx=grid_pad, pady=grid_pad)
    can.create_rectangle(10, 30, 15, 70, fill=colors[color].foreground, outline=colors[color].foreground)
    can.create_oval(50-4, 50-4, 50+4, 50+4, fill=colors[color].foreground, outline=colors[color].foreground)
    tk.Button(frame, text='<', command=lambda: change_color('previous', can, frame)).grid(column=0, row=1, padx=grid_pad, pady=grid_pad)
    tk.Button(frame, text='>', command=lambda: change_color('next', can, frame)).grid(column=2, row=1, padx=grid_pad, pady=grid_pad)
    tk.Radiobutton(frame, indicatoron=0, variable=win_point, text="5 points", value=5, state="active").grid(column=0, row=2, padx=grid_pad, pady=grid_pad)
    tk.Radiobutton(frame, indicatoron=0, variable=win_point, text="10 points", value=10, state="normal").grid(column=1, row=2, padx=grid_pad, pady=grid_pad)
    tk.Radiobutton(frame, indicatoron=0, variable=win_point, text="15 points", value=15, state="normal").grid(column=2, row=2, padx=grid_pad, pady=grid_pad)

    tk.Radiobutton(frame, indicatoron=0, variable=speed, text="Vitesse lente", value=1, state="normal").grid(column=0, row=3, padx=grid_pad, pady=grid_pad)
    tk.Radiobutton(frame, indicatoron=0, variable=speed, text="Vitesse moyenne", value=1.5, state="active").grid(column=1, row=3, padx=grid_pad, pady=grid_pad)
    tk.Radiobutton(frame, indicatoron=0, variable=speed, text="Vitesse rapide", value=2, state="normal").grid(column=2, row=3, padx=grid_pad, pady=grid_pad)

    tk.Radiobutton(frame, indicatoron=0, variable=players, text="2 joueurs", value=2, state="active").grid(column=0, row=4, padx=grid_pad, pady=grid_pad)
    tk.Radiobutton(frame, indicatoron=0, variable=players, text="3 joueurs", value=3, state="normal").grid(column=1, row=4, padx=grid_pad, pady=grid_pad)
    tk.Radiobutton(frame, indicatoron=0, variable=players, text="4 joueurs", value=4, state="normal").grid(column=2, row=4, padx=grid_pad, pady=grid_pad)
    tk.Radiobutton(frame, indicatoron=0, variable=players, text="Jouer contre un bot", value=1, state="normal").grid(column=1, row=5, padx=grid_pad, pady=0)

    tk.Button(frame, text='Valider et retour au menu', command=lambda: change_frame('menu')).grid(column=0, row=6, padx=grid_pad, pady=2*grid_pad)
    tk.Button(frame, text='Valider et jouer', command=lambda: change_frame('game')).grid(column=2, row=6, padx=grid_pad, pady=2*grid_pad)
    return frame

#--------------game frame
def down(event, paddle, canvas):
    paddle.moveObject(height=height, width=width)
    canvas.delete(paddle.tag)
    paddle.drawObject(canvas)

def up(event, paddle, canvas):
    paddle.moveObject(up=True, height=height, width=width)
    canvas.delete(paddle.tag)
    paddle.drawObject(canvas)

def left(event, paddle, canvas):
    paddle.moveObject(height=height, width=width)
    canvas.delete(paddle.tag)
    paddle.drawObject(canvas)

def right(event, paddle, canvas):
    paddle.moveObject(right=True, height=height, width=width)
    canvas.delete(paddle.tag)
    paddle.drawObject(canvas)

def bubble_effect(num, ball, paddles, canvas):
    if num == 0:
        if ball.sx < 0:
            ball.sx -= 0.5
        elif ball.sx > 0:
            ball.sx += 0.5
        if ball.sy < 0:
            ball.sy -= 0.5
        elif ball.sy > 0:
            ball.sy += 0.5
    if num == 1:
        if ball.sx > 0.5:
            ball.sx -= 0.5
        elif ball.sx < -0.5:
            ball.sx += 0.5
        if ball.sy > 0.5:
            ball.sy -= 0.5
        elif ball.sy < -0.5:
            ball.sy += 0.5
    if ball.last_touch != None:
        if num == 2:
            if ball.last_touch < 2:
                paddles[ball.last_touch].sizey = 180
                paddles[ball.last_touch].y1 -= 10
                paddles[ball.last_touch].y2 += 10
            else:
                paddles[ball.last_touch].sizex = 180
                paddles[ball.last_touch].x1 -= 10
                paddles[ball.last_touch].x2 += 10
            canvas.delete(paddles[ball.last_touch].tag)
            paddles[ball.last_touch].drawObject(canvas)
        if num == 3:
            for paddle in paddles:
                if paddles.index(paddle) != ball.last_touch:
                    if paddles.index(paddle) < 2:
                        paddle.sizey = 140
                        paddle.y1 += 10
                        paddle.y2 -= 10
                    else:
                        paddle.sizex = 140
                        paddle.x1 += 10
                        paddle.x2 -= 10
                    canvas.delete(paddle.tag)
                    paddle.drawObject(canvas)
        if num == 4:
            for paddle in paddles:
                ind = paddles.index(paddle)
                if ind != ball.last_touch:
                    if ind == 0:
                        canvas.unbind_all('<s>')
                        canvas.unbind_all('<z>')
                        canvas.bind_all('<z>', lambda event, paddle=paddle, canvas=canvas: down(event, paddle, canvas))
                        canvas.bind_all('<s>', lambda event, paddle=paddle, canvas=canvas: up(event, paddle, canvas))
                    if ind == 1:
                        canvas.unbind_all('<Down>')
                        canvas.unbind_all('<Up>')
                        canvas.bind_all('<Up>', lambda event, paddle=paddle, canvas=canvas: down(event, paddle, canvas))
                        canvas.bind_all('<Down>', lambda event, paddle=paddle, canvas=canvas: up(event, paddle, canvas))
                    if ind == 2:
                        canvas.unbind_all('<f>')
                        canvas.unbind_all('<g>')
                        canvas.bind_all('<g>', lambda event, paddle=paddle, canvas=canvas: left(event, paddle, canvas))
                        canvas.bind_all('<f>', lambda event, paddle=paddle, canvas=canvas: right(event, paddle, canvas))
                    if ind == 3:
                        canvas.unbind_all('<j>')
                        canvas.unbind_all('<k>')
                        canvas.bind_all('<k>', lambda event, paddle=paddle, canvas=canvas: left(event, paddle, canvas))
                        canvas.bind_all('<j>', lambda event, paddle=paddle, canvas=canvas: right(event, paddle, canvas))

def spawn_bubbles(canvas, bubbles):
    spawn_prob = random.random()
    if spawn_prob >= 0.99:
        x1 = random.randint(40, width - 80)
        y1 = random.randint(40, height - 80)
        bubbles.append(Bubble(x1, y1, random.randint(0, 4), x2=x1 + 40, y2=y1 + 40, tag="bubbles"))
    return bubbles

def move_ball(canvas, ball, paddles, scores, bubbles):
    global winner
    won = False
    ball.moveObject(height, width, paddles, scores)
    canvas.delete("ball")
    ball.drawObject(canvas)
    if ball.start:
        bubbles = []
        canvas.delete("all")
        ball.drawObject(canvas)
        rsx = random.randint(0, 1)
        if rsx == 0:
            rsx = -1
        ball.sx = speed.get() * rsx
        rsy = random.randint(0, 1)
        if rsy == 0:
            rsy = -1
        ball.sy = speed.get() * rsy
        for paddle in paddles:
            ind = paddles.index(paddle)
            if ind < 2:
                paddle.sizey = 160
                paddle.y1 = height / 2 - paddle.sizey / 2
                paddle.y2 = height / 2 + paddle.sizey / 2
            else:
                paddle.sizex = 160
                paddle.x1 = width / 2 - paddle.sizex / 2
                paddle.x2 = width / 2 + paddle.sizex / 2
            paddle.drawObject(canvas)

            if ind == 0:
                canvas.unbind_all('<s>')
                canvas.unbind_all('<z>')
                canvas.bind_all('<s>', lambda event, paddle=paddle, canvas=canvas: down(event, paddle, canvas))
                canvas.bind_all('<z>', lambda event, paddle=paddle, canvas=canvas: up(event, paddle, canvas))
            if ind == 1:
                canvas.unbind_all('<Down>')
                canvas.unbind_all('<Up>')
                canvas.bind_all('<Down>', lambda event, paddle=paddle, canvas=canvas: down(event, paddle, canvas))
                canvas.bind_all('<Up>', lambda event, paddle=paddle, canvas=canvas: up(event, paddle, canvas))
            if ind == 2:
                canvas.unbind_all('<f>')
                canvas.unbind_all('<g>')
                canvas.bind_all('<f>', lambda event, paddle=paddle, canvas=canvas: left(event, paddle, canvas))
                canvas.bind_all('<g>', lambda event, paddle=paddle, canvas=canvas: right(event, paddle, canvas))
            if ind == 3:
                canvas.unbind_all('<j>')
                canvas.unbind_all('<k>')
                canvas.bind_all('<j>', lambda event, paddle=paddle, canvas=canvas: left(event, paddle, canvas))
                canvas.bind_all('<k>', lambda event, paddle=paddle, canvas=canvas: right(event, paddle, canvas))
        for score in scores:
            if score.value == win_point.get():
                won = 'True'
                break
            if score.value == -win_point.get():
                won = scores.index(score)
                break
        if won == False:
            canvas.delete("score")
            for score in scores:
                ind = scores.index(score)
                if ind == 0:
                    score.drawScore(canvas, height, width, one=True)
                elif ind == 1:
                    score.drawScore(canvas, height, width, two=True)
                elif ind == 2:
                    score.drawScore(canvas, height, width, three=True)
                elif ind == 3:
                    score.drawScore(canvas, height, width, four=True)
            ball.start = False
            canvas.after(move_update + 495, move_ball, canvas, ball, paddles, scores, bubbles)
        elif won == 'True':
            winner = str(scores.index(score) + 1)
            canvas.unbind_all('<s>')
            canvas.unbind_all('<Down>')
            canvas.unbind_all('<z>')
            canvas.unbind_all('<Up>')
            canvas.unbind_all('<f>')
            canvas.unbind_all('<g>')
            canvas.unbind_all('<j>')
            canvas.unbind_all('<k>')
            scores.clear()
            paddles.clear()
            change_frame('end')
        else:
            canvas.unbind_all('<s>')
            canvas.unbind_all('<Down>')
            canvas.unbind_all('<z>')
            canvas.unbind_all('<Up>')
            canvas.unbind_all('<f>')
            canvas.unbind_all('<g>')
            canvas.unbind_all('<j>')
            canvas.unbind_all('<k>')
            if won != len(paddles) - 1:
                scores.insert(won, scores.pop(-1))
            canvas.delete(paddles[-1].tag)
            scores.pop(-1)
            paddles.pop(-1)
            canvas.delete("score")
            for score in scores:
                ind = scores.index(score)
                if ind == 0:
                    score.drawScore(canvas, height, width, one=True)
                elif ind == 1:
                    score.drawScore(canvas, height, width, two=True)
                elif ind == 2:
                    score.drawScore(canvas, height, width, three=True)
                elif ind == 3:
                    score.drawScore(canvas, height, width, four=True)
            change_players(str(len(paddles) + 1), str(won + 1), canvas)
            won = False
            canvas.after(5000, move_ball, canvas, ball, paddles, scores, bubbles)
    else:
        if len(bubbles) < 1:
            bubbles = spawn_bubbles(canvas, bubbles)
        for bubble in bubbles:
            if bubble.drawn == False:
                bubble.drawObject(canvas)
            if bubble.touchBall(ball):
                bubble_effect(bubble.number, ball, paddles, canvas)
                canvas.delete(bubble.tag)
                bubbles.remove(bubble)
        if players.get() == 1:
            gotit = random.random()
            if gotit > 0.93:
                if paddles[1].y1 + paddles[1].sizey / 2 > ball.y1 + ball.sizey / 2:
                    paddles[1].y1 -= 15
                    paddles[1].y2 -= 15
                elif paddles[1].y1 + paddles[1].sizey / 2 < ball.y1 + ball.sizey / 2:
                    paddles[1].y1 += 15
                    paddles[1].y2 += 15
                canvas.delete(paddles[1].tag)
                paddles[1].drawObject(canvas)
        canvas.after(move_update, move_ball, canvas, ball, paddles, scores, bubbles)

def change_players(nbplayers, looser, canvas):
    loose = "J" + looser + " a perdu."
    change = None
    if nbplayers != looser:
        change = "J" + nbplayers + " devient J" + looser
    canvas.create_rectangle(0, 0, width, height, fill=colors[color].background, tag="mid")
    canvas.create_text(width/2, 50, text=loose, font=("Helvetica", 32), fill=colors[color].foreground, tag="mid")
    if change != None:
        canvas.create_text(width/2, 100, text=change, font=("Helvetica", 25), fill=colors[color].foreground, tag="mid")
    rules(canvas, int(nbplayers) - 1)
    canvas.after(5000, canvas.delete, "mid")

def rules(can, players):
    can.create_text(width/2, height/2, text="Règles", font=("Helvetica", 32), fill=colors[color].foreground, tag="rules")
    can.create_text(width/2, height/2 + 50, text="J1 : à gauche, haut -> Z, bas -> S", font=("Helvetica", 25), fill=colors[color].foreground, tag="rules")
    if players > 1:
        can.create_text(width/2, height/2 + 100, text="J2 : à droite, haut -> ↑, bas -> ↓", font=("Helvetica", 25), fill=colors[color].foreground, tag="rules")
    if players > 2:
        can.create_text(width/2, height/2 + 150, text="J3 : en haut, gauche -> F, bas -> G", font=("Helvetica", 25), fill=colors[color].foreground, tag="rules")
    if players > 3:
        can.create_text(width/2, height/2 + 200, text="J4 : en bas, gauche -> J, bas -> K", font=("Helvetica", 25), fill=colors[color].foreground, tag="rules")
    can.after(5000, can.delete, "rules")

def get_game_frame(master):
    global start_time
    start_time = time.time()
    frame = tk.Frame(master)
    canvas = tk.Canvas(frame, bg=colors[color].background, height=height, width=width)
    canvas.pack()
    ball = Ball(width / 2, height / 2, sizex=20, sizey=20, sx=speed.get(), sy=speed.get(), color=colors[color].foreground, outline=colors[color].foreground, tag="ball")
    ball.drawObject(canvas)
    paddles = []
    scores = []
    bubbles = []
    for i in range(players.get()):
        if i == 0:
            paddles.append(Paddle(23, height / 2, sizex=paddlew, sizey=paddleh, sy=paddlespeed, color=colors[color].foreground, outline=colors[color].foreground, tag="paddleL"))
            canvas.bind_all('<s>', lambda event, paddle=paddles[0], canvas=canvas: down(event, paddle, canvas))
            canvas.bind_all('<z>', lambda event, paddle=paddles[0], canvas=canvas: up(event, paddle, canvas))
        if i == 1:
            paddles.append(Paddle(width - 23, height / 2, sizex=paddlew, sizey=paddleh, sy=paddlespeed, color=colors[color].foreground, outline=colors[color].foreground, tag="paddleR"))
            canvas.bind_all('<Down>', lambda event, paddle=paddles[1], canvas=canvas: down(event, paddle, canvas))
            canvas.bind_all('<Up>', lambda event, paddle=paddles[1], canvas=canvas: up(event, paddle, canvas))
        if i == 2:
            paddles.append(Paddle(width / 2, 23, sizex=paddleh, sizey=paddlew, sx=paddlespeed, color=colors[color].foreground, outline=colors[color].foreground, tag="paddleT"))
            canvas.bind_all('<f>', lambda event, paddle=paddles[2], canvas=canvas: left(event, paddle, canvas))
            canvas.bind_all('<g>', lambda event, paddle=paddles[2], canvas=canvas: right(event, paddle, canvas))
        if i == 3:
            paddles.append(Paddle(width / 2, height - 23, sizex=paddleh, sizey=paddlew, sx=paddlespeed, color=colors[color].foreground, outline=colors[color].foreground, tag="paddleD"))
            canvas.bind_all('<j>', lambda event, paddle=paddles[3], canvas=canvas: left(event, paddle, canvas))
            canvas.bind_all('<k>', lambda event, paddle=paddles[3], canvas=canvas: right(event, paddle, canvas))
        paddles[i].drawObject(canvas)
        scores.append(Score(0, color=colors[color].foreground))
        if i == 0:
            scores[i].drawScore(canvas, height, width, one=True)
        elif i == 1:
            scores[i].drawScore(canvas, height, width, two=True)
        elif i == 2:
            scores[i].drawScore(canvas, height, width, three=True)
        elif i == 3:
            scores[i].drawScore(canvas, height, width, four=True)
    if players.get() == 1:
        paddles.append(Paddle(width - 23, height / 2, sizex=15, sizey=160, sy=15, color=colors[color].foreground, outline=colors[color].foreground, tag="paddleR"))
        paddles[1].drawObject(canvas)
        scores.append(Score(0, color=colors[color].foreground))
        scores[1].drawScore(canvas, height, width, two=True)

    rsx = random.randint(0, 1)
    if rsx == 0:
        rsx = -1
    ball.sx = ball.sx * rsx
    rsy = random.randint(0, 1)
    if rsy == 0:
        rsy = -1
    ball.sy = ball.sy * rsy

    ball.start = False
    canvas.create_rectangle(0, 0, width, height, fill=colors[color].background, tag="rules")
    rules(canvas, players.get())
    canvas.after(5000, move_ball, canvas, ball, paddles, scores, bubbles)
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
    canvas = tk.Canvas(frame, bg=colors[color].background, height=height, width=width)
    canvas.grid(column=0, row=0, columnspan=2)
    canvas.create_text(width/2, height/2, text=wins, font=("Helvetica", 32), fill=colors[color].foreground)
    canvas.create_text(width/2, height/2 + 50, text=end_time, font=("Helvetica", 25), fill=colors[color].foreground)
    tk.Button(frame, text='Retour au menu', command=lambda: change_frame('menu')).grid(column=0, row=1)
    tk.Button(frame, text='Rejouer', command=lambda: change_frame('game')).grid(column=1, row=1)
    return frame

all_frames = {'game': get_game_frame, 'option': get_option_frame, 'menu': get_menu_frame, 'end': get_end_frame}
frame = get_menu_frame(root)
frame.pack()
root.mainloop()
