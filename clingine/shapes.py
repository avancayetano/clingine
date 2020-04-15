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
		self.direction = tuple(direction)
		self.speed = tuple(speed)
		self.char = char
		if type(color_pair) != None:
			self.color_pair = tuple(color_pair)
		else:
			self.color_pair = color_pair
		self.group = group
		if type(self.group) == list:
			self.group.append(self)
			
	def update(self, dt):
		self.unrender()
		self.x += self.direction[0] * self.speed[0] * dt
		self.y += self.direction[1] * self.speed[1] * dt
		self.check_bounds()

	def check_bounds(self):
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


class Triangle:
	def __init__(self, window, vertices=(), direction=(0, 0), speed=(0, 0), char="*", color_pair=None, group=None):
		self.window = window
		self.vertices = tuple(tuple(v) for v in sorted(list(vertices), key=lambda x: (x[1], x[0])))
		print(self.vertices)
		self.direction = tuple(direction)
		self.speed = tuple(speed)
		if type(color_pair) != None:
			self.color_pair = tuple(color_pair)
		else:
			self.color_pair = color_pair
		self.char = char
		self.group = group
		if type(self.group) == list:
			self.group.append(self)

	def update(self, dt):
		self.unrender()
		new_vertices = []
		for x, y in self.vertices:
			new_vertices.append((x + self.direction[0] * self.speed[0] * dt, y + self.direction[1] * self.speed[1] * dt))

		self.vertices = tuple(new_vertices)
		self.check_bounds()

	def check_bounds(self):
		pass


	def render(self):
		x1, y1 = self.vertices[0][0], self.vertices[0][1]
		x2, y2 = self.vertices[1][0], self.vertices[1][1]
		x3, y3 = self.vertices[2][0], self.vertices[2][1]

		if y2 == y3:
			self.fill_bottom(x1, y1, x2, y2, x3, y3, self.char, self.color_pair)
		elif y1 == y2:
			self.fill_top(x1, y1, x2, y2, x3, y3, self.char, self.color_pair)
		else:
			x4 = x1 + (y2 - y1) / (y3 - y1) * (x3 - x1)
			y4 = y2
			self.fill_bottom(x1, y1, x2, y2, x4, y4, self.char, self.color_pair)
			self.fill_top(x2, y2, x4, y4, x3, y3, self.char, self.color_pair)

	def unrender(self):
		x1, y1 = self.vertices[0][0], self.vertices[0][1]
		x2, y2 = self.vertices[1][0], self.vertices[1][1]
		x3, y3 = self.vertices[2][0], self.vertices[2][1]
		if y2 == y3:
			self.fill_bottom(x1, y1, x2, y2, x3, y3, self.window.char, self.window.screen_color_pair)
		elif y1 == y2:
			self.fill_top(x1, y1, x2, y2, x3, y3, self.window.char, self.window.screen_color_pair)
		else:
			x4 = x1 + (y2 - y1) / (y3 - y1) * (x3 - x1)
			y4 = y2
			self.fill_bottom(x1, y1, x2, y2, x4, y4, self.window.char, self.window.screen_color_pair)
			self.fill_top(x2, y2, x4, y4, x3, y3, self.window.char, self.window.screen_color_pair)

	def draw_line(self, x1, x2, y, char, color_pair):
		for x in range(math.floor(x1), math.floor(x2) + 1):
			if 0 <= x <= self.window.width - 1 and 0 <= y <= self.window.height - 1:
				self.window.screen_array[y][x] = [True, char, color_pair]

	def fill_bottom(self, x1, y1, x2, y2, x3, y3, char, color_pair):
		slope_1 = (x2 - x1) / (y2 - y1)
		slope_2 = (x3 - x1) / (y3 - y1)
		cur_x1 = x1
		cur_x2 = x1
		for y in range(math.floor(y1), math.floor(y2) + 1):
			self.draw_line(cur_x1, cur_x2, y, char, color_pair)
			cur_x1 += slope_1
			cur_x2 += slope_2


	def fill_top(self, x1, y1, x2, y2, x3, y3, char, color_pair):
		slope_1 = (x3 - x1) / (y3 - y1)
		slope_2 = (x3 - x2) / (y3 - y2)

		cur_x1 = x3
		cur_x2 = x3

		for y in range(math.floor(y3), math.floor(y1), -1):
			self.draw_line(cur_x1, cur_x2, y, char, color_pair)
			cur_x1 -= slope_1
			cur_x2 -= slope_2

	def check_group_collision(self, others):
		for obj in others:
			collided = self.is_collided_with(obj)
			if not(collided is self) and collided:
				return collided

	def is_collided_with(self, other):
		pass

	def destroy(self):
		self.unrender()
		if self.group:
			self.group.remove(self)


class Polygon:
	def __init__(self, window, vertices=(), direction=(0, 0), speed=(0, 0), char="*", color_pair=None, group=None):
		self.window = window
		self.vertices = (tuple(v) for v in vertices)
		self.direction = tuple(direction)
		self.speed = tuple(speed)
		if type(color_pair) != None:
			self.color_pair = tuple(color_pair)
		else:
			self.color_pair = color_pair
		self.char = char
		self.group = group
		if type(self.group) == list:
			self.group.append(self)

	def sort_vertices(self):
		sorted_vertices = []
		pt = sorted(self.vertices, key=lambda v: v[0])[0]
		i = 0
		while True:
			sorted_vertices[i] = pt
			endpoint = self.vertices[0]
			for j in range(len(self.vertices) + 1):
				if endpoint == pt or self.is_vertex_left_of_line(self.vertices[j], self.vertices[i], endpoint):
					endpoint = self.vertices[j]
			if endpoint == sorted_vertices[0]:
				break

	def is_vertex_left_of_line(vertex, point_on_hull, endpoint):
		pass


	def update(self, dt):
		self.unrender()
		new_vertices = []
		for x, y in self.vertices:
			new_vertices.append((x + self.direction[0] * self.speed * dt, y + self.direction[1] * self.speed[1] * dt))

		self.vertices = tuple(new_vertices)
		self.check_bounds()

	def check_bounds(self, dt):
		pass

	def unrender(self):
		pass

	def render(self):
		pass

	def check_group_collision(self, others):
		pass

	def is_collided_with(self, other):
		pass

	def destroy(self):
		self.unrender()
		if self.group:
			self.group.remove(self)


class Circle:
	def __init__(self, window, center=(0, 0), radius=1, char="*", color_pair=None, group=None):
		self.window = window
		self.center = tuple(center)
		self.radius = radius
		self.char = char
		if type(color_pair) != None:
			self.color_pair = tuple(color_pair)
		else:
			self.color_pair = color_pair
		self.group = group
		if type(self.group) == list:
			self.group.append(self)

	def update(self, dt):
		self.unrender()
		self.center = (self.center[i] + self.direction[i] * self.speed[i] * dt for i in range(len(self.center)))
		self.check_bounds()

	def check_bounds(self, dt):
		pass

	def unrender(self):
		pass

	def render(self):
		pass

	def check_group_collision(self, others):
		pass

	def is_collided_with(self, other):
		pass

	def destroy(self):
		self.unrender()
		if self.group:
			self.group.remove(self)