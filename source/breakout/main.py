
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
        self.mode = 2
        self.end_score = 0
       

    def load_image(self, src):
        img = sdl2.SDL_LoadBMP(src)
        if not img:
            print("Error loading image: ", sdl2.SDL_GetError())
        tex = self.create_texture_from_surface(self.renderer, img)
        if not tex:
            print("Error loading texture: ", sdl2.SDL_GetError())
        sdl2.SDL_FreeSurface(img)
        return tex

    def release(self):
        sdl2.SDL_DestroyTexture(self.background)
        for i in self.img_tex:
            sdl2.SDL_DestroyTexture(i)
        sdl2.SDL_DestroyTexture(self.start_img)
        sdl2.SDL_DestroyTexture(self.gameover)
        
    def set_window(self, window):
        self.renderer = sdl2.ext.Renderer(window)
        self.background = self.load_image(b"./img/bg.bmp")
        img_files = (b"./img/block_ltblue.bmp", b"./img/block_dblue.bmp", b"./img/block_pink.bmp", b"./img/block_yellow.bmp", b"./img/block_red.bmp")
        self.img_tex = list()
        self.img_tex.append(None)
        for i in range(0, len(img_files)):
            self.img_tex.append(self.load_image(img_files[i]))
        self.start_img = self.load_image(b"./img/start.bmp")
        self.gameover =  self.load_image(b"./img/gameover.bmp")



    
    def draw(self, font):
        sdl2.SDL_SetRenderDrawColor(self.renderer.sdlrenderer, 0, 0, 0, 255)
        self.renderer.clear()
        if self.mode == 2:
            sdl2.SDL_RenderCopy(self.renderer.sdlrenderer, self.start_img, None, None)
            self.printtext(self.renderer, font, "[Press Enter to Play]", (255,255,255), (25, 25))
        if self.mode == 0:
            sdl2.SDL_RenderCopy(self.renderer.sdlrenderer, self.background, None, None)
            self.grid.draw(self.renderer, self.img_tex)
            self.paddle.draw(self.renderer)
            self.ball.draw(self.renderer)
            self.printtext(self.renderer, font, "Score: %d Lives: %d" %(self.ball.score, self.ball.lives), (255, 255, 255), (15, 275))
        elif self.mode == 1:
            sdl2.SDL_RenderCopy(self.renderer.sdlrenderer, self.gameover, None, None)
            self.printtext(self.renderer, font, "Game Over - [ Score: %d ] Press Return" % (self.end_score), (255, 255, 255), (100, 100))
        self.renderer.present()
    
    def event(self, e):
        if e.type == sdl2.SDL_KEYDOWN:
            if self.mode == 1 and e.key.keysym.sym == sdl2.SDLK_RETURN:
                self.setup()
            elif self.mode == 2 and e.key.keysym.sym == sdl2.SDLK_RETURN:
                self.mode = 0
        
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
