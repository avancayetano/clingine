import sys, random
sys.path.append(sys.path[0] + "/../..") # cause main.py is two directories away from the clingine package

import clingine
class GameWindow(clingine.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rects = []
		self.player = clingine.shapes.Rect(self, x=self.width//2, y=self.height//2, width=1, height=1, direction=(0, 0), speed=(40, 20), 
			char="o", color_pair=((255, 255, 255),(0, 0, 0)))

	def run(self):
		while self.running:
			dt = self.clock.get_dt()
			clicked = self.mouse.get_clicked()
			pressed = self.keyboard.get_pressed()
			self.player.direction = (0, 0)
			if "up" in pressed and not ("down" in pressed):
				self.player.direction = (self.player.direction[0], -1)
			if "down" in pressed and not ("up" in pressed):
				self.player.direction = (self.player.direction[0], 1)
			if "right" in pressed and not ("left" in pressed):
				self.player.direction = (1, self.player.direction[1])
			if "left" in pressed and not ("right" in pressed):
				self.player.direction = (-1, self.player.direction[1])

			if "q" in pressed:
				self.exit()

			if clicked and clicked.button == 1:
				clingine.shapes.Rect(self, x=clicked.x, y=clicked.y, width=1, height=1, direction=(0, 0), speed=(0, 0), 
					char="#", color_pair=((255, 255, 255),(0, 0, 0)), group=self.rects)

			for rect in self.rects:
				rect.update(dt)
				rect.render()
			self.player.update(dt)
			self.player.render()
			self.update(self.fps)
		return

if __name__ == "__main__":
	window = GameWindow(width=130, height=50, fps=60)
	window.start(window.run)