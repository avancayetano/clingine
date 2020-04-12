import curses, os
class Image:
	def __init__(self, value, source, width, height):
		self.value = value
		self.source = source
		self.width = width
		self.height = height


# rgb values range from 0 to 255
class Colors:
	def __init__(self):
		self.custom_colors = {}

	def add(self, *rgbs):
		for rgb in rgbs:
			color_number = self.generate_color_number()
			self.custom_colors[rgb] = color_number
			rgb = self.interpolate(rgb) # need to interpolate the input rgb values to values from 0 to 1000 so that curses can read them properly
			curses.init_color(color_number, rgb[0], rgb[1], rgb[2])

	def remove(self, *rgbs):
		for rgb in rgbs:
			del self.custom_colors[rgb]

	def interpolate(self, rgb):
		interpolated = []
		for i in rgb:
			x = i * 1000 // 255
			interpolated.append(x)
		return tuple(interpolated)

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