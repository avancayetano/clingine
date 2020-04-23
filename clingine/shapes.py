from . import sprite, shapes, clock
import math
class Rect:
	def __init__(self, window, x=0, y=0, width=1, height=1, direction=(0, 0), speed=(0, 0), char="*", fill=True, color_pair=None, group=None):
		# x, y is the top left position of Rect
		self.window = window
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.direction = tuple(direction)
		self.speed = tuple(speed)
		self.char = char
		self.fill = fill
		if color_pair != None:
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
		if self.fill:
			for y in range(math.floor(self.height)):
				for x in range(math.floor(self.width)):
					if 0 <= math.floor(self.x) + x <= self.window.width - 1 and 0 <= math.floor(self.y) + y <= self.window.height - 1:
						is_changed = not(self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x][1:] == [self.window.char, self.window.color_pair])
						if not is_changed:
							is_changed = self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x][0]
						self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x] = [is_changed, self.window.char, self.window.color_pair]
		else:
			for y in range(math.floor(self.height)):
				if 0 <= math.floor(self.x) <= self.window.width - 1 and 0 <= math.floor(self.y) + y <= self.window.height - 1:
					self.window.screen_array[math.floor(self.y) + y][math.floor(self.x)] = [True, self.window.char, self.window.color_pair]
				if 0 <= math.floor(self.x) + math.floor(self.width) <= self.window.width - 1 and 0 <= math.floor(self.y) + y <= self.window.height - 1:
					self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + math.floor(self.width)] = [True, self.window.char, self.window.color_pair]
				if (y == 0 or y == math.floor(self.height) - 1) and (0 <= math.floor(self.y) + y <= self.window.height - 1):
					for x in range(math.floor(self.width)):
						if 0 <= math.floor(self.x) + x <= self.window.width - 1:
							self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x] = [True, self.window.char, self.window.color_pair]
				
	def render(self):
		if self.fill:
			for y in range(math.floor(self.height)):
				for x in range(math.floor(self.width)):
					if 0 <= math.floor(self.x) + x <= self.window.width - 1 and 0 <= math.floor(self.y) + y <= self.window.height - 1:
						is_changed = not(self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x][1:] == [self.char, self.color_pair])
						if not is_changed:
							is_changed = self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x][0]
						self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x] = [is_changed, self.char, self.color_pair]
		else:
			for y in range(math.floor(self.height)):
				if 0 <= math.floor(self.x) <= self.window.width - 1 and 0 <= math.floor(self.y) + y <= self.window.height - 1:
					self.window.screen_array[math.floor(self.y) + y][math.floor(self.x)] = [True, self.char, self.color_pair]
				if 0 <= math.floor(self.x) + math.floor(self.width) <= self.window.width - 1 and 0 <= math.floor(self.y) + y <= self.window.height - 1:
					self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + math.floor(self.width)] = [True, self.char, self.color_pair]
				if (y == 0 or y == math.floor(self.height) - 1) and (0 <= math.floor(self.y) + y <= self.window.height - 1):
					for x in range(math.floor(self.width)):
						if 0 <= math.floor(self.x) + x <= self.window.width - 1:
							self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x] = [True, self.char, self.color_pair]

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

	def rotate(self):
		pass

	def update_shape(self, **kwargs):
		self.unrender()
		self.x = kwargs.get("x", self.x)
		self.y = kwargs.get("y", self.y)
		self.width = kwargs.get("width", self.width)
		self.height = kwargs.get("height", self.height)
		self.char = kwargs.get("char", self.char)
		self.fill = kwargs.get("fill", self.fill)
		color_pair = kwargs.get("color_pair", self.color_pair)
		if color_pair != None:
			self.color_pair = tuple(color_pair)
		else:
			self.color_pair = color_pair



