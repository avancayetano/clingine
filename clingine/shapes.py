from . import sprite, shapes, clock
import math
class Rect:
	def __init__(self, window, x=0, y=0, width=1, height=1, direction=(0, 0), speed=(0, 0), char="*", color_pair=None, group=None):
		# x, y is the top left position of Rect
		self.window = window
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.direction = direction
		self.speed = speed
		self.char = char
		self.color_pair = color_pair
		self.group = group
		if type(self.group) == list:
			self.group.append(self)
			
	def update(self, dt):
		self.unrender()
		self.x += self.direction[0] * self.speed[0] * dt
		self.y += self.direction[1] * self.speed[1] * dt
		self.check_bounds()

	def check_bounds():
		pass

	def unrender(self):
		for y in range(self.height):
			for x in range(self.width):
				if 0 <= math.floor(self.x) + x <= self.window.width - 1 and 0 <= math.floor(self.y) + y <= self.window.height - 1:
					is_changed = not(self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x][1:] == [self.window.char, self.window.screen_color_pair])
					if not is_changed:
						is_changed = self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x][0]
					self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x] = [is_changed, self.window.char, self.window.screen_color_pair]

	def render(self):
		for y in range(self.height):
			for x in range(self.width):
				if 0 <= math.floor(self.x) + x <= self.window.width -1 and 0 <= math.floor(self.y) + y <= self.window.height - 1:
					is_changed = not(self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x][1:] == [self.char, self.color_pair])
					if not is_changed:
						is_changed = self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x][0]
					self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x] = [is_changed, self.char, self.color_pair]

	def check_group_collision(self, others):
		for obj in others:
			collided = self.is_collided_with(obj)
			if not(collided is self) and collided:
				return collided

	def is_collided_with(self, other):
		if (self.x < other.x + other.width and self.x + self.width > other.x) and (self.y < other.y + other.height and self.y + self.height > other.y) \
				and (isinstance(other,shapes.Rect) or isinstance(other,sprite.Sprite)):
			return other

	def destroy(self):
		self.unrender()
		if self.group:
			self.group.remove(self)