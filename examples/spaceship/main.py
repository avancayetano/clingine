import sys, os, time, random, curses

# warning: hard-coded shit below: 
sys.path.append(sys.path[0] + "/../..") # cause main.py is two directories away from the clingine package


import clingine
from engine import player_obj, asteroid, button, star

class GameWindow(clingine.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.title = clingine.label.Label(window=self, text=["< == SPACE == >"], x=self.width // 2, y=15, anchor="center", color_pair=((0, 255, 0), (0, 0, 255)))
		self.help = clingine.label.Label(window=self, text=["Arrow Keys - Controls | Shift - Boost | Space - Shoot"],
			x=self.width // 2, y=self.height - 10, anchor="center", color_pair=((0, 255, 0), (255, 0, 0)))

		buttons_text = ["PLAY", "QUIT"]
		self.buttons = []
		for idx, txt in enumerate(buttons_text):
			button.Button(window=self, text=[txt], x=self.width // 2, y=20 + idx, anchor="center", color_pair=((0, 255, 0), None), group=self.buttons)

		self.buttons[0].active = True
		
		self.player = player_obj.Player(window=self, x=self.width // 2, y=self.height - 4, direction=(0, 0), speed=(120, 60), 
			images=clingine.util.load_images("resources/spaceship/"), color_pair=((128, 40, 200), None))

		asteroid_imgs = clingine.util.load_images("resources/asteroid/")
		self.asteroids = []
		for i in range(7):
			asteroid.Asteroid(window=self, x=random.randrange(1, self.width - 1 - asteroid_imgs[0].width), y=random.randrange(-asteroid_imgs[0].height - 40, -asteroid_imgs[0].height),
				direction=(0, 1), speed=(0, 60), images=asteroid_imgs, image_num=random.randrange(len(asteroid_imgs)), color_pair=((128, 128, 128), None), group=self.asteroids)


		self.explosion_imgs = clingine.util.load_images("resources/explosion")
		self.explosions = []

		self.score = clingine.label.Label(window=self, text=["SCORE: {}".format(self.player.score)], x=0, y=self.height - 2, color_pair=((0, 255, 0), None))
		self.bullets_left = clingine.label.Label(window=self, text=["BULLETS LEFT: {}".format(self.player.bullets_count)], x=0, y=self.height - 3, color_pair=((0, 255, 0), (0, 0, 255)))

		self.stars = []
		for i in range(20):
			star.Star(window=self, x=random.randrange(0, self.width - 1), width=1, height=1, 
				y=random.randrange(self.height - 1), direction=(0, 1), speed=(0, 60), color_pair=((255, 255, 255), None), group=self.stars)

		self.cursor = 0


	def handle_key_events(self):
		if self.player.state == "alive":
			self.player.direction = (0, 0)
			self.player.speed = self.player.init_speed
			if "shift" in self.pressed_keys:
				self.player.speed = (self.player.speed[0] * 2, self.player.speed[1] * 2)
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
			if "space" in self.released_keys:
				self.player.shoot_cooldown = 0
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

			if ("enter" in self.pressed_keys) and self.cursor == 0:
				self.reset()
				self.buttons[1].active_help = False
				self.player.state = "alive"
				self.cursor = 0
				self.player.reset()
				self.buttons[self.cursor].active_help = False

			if ("enter" in self.pressed_keys) and self.cursor == 1:
				self.exit()

			if self.cursor < 0:
				self.cursor = len(self.buttons) - 1
			if self.cursor > len(self.buttons) - 1:
				self.cursor = 0
			self.buttons[self.cursor].active = True
			self.buttons[self.cursor].update()

	def run(self):
		while self.running:
			dt = self.get_dt()
			self.handle_key_events()
			for star in self.stars:
				star.update(dt)
				star.render()
			if self.player.state == "dead":
				self.title.render()
				self.help.render()
				for btn in self.buttons:
					btn.update()
					btn.render()
			else:
				
				self.player.update(dt)
				self.player.animate(loop=True, rate=dt)
				for bullet in self.player.bullets:
					bullet.update(dt)
					bullet.render()
				for ast in self.asteroids:
					ast.update(dt)
					if self.player.state == "dead":
						self.reset()
						break
					ast.animate(loop=True, rate=dt)
				for exp in self.explosions:
					exp.animate(loop=False, rate=3*dt)
			self.bullets_left.update(["BULLETS LEFT: {}".format(self.player.bullets_count)])
			self.bullets_left.render()
			self.score.update(["SCORE: {}".format(self.player.score)])
			self.score.render()
			self.update()
			self.tick(self.fps)

		return
			

if __name__ == "__main__":
	window = GameWindow(width=130, height=50, fps=60)
	window.start(window.run)
