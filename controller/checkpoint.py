import json
import os


class CheckpointManager:
    def __init__(self, path):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def save(self, last_index, results):
        data = {
            "last_index": last_index,
            "results": results
        }

        with open(self.path, "w") as f:
            json.dump(data, f)

    def load(self):
        if not os.path.exists(self.path):
            return 0, []

        with open(self.path, "r") as f:
            data = json.load(f)

        return data["last_index"], data["results"]

    def clear(self):
        if os.path.exists(self.path):
            os.remove(self.path)