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
					[not(self.window.screen_array[self.y + idx][self.x - (len(line) - 1) // 2 + i][1:] == [self.window.char, self.window.screen_color_pair])
						if not(self.window.screen_array[self.y + idx][self.x - (len(line) - 1) // 2 + i][1:] == [self.window.char, self.window.screen_color_pair])
						else self.window.screen_array[self.y + idx][self.x - (len(line) - 1) // 2 + i][0], # check if this point changed
						self.window.char, self.window.screen_color_pair] for i, c in enumerate(line)]
		elif self.anchor == "left":
			for idx	in range((len(self.text))):
				line = self.text[idx]
				self.window.screen_array[self.y + idx][self.x: self.x + len(line)] = [
					[not(self.window.screen_array[self.y + idx][self.x + i][1:] == [self.window.char, self.window.screen_color_pair])
						if not(self.window.screen_array[self.y + idx][self.x + i][1:] == [self.window.char, self.window.screen_color_pair])
						else self.window.screen_array[self.y + idx][self.x + i][0], # check if this point changed
						self.window.char, self.window.screen_color_pair] for i, c in enumerate(line)]


	def render(self):
		if self.anchor == "center":
			for idx in range(len(self.text)):
				line = self.text[idx]
				self.window.screen_array[self.y + idx][self.x - (len(line) - 1) // 2: self.x + math.ceil((len(line) + 1) / 2)] = [
					[not(self.window.screen_array[self.y + idx][self.x - (len(line) - 1) // 2 + i][1:] == [char, self.color_pair])
						if not(self.window.screen_array[self.y + idx][self.x - (len(line) - 1) // 2 + i][1:] == [char, self.color_pair])
						else self.window.screen_array[self.y + idx][self.x - (len(line) - 1) // 2 + i][0],  # check if this point changed
						char, self.color_pair] for i, char in enumerate(line)]
		elif self.anchor == "left":
			for idx in range(len(self.text)):
				line = self.text[idx]
				self.window.screen_array[self.y + idx][self.x: self.x + len(line)] = [
					[not(self.window.screen_array[self.y + idx][self.x + i][1:] == [char, self.color_pair])
						if not(self.window.screen_array[self.y + idx][self.x + i][1:] == [char, self.color_pair])
						else self.window.screen_array[self.y + idx][self.x + i][0],  # check if this point changed
						char, self.color_pair] for i, char in enumerate(line)]

	def destroy(self):
		self.unrender()
		if self.group:
			self.group.remove(self)
