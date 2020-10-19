

# this example is in the same directory as clingine


import clingine
class GameWindow(clingine.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rect_obj = clingine.shapes.Rect(self, x=0, y=0, width=10, height=5, direction=(0, 0), speed=(100, 60), char="#", color_pair=((255, 255, 255),(0, 0, 0)))

	def run(self):
		while self.running:
			dt = self.clock.get_dt()
			pressed_keys = self.keyboard.get_pressed()

			if "q" in pressed_keys:
				self.exit()
			# game logic here
			self.rect_obj.update(dt)
			self.rect_obj.render()
			self.update(self.fps)
		return

if __name__ == "__main__":
	window = GameWindow(width=130, height=50, fps=60)
	window.start(window.run)