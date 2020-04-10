import sys, os, time, random, curses

# warning: hard-coded shit below: 
sys.path.append(sys.path[0] + "/../..") # cause main.py is two directories away from the clingine package


import clingine
from engine import player_obj, asteroid, button
from pynput import keyboard

class GameWindow(clingine.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.title = clingine.label.Label(window=self, text="< == SPACE == >", x=self.width // 2, y=15, anchor="center")
		buttons_text = ["PLAY", "HELP", "QUIT"]
		self.buttons = [button.Button(window=self, text=txt, x=self.width // 2, y=20 + idx, anchor="center") 
			for idx, txt in enumerate(buttons_text)]
		self.buttons[0].active = True
		self.player = player_obj.Player(window=self, x=self.width // 2, y=self.height - 4, direction=(0, 0), speed=(2, 1), 
			image=clingine.util.load_image("resources/spaceship.txt"))
		asteroid_img = clingine.util.load_image("resources/obstacles.txt")
		self.asteroids = [asteroid.Asteroid(window=self, x=random.randrange(1, self.width - 1 - asteroid_img.width), 
			y=random.randrange(-asteroid_img.height - 20, -asteroid_img.height),
			direction=(0, 1), speed=(0, 1), image=asteroid_img) for i in range(4)]
		self.score = clingine.label.Label(window=self, text="SCORE: {}".format(self.player.score), x=0, y=self.height - 2)

		self.cursor = 0

	# overwritten on_press method of the Window class (see the clingine.window.Window class)
	def on_press(self, key):
		try:
			key = key.char
		except:
			key = key.name
		if self.player.state == "dead":
			if key == "up":
				self.buttons[self.cursor].active = False
				self.buttons[self.cursor].update()
				self.cursor -= 1
			if key == "down":
				self.buttons[self.cursor].active = False
				self.buttons[self.cursor].update()
				self.cursor += 1

			if (key == "space" or key == "enter") and "PLAY" in self.buttons[self.cursor].text:
				self.reset()
				self.buttons[1].active_help = False
				self.player.state = "alive"
				self.cursor = 0
				self.player.score = 0
				self.buttons[self.cursor].active_help = False

			if (key == "space" or key == "enter") and "HELP" in self.buttons[self.cursor].text:
				self.buttons[self.cursor].active_help = not self.buttons[self.cursor].active_help
				self.buttons[self.cursor].toggle_help()

			if (key == "space" or key == "enter") and "QUIT" in self.buttons[self.cursor].text:
				self.exit()

			if self.cursor < 0:
				self.cursor = len(self.buttons) - 1
			if self.cursor > len(self.buttons) - 1:
				self.cursor = 0
			self.buttons[self.cursor].active = True
			self.buttons[self.cursor].update()

		else:
			if key == "shift":
				self.player.speed = (6, 3)
			if key == "up":
				self.player.direction = (self.player.direction[0], -1)
			if key == "down":
				self.player.direction = (self.player.direction[0], 1)
			if key == "right":
				self.player.direction = (1, self.player.direction[1])
			if key == "left":
				self.player.direction = (-1, self.player.direction[1])

	# overwritten on_release method of the Window class
	def on_release(self, key):
		if self.player.state == "alive":
			try:
				key = key.char
			except:
				key = key.name
			if key == "shift":
				self.player.speed = self.player.init_speed

			if key == "up" or key == "down":
				self.player.direction = (self.player.direction[0], 0)
			if key == "left" or key == "right":
				self.player.direction = (0, self.player.direction[1])

	def run(self, stdscr):
		self.fill(stdscr, "black")
		while self.running:
			self.score.text = "SCORE: {}".format(self.player.score)
			self.score.update()
			self.score.render()
			if self.player.state == "dead":
				self.title.render()
				for btn in self.buttons:
					btn.update()
					btn.render()
			else:
				self.player.update()
				self.player.render()
				for ast in self.asteroids:
					ast.update()
					if self.player.state == "dead":
						self.reset()
						break
					ast.render()

			self.draw(stdscr)
			stdscr.refresh()
			self.tick(self.fps)

		return
			

if __name__ == "__main__":
	window = GameWindow(width=130, height=50, char=" ", fps=60)
	window.start(window.run)
