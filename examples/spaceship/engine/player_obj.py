import clingine, curses
class Player(clingine.sprite.Sprite):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.score = 0
		self.state = "dead"
		self.init_speed = self.speed
		self.init_pos = (self.x, self.y)
		self.init_direction = self.direction

		self.init_bullets_count = 200
		self.bullets_count = self.init_bullets_count
		self.bullets = []
		self.init_shoot_cooldown = 5
		self.shoot_cooldown = 0

	def reset(self):
		self.score = 0
		self.bullets = []
		self.bullets_count = self.init_bullets_count
		self.shoot_cooldown = 0
		self.x = self.init_pos[0]
		self.y = self.init_pos[1]
		self.direction = self.init_direction
		self.speed = self.init_speed

	def update(self, dt):
		self.unrender()
		self.score += 1
		self.x += self.direction[0] * self.speed[0] * dt
		self.y += self.direction[1] * self.speed[1] * dt
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

	def shoot(self):
		if self.bullets_count > 0 and self.shoot_cooldown == 0:
			self.shoot_cooldown = self.init_shoot_cooldown
			self.bullets_count -= 2
			Bullet(window=self.window, x=self.x, y=self.y, width=1, height=1, direction=(0, -1), speed=(0, 100), char="O", group=self.bullets, color_pair=((255, 255, 0), None))
			Bullet(window=self.window, x=self.x + self.width - 1, y=self.y, width=1, height=1, direction=(0, -1), speed=(0, 100), char="O", group=self.bullets, color_pair=((255, 255, 0), None))
		self.shoot_cooldown -= 1

class Bullet(clingine.shapes.Rect):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def check_bounds(self):
		if self.y < -1:
			self.unrender()
			self.window.player.bullets.remove(self)
