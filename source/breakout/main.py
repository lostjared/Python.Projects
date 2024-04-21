
import skeleton
import sys
import sdl2
import sdl2.ext
import breakout

class Game(skeleton.GameInternal):
    def __init__(self):
        self.grid = breakout.Grid(breakout.grid_width, breakout.grid_height)
        self.paddle = breakout.Paddle()
        self.ball = breakout.Ball()
        self.score = 0
        self.keys = dict()
        self.keys[sdl2.SDLK_LEFT] = 0
        self.keys[sdl2.SDLK_RIGHT] = 0

    def set_window(self, window):
        self.renderer = sdl2.ext.Renderer(window)
    
    def draw(self, font):
        sdl2.SDL_SetRenderDrawColor(self.renderer.sdlrenderer, 0, 0, 0, 255)
        self.renderer.clear()
        self.grid.draw(self.renderer)
        self.paddle.draw(self.renderer)
        self.ball.drwa(self.renderer)
        self.printtext(self.renderer, font, "Score: %d" %(self.score), (255, 255, 255), (15, 275))
        self.renderer.present()
    
    def event(self, e):
        if e.type == sdl2.SDL_KEYDOWN:
            self.keys[e.key.keysym.sym] = 1
        elif e.type == sdl2.SDL_KEYUP:
            self.keys[e.key.keysym.sym] = 0
    
    def proc(self):
        if  self.keys[sdl2.SDLK_LEFT] == 1:
            self.paddle.move_left()
        elif self.keys[sdl2.SDLK_RIGHT] == 1:
            self.paddle.move_right()
    def tproc(self):
        pass


if __name__ == "__main__":
    object = skeleton.XObject("Skeleton", (1440, 1080))
    sys.exit(object.main(sys.argv, Game()))
