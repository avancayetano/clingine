import sys, os, time, random, curses

# warning: hard-coded shit below: 
sys.path.append(sys.path[0] + "/../..") # cause main.py is two directories away from the clingine package


import clingine
from engine import player_obj, asteroid, button, star

class GameWindow(clingine.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.title = clingine.label.Label(window=self, text="< == SPACE == >", x=self.width // 2, y=15, anchor="center")
		self.help = clingine.label.Label(window=self, text="Arrow Keys - Controls | Shift - Boost | Space - Shoot",
			x=self.width // 2, y=self.height - 10, anchor="center")
		buttons_text = ["PLAY", "QUIT"]
		self.buttons = [button.Button(window=self, text=txt, x=self.width // 2, y=20 + idx, anchor="center") 
			for idx, txt in enumerate(buttons_text)]
		self.buttons[0].active = True
		
		self.player = player_obj.Player(window=self, x=self.width // 2, y=self.height - 4, direction=(0, 0), speed=(2, 1), 
			images=clingine.util.load_images("resources/spaceship/"))
		asteroid_imgs = clingine.util.load_images("resources/asteroid/")

		self.asteroids = [asteroid.Asteroid(window=self, x=random.randrange(1, self.width - 1 - asteroid_imgs[0].width), 
			y=random.randrange(-asteroid_imgs[0].height - 40, -asteroid_imgs[0].height),
			direction=(0, 1), speed=(0, 1), images=asteroid_imgs, image_num=random.randrange(len(asteroid_imgs))) for i in range(7)]

		self.score = clingine.label.Label(window=self, text="SCORE: {}".format(self.player.score), x=0, y=self.height - 2)
		self.bullets_left = clingine.label.Label(window=self, text="BULLETS LEFT: {}".format(self.player.bullets_count), x=0, y=self.height - 3)

		self.stars = [star.Star(window=self, x=random.randrange(0, self.width - 1), width=1, height=1, 
			y=random.randrange(self.height - 1), direction=(0, 1), speed=(0, 1)) for i in range(20)]

		self.cursor = 0


	def handle_key_events(self):
		if self.player.state == "alive":
			self.player.direction = (0, 0)
			self.player.speed = self.player.init_speed
			if "shift" in self.pressed_keys:
				self.player.speed = (6, 3)
			if "up" in self.pressed_keys and not ("down" in self.pressed_keys):
				self.player.direction = (self.player.direction[0], -1)
			if "down" in self.pressed_keys and not ("up" in self.pressed_keys):
				self.player.direction = (self.player.direction[0], 1)
			if "right" in self.pressed_keys and not ("left" in self.pressed_keys):
				self.player.direction = (1, self.player.direction[1])
			if "left" in self.pressed_keys and not ("right" in self.pressed_keys):
				self.player.direction = (-1, self.player.direction[1])
			if "space" in self.pressed_keys:
				self.player.shoot()
		else:
			if "up" in self.released_keys:
				self.buttons[self.cursor].active = False
				self.buttons[self.cursor].update()
				self.cursor -= 1
				self.released_keys.remove("up")
			if "down" in self.released_keys:
				self.buttons[self.cursor].active = False
				self.buttons[self.cursor].update()
				self.cursor += 1
				self.released_keys.remove("down")

			if ("space" in self.pressed_keys) and "PLAY" in self.buttons[self.cursor].text:
				self.reset()
				self.buttons[1].active_help = False
				self.player.state = "alive"
				self.cursor = 0
				self.player.score = 0
				self.buttons[self.cursor].active_help = False

			if ("space" in self.pressed_keys) and "QUIT" in self.buttons[self.cursor].text:
				self.exit()

			if self.cursor < 0:
				self.cursor = len(self.buttons) - 1
			if self.cursor > len(self.buttons) - 1:
				self.cursor = 0
			self.buttons[self.cursor].active = True
			self.buttons[self.cursor].update()


	def run(self, stdscr):
		self.fill(stdscr, "black")
		while self.running:
			self.handle_key_events()
			self.score.text = "SCORE: {}".format(self.player.score)
			self.score.update()
			self.score.render()
			for star in self.stars:
				star.update()
				star.render()
			if self.player.state == "dead":
				self.title.render()
				self.help.render()
				for btn in self.buttons:
					btn.update()
					btn.render()
			else:
				self.bullets_left.text = "BULLETS LEFT: {}".format(self.player.bullets_count)
				self.bullets_left.update()
				self.bullets_left.render()
				self.player.animate(loop=True, rate=1)
				self.player.update()
				self.player.render()
				for bullet in self.player.bullets:
					bullet.update()
					bullet.render()
				for ast in self.asteroids:
					ast.update()
					if self.player.state == "dead":
						self.reset()
						break
					ast.animate(loop=True, rate=2)
					ast.render()

			self.draw(stdscr)
			stdscr.refresh()
			self.tick(self.fps)

		return
			

if __name__ == "__main__":
	window = GameWindow(width=130, height=50, char=" ", fps=60)
	window.start(window.run)
