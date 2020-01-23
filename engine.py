import numpy as np

FRUIT_TYPES = {
	"APPLE": 0,
	"BANANA": 1,
	"ORANGE": 2
}

DEFAULT_CONFIG = {
	"fruits_max_prop": 0.5,
	"max_turns": 200,
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
		self.max_fruit = 0

		self.new_map()

	def new_map(self):
		self.max_fruit = int(DEFAULT_CONFIG["fruits_max_prop"] * self.size ** 2)

		fruit_pos = []
		self.fruit_assignments = np.repeat(np.array([0, 1, 2]), self.max_fruit / 3)
		for idx in range(self.max_fruit):
			while True:
				candidate = tuple(np.random.randint(0, self.size, size=2))
				if candidate not in fruit_pos:
					fruit_pos.append(candidate)
					fruit = Fruit(np.array([candidate[0], candidate[1]]), self.fruit_assignments[idx])
					self.fruit.append(fruit)
					break

		while True:
			candidate = tuple(np.random.randint(0, self.size, size=2))
			if candidate not in fruit_pos:
				self.bots.append(Bot(np.array([candidate[0], candidate[1]])))
				break


class Engine:
	def __init__(self):
		self.turn = 0
		self.done = False
		self.won = False
		self.map = Map(5)

	def get_info(self):
		return {
			"turn": self.turn,
			"map": {
				"size": self.map.size,
			},
			"done": self.done
		}

	def get_state_vec(self):
		map_vec = np.zeros((4, self.map.size, self.map.size))
		state = np.zeros(4)  # fruit, turn

		bot = self.map.bots[0]
		for fruit in self.map.fruit:
			map_vec[fruit.ftype, fruit.position[0], fruit.position[1]] = 1
		map_vec[3, bot.position[0], bot.position[1]] = 1

		state[0:3] = self.map.bots[0].owned_fruit / np.bincount(self.map.fruit_assignments)
		state[-1] = self.turn / DEFAULT_CONFIG["max_turns"]

		return map_vec, state

	def step(self, action):
		if self.turn > DEFAULT_CONFIG["max_turns"]:
			self.done = True
		self.turn += 1

		bot_pos = self.map.bots[0].position
		pos_delta = np.array([0, 0])
		if action == ACTIONS["UP"]:
			pos_delta[1] -= 1
		elif action == ACTIONS["DOWN"]:
			pos_delta[1] += 1
		elif action == ACTIONS["LEFT"]:
			pos_delta[0] -= 1
		elif action == ACTIONS["RIGHT"]:
			pos_delta[0] += 1

		new_pos = bot_pos + pos_delta
		if new_pos[0] >= self.map.size or new_pos[1] >= self.map.size or \
				new_pos[0] < 0 or new_pos[1] < 0:
			# invalid move
			pass
		else:
			self.map.bots[0].position = new_pos
			for fruit in self.map.fruit:
				if np.array_equal(fruit.position, new_pos):
					self.map.bots[0].owned_fruit[fruit.ftype] += 1
					self.map.fruit.remove(fruit)

		if len(self.map.fruit) == 0:
			self.done = True
			self.won = True