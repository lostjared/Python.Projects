import sdl2
import sys
import skeleton


class Game:
    def __init__(self, title, w, h):
        self.title = title
        self.w = w
        self.h = h
    def init(self):
        pass
    def event(self, event):
        pass
    def render(self, remderer):
        pass

def main(args):
    obj = skeleton.GameObject(Game(b"Test App", 640, 480))
    obj.loop()
    obj.cleanup()
    return 0

sys.exit(main(sys.argv))
