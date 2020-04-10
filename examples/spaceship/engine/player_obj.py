import clingine
class Player(clingine.sprite.Sprite):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.score = 0
		self.state = "dead"
		self.init_speed = self.speed
		self.init_pos = (self.x, self.y)
		self.init_direction = self.direction

	def reset(self):
		self.x = self.init_pos[0]
		self.y = self.init_pos[1]
		self.direction = self.init_direction
		self.speed = self.init_speed

	def update(self):
		self.unrender()
		self.score += 1
		self.window.score.text = "SCORE: {}".format(self.score)
		self.x += self.direction[0] * self.speed[0]
		self.y += self.direction[1] * self.speed[1]
		self.check_bounds()

	def check_bounds(self):
		if self.x < 1:
			self.x = 1
		if self.x + self.width > self.window.width - 1:
			self.x = self.window.width - 1 - self.width
		if self.y < 1:
			self.y = 1
		if self.y + self.height > self.window.height - 1:
			self.y = self.window.height - 1 - self.height
