# clingine
CLIngine is a Python game engine for developing command line interface (CLI) games.

# Screenshots:
![gameplay](screenshots/gameplay.png?raw=true "gameplay")

![sample](screenshots/sample.gif?raw=true "sample")


Just clone this repo and copy the clingine directory to your project, then import it.
I don't know how to publish this package and I'm too lazy to learn. Make sure that your project is in the same directory as clingine.

Note: If you're using windows os, pip install requirements_windows.txt, otherwise pip install requirements.txt.


### HOW TO USE:
```Python

import clingine
window = clingine.window.Window(width=130, height=50, fps=60)
rect_obj = clingine.shapes.Rect(window, x=0, y=0, width=10, height=5, direction=(0, 0), speed=(100, 60), char="#", color_pair=((255, 255, 255),(0, 0, 0)))
def game_loop():
	while window.running:
		dt = self.get_dt()
		pressed_keys = window.keyboard.get_pressed()
		# your game logic here...
		rect_obj.update(dt)
		rect_obj.render()

		window.update(window.fps)
	return

window.start(game_loop)

```
The code structure above works, but I don't recommend it. What I recommend is subclassing the ```Window``` object, as it reduces the need for global variables:
```Python
import clingine
class GameWindow(clingine.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rect_obj = clingine.shapes.Rect(self, x=0, y=0, width=10, height=5, direction=(0, 0), speed=(100, 60), char="#", color_pair=((255, 255, 255),(0, 0, 0)))

	def run(self):
		while self.running:
			dt = self.clock.get_dt()
			pressed_keys = self.keyboard.get_pressed()
			# game logic here
			self.rect_obj.update(dt)
			self.rect_obj.render()
			self.update(self.fps)
		return

if __name__ == "__main__":
	window = GameWindow(width=130, height=50, fps=60)
	window.start(window.run)

```
See examples/spaceship for another example on how to use this code stucture...

### TO DO:
* More shapes
* Image properties
* Improve error handling and display
* MapLoader
* Surface objects
* Mouse input (improve)
* Physics engine
* New window
* Audio
* Docs!
* Publish
