import clingine, random

class Star(clingine.shapes.Rect):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.char = random.choice(["*", ".", "o"])

	def reset(self):
		self.y = 0
		self.x = random.randrange(self.window.width - 1)

	def check_bounds(self):
		if self.y > self.window.height:
			self.reset()