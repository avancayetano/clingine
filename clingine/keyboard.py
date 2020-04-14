import pynput

class Keyboard:
	def __init__(self, window):
		self.pressed = set()
		self.released = set()
		self.listener = pynput.keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
		self.listener.start()
		
	def on_press(self, key):
		try:
			key = key.char
		except:
			key = key.name
		self.pressed.add(key)
		if key in self.released:
			self.released.remove(key)


	def on_release(self, key):
		try:
			key = key.char
		except:
			key = key.name
		self.released.add(key)
		if key in self.pressed:
			self.pressed.remove(key)

	def clear_events(self):
		self.pressed = set()
		self.released = set()

	def clear_pressed_events(self):
		self.pressed = set()

	def clear_released_events(self):
		self.released = set()

	def get_events(self):
		return {
			"pressed": self.pressed,
			"released": self.released
		}

	def get_pressed(self):
		return self.pressed

	def get_released(self):
		return self.released