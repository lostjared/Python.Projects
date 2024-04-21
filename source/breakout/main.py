
import skeleton
import sys
import sdl2
import sdl2.ext
import breakout

class Game(skeleton.GameInternal):
    def __init__(self):
        self.text = "Hello, World! Press a Key"
        self.grid = breakout.Grid(breakout.grid_width, breakout.grid_height)
        self.paddle = breakout.Paddle()

    def set_window(self, window):
        self.renderer = sdl2.ext.Renderer(window)
    
    def draw(self, font):
        sdl2.SDL_SetRenderDrawColor(self.renderer.sdlrenderer, 0, 0, 0, 255)
        self.renderer.clear()
        self.printtext(self.renderer, font, self.text, (255, 255, 255), (15, 15))
        self.grid.draw(self.renderer)
        self.paddle.draw(self.renderer)
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
