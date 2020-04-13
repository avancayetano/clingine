import math
class Label:
	def __init__(self, window, text=[""], x=0, y=0, anchor="left", color_pair=None, group=None):
		self.window = window
		self.text = text

		self.x = x
		self.y = y
		self.anchor = anchor
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
			for idx in range(len(self.text)):
				line = self.text[idx]
				self.window.screen_array[self.y + idx][self.x - (len(line) - 1) // 2: self.x + math.ceil((len(line) + 1) / 2)] = [
					[i != self.window.char, self.window.char, None] for i in line]
		elif self.anchor == "left":
			for idx	in range((len(self.text))):
				line = self.text[idx]
				self.window.screen_array[self.y + idx][self.x: self.x + len(line)] = [
					[i != self.window.char, self.window.char, None] for i in line]


	def render(self):
		if self.anchor == "center":
			for idx in range(len(self.text)):
				line = self.text[idx]
				self.window.screen_array[self.y + idx][self.x - (len(line) - 1) // 2: self.x + math.ceil((len(line) + 1) / 2)] = [
					[self.window.screen_array[self.y + idx][self.x - (len(line) - 1) // 2 + i][0] != char, char, self.color_pair] for i, char in enumerate(line)]
		elif self.anchor == "left":
			for idx in range(len(self.text)):
				line = self.text[idx]
				self.window.screen_array[self.y + idx][self.x: self.x + len(line)] = [
					[self.window.screen_array[self.y + idx][self.x + i] != char, char, self.color_pair] for i, char in enumerate(line)]

	def destroy(self):
		self.unrender()
		if self.group:
			self.group.remove(self)
