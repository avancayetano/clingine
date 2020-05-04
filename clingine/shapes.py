from . import sprite, shapes, clock
import math
class Rect:
	def __init__(self, window, x=0, y=0, width=1, height=1, direction=(0, 0), speed=(0, 0), char="*", fill=True, color_pair=None, group=None):
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
		y1 = math.floor(self.y) if math.floor(self.y) > 0 else 0
		y2 = math.floor(self.y + self.height) if math.floor(self.y + self.height) < self.window.height - 2 else self.window.height - 2
		x1 = self.x if self.x > 0 else 0
		x2 = self.x + self.width - 1 if self.x + self.width - 1 < self.window.width - 2 else self.window.width - 2
		for y in range(y1, y2):
			if self.fill:
				self.draw_line(x1, x2, y, self.window.char, self.window.color_pair)
			else:
				self.draw_edge(x1, x2, y, self.window.char, self.window.color_pair)

	
	def draw_line(self, x1, x2, y, char, color_pair):
		y = math.floor(y)
		for x in range(math.floor(x1), math.floor(x2) + 1):
			if 0 <= x <= self.window.width - 2 and 0 <= y <= self.window.height - 2:
				is_changed = not(self.window.screen_array[y][x][1:] == [char, color_pair])
				if not is_changed:
					is_changed = self.window.screen_array[y][x][0]
				self.window.screen_array[y][x] = [is_changed, char, color_pair]

	def draw_edge(self, x1, x2, y, char, color_pair):
		y = math.floor(y)
		x1 = math.floor(x1)
		x2 = math.floor(x2)
		if 0 <= x1 <= self.window.width - 2 and 0 <= y <= self.window.height - 2:
			is_changed = not(self.window.screen_array[y][x1][1:] == [char, color_pair])
			if not is_changed:
				is_changed = self.window.screen_array[y][x1][0]
			self.window.screen_array[y][x1] = [is_changed, char, color_pair]
		if 0 <= x2 <= self.window.width - 2 and 0 <= y <= self.window.height - 2:
			is_changed = not(self.window.screen_array[y][x2][1:] == [char, color_pair])
			if not is_changed:
				is_changed = self.window.screen_array[y][x2][0]
			self.window.screen_array[y][x2] = [is_changed, char, color_pair]


	def render(self):
		y1 = math.floor(self.y) if math.floor(self.y) > 0 else 0
		y2 = math.floor(self.y + self.height) if math.floor(self.y + self.height) < self.window.height - 2 else self.window.height - 2
		x1 = self.x if self.x > 0 else 0
		x2 = self.x + self.width - 1 if self.x + self.width - 1 < self.window.width - 2 else self.window.width - 2
		for y in range(y1, y2):
			if self.fill:
				self.draw_line(x1, x2, y, self.char, self.color_pair)
			else:
				self.draw_edge(x1, x2, y, self.char, self.color_pair)


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
		self.vertices = self.arrange_vertices(vertices)
		self.center = self.get_center(self.vertices)
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

	def arrange_vertices(self, vertices):
		return tuple(tuple(v) for v in sorted(list(vertices), key=lambda x: (x[1], x[0])))

	def get_center(self, vertices):
		vertices = sorted(list(vertices), key=lambda x: (x[0]))
		x = (vertices[0][0] + vertices[-1][0]) / 2
		vertices = sorted(list(vertices), key=lambda x: (x[1]))
		y = (vertices[0][1] + vertices[-1][1]) / 2
		return (x, y)


	def render(self):
		x1, y1 = self.vertices[0]
		x2, y2 = self.vertices[1]
		x3, y3 = self.vertices[2]
		if y1 == y2 and y2 == y3:
			cur_x1 = min(x1, x2, x3) if min(x1, x2, x3) > 0 else 0
			cur_x2 = max(x1, x2, x3) if max(x1, x2, x3) < self.window.width - 2 else self.window.width - 2
			if self.fill:
				self.draw_line(cur_x1, cur_x2, y1, self.char, self.color_pair)
			else:
				self.draw_edge(cur_x1, cur_x2, y1, self.char, self.color_pair)
		elif y2 == y3:
			self.fill_flat_bottom_triangle(x1, y1, x2, y2, x3, y3, self.char, self.color_pair)
		elif y1 == y2:
			self.fill_flat_top_triangle(x1, y1, x2, y2, x3, y3, self.char, self.color_pair)
		else:
			x4 = x1 + (y2 - y1) / (y3 - y1) * (x3 - x1)
			y4 = y2
			self.fill_flat_bottom_triangle(x1, y1, x2, y2, x4, y4, self.char, self.color_pair)
			self.fill_flat_top_triangle(x2, y2, x4, y4, x3, y3, self.char, self.color_pair)


	def draw_line(self, x1, x2, y, char, color_pair):
		y = math.floor(y)
		if x1 > x2:
			x1, x2 = x2, x1
		for x in range(math.floor(x1), math.floor(x2) + 1):
			if 0 <= x <= self.window.width - 2 and 0 <= y <= self.window.height - 2:
				is_changed = not(self.window.screen_array[y][x][1:] == [char, color_pair])
				if not is_changed:
					is_changed = self.window.screen_array[y][x][0]
				self.window.screen_array[y][x] = [is_changed, char, color_pair]

	def draw_edge(self, x1, x2, y, char, color_pair):
		y = math.floor(y)
		x1 = math.floor(x1)
		x2 = math.floor(x2)
		if 0 <= x1 <= self.window.width - 2 and 0 <= y <= self.window.height - 2:
			is_changed = not(self.window.screen_array[y][x1][1:] == [char, color_pair])
			if not is_changed:
				is_changed = self.window.screen_array[y][x1][0]
			self.window.screen_array[y][x1] = [is_changed, char, color_pair]
		if 0 <= x2 <= self.window.width - 2 and 0 <= y <= self.window.height - 2:
			is_changed = not(self.window.screen_array[y][x2][1:] == [char, color_pair])
			if not is_changed:
				is_changed = self.window.screen_array[y][x2][0]
			self.window.screen_array[y][x2] = [is_changed, char, color_pair]


	def fill_flat_bottom_triangle(self, x1, y1, x2, y2, x3, y3, char, color_pair):
		dx_1 = (x2 - x1) / (y2 - y1)
		dx_2 = (x3 - x1) / (y3 - y1)
		cur_x1 = x1
		cur_x2 = x1
		is_cur_x1_outside = False
		is_cur_x2_outside = False
		if y1 < 0:
			y1 = 0
		elif y1 > self.window.height - 2:
			y1 = self.window.height - 2
		if y2 < 0:
			y2 = 0
		elif y2 > self.window.height - 2:
			y2 = self.window.height - 2
		for y in range(math.floor(y1), math.floor(y2) + 1):
			if self.fill:
				self.draw_line(cur_x1, cur_x2, y, char, color_pair)
			else:
				self.draw_edge(cur_x1, cur_x2, y, char, color_pair)
			if not is_cur_x1_outside:
				cur_x1 += dx_1
			if not is_cur_x2_outside:
				cur_x2 += dx_2
			if cur_x1 > self.window.width - 2:
				cur_x1 = self.window.width - 2
				is_cur_x1_outside = True
			elif cur_x1 < 0:
				cur_x1 = 0
				is_cur_x1_outside = True
			if cur_x2 > self.window.width - 2:
				cur_x2 = self.window.width - 2
				is_cur_x2_outside = True
			elif cur_x2 < 0:
				cur_x2 = 0
				is_cur_x2_outside = True

	def fill_flat_top_triangle(self, x1, y1, x2, y2, x3, y3, char, color_pair):
		dx_1 = (x3 - x1) / (y3 - y1)
		dx_2 = (x3 - x2) / (y3 - y2)
		cur_x1 = x3
		cur_x2 = x3
		is_cur_x1_outside = False
		is_cur_x2_outside = False
		if y1 < 0:
			y1 = 0
		elif y1 > self.window.height - 2:
			y1 = self.window.height - 2
		if y3 < 0:
			y3 = 0
		elif y3 > self.window.height - 2:
			y3 = self.window.height - 2
		for y in range(math.floor(y3), math.floor(y1), -1):
			if self.fill:
				self.draw_line(cur_x1, cur_x2, y, char, color_pair)
			else:
				self.draw_edge(cur_x1, cur_x2, y, char, color_pair)
			if not is_cur_x1_outside:
				cur_x1 -= dx_1
			if not is_cur_x2_outside:
				cur_x2 -= dx_2
			if cur_x1 > self.window.width - 2:
				cur_x1 = self.window.width - 2
				is_cur_x1_outside = True
			elif cur_x1 < 0:
				cur_x1 = 0
				is_cur_x1_outside = True
			if cur_x2 > self.window.width - 2:
				cur_x2 = self.window.width - 2
				is_cur_x2_outside = True
			elif cur_x2 < 0:
				cur_x2 = 0
				is_cur_x2_outside = True

	def update(self, dt):
		self.unrender()
		new_vertices = []
		for x, y in self.vertices:
			new_vertices.append((x + self.direction[0] * self.speed[0] * dt, y + self.direction[1] * self.speed[1] * dt))
		self.center = tuple(self.center[i] + self.direction[i] * self.speed[i] * dt for i in range(len(self.center)))
		self.vertices = tuple(new_vertices)
		self.check_bounds()

	def check_bounds(self):
		pass


	def unrender(self):
		x1, y1 = self.vertices[0]
		x2, y2 = self.vertices[1]
		x3, y3 = self.vertices[2]
		if y1 == y2 and y2 == y3:
			cur_x1 = min(x1, x2, x3) if min(x1, x2, x3) > 0 else 0
			cur_x2 = max(x1, x2, x3) if max(x1, x2, x3) < self.window.width - 2 else self.window.width - 2
			if self.fill:
				self.draw_line(cur_x1, cur_x2, y1, self.window.char, self.window.color_pair)
			else:
				self.draw_edge(cur_x1, cur_x2, y1, self.window.char, self.window.color_pair)
		elif y2 == y3:
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

	def rotate(self, dt, angle, point=None, clockwise=False):
		self.unrender()
		angle *= dt
		in_place = False
		if point == None:
			point = self.center
			in_place = True
		new_vertices = []
		for v in self.vertices:
			if clockwise:
				x = math.cos(angle) * (v[0] - point[0]) - math.sin(angle) * (v[1] - point[1]) + point[0]
				y = math.sin(angle) * (v[0] - point[0]) + math.cos(angle) * (v[1] - point[1]) + point[1]
			else:
				x = math.cos(angle) * (v[0] - point[0]) + math.sin(angle) * (v[1] - point[1]) + point[0]
				y = -math.sin(angle) * (v[0] - point[0]) + math.cos(angle) * (v[1] - point[1]) + point[1]
			new_vertices.append((x, y))
		self.vertices = self.arrange_vertices(new_vertices)
		if not in_place:
			self.center = self.get_center(self.vertices)



	def update_shape(self, **kwargs):
		self.unrender()
		self.vertices = self.arrange_vertices(kwargs.get("vertices", self.vertices))
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
		self.edges = self.arrange_edges(self.vertices)
		self.center = self.get_center(self.vertices)
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

	def arrange_edges(self, vertices):
		return tuple(sorted([tuple(sorted([vertices[v], vertices[(v + 1) % len(vertices)]], key=lambda v: v[1])) 
			for v in range(len(vertices))], key=lambda e: min(e[0][1], e[1][1])))

	def get_center(self, vertices):
		vertices = sorted(list(vertices), key=lambda x: (x[0]))
		x = (vertices[0][0] + vertices[-1][0]) / 2
		vertices = sorted(list(vertices), key=lambda x: (x[1]))
		y = (vertices[0][1] + vertices[-1][1]) / 2
		return (x, y)


	def render(self):
		for y in range(math.floor(self.edges[0][0][1]), math.floor(self.edges[-1][1][1]) + 1):
			intersections = []
			intersected_edges = {}
			for e in self.edges:
				if e[0][1] <= y <= e[1][1]:
					if e[0][1] != e[1][1]:
						dx = (e[1][0] - e[0][0]) / (e[1][1] - e[0][1]) * (y - e[0][1])
						x = math.floor(e[0][0] + dx)
						intersected_edge = intersected_edges.get(x, False)
						if intersected_edge:
							if (intersected_edge[1][1] > y and e[1][1] > y) or (intersected_edge[0][1] < y and e[0][1] < y):
								intersections.append(x)
						else:
							intersected_edges[x] = e
							intersections.append(x)
					else:
						x = sorted([e[0][0], e[1][0]])
						self.draw_line(x[0], x[1], y, self.char, self.color_pair)

			intersections.sort()
			for i in range(0, len(intersections), 2):
				if self.fill:
					self.draw_line(intersections[i], intersections[i + 1], y, self.char, self.color_pair)
				else:
					self.draw_edge(intersections[i], intersections[i + 1], y, self.char, self.color_pair)

	def draw_line(self, x1, x2, y, char, color_pair):
		y = math.floor(y)
		if x1 > x2:
			x1, x2 = x2, x1
		for x in range(math.floor(x1), math.floor(x2) + 1):
			if 0 <= x <= self.window.width - 2 and 0 <= y <= self.window.height - 2:
				is_changed = not(self.window.screen_array[y][x][1:] == [char, color_pair])
				if not is_changed:
					is_changed = self.window.screen_array[y][x][0]
				self.window.screen_array[y][x] = [is_changed, char, color_pair]

	def draw_edge(self, x1, x2, y, char, color_pair):
		y = math.floor(y)
		x1 = math.floor(x1)
		x2 = math.floor(x2)
		if 0 <= x1 <= self.window.width - 2 and 0 <= y <= self.window.height - 2:
			is_changed = not(self.window.screen_array[y][x1][1:] == [char, color_pair])
			if not is_changed:
				is_changed = self.window.screen_array[y][x1][0]
			self.window.screen_array[y][x1] = [is_changed, char, color_pair]
		if 0 <= x2 <= self.window.width - 2 and 0 <= y <= self.window.height - 2:
			is_changed = not(self.window.screen_array[y][x2][1:] == [char, color_pair])
			if not is_changed:
				is_changed = self.window.screen_array[y][x2][0]
			self.window.screen_array[y][x2] = [is_changed, char, color_pair]

	def update(self, dt):
		self.unrender()
		new_vertices = []
		for x, y in self.vertices:
			new_vertices.append((x + self.direction[0] * self.speed[0] * dt, y + self.direction[1] * self.speed[1] * dt))
		self.center = tuple(self.center[i] + self.direction[i] * self.speed[i] * dt for i in range(len(self.center)))
		self.vertices = tuple(new_vertices)
		self.edges = self.arrange_edges(self.vertices)
		self.check_bounds()

	def check_bounds(self):
		pass

	def unrender(self):
		for y in range(math.floor(self.edges[0][0][1]), math.floor(self.edges[-1][1][1]) + 1):
			intersections = []
			intersected_edges = {}
			for e in self.edges:
				if e[0][1] <= y <= e[1][1]:
					if e[0][1] != e[1][1]:
						dx = (e[1][0] - e[0][0]) / (e[1][1] - e[0][1]) * (y - e[0][1])
						x = math.floor(e[0][0] + dx)
						intersected_edge = intersected_edges.get(x, False)
						if intersected_edge:
							if (intersected_edge[1][1] > y and e[1][1] > y) or (intersected_edge[0][1] < y and e[0][1] < y):
								intersections.append(x)
						else:
							intersected_edges[x] = e
							intersections.append(x)
					else:
						x = sorted([e[0][0], e[1][0]])
						self.draw_line(x[0], x[1], y, self.window.char, self.window.color_pair)

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

	def rotate(self, dt, angle, point=None, clockwise=False):
		self.unrender()
		angle *= dt
		in_place = False
		if point == None:
			point = self.center
			in_place = True
		new_vertices = []
		for v in self.vertices:
			if clockwise:
				x = math.cos(angle) * (v[0] - point[0]) - math.sin(angle) * (v[1] - point[1]) + point[0]
				y = math.sin(angle) * (v[0] - point[0]) + math.cos(angle) * (v[1] - point[1]) + point[1]
			else:
				x = math.cos(angle) * (v[0] - point[0]) + math.sin(angle) * (v[1] - point[1]) + point[0]
				y = -math.sin(angle) * (v[0] - point[0]) + math.cos(angle) * (v[1] - point[1]) + point[1]
			new_vertices.append((x, y))
		self.vertices = tuple(new_vertices)
		self.edges = self.arrange_edges(self.vertices)
		if not in_place:
			self.center = self.get_center(self.vertices)

	def update_shape(self, **kwargs):
		self.unrender()
		self.vertices = tuple(tuple(v) for v in kwargs.get("vertices", self.vertices))
		self.edges = self.arrange_edges(self.vertices)
		self.center = self.get_center(self.vertices)
		self.char = kwargs.get("char", self.char)
		self.fill = kwargs.get("fill", self.fill)
		color_pair = kwargs.get("color_pair", self.color_pair)
		if color_pair != None:
			self.color_pair = tuple(color_pair)
		else:
			self.color_pair = color_pair
		

