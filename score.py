class Score:
    def __init__(self, value, color="black"):
        self.value = value
        self.color = color

    def drawScore(self, canvas, height, width, one=False, two=False, three=False, four=False):
        if one:
            text = "J1 : " + str(self.value)
            x = width / 4
            y = 30
        if two:
            text = "J2 : " + str(self.value)
            x = 3 * width / 4
            y = height - 30
        if three:
            text = "J3 : " + str(self.value)
            x = 3 * width / 4
            y = 30
        if four:
            text = "J4 : " + str(self.value)
            x = width / 4
            y = height - 30
        canvas.create_text(x, y, text=text, font=("Helvetica", 20), fill=self.color, tag="score")

    def __del__(self):
        print("score del")
