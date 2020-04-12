import os, time, sys, curses, pynput
from . import label, shapes, util

class Window:
	def __init__(self, width=80, height=22, char=" ", fps=60):
		sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=height, cols=width)) # changes terminal dimensions
		print() # this print is necessary; we need to print something to update the terminal dimensions after executing the line above
		self.width = width
		self.height = height
		self.char = char
		self.fps = fps


	def on_press(self, key):
		try:
			key = key.char
		except:
			key = key.name
		self.pressed_keys.add(key)
		if key in self.released_keys:
			self.released_keys.remove(key)

	def on_release(self, key):
		try:
			key = key.char
		except:
			key = key.name
		self.released_keys.add(key)
		self.pressed_keys.remove(key)

	def start(self):
		try:
			self.screen = curses.initscr()
			curses.start_color()
			curses.noecho()
			curses.cbreak()
			curses.curs_set(0)
			self.screen.nodelay(True)
			self.screen.keypad(True)
			self.running = True
			self.clock = time.time()
			self.key_listener = pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
			self.pressed_keys = set()
			self.released_keys = set()
			self.key_listener.start()
			self.reset()
			self.run() # the main game loop
			self.exit()

		except Exception as e:
			self.exit()
			raise e
			

	def fill(self, color_pair):
		self.screen.bkgd(self.char, color_pair)

	def reset(self):
		self.screen_array = [] # 2D array of arrays, each with three values, flag, char, and color_pair
		# flag is a boolean that indicates whether that particular screen_arr value is changed / updated
		for i in range(self.height):
			self.screen_array.append([[True, self.char, None] for j in range(self.width)])

	
	def run(self):
		# your game logic here...
		pass


	def tick(self, fps):
		self.clock = time.time()
		time.sleep(1 / fps)

	def exit(self):
		self.running = False
		curses.nocbreak()
		self.screen.keypad(False)
		curses.echo()
		curses.endwin()

	def update(self):
		self.screen.getch() # this is necessary so that the keys you inputted while playing wont echo in the terminal after you exit the game
		for y in range(self.height):
			for x in range(self.width):
				if y != self.height - 1 and x != self.width - 1:
					try:
						if self.screen_array[y][x][0]: # if that particular point is updated...
							color_pair = self.screen_array[y][x][2]
							if color_pair:
								self.screen.addstr(y, x, self.screen_array[y][x][1], color_pair)
							else:
								self.screen.addstr(y, x, self.screen_array[y][x][1], curses.color_pair(1))
						self.screen_array[y][x][0] = False
					except:
						# this happens when the terminal size is smaller than the self.screen_array size
						self.screen.resize(self.height, self.width)
		self.screen.refresh()
