class Score:
    def __init__(self, value):
        self.value = value

    def drawScore(self, canvas, height, width, r=False):
        if r:
            canvas.create_text(width-50, 10, text=str(self.value))
        else:
            canvas.create_text(10, 10, text=str(self.value))
