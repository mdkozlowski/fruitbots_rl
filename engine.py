import numpy as np

FRUIT_TYPES = {
	"APPLE": 0,
	"BANANA": 1,
	"ORANGE": 2
}

DEFAULT_CONFIG = {
	"fruits_max": 0.3,
}

ACTIONS = {
	"UP": 0,
	"DOWN": 1,
	"LEFT": 2,
	"RIGHT": 3
}


class Fruit:
	def __init__(self, pos, ftype):
		self.position = pos
		self.ftype = ftype

	def __repr__(self):
		return f"{{{self.position[0]}, {self.position[1]}| {self.ftype}}}"


class Bot:
	def __init__(self, pos):
		self.position = pos
		self.owned_fruit = [0, 0, 0]

	def pos(self):
		return self.position[0], self.position[1]

	def set_pos(self, pos):
		self.position = pos


class Map:
	def __init__(self, size):
		self.size = size
		self.fruit = []
		self.bots = []

		self.new_map()

	def new_map(self):
		max_fruit = int(DEFAULT_CONFIG["fruits_max"] * self.size ** 2)
		fruit_pos = []
		for idx in range(max_fruit):
			candidate = tuple(np.random.randint(0, self.size, size=2))
			if candidate not in fruit_pos:
				fruit_pos.append(candidate)
		for pos in fruit_pos:
			fruit = Fruit(np.array([pos[0], pos[1]]), np.random.choice(3))
			self.fruit.append(fruit)

		while True:
			candidate = tuple(np.random.randint(0, self.size, size=2))
			if candidate not in fruit_pos:
				self.bots.append(Bot(np.array([candidate[0], candidate[1]])))
				break


class Engine:
	def __init__(self):
		self.turn = 0
		self.map = Map(5)

	def step(self, action):
		self.turn += 1

		bot_pos = self.map.bots[0].position
		pos_delta = np.array([0, 0])
		if action == ACTIONS["UP"]:
			pos_delta[1] -= 1
		elif action == ACTIONS["DOWN"]:
			pos_delta[1] += 1
		elif action == ACTIONS["LEFT"]:
			pos_delta[0] -= 1
		elif action == ACTIONS["UP"]:
			pos_delta[0] += 1

		new_pos = bot_pos + pos_delta
		if new_pos[0] >= self.map.size or new_pos[1] >= self.map.size or \
				new_pos[0] < 0 or new_pos[1] < 0:
			# invalid move
			pass
		else:
			self.map.bots[0].position = new_pos
			for fruit in self.map.fruit:
				if fruit.position == new_pos:
					self.map.bots[0].owned_fruit[fruit.ftype] += 1
					self.map.fruit.remove(fruit)
