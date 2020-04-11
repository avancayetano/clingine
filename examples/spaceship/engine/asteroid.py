import clingine, random, time

class Asteroid(clingine.sprite.Sprite):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.init_health = 2
		self.health = self.init_health
		
	def reset(self):
		self.health = self.init_health
		self.unrender()
		self.y = random.randrange(-self.height - 40, -self.height)
		self.x = random.randrange(1, self.window.width - 1 - self.width)

	def check_bounds(self):
		if self.y > self.window.height:
			self.reset()

		if self.is_collided_with(self.window.player) and self.window.player.state == "alive":
			self.window.player.state = "dead"
			for ast in self.window.asteroids:
				ast.reset()
			time.sleep(1)

