
import skeleton
import sys
import sdl2
import sdl2.ext;

class Game(skeleton.GameInternal):
    def __init__(self):
        self.text = "Hello, World! Press a Key"
    def set_window(self, window):
        self.renderer = sdl2.ext.Renderer(window)
    
    def draw(self, font):
        self.renderer.clear()
        self.printtext(self.renderer, font, self.text, (255, 255, 255), (15, 15))
        self.renderer.present()
    
    def event(self, e):
        if e.type == sdl2.SDL_KEYDOWN:
            self.text = "KeyCode: %d" % (e.key.keysym.sym)
        elif e.type == sdl2.SDL_KEYUP:
            self.text = "Hello, World! Press a Key"
    
    def proc(self):
        pass

if __name__ == "__main__":
    object = skeleton.XObject("Skeleton", (1440, 1080))
    sys.exit(object.main(sys.argv, Game()))
