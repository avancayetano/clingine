import clingine

class Button(clingine.label.Label):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.active = False
		self.init_text = self.text
		self.active_help = False

	def update(self):
		if self.active:
			self.text = "> {}".format(self.init_text)
		else:
			self.unrender()
			self.text = self.init_text

	def toggle_help(self):
		text = "Arrow Keys - Controls | Shift - Boost | Space - Shoot"
		if len(text) % 2 != 0:
			text += " "
		if self.active_help:
			self.window.screen[self.window.height - 7][self.x - len(text) // 2: self.x + len(text) // 2] = list(text)
		else:
			self.window.screen[self.window.height - 7][self.x - len(text) // 2: self.x + len(text) // 2] = list(self.window.char * len(text))