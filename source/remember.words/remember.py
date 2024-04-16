# in progress

import sys
import sdl2
import sdl2.ext;
import random

def load_font(font_path, font_size):
    font = sdl2.sdlttf.TTF_OpenFont(font_path.encode('utf-8'), font_size)
    if not font:
        print("Failed to load the font: %s" % sdl2.sdlttf.TTF_GetError())
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

class Words:
    def __init__(self, filename):
        data = open(filename).read()
        self.words = data.split("\n")
        self.index = 0
        if len(self.words) <= 5:
            print("Not enough words in list file: %s" % (filename))
            sys.exit(1)

    def __len__(self):
        return len((self.words))
    
    def __getitem__(self, index):
        return self.words[index]
    
    def shuffle(self):
        random.shuffle(self.words)

    def next(self):
        if self.index < len(self.words):
            word = self.words[self.index]
            self.index += 1
            return word
        else:
            random.shuffle(self.words)
            self.index = 0
        return self.words[0]

class Game:
    mode = 0
    cur_time = 3
    timeout_t = 1000 * cur_time
    def __init__(self, window):
        self.renderer = sdl2.ext.Renderer(window)
        self.new_game()

    def new_game(self):
        self.words = Words("./nouns.txt")
        self.words.shuffle()
        self.text = "Press Space to Start Game"
        self.word_text = ""
        self.mode = 0
        self.timeout_t = 1000 * 15
        self.input_text = ""

       
    def draw(self, font):
        self.renderer.clear()
        if self.mode == 0:
            printtext(self.renderer, font, self.text, (255, 255, 255), (15, 15))
        elif self.mode == 1:
            printtext(self.renderer, font, self.word_text, (255, 0, 0), (15, 15))
            printtext(self.renderer, font, "Press Enter when ready to start countdown", (255, 255, 255), (15, 80))
        elif self.mode == 2:
            self.timeout_t = (sdl2.SDL_GetTicks()-self.start_ticks)/1000
            if self.timeout_t > self.cur_time:
                self.mode = 3
                self.cur_time += 1
                self.input_text = ""

            printtext(self.renderer, font, "%d"%(self.timeout_t), (255,255,255), (15,80))
        elif self.mode == 3:
            printtext(self.renderer, font, self.input_text + "_", (255, 255, 255), (15, 15))  
        elif self.mode == 4:
            printtext(self.renderer, font, "Correct! Press Space to Continue", (255,255,255), (15, 15))
        elif self.mode == 5:
            printtext(self.renderer, font, "Incorrect Game Over", (0,0,255),  (15,15))  
        self.renderer.present()
    
    def add_word(self):
        if len(self.word_text) == 0:
            self.word_text = self.words.next()
        else:
            self.word_text = self.word_text + " " + self.words.next()
    
    def timeout(self):
        pass

    def check_input(self):
        if self.input_text == self.word_text:
            self.mode = 4
        else:
            self.mode = 5

    def event(self, e):
        if self.mode == 0 or self.mode == 4 and e.type == sdl2.SDL_KEYDOWN and e.key.keysym.sym == sdl2.SDLK_SPACE:
            self.add_word()
            self.mode = 1
        elif self.mode == 1 and e.type == sdl2.SDL_KEYDOWN and e.key.keysym.sym == sdl2.SDLK_RETURN:
            self.start_ticks = sdl2.SDL_GetTicks()
            self.mode = 2
        elif self.mode == 3 and e.type == sdl2.SDL_KEYDOWN and e.key.keysym.sym == sdl2.SDLK_BACKSPACE and len(self.input_text) >= 1:
            self.input_text = self.input_text[0:len(self.input_text)-1]
        elif self.mode == 3 and e.type == sdl2.SDL_KEYDOWN and e.key.keysym.sym == sdl2.SDLK_RETURN and len(self.input_text) >= 1:
            self.check_input()
        elif self.mode == 3 and e.type == sdl2.SDL_KEYDOWN:
            self.input_text = self.input_text + chr(e.key.keysym.sym)
        elif self.mode == 5 and e.type == sdl2.SDL_KEYDOWN and e.key.keysym.sym == sdl2.SDLK_RETURN:
            self.new_game()
        

    def proc(event):
        pass

def main(args):
    timeout = 1000 * 10
    if len(args) >= 2:
        timeout = int(args[1])
    sdl2.ext.init()
    if sdl2.sdlttf.TTF_Init() == -1:
         print("TTF_Font: %s" % sdl2.sdlttf.TTF_GetError())
         return 1
    font = load_font("font.ttf", 24)

    window =  sdl2.ext.Window("Puzzle Game [ Python Edition ]", size=(1440, 1080))
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
        gameobj.timeout();
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

sys.exit(main(sys.argv))