class Triangle:
	def __init__(self, window, vertices=(), direction=(0, 0), speed=(0, 0), char="*", fill=True, color_pair=None, group=None):
		self.window = window
		self.vertices = tuple(tuple(v) for v in sorted(list(vertices), key=lambda x: (x[1], x[0])))
		self.direction = tuple(direction)
		self.speed = tuple(speed)
		self.fill = fill
		if color_pair != None:
			self.color_pair = tuple(color_pair)
		else:
			self.color_pair = color_pair
		self.char = char
		self.group = group
		if type(self.group) == list:
			self.group.append(self)


	def render(self):
		x1, y1 = self.vertices[0][0], self.vertices[0][1]
		x2, y2 = self.vertices[1][0], self.vertices[1][1]
		x3, y3 = self.vertices[2][0], self.vertices[2][1]

		if y2 == y3:
			self.fill_flat_bottom_triangle(x1, y1, x2, y2, x3, y3, self.char, self.color_pair)
		elif y1 == y2:
			self.fill_flat_top_triangle(x1, y1, x2, y2, x3, y3, self.char, self.color_pair)
		else:
			x4 = x1 + (y2 - y1) / (y3 - y1) * (x3 - x1)
			y4 = y2
			self.fill_flat_bottom_triangle(x1, y1, x2, y2, x4, y4, self.char, self.color_pair)
			self.fill_flat_top_triangle(x2, y2, x4, y4, x3, y3, self.char, self.color_pair)


	def draw_line(self, x1, x2, y, char, color_pair):
		for x in range(math.floor(x1), math.floor(x2) + 1):
			if 0 <= x <= self.window.width - 1 and 0 <= y <= self.window.height - 1:
				self.window.screen_array[y][x] = [True, char, color_pair]

	def draw_edge(self, x1, x2, y, char, color_pair):
		if 0 <= math.floor(x1) <= self.window.width - 1 and 0 <= y <= self.window.height - 1:
			self.window.screen_array[y][math.floor(x1)] = [True, char, color_pair]
		if 0 <= math.floor(x2) <= self.window.width - 1 and 0 <= y <= self.window.height - 1:
			self.window.screen_array[y][math.floor(x2)] = [True, char, color_pair]


	def fill_flat_bottom_triangle(self, x1, y1, x2, y2, x3, y3, char, color_pair):
		dx_1 = (x2 - x1) / (y2 - y1)
		dx_2 = (x3 - x1) / (y3 - y1)
		cur_x1 = x1
		cur_x2 = x1
		for y in range(math.floor(y1), math.floor(y2) + 1):
			if self.fill:
				self.draw_line(cur_x1, cur_x2, y, char, color_pair)
			else:
				self.draw_edge(cur_x1, cur_x2, y, char, color_pair)
			cur_x1 += dx_1
			cur_x2 += dx_2


	def fill_flat_top_triangle(self, x1, y1, x2, y2, x3, y3, char, color_pair):
		dx_1 = (x3 - x1) / (y3 - y1)
		dx_2 = (x3 - x2) / (y3 - y2)
		cur_x1 = x3
		cur_x2 = x3
		for y in range(math.floor(y3), math.floor(y1), -1):
			if self.fill:
				self.draw_line(cur_x1, cur_x2, y, char, color_pair)
			else:
				self.draw_edge(cur_x1, cur_x2, y, char, color_pair)
			cur_x1 -= dx_1
			cur_x2 -= dx_2

	def update(self, dt):
		self.unrender()
		new_vertices = []
		for x, y in self.vertices:
			new_vertices.append((x + self.direction[0] * self.speed[0] * dt, y + self.direction[1] * self.speed[1] * dt))

		self.vertices = tuple(new_vertices)
		self.check_bounds()

	def check_bounds(self):
		pass


	def unrender(self):
		x1, y1 = self.vertices[0][0], self.vertices[0][1]
		x2, y2 = self.vertices[1][0], self.vertices[1][1]
		x3, y3 = self.vertices[2][0], self.vertices[2][1]
		if y2 == y3:
			self.fill_flat_bottom_triangle(x1, y1, x2, y2, x3, y3, self.window.char, self.window.color_pair)
		elif y1 == y2:
			self.fill_flat_top_triangle(x1, y1, x2, y2, x3, y3, self.window.char, self.window.color_pair)
		else:
			x4 = x1 + (y2 - y1) / (y3 - y1) * (x3 - x1)
			y4 = y2
			self.fill_flat_bottom_triangle(x1, y1, x2, y2, x4, y4, self.window.char, self.window.color_pair)
			self.fill_flat_top_triangle(x2, y2, x4, y4, x3, y3, self.window.char, self.window.color_pair)

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

	def rotate(self):
		pass

	def update_shape(self, **kwargs):
		self.unrender()
		self.vertices = tuple(tuple(v) for v in sorted(list(kwargs.get("vertices", self.vertices)), key=lambda x: (x[1], x[0])))
		self.fill = kwargs.get("fill", self.fill)
		self.char = kwargs.get("char", self.char)
		color_pair = kwargs.get("color_pair", self.color_pair)
		if color_pair != None:
			self.color_pair = tuple(color_pair)
		else:
			self.color_pair = color_pair
		


