import curses, os
class Image:
	def __init__(self, value, source, width, height):
		self.value = value
		self.source = source
		self.width = width
		self.height = height

DEFAULT_COLORS = {
	"black": curses.COLOR_BLACK,
	"blue": curses.COLOR_BLUE,
	"cyan": curses.COLOR_CYAN,
	"green": curses.COLOR_GREEN,
	"magenta": curses.COLOR_MAGENTA,
	"red": curses.COLOR_RED,
	"white": curses.COLOR_WHITE,
	"yellow": curses.COLOR_YELLOW,
}

class Colors:
	def __init__(self):
		self.custom_colors = {}

	def add(self, *rgbs):
		for rgb in rgbs:
			color_number = self.generate_color_number()
			self.custom_colors[rgb] = color_number
			curses.init_color(color_number, rgb[0], rgb[1], rgb[2])

	def remove(self, *rgbs):
		for rgb in rgbs:
			del self.custom_colors[rgb]

	def get_color_number(self, rgb):
		return self.custom_colors[rgb]	

	def generate_color_number(self):
		nums = sorted([self.custom_colors[key] for key in self.custom_colors])
		if len(nums) == 0:
			return 1
		i = 0
		while i < len(nums):
			if i + 1 != nums[i]:
				return i + 1
			i += 1
		return i + 1


class ColorPairs:
	def __init__(self, colors):
		self.colors = colors
		self.color_pairs = {}


	def add(self, *rgb_pairs):
		for rgb_pair in rgb_pairs:
			color_pair_number = self.generate_color_pair_number()
			self.color_pairs[rgb_pair] = color_pair_number
			curses.init_pair(color_pair_number, self.colors.get_color_number(rgb_pair[0]), self.colors.get_color_number(rgb_pair[1]))

	def remove(self, *rgb_pairs):
		for rgb_pair in rgb_pairs:
			del self.color_pairs[rgb_pair]

	def generate_color_pair_number(self):
		nums = sorted([self.color_pairs[key] for key in self.color_pairs])
		if len(nums) == 0:
			return 1
		i = 0
		while i < len(nums):
			if i + 1 != nums[i]:
				return i + 1
			i += 1
		return i + 1

	def get_color_pair_number(self, rgb_pair):
		return self.color_pairs[rgb_pair]

	def get_color_pair(self, rgb_pair):
		return curses.color_pair(self.get_color_pair_number(rgb_pair))


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
	val = tuple(val)
	img = Image(val, source, width, height)
	return img

def load_images(source):
	imgs = []
	for file in os.listdir(source):
		imgs.append(load_image("{}/{}".format(source, file)))
	return imgs