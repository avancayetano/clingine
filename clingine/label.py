import math
class Label:
	def __init__(self, window, text=[""], x=0, y=0, anchor="left", color_pair=None, group=None):
		self.window = window
		self.text = text

		self.x = x
		self.y = y
		self.anchor = anchor
		if color_pair != None:
			self.color_pair = tuple(color_pair)
		else:
			self.color_pair = color_pair
		self.group = group
		if type(self.group) == list:
			self.group.append(self)

	def update(self, new_text=None):
		self.unrender()
		if new_text:
			self.text = new_text[:]

	def unrender(self):
		if self.anchor == "center":
			for y in range(len(self.text)):
				line = self.text[y]
				for x in range(len(line)):
					if 0 <= math.floor(self.x) - (len(line) - 1) // 2 + x <= self.window.width - 2 and 0 <= math.floor(self.y) + y <= self.window.height - 2:
						is_changed = not(self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) - (len(line) - 1) // 2 + x][1:] == [self.window.char, self.window.color_pair])
						if not is_changed:
							is_changed = self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) - (len(line) - 1) // 2 + x][0]
						self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) - (len(line) - 1) // 2 + x] = [is_changed, self.window.char, self.window.color_pair]

		elif self.anchor == "left":
			for y in range(len(self.text)):
				line = self.text[y]
				for x in range(len(line)):
					if 0 <= math.floor(self.x) + x <= self.window.width - 2 and 0 <= math.floor(self.y) + y <= self.window.height - 2:
						is_changed = not(self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x][1:] == [self.window.char, self.window.color_pair])
						if not is_changed:
							is_changed = self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x][0]
						self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x] = [is_changed, self.window.char, self.window.color_pair]


	def render(self):
		if self.anchor == "center":
			for y in range(len(self.text)):
				line = self.text[y]
				for x in range(len(line)):
					if 0 <= math.floor(self.x) - (len(line) - 1) // 2 + x <= self.window.width - 2 and 0 <= math.floor(self.y) + y <= self.window.height - 2:
						is_changed = not(self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) - (len(line) - 1) // 2 + x][1:] == [line[x], self.color_pair])
						if not is_changed:
							is_changed = self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) - (len(line) - 1) // 2 + x][0]
						self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) - (len(line) - 1) // 2 + x] = [is_changed, line[x], self.color_pair]

		elif self.anchor == "left":
			for y in range(len(self.text)):
				line = self.text[y]
				for x in range(len(line)):
					if 0 <= math.floor(self.x) + x <= self.window.width - 2 and 0 <= math.floor(self.y) + y <= self.window.height - 2:
						is_changed = not(self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x][1:] == [line[x], self.color_pair])
						if not is_changed:
							is_changed = self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x][0]
						self.window.screen_array[math.floor(self.y) + y][math.floor(self.x) + x] = [is_changed, line[x], self.color_pair]

	def destroy(self):
		self.unrender()
		if self.group:
			self.group.remove(self)
