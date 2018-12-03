import tkinter as tk
height = 800
width = 800
root = tk.Tk()
root.title("Test")
can = tk.Canvas(root, bg="#ffffff", height=height, width=width)
can.pack()
root.update_idletasks()

can.create_oval(width / 2 - 10, height / 2 - 10, width / 2 + 10, height / 2 + 10, fill="black", tags="Balle")

x = 0.20
y = 0.10

while True:
    can.move("Balle", x, y)
    bx1, by1, bx2, by2 = can.coords("Balle")
    if bx2 >= width or bx1 <= 0:
        x = -x
    if by2 >= height or by1 <= 0:
        y = -y
    can.update()
root.mainloop()