class Polygon:
	def __init__(self, window, vertices=(), direction=(0, 0), speed=(0, 0), char="*", fill=True, color_pair=None, group=None):
		self.window = window
		self.vertices = tuple(tuple(v) for v in vertices)
		self.edges = tuple(sorted([tuple(sorted([self.vertices[v], self.vertices[(v + 1) % len(self.vertices)]], key=lambda v: v[1])) 
			for v in range(len(self.vertices))], key=lambda e: min(e[0][1], e[1][1])))
		self.direction = tuple(direction)
		self.speed = tuple(speed)
		self.fill = fill
		if color_pair != None:
			self.color_pair = tuple(color_pair)
		else:
			self.color_pair = color_pair
		self.char = char
		self.group = group
		if type(self.group) == list:
			self.group.append(self)

	def render(self):
		for y in range(math.floor(self.edges[0][0][1]), math.floor(self.edges[-1][1][1]) + 1):
			intersections = []
			intersected_edges = []
			for e in self.edges:
				if e[0][1] <= y <= e[1][1]:
					if e[0][1] != e[1][1]:
						intersected_edges.append(e)
						dx = (e[1][0] - e[0][0]) / (e[1][1] - e[0][1]) * (y - e[0][1])
						x = math.floor(e[0][0] + dx)
						if x not in intersections:
							intersections.append(x)
					else:
						x = sorted([e[0][0], e[1][0]])
						self.draw_line(x[0], x[1], y, self.char, self.color_pair)

			doubles = []
			for x in intersections:
				vertex_intersections = []
				for e in intersected_edges:
					if (x == math.floor(e[0][0]) and y == math.floor(e[0][1])) or (x == math.floor(e[1][0]) and y == math.floor(e[1][1])):
						vertex_intersections.append(e)
				if len(vertex_intersections) == 2 and ((vertex_intersections[0][1][1] > y and vertex_intersections[1][1][1] > y) or (vertex_intersections[0][0][1] < y and vertex_intersections[1][0][1]) < y):
					doubles.append(x)
			intersections.extend(doubles)
			intersections.sort()
			for i in range(0, len(intersections), 2):
				if self.fill:
					self.draw_line(intersections[i], intersections[i + 1], y, self.char, self.color_pair)
				else:
					self.draw_edge(intersections[i], intersections[i + 1], y, self.char, self.color_pair)


	def draw_line(self, x1, x2, y, char, color_pair):
		for x in range(math.floor(x1), math.floor(x2) + 1):
			if 0 <= x <= self.window.width - 1 and 0 <= y <= self.window.height - 1:
				self.window.screen_array[y][x] = [True, char, color_pair]

	def draw_edge(self, x1, x2, y, char, color_pair):
		if 0 <= math.floor(x1) <= self.window.width - 1 and 0 <= y <= self.window.height - 1:
			self.window.screen_array[y][math.floor(x1)] = [True, char, color_pair]
		if 0 <= math.floor(x2) <= self.window.width - 1 and 0 <= y <= self.window.height - 1:
			self.window.screen_array[y][math.floor(x2)] = [True, char, color_pair]

	def update(self, dt):
		self.unrender()
		new_vertices = []
		for x, y in self.vertices:
			new_vertices.append((x + self.direction[0] * self.speed[0] * dt, y + self.direction[1] * self.speed[1] * dt))
		self.vertices = tuple(new_vertices)
		self.edges = tuple(sorted([tuple(sorted([self.vertices[v], self.vertices[(v + 1) % len(self.vertices)]], key=lambda v: v[1])) 
			for v in range(len(self.vertices))], key=lambda e: min(e[0][1], e[1][1])))
		self.check_bounds()

	def check_bounds(self):
		pass

	def unrender(self):
		for y in range(math.floor(self.edges[0][0][1]), math.floor(self.edges[-1][1][1]) + 1):
			intersections = []
			intersected_edges = []
			for e in self.edges:
				if e[0][1] <= y <= e[1][1]:
					if e[0][1] != e[1][1]:
						intersected_edges.append(e)
						dx = (e[1][0] - e[0][0]) / (e[1][1] - e[0][1]) * (y - e[0][1])
						x = math.floor(e[0][0] + dx)
						if x not in intersections:
							intersections.append(x)
					else:
						x = sorted([e[0][0], e[1][0]])
						self.draw_line(x[0], x[1], y, self.window.char, self.window.color_pair)
			doubles = []
			for x in intersections:
				vertex_intersections = []
				for e in intersected_edges:
					if (x == math.floor(e[0][0]) and y == math.floor(e[0][1])) or (x == math.floor(e[1][0]) and y == math.floor(e[1][1])):
						vertex_intersections.append(e)
				if len(vertex_intersections) == 2 and ((vertex_intersections[0][1][1] > y and vertex_intersections[1][1][1] > y) or (vertex_intersections[0][0][1] < y and vertex_intersections[1][0][1]) < y):
					doubles.append(x)
			intersections.extend(doubles)
			intersections.sort()
			for i in range(0, len(intersections), 2):
				if self.fill:
					self.draw_line(intersections[i], intersections[i + 1], y, self.window.char, self.window.color_pair)
				else:
					self.draw_edge(intersections[i], intersections[i + 1], y, self.window.char, self.window.color_pair)


	def check_group_collision(self, others):
		pass

	def is_collided_with(self, other):
		pass

	def destroy(self):
		self.unrender()
		if self.group:
			self.group.remove(self)

	def rotate(self):
		pass

	def update_shape(self, **kwargs):
		self.unrender()
		self.vertices = tuple(tuple(v) for v in kwargs.get("vertices", self.vertices))
		self.edges = tuple(sorted([tuple(sorted([self.vertices[v], self.vertices[(v + 1) % len(self.vertices)]], key=lambda v: v[1])) 
			for v in range(len(self.vertices))], key=lambda e: min(e[0][1], e[1][1])))
		self.char = kwargs.get("char", self.char)
		self.fill = kwargs.get("fill", self.fill)
		color_pair = kwargs.get("color_pair", self.color_pair)
		if color_pair != None:
			self.color_pair = tuple(color_pair)
		else:
			self.color_pair = color_pair
		

class Circle:
	def __init__(self, window, center=(0, 0), radius=1, char="*", fill=True, color_pair=None, group=None):
		self.window = window
		self.center = tuple(center)
		self.radius = radius
		self.char = char
		self.fill = fill
		if color_pair != None:
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


	def update_shape(self, **kwargs):
		self.unrender()
		self.center = tuple(kwargs.get("center", self.center))
		self.radius = kwargs.get("radius", self.radius)
		self.char = kwargs.get("char", self.char)
		self.fill = kwargs.get("fill", self.fill)
		color_pair = kwargs.get("color_pair", self.color_pair)
		if color_pair != None:
			self.color_pair = tuple(color_pair)
		else:
			self.color_pair = color_pair

class Ellipse:
	pass