import sys
sys.path.append(sys.path[0] + "/..")

import clingine

class GameWindow(clingine.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.triangle = clingine.shapes.Triangle(self, fill=True, speed=(30, 20), direction=(1, 0), vertices=((self.width / 2.7, 2.11312 * self.height / 3.123123), (self.width / 2.123123, self.height / 3), (2 * self.width / 3, 2 * self.height / 3)))

	def run(self):
		import math
		angle = math.pi / 1.2
		while self.running:
			dt = self.clock.get_dt()
			clicked = self.mouse.get_clicked()
			pressed = self.keyboard.get_pressed()

			if "q" in pressed:
				self.exit()

			self.triangle.update(dt)
			self.triangle.render()

			self.update(self.fps)
		return

if __name__ == "__main__":
	window = GameWindow(width=130, height=50, fps=60)
	window.start(window.run)