import clingine

class Button(clingine.label.Label):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.active = False
		self.init_text = self.text

	def update(self):
		if self.active:
			self.text = "> {}".format(self.init_text)
		else:
			self.unrender()
			self.text = self.init_text
