class DataService:
    def __init__(self):
        self._points = 0
        self._lives = 3
        self._level = 1
        self._record = 500

        self.time_start = 0
        self.time_death = 0

    def add_points(self, points:int):
        self._points += points
        if self._points > self._record:
            self._record = self._points
    
    def kill_player(self):
        self._lives -= 1

    def pass_level(self):
        self._level += 1

    def get_data(self):
        return {"points": self._points,
                "lives": self._lives,
                "level": self._level,
                "record": self._record}

    