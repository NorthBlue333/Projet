class Object:
    def __init__(self, x1, y1, x2=0, y2=0, sizex=0, sizey=0, sx=0, sy=0, color="black", outline="black", tag=""):
        if sizex == 0:
            self.x1 = x1
            self.x2 = x2
        else:
            self.x1 = x1 - (sizex / 2)
            self.x2 = x1 + (sizex / 2)
        if sizey == 0:
            self.y1 = y1
            self.y2 = y2
        else:
            self.y1 = y1 - (sizey / 2)
            self.y2 = y1 + (sizey / 2)
        self.sx = sx
        self.sy = sy
        self.color = color
        self.outline = outline
        self.tag = tag
        self.sizex = sizex
        self.sizey = sizey
        self.last_touch = None

    def drawObject(self, canvas):
        pass

    def moveObject(self):
        self.x1 += self.sx
        self.y1 += self.sy
        self.x2 += self.sx
        self.y2 += self.sy
        return [self.x1, self.y1, self.x2, self.y2]

class Ball(Object):
    def __init__(self, x1, y1, x2=0, y2=0, sizex=0, sizey=0, sx=0, sy=0, color="black", outline="black", tag=""):
        self.start = True
        super().__init__(x1, y1, x2, y2, sizex, sizey, sx, sy, color, outline, tag)

    def drawObject(self, canvas):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=self.color, outline=self.outline, tag=self.tag)

    def moveObject(self, height=None, width=None, objects=None, scores=None):
        if len(objects) == 2:
            if height != None:
                if self.y1 <= 0 or self.y2 >= height:
                    self.sy = -self.sy
        elif len(objects) == 3:
            if height != None:
                if self.y2 >= height:
                    self.sy = -self.sy
        if objects != None:
            if len(objects) > 1:
                if width != None:
                    if self.x1 <= 0:
                        if scores != None:
                            if len(scores) == 2:
                                scores[1].value += 1
                            else:
                                scores[0].value -= 1
                        self.x1 = width/2 - self.sizex / 2
                        self.x2 = width/2 + self.sizex / 2
                        self.y1 = height/2 - self.sizey / 2
                        self.y2 = height/2 + self.sizey / 2
                        self.start = True
                    elif self.x2 >= width:
                        if scores != None:
                            if len(scores) == 2:
                                scores[0].value += 1
                            else:
                                scores[1].value -= 1
                        self.x1 = width/2 - self.sizex / 2
                        self.x2 = width/2 + self.sizex / 2
                        self.y1 = height/2 - self.sizey / 2
                        self.y2 = height/2 + self.sizey / 2
                        self.start = True
                if (self.y2 - self.sizey / 2 >= objects[0].y1 and self.y1 + self.sizey / 2 <= objects[0].y2) and self.x1 <= objects[0].x2:
                    self.sx = -self.sx
                    self.last_touch = 0
                if (self.y2 - self.sizey / 2 >= objects[1].y1 and self.y1 + self.sizey / 2 <= objects[1].y2) and self.x2 >= objects[1].x1:
                    self.sx = -self.sx
                    self.last_touch = 1
            if len(objects) > 2:
                if height != None:
                    if self.y1 <= 0:
                        if scores != None:
                            scores[2].value -= 1
                        self.x1 = width/2 - self.sizex / 2
                        self.x2 = width/2 + self.sizex / 2
                        self.y1 = height/2 - self.sizey / 2
                        self.y2 = height/2 + self.sizey / 2
                        self.start = True
                if (self.x2 - self.sizex / 2 >= objects[2].x1 and self.x1 + self.sizex / 2 <= objects[2].x2) and self.y1 <= objects[2].y2:
                    self.sy = -self.sy
                    self.last_touch = 2
            if len(objects) > 3:
                if height != None:
                    if self.y2 >= height:
                        if scores != None:
                            scores[3].value -= 1
                        self.x1 = width/2 - self.sizex / 2
                        self.x2 = width/2 + self.sizex / 2
                        self.y1 = height/2 - self.sizey / 2
                        self.y2 = height/2 + self.sizey / 2
                        self.start = True
                if (self.x2 - self.sizex / 2 >= objects[3].x1 and self.x1 + self.sizex / 2 <= objects[3].x2) and self.y2 >= objects[3].y1:
                    self.sy = -self.sy
                    self.last_touch = 3

        super().moveObject()

class Paddle(Object):
    def drawObject(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill=self.color, outline=self.outline, tag=self.tag)

    def moveObject(self, up=False, right=False, height=0, width=0):
        if up and self.sy > 0:
            self.sy = -self.sy
        elif not up and self.sy < 0:
            self.sy = -self.sy
        if right and self.sx < 0:
            self.sx = -self.sx
        elif not right and self.sx > 0:
            self.sx = -self.sx
        if ((up and self.y1 > 0) or (not up and self.y2 < height)) and ((right and self.x2 < width) or (not right and self.x1 > 0)):
            super().moveObject()

class Bubble(Object):
    def __init__(self, x1, y1, number, x2=0, y2=0, sizex=0, sizey=0, sx=0, sy=0, color="black", outline="black", tag=""):
        self.number = number
        if number < 2:
            self.color = "yellow"
        elif number == 2:
            self.color = "green"
        else:
            self.color = "red"
        self.drawn = False
        super().__init__(x1, y1, x2, y2, sizex, sizey, sx, sy, self.color, self.color, tag)

    def drawObject(self, canvas):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill=self.color, outline=self.color, tag=self.tag)
        self.drawn = True

    def touchBall(self, ball):
        if self.x2 >= ball.x1 and self.x1 <= ball.x2 and self.y1 <= ball.y2 and self.y2 >= ball.y1:
            return True
        else:
            return False
