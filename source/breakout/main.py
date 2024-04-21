
import skeleton
import sys
import sdl2
import sdl2.ext
import breakout

class Game(skeleton.GameInternal):
    def __init__(self):
        self.setup()
    def setup(self):
        self.grid = breakout.Grid(breakout.grid_width, breakout.grid_height)
        self.paddle = breakout.Paddle()
        self.ball = breakout.Ball()
        self.score = 0
        self.keys = dict()
        self.keys[sdl2.SDLK_LEFT] = 0
        self.keys[sdl2.SDLK_RIGHT] = 0
        self.mode = 0
        self.end_score = 0

    def set_window(self, window):
        self.renderer = sdl2.ext.Renderer(window)
    
    def draw(self, font):
        sdl2.SDL_SetRenderDrawColor(self.renderer.sdlrenderer, 0, 0, 0, 255)
        self.renderer.clear()
        if self.mode == 0:
            self.grid.draw(self.renderer)
            self.paddle.draw(self.renderer)
            self.ball.draw(self.renderer)
            self.printtext(self.renderer, font, "Score: %d Lives: %d" %(self.ball.score, self.ball.lives), (255, 255, 255), (15, 275))
        elif self.mode == 1:
            self.printtext(self.renderer, font, "Game Over - [ Score: %d ] Press Return" % (self.end_score), (255, 255, 255), (100, 100))
        self.renderer.present()
    
    def event(self, e):
        if e.type == sdl2.SDL_KEYDOWN:
            if self.mode == 1 and e.key.keysym.sym == sdl2.SDLK_RETURN:
                self.setup()
        
    def proc(self):
        if self.mode == 0:
              key_states = sdl2.SDL_GetKeyboardState(None)
              if key_states[sdl2.SDL_SCANCODE_LEFT]:
                self.paddle.move_left()
              if key_states[sdl2.SDL_SCANCODE_RIGHT]:
                self.paddle.move_right()

    def tproc(self):
        if self.mode == 0:
            self.ball.update(self.paddle, self.grid)
            if self.ball.lives <= 0:
               self.end_score = self.ball.score
               self.mode = 1
            else:
                if self.grid.is_empty():
                    self.grid.reset()
            
if __name__ == "__main__":
    object = skeleton.XObject("Breakout", (1440, 1080))
    sys.exit(object.main(sys.argv, Game()))
