class Object:
    def __init__(self, x1, y1, x2, y2, vx=0, vy=0, color="black", outline="black", tag=""):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.vx = vx
        self.vy = vy
        self.color = color
        self.outline = outline
        self.tag = tag
        self.sizex = x2 - x1
        self.sizey = y2 - y1

    def drawObject(self, canvas):
        pass

    def moveObject(self):
        self.x1 += self.vx
        self.y1 += self.vy
        self.x2 += self.vx
        self.y2 += self.vy
        return [self.x1, self.y1, self.x2, self.y2]

class Ball(Object):
    def __init__(self, x1, y1, x2, y2, vx=0, vy=0, color="black", outline="black", tag=""):
        self.start = True
        super().__init__(x1, y1, x2, y2, vx, vy, color, outline, tag)

    def __del__(self):
        print("ball del")

    def drawObject(self, canvas):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=self.color, outline=self.outline, tag=self.tag)

    def moveObject(self, height=None, width=None, objects=None, scores=None):
        if height != None:
            if self.y1 <= 0 or self.y2 >= height:
                self.vy = -self.vy
        if width != None:
            if self.x1 <= 0:
                if scores != None:
                    scores[1].value += 1
                self.x1 = width/2 - self.sizex / 2
                self.x2 = width/2 + self.sizex / 2
                self.y1 = height/2 - self.sizey / 2
                self.y2 = height/2 + self.sizey / 2
                self.start = True
            elif self.x2 >= width:
                if scores != None:
                    scores[0].value += 1
                self.x1 = width/2 - self.sizex / 2
                self.x2 = width/2 + self.sizex / 2
                self.y1 = height/2 - self.sizey / 2
                self.y2 = height/2 + self.sizey / 2
                self.start = True
        if objects != None:
            if (self.y2 - self.sizey / 2 >= objects[0].y1 and self.y1 + self.sizey / 2 <= objects[0].y2) and self.x1 <= objects[0].x2:
                self.vx = -self.vx
                self.last_touch = 1
            if (self.y2 - self.sizey / 2 >= objects[1].y1 and self.y1 + self.sizey / 2 <= objects[1].y2) and self.x2 >= objects[1].x1:
                self.vx = -self.vx
                self.last_touch = 2
        super().moveObject()

class Paddle(Object):
    def __del__(self):
        print("paddle del")

    def drawObject(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.color, outline=self.outline, tag=self.tag)

    def moveObject(self, up=False):
        if up and self.vy > 0:
            self.vy = -self.vy
        elif not up and self.vy < 0:
            self.vy = -self.vy
        super().moveObject()
