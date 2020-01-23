import uuid

from flask import Flask, jsonify
from flask_cors import CORS

import fruitbots_env

app = Flask(__name__)
CORS(app)
environments = {}


@app.route("/get_environments")
def get_environments():
	envs = [{code: environments[code].engine.get_info()} for code in environments]
	return jsonify(envs)


@app.route("/launch_environment")
def launch_env():
	env_code = uuid.uuid4().hex
	env = fruitbots_env.FruitbotsEnvSP()
	env.reset()
	env.render()

	environments[env_code] = env
	return env_code


if __name__ == '__main__':
	launch_env()
	app.run(port=8721)
