Fruitbots Reinforcement Learning
--------

Implementation of [Fruitbots](http://fruitbots.org/) game with an OpenAI gym interface.
Goal is to use this game as an RL environment for learning, not to train bots that will 
play on the actual fruitbots.org platform.

Testing environments:
- Single agent, goal is to collect all fruit. For diagnostics
- Multiagent, usual fruitbots rules

Train multiagents using 
1. supervised learning, from scraped match replays
2. competetive self-play