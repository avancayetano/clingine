import sys, random
sys.path.append(sys.path[0] + "/../..") # cause main.py is two directories away from the clingine package

import clingine
class GameWindow(clingine.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rects = []

	def run(self):
		while self.running:
			dt = self.clock.get_dt()
			clicked = self.mouse.get_clicked()
			pressed = self.keyboard.get_pressed()


			if "q" in pressed:
				self.exit()

			if clicked and clicked.button == 1:
				clingine.shapes.Rect(self, x=clicked.x, y=clicked.y, width=4, height=2, direction=(0, 0), speed=(0, 0), 
					char="#", color_pair=((255, 255, 255),(0, 0, 0)), group=self.rects)
			# print(len(self.rects))


			for rect in self.rects:
				rect.update(dt)
				rect.render()


			self.update(self.fps)
		return

if __name__ == "__main__":
	window = GameWindow(width=130, height=50, fps=60)
	window.start(window.run)