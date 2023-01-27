class Timer:
    def __init__(self, framerate):
        self.time = 0
        self.framerate = framerate

    # returns time in seconds
    def get_time(self):
        return self.time // self.framerate

    def tick(self):
        self.time += 1

    def reset_time(self):
        self.time = 0