class Circle:
	def __init__(self, window, center=(0, 0), radius=1, direction=(0, 0), speed=(0, 0), char="*", fill=True, color_pair=None, group=None):
		self.window = window
		self.center = tuple(center)
		self.radius = radius
		self.speed = tuple(speed)
		self.direction = tuple(direction)
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
		self.center = tuple(self.center[i] + self.direction[i] * self.speed[i] * dt for i in range(len(self.center)))
		self.check_bounds()

	def check_bounds(self):
		pass

	def unrender(self):
		x = self.center[0]
		y = self.center[1]
		rx, ry = (self.radius * 2, self.radius) 
		p = 0
		q = ry
		d1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)
		dx = 2 * ry * ry * p
		dy = 2 * rx * rx * q

		while dx < dy:
			cur_x1 = x - p if x - p > 0 else 0
			cur_x2 = x + p if x + p < self.window.width - 2 else self.window.width - 2
			if self.fill:
				self.draw_line(cur_x1, cur_x2, y + q, self.window.char, self.window.color_pair)
				self.draw_line(cur_x1, cur_x2, y - q, self.window.char, self.window.color_pair)
			else:
				self.draw_edge(cur_x1, cur_x2, y + q, self.window.char, self.window.color_pair)
				self.draw_edge(cur_x1, cur_x2, y - q, self.window.char, self.window.color_pair)
			if d1 < 0:
				p += 1
				dx += 2 * ry * ry
				d1 += dx + ry * ry
			else:
				p += 1
				q -= 1
				dx += 2 * ry * ry
				dy -= 2 * rx * rx
				d1 += dx - dy + ry * ry

		d2 = ((ry * ry) * ((p + 0.5) * (p + 0.5))) + ((rx * rx) * ((q - 1) * (q - 1))) - (rx * rx * ry * ry)
		
		while q >= 0:
			cur_x1 = x - p if x - p > 0 else 0
			cur_x2 = x + p if x + p < self.window.width - 2 else self.window.width - 2
			if self.fill:
				self.draw_line(cur_x1, cur_x2, y + q, self.window.char, self.window.color_pair)
				self.draw_line(cur_x1, cur_x2, y - q, self.window.char, self.window.color_pair)
			else:
				self.draw_edge(cur_x1, cur_x2, y + q, self.window.char, self.window.color_pair)
				self.draw_edge(cur_x1, cur_x2, y - q, self.window.char, self.window.color_pair)
			if d2 > 0:
				q -= 1
				dy -= 2 * rx * rx
				d2 += rx * rx - dy
			else:
				p += 1
				q -= 1
				dx += 2 * ry * ry
				dy -= 2 * rx * rx
				d2 += dx - dy + rx * rx

	def render(self):
		x = self.center[0]
		y = self.center[1]
		rx, ry = (self.radius * 2, self.radius) 
		p = 0
		q = ry
		d1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)
		dx = 2 * ry * ry * p
		dy = 2 * rx * rx * q

		while dx < dy:
			cur_x1 = x - p if x - p > 0 else 0
			cur_x2 = x + p if x + p < self.window.width - 2 else self.window.width - 2
			if self.fill:
				self.draw_line(cur_x1, cur_x2, y + q, self.char, self.color_pair)
				self.draw_line(cur_x1, cur_x2, y - q, self.char, self.color_pair)
			else:
				self.draw_edge(cur_x1, cur_x2, y + q, self.char, self.color_pair)
				self.draw_edge(cur_x1, cur_x2, y - q, self.char, self.color_pair)
			if d1 < 0:
				p += 1
				dx += 2 * ry * ry
				d1 += dx + ry * ry
			else:
				p += 1
				q -= 1
				dx += 2 * ry * ry
				dy -= 2 * rx * rx
				d1 += dx - dy + ry * ry

		d2 = ((ry * ry) * ((p + 0.5) * (p + 0.5))) + ((rx * rx) * ((q - 1) * (q - 1))) - (rx * rx * ry * ry)
		
		while q >= 0:
			cur_x1 = x - p if x - p > 0 else 0
			cur_x2 = x + p if x + p < self.window.width - 2 else self.window.width - 2
			if self.fill:
				self.draw_line(cur_x1, cur_x2, y + q, self.char, self.color_pair)
				self.draw_line(cur_x1, cur_x2, y - q, self.char, self.color_pair)
			else:
				self.draw_edge(cur_x1, cur_x2, y + q, self.char, self.color_pair)
				self.draw_edge(cur_x1, cur_x2, y - q, self.char, self.color_pair)
			if d2 > 0:
				q -= 1
				dy -= 2 * rx * rx
				d2 += rx * rx - dy
			else:
				p += 1
				q -= 1
				dx += 2 * ry * ry
				dy -= 2 * rx * rx
				d2 += dx - dy + rx * rx
				
	def draw_line(self, x1, x2, y, char, color_pair):
		y = math.floor(y)
		if x1 > x2:
			x1, x2 = x2, x1
		for x in range(math.floor(x1), math.floor(x2) + 1):
			if 0 <= x <= self.window.width - 2 and 0 <= y <= self.window.height - 2:
				is_changed = not(self.window.screen_array[y][x][1:] == [char, color_pair])
				if not is_changed:
					is_changed = self.window.screen_array[y][x][0]
				self.window.screen_array[y][x] = [is_changed, char, color_pair]

	def draw_edge(self, x1, x2, y, char, color_pair):
		y = math.floor(y)
		x1 = math.floor(x1)
		x2 = math.floor(x2)
		if 0 <= x1 <= self.window.width - 2 and 0 <= y <= self.window.height - 2:
			is_changed = not(self.window.screen_array[y][x1][1:] == [char, color_pair])
			if not is_changed:
				is_changed = self.window.screen_array[y][x1][0]
			self.window.screen_array[y][x1] = [is_changed, char, color_pair]
		if 0 <= x2 <= self.window.width - 2 and 0 <= y <= self.window.height - 2:
			is_changed = not(self.window.screen_array[y][x2][1:] == [char, color_pair])
			if not is_changed:
				is_changed = self.window.screen_array[y][x2][0]
			self.window.screen_array[y][x2] = [is_changed, char, color_pair]

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
	def __init__(self, window, center=(0, 0), radius=(1, 1), direction=(0, 0), speed=(0, 0), char="*", fill=True, color_pair=None, group=None):
		self.window = window
		self.center = tuple(center)
		self.radius = tuple(radius)
		self.speed = tuple(speed)
		self.direction = tuple(direction)
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
		self.center = tuple(self.center[i] + self.direction[i] * self.speed[i] * dt for i in range(len(self.center)))
		self.check_bounds()

	def check_bounds(self):
		pass

	def unrender(self):
		x = self.center[0]
		y = self.center[1]
		rx, ry = self.radius
		p = 0
		q = ry
		d1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)
		dx = 2 * ry * ry * p
		dy = 2 * rx * rx * q

		while dx < dy:
			cur_x1 = x - p if x - p > 0 else 0
			cur_x2 = x + p if x + p < self.window.width - 2 else self.window.width - 2
			if self.fill:
				self.draw_line(cur_x1, cur_x2, y + q, self.window.char, self.window.color_pair)
				self.draw_line(cur_x1, cur_x2, y - q, self.window.char, self.window.color_pair)
			else:
				self.draw_edge(cur_x1, cur_x2, y + q, self.window.char, self.window.color_pair)
				self.draw_edge(cur_x1, cur_x2, y - q, self.window.char, self.window.color_pair)
			if d1 < 0:
				p += 1
				dx += 2 * ry * ry
				d1 += dx + ry * ry
			else:
				p += 1
				q -= 1
				dx += 2 * ry * ry
				dy -= 2 * rx * rx
				d1 += dx - dy + ry * ry

		d2 = ((ry * ry) * ((p + 0.5) * (p + 0.5))) + ((rx * rx) * ((q - 1) * (q - 1))) - (rx * rx * ry * ry)
		
		while q >= 0:
			cur_x1 = x - p if x - p > 0 else 0
			cur_x2 = x + p if x + p < self.window.width - 2 else self.window.width - 2
			if self.fill:
				self.draw_line(cur_x1, cur_x2, y + q, self.window.char, self.window.color_pair)
				self.draw_line(cur_x1, cur_x2, y - q, self.window.char, self.window.color_pair)
			else:
				self.draw_edge(cur_x1, cur_x2, y + q, self.window.char, self.window.color_pair)
				self.draw_edge(cur_x1, cur_x2, y - q, self.window.char, self.window.color_pair)
			if d2 > 0:
				q -= 1
				dy -= 2 * rx * rx
				d2 += rx * rx - dy
			else:
				p += 1
				q -= 1
				dx += 2 * ry * ry
				dy -= 2 * rx * rx
				d2 += dx - dy + rx * rx


	def render(self):
		x = self.center[0]
		y = self.center[1]
		rx, ry = self.radius
		p = 0
		q = ry
		d1 = (ry * ry) - (rx * rx * ry) + (0.25 * rx * rx)
		dx = 2 * ry * ry * p
		dy = 2 * rx * rx * q

		while dx < dy:
			cur_x1 = x - p if x - p > 0 else 0
			cur_x2 = x + p if x + p < self.window.width - 2 else self.window.width - 2
			if self.fill:
				self.draw_line(cur_x1, cur_x2, y + q, self.char, self.color_pair)
				self.draw_line(cur_x1, cur_x2, y - q, self.char, self.color_pair)
			else:
				self.draw_edge(cur_x1, cur_x2, y + q, self.char, self.color_pair)
				self.draw_edge(cur_x1, cur_x2, y - q, self.char, self.color_pair)
			if d1 < 0:
				p += 1
				dx += 2 * ry * ry
				d1 += dx + ry * ry
			else:
				p += 1
				q -= 1
				dx += 2 * ry * ry
				dy -= 2 * rx * rx
				d1 += dx - dy + ry * ry

		d2 = ((ry * ry) * ((p + 0.5) * (p + 0.5))) + ((rx * rx) * ((q - 1) * (q - 1))) - (rx * rx * ry * ry)
		
		while q >= 0:
			cur_x1 = x - p if x - p > 0 else 0
			cur_x2 = x + p if x + p < self.window.width - 2 else self.window.width - 2
			if self.fill:
				self.draw_line(cur_x1, cur_x2, y + q, self.char, self.color_pair)
				self.draw_line(cur_x1, cur_x2, y - q, self.char, self.color_pair)
			else:
				self.draw_edge(cur_x1, cur_x2, y + q, self.char, self.color_pair)
				self.draw_edge(cur_x1, cur_x2, y - q, self.char, self.color_pair)
			if d2 > 0:
				q -= 1
				dy -= 2 * rx * rx
				d2 += rx * rx - dy
			else:
				p += 1
				q -= 1
				dx += 2 * ry * ry
				dy -= 2 * rx * rx
				d2 += dx - dy + rx * rx
				
	def draw_line(self, x1, x2, y, char, color_pair):
		y = math.floor(y)
		if x1 > x2:
			x1, x2 = x2, x1
		for x in range(math.floor(x1), math.floor(x2) + 1):
			if 0 <= x <= self.window.width - 2 and 0 <= y <= self.window.height - 2:
				is_changed = not(self.window.screen_array[y][x][1:] == [char, color_pair])
				if not is_changed:
					is_changed = self.window.screen_array[y][x][0]
				self.window.screen_array[y][x] = [is_changed, char, color_pair]

	def draw_edge(self, x1, x2, y, char, color_pair):
		y = math.floor(y)
		x1 = math.floor(x1)
		x2 = math.floor(x2)
		if 0 <= x1 <= self.window.width - 2 and 0 <= y <= self.window.height - 2:
			is_changed = not(self.window.screen_array[y][x1][1:] == [char, color_pair])
			if not is_changed:
				is_changed = self.window.screen_array[y][x1][0]
			self.window.screen_array[y][x1] = [is_changed, char, color_pair]
		if 0 <= x2 <= self.window.width - 2 and 0 <= y <= self.window.height - 2:
			is_changed = not(self.window.screen_array[y][x2][1:] == [char, color_pair])
			if not is_changed:
				is_changed = self.window.screen_array[y][x2][0]
			self.window.screen_array[y][x2] = [is_changed, char, color_pair]

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
		self.radius = tuple(kwargs.get("radius", self.radius))
		self.char = kwargs.get("char", self.char)
		self.fill = kwargs.get("fill", self.fill)
		color_pair = kwargs.get("color_pair", self.color_pair)
		if color_pair != None:
			self.color_pair = tuple(color_pair)
		else:
			self.color_pair = color_pair

