import curses, os

# rgb values range from 0 to 255
class Colors:
	def __init__(self):
		self.colors = {}

	def add(self, *rgbs):
		for rgb in rgbs:
			color_number = self.generate_color_number()
			self.colors[rgb] = color_number
			rgb = self.interpolate(rgb) # need to interpolate the input rgb values to values from 0 to 1000 so that curses can read them properly
			curses.init_color(color_number, rgb[0], rgb[1], rgb[2])

	def remove(self, *rgbs):
		for rgb in rgbs:
			del self.colors[rgb]

	def interpolate(self, rgb):
		interpolated = []
		for i in rgb:
			x = i * 1000 // 255
			interpolated.append(x)
		return tuple(interpolated)


	def generate_color_number(self):
		nums = sorted([self.colors[key] for key in self.colors])
		if len(nums) == 0:
			return 1
		i = 0
		while i < len(nums):
			if i + 1 != nums[i]:
				return i + 1
			i += 1
		return (i + 1) % (curses.COLORS + 1)


class ColorPairs:
	def __init__(self, window):
		self.window = window
		self.colors = Colors()
		self.color_pairs = {}


	def add(self, *rgb_pairs):
		for rgb_pair in rgb_pairs:
			color_pair_number = self.generate_color_pair_number()
			self.color_pairs[rgb_pair] = color_pair_number
			fg_color_number = self.colors.colors.get(rgb_pair[0], False)
			bg_color_number = self.colors.colors.get(rgb_pair[1], False)
			if not fg_color_number:
				self.colors.add(rgb_pair[0])
				fg_color_number = self.colors.colors[rgb_pair[0]]
			if not bg_color_number:
				self.colors.add(rgb_pair[1])
				bg_color_number = self.colors.colors[rgb_pair[1]]
			curses.init_pair(color_pair_number, fg_color_number, bg_color_number)

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
		return (i + 1) % (curses.COLOR_PAIRS)

	def get_color_pair(self, rgb_pair):
		rgb_pair_buffer = []
		for i in range(len(rgb_pair)):
			if not rgb_pair[i]:
				rgb_pair_buffer.append(self.window.screen_color_pair[i])
			else:
				rgb_pair_buffer.append(rgb_pair[i])
		rgb_pair = tuple(rgb_pair_buffer)
		color_pair_number = self.color_pairs.get(rgb_pair, False)
		if not color_pair_number:
			self.add(rgb_pair)
			color_pair_number = self.color_pairs[rgb_pair]
		return curses.color_pair(color_pair_number)


class Image:
	def __init__(self, value, source, width, height):
		self.value = value
		self.source = source
		self.width = width
		self.height = height



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