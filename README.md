# [DISCONTINUED]. REASON: i give up


# clingine
CLIngine is a Python game engine for developing command line interface (CLI) games.

# Screenshots:
![gameplay](https://github.com/avancayetano/clingine/blob/master/screenshots/gameplay.png "gameplay")

![sample](https://github.com/avancayetano/clingine/blob/master/screenshots/sample.gif "sample")


Just clone this repo and copy the clingine directory to your project, then import it.
I don't know how to publish this package and I'm too lazy to learn. 

*NOTE: Make sure that your project is in the same directory as clingine (the inner clingine).*

Note: If you're using windows os, pip install -r requirements_windows.txt, otherwise pip install -r requirements.txt.


### HOW TO USE:
```Python

import clingine
window = clingine.window.Window(width=130, height=50, fps=60)
rect_obj = clingine.shapes.Rect(window, x=0, y=0, width=10, height=5, direction=(0, 0), speed=(100, 60), char="#", color_pair=((255, 255, 255),(0, 0, 0)))
def game_loop():
	while window.running:
		dt = window.clock.get_dt()
		pressed_keys = window.keyboard.get_pressed()
		# your game logic here...

		if "q" in pressed_keys:
			window.exit()

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

			if "q" in pressed_keys:
				self.exit()
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
* Tile mapping
* Physics engine
* New window
* Audio
* Docs!
* Publish
