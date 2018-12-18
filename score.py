class Score:
    def __init__(self, value, color="black"):
        self.value = value
        self.color = color

    def drawScore(self, canvas, height, width, r=False):
        if r:
            text = "J2 : " + str(self.value)
            x = 3 * width / 4
        else:
            text = "J1 : " + str(self.value)
            x = width / 4
        canvas.create_text(x, 30, text=text, font=("Helvetica", 20), fill=self.color, tag="score")

    def __del__(self):
        print("score del")
