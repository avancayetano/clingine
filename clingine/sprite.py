import clingine
class Sprite:
	def __init__(self, window, x=0, y=0, direction=(0, 0), speed=(1, 1), images=[], image_num=0):
		self.window = window
		self.x = x
		self.y = y
		self.direction = direction
		self.speed = speed

		self.images = images
		self.image_num = image_num

		self.source = self.images[self.image_num].source
		self.width = self.images[self.image_num].width
		self.height = self.images[self.image_num].height
		self.image = self.images[self.image_num].value

		self.animate_count = 0

	def check_bounds(self):
		pass

	def unrender(self):
		for y in range(len(self.image)):
			for x in range(len(self.image[y])):
				if self.image[y][x] != " " and 0 <= int(self.x) + x <= self.window.width - 1 and 0 <= int(self.y) + y <= self.window.height - 1:
					self.window.screen[int(self.y) + y][int(self.x) + x] = self.window.char

	def render(self):
		for y in range(len(self.image)):
			for x in range(len(self.image[y])):
				if self.image[y][x] != " " and 0 <= int(self.x) + x <= self.window.width - 1 and 0 <= int(self.y) + y <= self.window.height - 1:
					self.window.screen[int(self.y) + y][int(self.x) + x] = self.image[y][x]

	def update(self):
		self.unrender()
		self.x += self.direction[0] * self.speed[0]
		self.y += self.direction[1] * self.speed[1]
		self.check_bounds()

	# its important to unrender first the sprite then animate, not animate then unrender
	# the sprite will animate every rate frames
	def animate(self, loop=True, rate=5):
		self.animate_count += 1
		if self.animate_count == rate:
			if self.image_num == len(self.images):
				self.image_num = 0
			self.source = self.images[self.image_num].source
			self.width = self.images[self.image_num].width
			self.height = self.images[self.image_num].height
			self.image = self.images[self.image_num].value
			self.image_num += 1
			self.animate_count = 0
		
	def check_group_collision(self, others):
		for obj in others:
			collided = self.is_collided_with(obj)
			if not(collided is self) and collided:
				return collided

	def is_collided_with(self, other):
		if (self.x < other.x + other.width and self.x + self.width > other.x) and (self.y < other.y + other.height and self.y + self.height > other.y) \
				and (isinstance(other, clingine.shapes.Rect) or isinstance(other, clingine.sprite.Sprite)):
			return other