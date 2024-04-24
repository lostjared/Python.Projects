# matrix
# python3 matrix.py 
# set color:
# python3 matrix.py R G B
# fo red:
# python3 matrix.py 255 0 0

import sys
import sdl2
import sdl2.ext;
import random


class Line:
    def __init__(self):
        self.data = list()
        self.release()
    def release(self):
        for i in range(0, int(1080/24)+3):
            self.data.append([random.randint(97, 123), i*24])
    def __len__(self):
        return len(self.data)
    def __getitem__(self, index):
        return self.data[index]


class Game:
    chz = list()
    dir = 0
    def __init__(self, window):
        self.renderer = sdl2.ext.Renderer(window)
        for _ in range(0, int(1440/24)):
            self.chz.append(Line())
        self.dir = 0
    
    def build_character_list(self, font, color):
        self.chars = dict()
        for i in range(97, 123):
            surf = self.create_text_surface(font, "%c" %(i), color)
            text = self.create_texture_from_surface(self.renderer, surf)
            self.chars[i] = (text, surf.contents.w, surf.contents.h)
            sdl2.SDL_FreeSurface(surf)
        for i in range(65, 91):
            surf = self.create_text_surface(font, "%c" %(i), color)
            text = self.create_texture_from_surface(self.renderer, surf)
            self.chars[i] = (text,surf.contents.w, surf.contents.h)
            sdl2.SDL_FreeSurface(surf)


    def draw(self, font):
        self.renderer.clear()
        start_x = 0
        while start_x < int(1440/24):
            l = self.chz[start_x]
            for i in range(0, len(l)):
                r = random.randint(97, 122)
                ch = self.chars[r]
                rc = sdl2.SDL_Rect( start_x*24, l[i][1], ch[1], ch[2])
                sdl2.SDL_RenderCopy(self.renderer.sdlrenderer, ch[0] , None, rc)
            start_x += 1

        self.renderer.present()
    
    def event(self, e):
        if e.type == sdl2.SDL_KEYDOWN and e.key.keysym.sym == sdl2.SDLK_UP:
            self.dir = 0
        if e.type == sdl2.SDL_KEYDOWN and e.key.keysym.sym == sdl2.SDLK_DOWN:
            self.dir = 1

    def proc(self):
        for i in self.chz:
            for z in i.data:
                if self.dir == 0:
                    z[1] += random.randint(1, 5)
                else:
                    z[1] -= random.randint(1, 5)

                if z[1] < -32:
                    z[1] = 1080+32
                if z[1] > 1080+32:
                    z[1] = -32

    def clean(self):
        for key in self.chars:
            sdl2.SDL_DestroyTexture(self.chars[key][0])   

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
        if len(args) == 4:
            color = (int(args[1]), int(args[2]), int(args[3]))
        else:
            color = (0, 255, 0)
        sdl2.ext.init()
        if sdl2.sdlttf.TTF_Init() == -1:
            print("TTF_Font: %s" % sdl2.sdlttf.TTF_GetError())
            return 1
        
        window =  sdl2.ext.Window(self.name, size=self.size)
        ticks = sdl2.SDL_GetTicks()
        time_t = 0
        self.gameobj = Game(window)
        self.font = self.gameobj.load_font("font.ttf", 24)
        self.gameobj.build_character_list(self.font, color)
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
            if(time_t > 10):
                self.gameobj.proc()
                time_t = 0
            window.refresh()
    

        self.gameobj.clean()
        sdl2.sdlttf.TTF_CloseFont(self.font)
        sdl2.sdlttf.TTF_Quit()
        sdl2.ext.quit()
        return 0

if __name__ == "__main__":
    object = XObject("Matrix", (1440, 1080))
    sys.exit(object.main(sys.argv))