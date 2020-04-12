import clingine

class Button(clingine.label.Label):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.active = False
		self.init_text = tuple(self.text)

	def update(self):
		if self.active:
			for idx in range(len(self.text)):
				self.text[idx] = "> {}".format(self.init_text[idx])
		else:
			self.unrender()
			for idx in range(len(self.text)):
				self.text[idx] = self.init_text[idx]
