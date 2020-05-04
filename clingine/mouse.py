import curses

class Mouse:
	def __init__(self, window):
		self.window = window
		self.clicked = None
		curses.mousemask(curses.ALL_MOUSE_EVENTS)


	def clear_events(self):
		self.clicked = None

	def is_clicked(self):
		return self.clicked != None

	def get_clicked(self):
		key = self.window.screen.getch()
		if key == curses.KEY_MOUSE:
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
		self.button = self.identify_button(self.bstate)

	def identify_button(self, bstate):
		btns = [curses.BUTTON1_PRESSED, curses.BUTTON2_PRESSED, curses.BUTTON3_PRESSED]
		for i in range(len(btns)):
			if bstate & btns[i]:
				return (i + 1)
