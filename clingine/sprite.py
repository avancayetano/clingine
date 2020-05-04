from . import shapes, sprite, clock
import time, math
class Sprite:
	def __init__(self, window, x=0, y=0, direction=(0, 0), speed=(0, 0), images=[], image_num=0, color_pair=None, group=None):
		self.window = window
		self.x = x
		self.y = y
		self.direction = tuple(direction)
		self.speed = tuple(speed)

		if color_pair != None:
			self.color_pair = tuple(color_pair)
		else:
			self.color_pair = color_pair

		self.images = images
		self.image_num = image_num

		self.source = self.images[self.image_num].source
		self.width = self.images[self.image_num].width
		self.height = self.images[self.image_num].height
		self.image = self.images[self.image_num].value

		self.animation_clock = clock.Clock()

		self.group = group
		if type(self.group) == list:
			self.group.append(self)

	def check_bounds(self):
		pass

	def unrender(self):
		for y in range(len(self.image)):
			for x in range(len(self.image[y])):
				if self.image[y][x] != " " and 0 <= math.floor(self.x) + x <= self.window.width - 2 and 0 <= math.floor(self.y) + y <= self.window.height - 2:
					is_changed = not(self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x][1:] == [self.window.char, self.window.color_pair])
					if not is_changed:
						is_changed = self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x][0]
					self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x] = [is_changed, self.window.char, self.window.color_pair]

	def render(self):
		for y in range(len(self.image)):
			for x in range(len(self.image[y])):
				if self.image[y][x] != " " and 0 <= math.floor(self.x) + x <= self.window.width - 2 and 0 <= math.floor(self.y) + y <= self.window.height - 2:
					is_changed = not(self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x][1:] == [self.image[y][x], self.color_pair])
					if not is_changed:
						is_changed = self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x][0]
					self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x] = [is_changed, self.image[y][x], self.color_pair]

	def update(self, dt):
		self.unrender()
		self.x += self.direction[0] * self.speed[0] * dt
		self.y += self.direction[1] * self.speed[1] * dt
		self.check_bounds()

	def animate(self, loop=True, fps=60):
		if self.animation_clock.get_dt() >= 1 / fps:
			if self.image_num == len(self.images):
				if loop:
					self.image_num = 0
				else:
					self.destroy()
					return
			self.unrender()
			self.source = self.images[self.image_num].source
			self.width = self.images[self.image_num].width
			self.height = self.images[self.image_num].height
			self.image = self.images[self.image_num].value
			self.image_num += 1
			self.animation_clock.update()
			self.render()

	def destroy(self):
		self.unrender()
		if self.group:
			self.group.remove(self)
		
	def check_group_collision(self, others):
		for obj in others:
			collided = self.is_collided_with(obj)
			if not(collided is self) and collided:
				return collided

	def is_collided_with(self, other):
		if (self.x < other.x + other.width and self.x + self.width > other.x) and (self.y < other.y + other.height and self.y + self.height > other.y) \
				and (isinstance(other, shapes.Rect) or isinstance(other, sprite.Sprite)):
			return other