
import sys
import sdl2
import sdl2.ext;
import random

def load_font(font_path, font_size):
    font = sdl2.sdlttf.TTF_OpenFont(font_path.encode('utf-8'), font_size)
    if not font:
        print("Failed to load the font: %s" % sdl2.sdlttf.TTF_GetError())
        sys.exit(1)
    return font

def create_text_surface(font, text, color):
    sdl_color = sdl2.SDL_Color(color[0], color[1], color[2])
    surface = sdl2.sdlttf.TTF_RenderText_Solid(font, text.encode('utf-8'), sdl_color)
    if not surface:
        print("Failed to create text surface: %s" % sdl2.sdlttf.TTF_GetError())
    return surface

def create_texture_from_surface(renderer, surface):
    texture = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, surface)
    if not texture:
        print("Failed to create texture: %s" % sdl2.SDL_GetError())
    return texture

def printtext(rend, font, text, color, dst):
     surf = create_text_surface(font, text, color)
     text = create_texture_from_surface(rend, surf)
     rect = sdl2.SDL_Rect(dst[0], dst[1], surf.contents.w, surf.contents.h)
     sdl2.SDL_RenderCopy(rend.sdlrenderer, text, None, rect)
     sdl2.SDL_DestroyTexture(text)
     sdl2.SDL_FreeSurface(surf)

class Game:
    def __init__(self, window):
        self.renderer = sdl2.ext.Renderer(window)
        self.text = "Hello, World!"
       
    def draw(self, font):
        self.renderer.clear()
        printtext(self.renderer, font, self.text, (255, 255, 255), (15, 15))
        self.renderer.present()
    
    def event(self, e):
        pass

    def proc(event):
        pass

def main(args):
    sdl2.ext.init()
    if sdl2.sdlttf.TTF_Init() == -1:
         print("TTF_Font: %s" % sdl2.sdlttf.TTF_GetError())
         return 1
    font = load_font("font.ttf", 24)
    window =  sdl2.ext.Window("Skeleton", size=(1440, 1080))
    ticks = sdl2.SDL_GetTicks()
    time_t = 0
    gameobj = Game(window)
    window.show()
    running = True
    while running:
        events = sdl2.ext.get_events()
        for event  in events:
            if event.type == sdl2.SDL_QUIT or (event.type == sdl2.SDL_KEYDOWN and event.key.keysym.sym == sdl2.SDLK_ESCAPE):
                running = False
                break
            else:
                gameobj.event(event)

        gameobj.draw(font)
        nticks = sdl2.SDL_GetTicks()
        time_t += nticks-ticks
        ticks = nticks
        if(time_t > 1000):
             gameobj.proc()
             time_t = 0
        window.refresh()

    sdl2.sdlttf.TTF_CloseFont(font)
    sdl2.sdlttf.TTF_Quit()
    sdl2.ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

