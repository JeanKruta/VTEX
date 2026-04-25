import json
import os


class TimeoutManager:
    def __init__(self, path):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def save(self, timeout_list):
        with open(self.path, "w") as f:
            json.dump(timeout_list, f)

    def load(self):
        if not os.path.exists(self.path):
            return []

        with open(self.path, "r") as f:
            return json.load(f)

    def clear(self):
        if os.path.exists(self.path):
            os.remove(self.path)