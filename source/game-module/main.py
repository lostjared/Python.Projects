
import skeleton
import sys
import sdl2
import sdl2.ext;

# Game class must contain

# load_gfx(self)
# cleanup(self)
# draw(self, font)
# event(self, e)
# proc(self)


class Game(skeleton.GameInternal):
    def __init__(self):
        self.text = "Hello, World! Press a Key"
      
    def load_gfx(self):
        self.image = sdl2.surface.SDL_LoadBMP("intro.bmp".encode('utf-8'))
        if not self.image:
            raise Exception
        self.tex = self.create_texture_from_surface(self.renderer, self.image)
        if not self.tex:
            raise Exception
        sdl2.SDL_FreeSurface(self.image)


    def cleanup(self):
        sdl2.SDL_DestroyTexture(self.tex)


    def set_window(self, window):
        self.renderer = sdl2.ext.Renderer(window)
    
    def draw(self, font):
        self.renderer.clear()
        self.draw_image(self.tex, self.renderer, (0, 0, 1440, 1080))
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
