import sys
import sdl2
import sdl2.ext

class PuzzlePiece:
     def __init__(self):
          self.blocks = [0, 0, 0]
          self.x = 0
          self.y = 0
          self.mode = 0
     def reset_piece(self):
          self.blocks = [0, 0, 0]
     
class PuzzleGrid:
     def __init__(self,rend, cols, rows, offset_x, offset_y):
          self.piece = PuzzlePiece()
          self.rend = rend
          self.w = cols
          self.h = rows
          self.off_x = offset_x
          self.off_y = offset_y
          self.puzzle_grid = [[0 for _ in range(cols)] for _ in range(rows)]

          
     def draw(self):
          for x1 in range(0, self.w):
               for y1 in range(0, self.h):
                    rect = sdl2.SDL_Rect(self.off_x+(x1*(32*3)), self.off_y+(y1*(16*3)), 32*3-2, 14*3-2)
                    sdl2.SDL_SetRenderDrawColor(self.rend.sdlrenderer, 255, 255, 255, 255)
                    sdl2.SDL_RenderFillRect(self.rend.sdlrenderer, rect)
        
     def proc(self):
          pass
     
class Game:
    def __init__(self, window):
          self.renderer = sdl2.ext.Renderer(window)
          self.grid = PuzzleGrid(self.renderer, 8, 17,325, 25)
    def draw(self):
        rect = sdl2.SDL_Rect(0, 0, 1440, 1080)
        sdl2.SDL_SetRenderDrawColor(self.renderer.sdlrenderer, 0, 0, 0, 255)
        self.renderer.clear()
         # sdl2.SDL_SetRenderDrawColor(self.renderer.sdlrenderer,255, 255, 255, 255)
        #  sdl2.SDL_RenderFillRect(self.renderer.sdlrenderer, rect)
        self.grid.draw()
        self.renderer.present()

    def event(self, event):
          if(event.type == sdl2.SDL_KEYDOWN):
                if(event.key.keysym.sym == sdl2.SDLK_LEFT):
                    self.move_left()
                elif(event.key.keysym.sym == sdl2.SDLK_RIGHT):
                    self.move_right()
                    
    def move_left(self):
        print("move left")
        pass
    def move_right(self):
        print("move right")
        pass

def main():
    sdl2.ext.init()
    window =  sdl2.ext.Window("Puzzle Game [ Python Edition ]", 
size=(1440, 1080))
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

        gameobj.draw()
        window.refresh()
    return 0

if __name__ == "__main__":
        sys.exit(main())
