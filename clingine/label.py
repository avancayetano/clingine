class Label:
	def __init__(self, window, text="", x=0, y=0, anchor="left"):
		self.window = window
		self.text = text
		if len(self.text) % 2 != 0:
			self.text += " "
		self.x = x
		self.y = y
		self.anchor = anchor

	def update(self, new_text=None):
		self.unrender()
		if new_text:
			self.text = new_text

	def unrender(self):
		if self.anchor == "center":
			self.window.screen_array[self.y][self.x - len(self.text) // 2: self.x + len(self.text) // 2] = [
				[i != self.window.char, self.window.char, None] for i in self.text]
		elif self.anchor == "left":
			self.window.screen_array[self.y][self.x: self.x + len(self.text)] = [
				[i != self.window.char, self.window.char, None] for i in self.text]


	def render(self, color_pair=None):
		if self.anchor == "center":
			self.window.screen_array[self.y][self.x - len(self.text) // 2: self.x + len(self.text) // 2] = [
				[self.window.screen_array[self.y][self.x-len(self.text)//2+idx][0] != char, char, color_pair] for idx, char in enumerate(self.text)]
		elif self.anchor == "left":
			self.window.screen_array[self.y][self.x: self.x + len(self.text)] = [
				[self.window.screen_array[self.y][self.x+idx] != char, char, color_pair] for idx, char in enumerate(self.text)]
