import json
import os
from http.server import HTTPServer
from api.app import MomoDataAPIHandler

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "processed", "dashboard.json")

def load_transactions():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_transactions(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def run(port=8080):
    MomoDataAPIHandler.data_file = DATA_FILE
    MomoDataAPIHandler.transactions = load_transactions()
    MomoDataAPIHandler.save = staticmethod(lambda: save_transactions(MomoDataAPIHandler.transactions))

    server = HTTPServer(("", port), MomoDataAPIHandler)
    print(f"Server running on http://localhost:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run()
