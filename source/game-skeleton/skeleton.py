# game skeleton

import sys
import sdl2
import sdl2.ext;
import random

class Game:
    def __init__(self, window):
        self.renderer = sdl2.ext.Renderer(window)
        self.text = "Hello, World! Press a Key"
    
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
    def load_font(self, font_path, font_size):
        font = sdl2.sdlttf.TTF_OpenFont(font_path.encode('utf-8'), font_size)
        if not font:
            print("Failed to load the font: %s" % sdl2.sdlttf.TTF_GetError())
            sys.exit(1)
        return font
    
    def create_text_surface(self, font, text, color):
        sdl_color = sdl2.SDL_Color(color[0], color[1], color[2])
        surface = sdl2.sdlttf.TTF_RenderText_Solid(font, text.encode('utf-8'), sdl_color)
        if not surface:
            print("Failed to create text surface: %s" % sdl2.sdlttf.TTF_GetError())
        return surface
    
    def create_texture_from_surface(self, renderer, surface):
        texture = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, surface)
        if not texture:
            print("Failed to create texture: %s" % sdl2.SDL_GetError())
        return texture
    
    def printtext(self, rend, font, text, color, dst):
        surf = self.create_text_surface(font, text, color)
        text = self.create_texture_from_surface(rend, surf)
        rect = sdl2.SDL_Rect(dst[0], dst[1], surf.contents.w, surf.contents.h)
        sdl2.SDL_RenderCopy(rend.sdlrenderer, text, None, rect)
        sdl2.SDL_DestroyTexture(text)
        sdl2.SDL_FreeSurface(surf)

class XObject:
    def __init__(self, name, size):
        self.name = name
        self.size = size
    
    def main(self, args):
        sdl2.ext.init()
        if sdl2.sdlttf.TTF_Init() == -1:
            print("TTF_Font: %s" % sdl2.sdlttf.TTF_GetError())
            return 1
        
        window =  sdl2.ext.Window(self.name, size=self.size)
        ticks = sdl2.SDL_GetTicks()
        time_t = 0
        self.gameobj = Game(window)
        self.font = self.gameobj.load_font("font.ttf", 24)
        window.show()
        running = True
        while running:
            events = sdl2.ext.get_events()
            for event  in events:
                if event.type == sdl2.SDL_QUIT or (event.type == sdl2.SDL_KEYDOWN and event.key.keysym.sym == sdl2.SDLK_ESCAPE):
                    running = False
                    break
                else:
                    self.gameobj.event(event)
            
            self.gameobj.draw(self.font)
            nticks = sdl2.SDL_GetTicks()
            time_t += nticks-ticks
            ticks = nticks
            if(time_t > 1000):
                self.gameobj.proc()
                time_t = 0
            window.refresh()
    
        sdl2.sdlttf.TTF_CloseFont(self.font)
        sdl2.sdlttf.TTF_Quit()
        sdl2.ext.quit()
        return 0

if __name__ == "__main__":
    object = XObject("Skeleton", (1440, 1080))
    sys.exit(object.main(sys.argv))

