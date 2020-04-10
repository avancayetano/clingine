import curses
class Image:
	def __init__(self, value, source, width, height):
		self.value = value
		self.source = source
		self.width = width
		self.height = height

colors = {
	"black": curses.COLOR_BLACK,
	"blue": curses.COLOR_BLUE,
	"cyan": curses.COLOR_CYAN,
	"green": curses.COLOR_GREEN,
	"magenta": curses.COLOR_MAGENTA,
	"red": curses.COLOR_RED,
	"white": curses.COLOR_WHITE,
	"yellow": curses.COLOR_YELLOW,
}

def load_image(source):
	val = []
	with open(source, "r") as file:
		lines = file.readlines()
		height = len(lines)
		width = 0
		for line in lines:
			if len(line) - 1 > width:
				width = len(line) - 1 
			val.append(line.rstrip("\n"))
	img = Image(val, source, width, height)
	return img