import clingine
class Rect:
	def __init__(self, window, x=0, y=0, width=1, height=1, direction=(0, 0), speed=(1, 1), char="*"):
		# x, y is the top left position of Rect
		self.window = window
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.direction = direction
		self.speed = speed
		self.char = char


	def update(self):
		self.unrender()
		self.x += self.direction[0] * self.speed[0]
		self.y += self.direction[1] * self.speed[1]
		self.check_bounds()

	def check_bounds():
		pass

	def unrender(self):
		for y in range(self.height):
			for x in range(self.width):
				if 0 <= int(self.x) + x <= self.window.width - 1 and 0 <= int(self.y) + y <= self.window.height - 1:
					self.window.screen[int(self.y) + y][int(self.x) + x] = self.window.char

	def render(self):
		for y in range(self.height):
			for x in range(self.width):
				if 0 <= int(self.x) + x <= self.window.width -1 and 0 <= int(self.y) + y <= self.window.height - 1:
					self.window.screen[int(self.y) + y][int(self.x) + x] = self.char

	def check_group_collision(self, others):
		for obj in others:
			collided = self.is_collided_with(obj)
			if not(collided is self) and collided:
				return collided

	def is_collided_with(self, other):
		if (self.x < other.x + other.width and self.x + self.width > other.x) and (self.y < other.y + other.height and self.y + self.height > other.y) \
				and (isinstance(other, clingine.shapes.Rect) or isinstance(other, clingine.sprite.Sprite)):
			return other