import gym
from gym import spaces

from engine import Engine, DEFAULT_CONFIG


class FruitbotsEnvSP(gym.Env):
	def __init__(self):
		super(FruitbotsEnvSP, self).__init__()

		self.engine = Engine()
		self.action_space = spaces.Discrete(4)
		self.observation_space = spaces.Dict({
			"map_vec": spaces.Box(0, 1, (4, self.engine.map.size, self.engine.map.size)),
			"state": spaces.Box(0, 1, shape=(4,))
		})
		print("Started environment")

	# print(self.observation_space.sample())

	def step(self, action):
		assert type(action) is dict

		self.engine.step(action)
		current_state = self.engine.get_state_vec(0)

		reward = 0
		if self.engine.done and self.engine.won:
			reward = 1.0

		if not self.engine.done:
			reward += -(self.engine.turn / DEFAULT_CONFIG["max_turns"])


		return current_state, reward, self.engine.done, {}

	def reset(self):
		self.engine = Engine()

		return self.engine.get_state_vec(0)

	def render(self, mode='human'):
		print(f"Fruit eaten: {self.engine.map.max_fruit - len(self.engine.map.fruit):3d}. Turn {self.engine.turn:3d}")
		pass

	pass


if __name__ == '__main__':
	env = FruitbotsEnvSP()
	env.step({
		# player_idx, action
		0: 0,
	})
	print(env.engine.get_state_vec(0))
