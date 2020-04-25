import sys, random
sys.path.append(sys.path[0] + "/../..") # cause main.py is two directories away from the clingine package

import clingine
class GameWindow(clingine.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.rects = [
		# 	clingine.shapes.Rect(self, x=0, y=0, width=self.width, height=1, char="#"),
		# 	clingine.shapes.Rect(self, x=0, y=self.height - 2, width=self.width, height=1, char="#"),
		# 	clingine.shapes.Rect(self, x=0, y=1, width=1, height=self.height - 3, char="#"),
		# 	clingine.shapes.Rect(self, x=self.width - 2, y=1, width=1, height=self.height - 3, char="#"),
		# ] # walls

		# self.player = clingine.shapes.Rect(self, x=self.width//2, y=self.height//2, width=10, height=10, direction=(0, 0), speed=(40, 20), 
		# 	char="o", color_pair=((255, 255, 255),(0, 0, 0)))

		# self.polygon = clingine.shapes.Polygon(self, vertices=((self.width // 2, 0), (1, self.height // 2), 
		# 	(self.width // 4, self.height - 2), (self.width - self.width // 4 - 1, self.height - 2), (self.width - 2, self.height // 2)), 
		# 	direction=(0, 0), speed=(10, 0), char="*", color_pair=((255, 255, 255), (0, 0, 0)))
		# def __init__(self, window, center=(0, 0), radius=1, char="*", fill=True, color_pair=None, group=None):
		# self.circle = clingine.shapes.Circle(self, center=(self.width // 2, 10), radius=5, direction=(1, 0), speed=(10, 0), fill=True, color_pair=((255, 255, 255), (0, 0, 0)))
		# self.triangle = clingine.shapes.Triangle(self, vertices=((0, 0), (self.width // 2, self.height), (self.width, 0)))
		# def __init__(self, window, vertices=(), direction=(0, 0), speed=(0, 0), char="*", fill=True, color_pair=None, group=None):
		# self.polygon = clingine.shapes.Polygon(self, vertices=((0, self.height - 2), (self.width // 5, 0), (self.width // 5 + 15, 0), 
		# 	(2 * self.width // 5, self.height - 2), (3 * self.width // 5, 0), (4 * self.width // 5, self.height - 2)), 
		# 	direction=(0, 0), speed=(0, 0), char="*", color_pair=((255, 255, 255), (0, 0, 0)))
		# def __init__(self, window, vertices=(), direction=(0, 0), speed=(0, 0), char="*", color_pair=None, group=None):
		# def __init__(self, window, center=(0, 0), radius=(1, 1), direction=(0, 0), speed=(0, 0), char="*", fill=True, color_pair=None, group=None):
		# self.ellipse = clingine.shapes.Ellipse(self, center=(self.width // 2, self.height - 12), radius=(20, 10), direction=(1, 0), speed=(10, 0))

	def run(self):
		import math
		angle = 0
		while self.running:
			dt = self.clock.get_dt()
			clicked = self.mouse.get_clicked()
			pressed = self.keyboard.get_pressed()
			# self.player.direction = (0, 0)
			# if "up" in pressed and not ("down" in pressed):
			# 	self.player.direction = (self.player.direction[0], -1)
			# if "down" in pressed and not ("up" in pressed):
			# 	self.player.direction = (self.player.direction[0], 1)
			# if "right" in pressed and not ("left" in pressed):
			# 	self.player.direction = (1, self.player.direction[1])
			# if "left" in pressed and not ("right" in pressed):
			# 	self.player.direction = (-1, self.player.direction[1])

			if "q" in pressed:
				self.exit()

			# if clicked and clicked.button == 1:
			# 	clingine.shapes.Rect(self, x=clicked.x, y=clicked.y, width=6, height=4, direction=(0, 0), speed=(0, 0), 
			# 		char="#", color_pair=((255, 255, 255),(0, 0, 0)), group=self.rects)

			# for rect in self.rects:
			# 	rect.update(dt)
			# 	rect.render()
			# self.polygon.update(dt)
			# self.polygon.rotate(dt, math.pi / 4, clockwise=True)
			# self.polygon.render()
			# self.triangle.update(dt)
			# self.triangle.rotate(dt, math.pi / 4)
			# print(self.triangle.center)
			# print(self.triangle.vertices)
			# self.triangle.render()


			self.update(self.fps)
		return

if __name__ == "__main__":
	window = GameWindow(width=130, height=50, fps=60)
	window.start(window.run)