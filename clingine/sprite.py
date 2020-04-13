import clingine, time
class Sprite:
	def __init__(self, window, x=0, y=0, direction=(0, 0), speed=(0, 0), images=[], image_num=0, color_pair=None, group=None):
		self.window = window
		self.x = x
		self.y = y
		self.direction = direction
		self.speed = speed

		self.color_pair = color_pair

		self.images = images
		self.image_num = image_num

		self.source = self.images[self.image_num].source
		self.width = self.images[self.image_num].width
		self.height = self.images[self.image_num].height
		self.image = self.images[self.image_num].value

		self.animation_clock = 0

		self.group = group
		if type(self.group) == list:
			self.group.append(self)

	def check_bounds(self):
		pass

	def unrender(self):
		for y in range(len(self.image)):
			for x in range(len(self.image[y])):
				if 0 <= int(self.x) + x <= self.window.width - 1 and 0 <= int(self.y) + y <= self.window.height - 1:
					is_changed = not(self.window.screen_array[int(self.y) + y][int(self.x) + x][1:] == [self.window.char, self.window.screen_color_pair])
					if not is_changed:
						is_changed = self.window.screen_array[int(self.y) + y][int(self.x) + x][0]
					self.window.screen_array[int(self.y) + y][int(self.x) + x] = [is_changed, self.window.char, self.window.screen_color_pair]

	def render(self):
		for y in range(len(self.image)):
			for x in range(len(self.image[y])):
				if 0 <= int(self.x) + x <= self.window.width - 1 and 0 <= int(self.y) + y <= self.window.height - 1:
					is_changed = not(self.window.screen_array[int(self.y) + y][int(self.x) + x][1:] == [self.image[y][x], self.color_pair])
					if not is_changed:
						is_changed = self.window.screen_array[int(self.y) + y][int(self.x) + x][0]
					self.window.screen_array[int(self.y) + y][int(self.x) + x] = [is_changed, self.image[y][x], self.color_pair]

	def update(self, dt):
		self.unrender()
		self.x += self.direction[0] * self.speed[0] * dt
		self.y += self.direction[1] * self.speed[1] * dt
		self.check_bounds()

	# its important to unrender first the sprite then animate, not animate then unrender
	# the sprite will animate every rate seconds
	def animate(self, loop=True, rate=1):
		if time.time() - self.animation_clock >= rate:
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
			self.animation_clock = time.time()
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
				and (isinstance(other, clingine.shapes.Rect) or isinstance(other, clingine.sprite.Sprite)):
			return other