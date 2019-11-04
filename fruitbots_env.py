import gym
from gym import spaces
from engine import Engine


class FruitbotsEnvSP(gym.Env):
	def __init__(self):
		self.turn = 0
		self.engine = Engine()

	def step(self, action):
		assert type(action) is int

		self.engine.step(action)

	def reset(self):
		self.turn = 0
		self.engine = Engine()

	def render(self, mode='human'):
		pass

	pass
