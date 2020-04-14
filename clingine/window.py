import os, time, sys, curses, pynput
from . import util, keyboard, clock, mouse

class Window:
	def __init__(self, width=80, height=22, char=" ", fps=60):
		if sys.platform == "win32" or sys.platform == "cygwin":
			os.system("mode {},{}".format(width, height))
		else:
			sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=height, cols=width)) # changes terminal dimensions
			print() # this print is necessary; we need to print something to update the terminal dimensions after executing the line above
		self.width = width
		self.height = height
		self.char = char
		self.fps = fps


	def start(self, func):
		try:
			self.screen = curses.initscr()
			curses.start_color()
			curses.noecho()
			curses.cbreak()
			curses.curs_set(0)
			self.screen.nodelay(True)
			self.screen.keypad(True)
			self.running = True
			self.clock = clock.Clock()
			self.keyboard = keyboard.Keyboard(self)
			self.mouse = mouse.Mouse(self)
			self.color_pairs = util.ColorPairs(self)
			self.screen_color_pair = ((255, 255, 255), (0, 0, 0))
			self.color_pairs.add(self.screen_color_pair)
			self.fill(self.screen_color_pair)
			self.reset()
			func() # the main game loop
			self.exit()

		except Exception as e:
			self.exit()
			raise e

	def fill(self, color_pair):
		self.screen_color_pair = color_pair
		color_pair = self.color_pairs.get_color_pair(color_pair)
		self.screen.bkgd(self.char, color_pair)

	def reset(self):

		self.screen_array = [] # 2D array of arrays, each with three values, flag, char, and color_pair
		# flag is a boolean that indicates whether that particular screen_arr value is changed / updated
		for i in range(self.height):
			self.screen_array.append([[True, self.char, self.screen_color_pair] for j in range(self.width)])

	
	def run(self):
		# your game logic here...
		pass


	def exit(self):
		self.running = False
		curses.nocbreak()
		self.screen.keypad(False)
		curses.echo()
		curses.endwin()

	def update(self, fps):
		if not self.mouse.listener_active:
			self.screen.getch()
		for y in range(self.height):
			for x in range(self.width):
				if y != self.height - 1 and x != self.width - 1:
					try:
						if self.screen_array[y][x][0]: # if that particular point is changed...
							if curses.can_change_color():
								color_pair = self.screen_array[y][x][2]
								if color_pair:
									self.screen.addstr(y, x, self.screen_array[y][x][1], self.color_pairs.get_color_pair(color_pair))
								else:
									self.screen_array[y][x][2] = self.screen_color_pair
									self.screen.addstr(y, x, self.screen_array[y][x][1], self.color_pairs.get_color_pair(self.screen_color_pair))
							else:
								self.screen.addstr(y, x, self.screen_array[y][x][1], curses.color_pair(0))
						self.screen_array[y][x][0] = False
					except:
						# this happens when the terminal size is smaller than the self.screen_array size
						self.screen.resize(self.height, self.width)
		self.mouse.clear_events()
		self.screen.refresh()
		self.clock.update()
		self.clock.delay(1 / fps)
