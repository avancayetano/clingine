import curses

class Mouse:
	def __init__(self, window):
		self.window = window
		self.clicked = None
		self.listener_active = False
		curses.mousemask(curses.ALL_MOUSE_EVENTS)


	def clear_events(self):
		self.clicked = None
		self.listener_active = False


	def is_clicked(self):
		return is_clicked != None

	def get_clicked(self):
		self.listener_active = True
		key = self.window.screen.getch()
		if key == curses.KEY_MOUSE:
			# print("...")
			self.clicked = MouseEvent(*curses.getmouse())
			return self.clicked
		return None


class MouseEvent:
	def __init__(self, mouse_id, x, y, z, bstate):
		self.mouse_id = mouse_id
		self.x = x
		self.y = y
		self.z = z
		self.bstate = bstate
	# 	self.button = self.identify_button(self.bstate)

	# def identify_button(self, bstate):
	# 	if any([self.bstate & i for i in [curses.BUTTON1_PRESSED, curses.BUTTON1_RELEASED, curses.BUTTON1_CLICKED, curses.BUTTON1_CLICKED, curses.BUTTON1_CLICKED]])
	# 			if self.bstate & curses.BUTTON1_CLICKED:
	# 		print('......asdasd')
