class Label:
	def __init__(self, window, text="", x=0, y=0, anchor="left"):
		self.window = window
		self.text = text
		if len(self.text) % 2 != 0:
			self.text += " "
		self.x = x
		self.y = y
		self.anchor = anchor

	def update(self):
		self.unrender()

	def unrender(self):
		if self.anchor == "center":
			self.window.screen[self.y][self.x - len(self.text) // 2: self.x + len(self.text) // 2] = list(self.window.char * len(self.text))
		elif self.anchor == "left":
			self.window.screen[self.y][self.x: self.x + len(self.text)] = list(self.window.char * len(self.text))


	def render(self):
		if self.anchor == "center":
			self.window.screen[self.y][self.x - len(self.text) // 2: self.x + len(self.text) // 2] = list(self.text)
		elif self.anchor == "left":
			self.window.screen[self.y][self.x: self.x + len(self.text)] = list(self.text)
