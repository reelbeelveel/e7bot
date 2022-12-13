import pickle

class Character_Cache:
    def __init__(self, path):
        self.path = path
        self.cache = None
        self.load_cache()
    
    def load_cache(self):
        try:
            with open(self.path, "rb") as f:
                self.cache = pickle.load(f)
        except FileNotFoundError:
            pass
        except Exception:
            print("Character cache was corrupt.")
        pass

    def save_cache(self):
        with open(self.path, "wb") as f:
            pickle.dump(self.cache, f)