import sys, random
sys.path.append(sys.path[0] + "/../..") # cause main.py is two directories away from the clingine package

import clingine
import math

class Edge:
	def __init__(self, sx, sy, ex, ey):
		self.sx = sx
		self.sy = sy
		self.ex = ex
		self.ey = ey

class Cell:
	def __init__(self):
		self.exist = False
		self.edge_exist = {
			"north": False,
			"south": False,
			"east": False,
			"west": False,
		}
		self.edge_id = {
			"north": 0,
			"south": 0,
			"east": 0,
			"west": 0,
		}

class GameWindow(clingine.window.Window):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.rects = [
			clingine.shapes.Rect(self, x=1, y=1, width=self.width - 3, height=1, char="#"),
			clingine.shapes.Rect(self, x=1, y=self.height - 3, width=self.width - 3, height=1, char="#"),
			clingine.shapes.Rect(self, x=1, y=2, width=1, height=self.height - 5, char="#"),
			clingine.shapes.Rect(self, x=self.width - 3, y=2, width=1, height=self.height - 5, char="#"),
		] # walls

		self.player = clingine.shapes.Rect(self, x=self.width//2, y=self.height//2, width=1, height=1, direction=(0, 0), speed=(40, 20), 
			char="o", color_pair=((255, 255, 255),(0, 0, 0)))

		self.world = [[Cell() for j in range(self.width)] for i in range(self.height)]
		for i in range(1, self.width - 2):
			self.world[1][i].exist = True
			self.world[self.height - 3][i].exist = True
		for i in range(2, self.height - 3):
			self.world[i][1].exist = True
			self.world[i][self.width - 3].exist = True

		self.edges = []
		self.visibility_points = []


	def convert_tile_to_polymap(self):
		self.edges = []
		for y in range(1, self.height - 1):
			for x in range(1, self.width - 1):
				n = (x, y - 1)
				s = (x, y + 1)
				e = (x + 1, y)
				w = (x - 1, y)
				if self.world[y][x].exist:
					if not self.world[w[1]][w[0]].exist:
						if self.world[n[1]][n[0]].edge_exist["west"]:
							self.edges[self.world[n[1]][n[0]].edge_id["west"]].ey = y
							self.world[y][x].edge_id["west"] = self.world[n[1]][n[0]].edge_id["west"]
							self.world[y][x].edge_exist["west"] = True
						else:
							edge = Edge(x, y, x, y)
							self.world[y][x].edge_id["west"] = len(self.edges)
							self.world[y][x].edge_exist["west"] = True
							self.edges.append(edge)

					if not self.world[e[1]][e[0]].exist:
						if self.world[n[1]][n[0]].edge_exist["east"]:
							self.edges[self.world[n[1]][n[0]].edge_id["east"]].ey = y
							self.world[y][x].edge_id["east"] = self.world[n[1]][n[0]].edge_id["east"]
							self.world[y][x].edge_exist["east"] = True
						else:
							edge = Edge(x, y, x, y)
							self.world[y][x].edge_id["east"] = len(self.edges)
							self.world[y][x].edge_exist["east"] = True
							self.edges.append(edge)


					if not self.world[n[1]][n[0]].exist:
						if self.world[w[1]][w[0]].edge_exist["north"]:
							self.edges[self.world[w[1]][w[0]].edge_id["north"]].ex = x
							self.world[y][x].edge_id["north"] = self.world[w[1]][w[0]].edge_id["north"]
							self.world[y][x].edge_exist["north"] = True
						else:
							edge = Edge(x, y, x, y)
							self.world[y][x].edge_id["north"] = len(self.edges)
							self.world[y][x].edge_exist["north"] = True
							self.edges.append(edge)


					if not self.world[s[1]][s[0]].exist:
						if self.world[w[1]][w[0]].edge_exist["south"]:
							self.edges[self.world[w[1]][w[0]].edge_id["south"]].ex = x
							self.world[y][x].edge_id["south"] = self.world[w[1]][w[0]].edge_id["south"]
							self.world[y][x].edge_exist["south"] = True
						else:
							edge = Edge(x, y, x, y)
							self.world[y][x].edge_id["south"] = len(self.edges)
							self.world[y][x].edge_exist["south"] = True
							self.edges.append(edge)


	def get_visibility_points(self, ox, oy, radius):
		self.visibility_points = []
		for e1 in self.edges:
			for i in range(2):
				rdx = e1.sx - ox if i == 0 else e1.ex - ox
				rdy = e1.sy if i == 0 else e1.ey - oy
				base_ang = math.atan2(rdy, rdx)
				for j in range(3):
					if j == 0:
						ang = math.atan2(rdy - 1, rdx)
					if j == 1:
						ang = base_ang
					if j == 2:
						ang = math.atan2(rdy + 1, rdx)

					rdx = radius * math.cos(ang)
					rdy = radius * math.sin(ang)
					min_t1 = 99
					min_px = 0
					min_py = 0
					min_ang = 0
					valid = False

					for e2 in self.edges:
						if e2 != e1:
							sdx = e2.ex - e2.sx
							sdy = e2.ey - e2.sy

							if abs(sdx - rdx) > 0 and abs(sdy - rdy) > 0:
								t2 = (rdx * (e2.sy - oy) + (rdy * (ox - e2.sx))) / (sdx * rdy - sdy * rdx)
								t1 = (e2.sx + sdx * t2 - ox) / rdx
								if t1 > 0 and t2 >= 0 and t2 <= 1:
									if t1 <= min_t1:
										min_t1 = t1
										min_px = ox + rdx * t1
										min_py = oy + rdy * t1
										min_ang = math.atan2(min_py - oy, min_px - ox)
										valid = True
					if valid:
						self.visibility_points.append((min_ang, min_px, min_py))

		self.visibility_points.sort(key=lambda p: p[0])

	def run(self):
		while self.running:
			dt = self.clock.get_dt()
			clicked = self.mouse.get_clicked()
			pressed = self.keyboard.get_pressed()
			self.player.direction = (0, 0)
			if "up" in pressed and not ("down" in pressed):
				self.player.direction = (self.player.direction[0], -1)
			if "down" in pressed and not ("up" in pressed):
				self.player.direction = (self.player.direction[0], 1)
			if "right" in pressed and not ("left" in pressed):
				self.player.direction = (1, self.player.direction[1])
			if "left" in pressed and not ("right" in pressed):
				self.player.direction = (-1, self.player.direction[1])

			if "q" in pressed:
				self.exit()

			self.reset()

			if clicked and clicked.button == 1:
				clingine.shapes.Rect(self, x=clicked.x, y=clicked.y, width=6, height=4, direction=(0, 0), speed=(0, 0), 
					char="#", color_pair=((255, 255, 255),(0, 0, 0)), group=self.rects)
				for y in range(4):
					for x in range(6):
						self.world[clicked.y + y][clicked.x + x].exist = True

			self.convert_tile_to_polymap()
			self.get_visibility_points(self.player.x, self.player.y, 1000)


			self.triangles = []
			chars = ["."]
			if len(self.visibility_points) > 1:
				for i in range(len(self.visibility_points) - 1):
					clingine.shapes.Polygon(self, vertices=((self.player.x, self.player.y), (self.visibility_points[i][1], self.visibility_points[i][2]), 
						(self.visibility_points[i + 1][1],self.visibility_points[i + 1][2])), char=chars[i % len(chars)], fill=True, group=self.triangles)
				clingine.shapes.Polygon(self, vertices=((self.player.x, self.player.y), (self.visibility_points[-1][1], self.visibility_points[-1][2]),
						(self.visibility_points[0][1], self.visibility_points[0][2])), char=chars[i % len(chars)], fill=True, group=self.triangles)
				for t in self.triangles:
					t.update(dt)
					t.render()
			for rect in self.rects:
				rect.update(dt)
				rect.render()
			self.player.update(dt)
			self.player.render()
			self.update(self.fps)
		return

if __name__ == "__main__":
	window = GameWindow(width=130, height=50, fps=60)
	window.start(window.run)