import clingine, random

class Asteroid(clingine.sprite.Sprite):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
	def reset(self):
		self.y = random.randrange(-self.height - 40, -self.height)
		self.x = random.randrange(1, self.window.width - 1 - self.width)

	def check_bounds(self):
		if self.y > self.window.height:
			self.reset()

		if self.is_collided_with(self.window.player) and self.window.player.state == "alive":
			self.window.player.state = "dead"
			for ast in self.window.asteroids:
				ast.reset()
			self.window.player.reset()