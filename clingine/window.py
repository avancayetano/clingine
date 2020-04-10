import os, time, sys, curses, pynput
from . import label, shapes, util

class Window:
	def __init__(self, width=80, height=22, char=" ", fps=30):
		sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=height, cols=width)) # changes terminal dimensions
		print() # this print is necessary; we need to print something to update the terminal dimensions
		self.width = width
		self.height = height
		self.char = char
		self.running = True

		self.fps = fps
		self.clock = time.time()
		
		self.reset()

		self.key_listener = pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
		self.pressed_keys = set()
		self.released_keys = set()
		self.key_listener.start()


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

	def start(self, func):
		curses.wrapper(func)

	def fill(self, stdscr, color):
	    curses.init_pair(1, curses.COLOR_WHITE, util.colors.get(color, curses.COLOR_BLACK))
	    stdscr.bkgd(self.char, curses.color_pair(1) | curses.A_BOLD)

	def reset(self):
		self.screen = []
		for i in range(self.height):
			self.screen.append([self.char for j in range(self.width)])

	
	def run(self, stdscr):
		# your game logic here...
		pass


	def tick(self, fps):
		self.clock = time.time()
		time.sleep(1 / fps)

	def exit(self):
		self.running = False


	def draw(self, stdscr):
		for y in range(self.height):
			for x in range(self.width):
				if y != self.height - 1 and x != self.width - 1:
					try:
						stdscr.addch(y, x, self.screen[y][x], curses.color_pair(1) | curses.A_BOLD)
					except:
						# this happens when the terminal size is smaller than the self.screen size
						stdscr.resize(self.height, self.width)
