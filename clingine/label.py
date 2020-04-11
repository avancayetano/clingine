class Label:
	def __init__(self, window, text="", x=0, y=0, anchor="left", color_pair=None):
		self.window = window
		self.text = text
		if len(self.text) % 2 != 0:
			self.text += " "
		self.x = x
		self.y = y
		self.anchor = anchor
		self.color_pair = color_pair

	def update(self):
		self.unrender()

	def unrender(self):
		if self.anchor == "center":
			self.window.screen_array[self.y][self.x - len(self.text) // 2: self.x + len(self.text) // 2] = [[self.window.char, None] for i in self.text]
		elif self.anchor == "left":
			self.window.screen_array[self.y][self.x: self.x + len(self.text)] = [[self.window.char, None] for i in self.text]


	def render(self):
		if self.anchor == "center":
			self.window.screen_array[self.y][self.x - len(self.text) // 2: self.x + len(self.text) // 2] = [[char, self.color_pair] for char in self.text]
		elif self.anchor == "left":
			self.window.screen_array[self.y][self.x: self.x + len(self.text)] = [[char, self.color_pair] for char in self.text]
