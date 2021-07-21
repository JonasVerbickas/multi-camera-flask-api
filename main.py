from code.flask_server import Server
import json


if __name__ == "__main__":
    with open('config.json') as f:
        json_config = json.load(f)
        server = Server(json_config)
