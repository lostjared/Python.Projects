import sys
import sdl2
import sdl2.ext
import random
import copy

class PuzzlePiece:
    def __init__(self):
          self.blocks = [0, 0, 0]
          self.x = 0
          self.y = 0
          self.mode = 0


    def reset_piece(self):
          self.blocks = [0, 0, 0]
          while self.blocks[0] == self.blocks[1] and self.blocks[0] == self.blocks[2]:
            self.blocks[0] = random.randint(1, 6)
            self.blocks[1] = random.randint(1, 6)
            self.blocks[2] = random.randint(1, 6)
          self.x = 3
          self.y = 0
          self.mode = 0

    def shift_blocks(self):
         tblock = copy.deepcopy(self.blocks)
         self.blocks[0] = tblock[2]
         self.blocks[1] = tblock[0]
         self.blocks[2] = tblock[1]

    def intToColor(self, i):
         if i == 0:
              return (0, 0, 0)
         elif i == 1:
              return (0,255,0)
         elif i == 2:
              return (0,0,255)
         elif i == 3:
              return (255,0,255)
         elif i == 4:
              return (255,255,0)
         elif i == 5:
              return (255,0, 0)
         else:
              return (0, 255, 255)
     


     
class PuzzleGrid:
    def __init__(self,rend, cols, rows, offset_x, offset_y):
          self.piece = PuzzlePiece()
          self.piece.reset_piece()
          self.rend = rend
          self.w = cols
          self.h = rows
          self.off_x = offset_x
          self.off_y = offset_y
          self.puzzle_grid = [[0 for _ in range(rows)] for _ in range(cols)]
          
    def draw(self):
        rect = sdl2.SDL_Rect(self.off_x, self.off_y, self.w*(32*3), self.h*(16*3))
        sdl2.SDL_SetRenderDrawColor(self.rend.sdlrenderer, 255,255,255,255)
        sdl2.SDL_RenderFillRect(self.rend.renderer, rect)
        for x1 in range(0, self.w):
           for y1 in range(0, self.h):
                rect = sdl2.SDL_Rect(self.off_x+(x1*(32*3))+1, self.off_y+(y1*(16*3))+1, 32*3-2, 14*3-2)
                colorval = self.piece.intToColor(self.puzzle_grid[x1][y1])
                sdl2.SDL_SetRenderDrawColor(self.rend.sdlrenderer, colorval[0], colorval[1], colorval[2], 255)
                sdl2.SDL_RenderFillRect(self.rend.sdlrenderer, rect)           
        self.draw_piece()
        
    def draw_piece(self):
        rect1 = sdl2.SDL_Rect(self.off_x+(self.piece.x*(32*3)), self.off_y+(self.piece.y*(16*3)), 32*3, 16*3)
        rect2 = sdl2.SDL_Rect(self.off_x+(self.piece.x*(32*3)), self.off_y+(self.piece.y+1*(16*3)), 32*3, 16*3)
        rect3 = sdl2.SDL_Rect(self.off_x+(self.piece.x*(32*3)), self.off_y+(self.piece.y+2*(16*3)), 32*3, 16*3)
        color1 = self.piece.intToColor(self.piece.blocks[0])
        color2 = self.piece.intToColor(self.piece.blocks[1])
        color3 = self.piece.intToColor(self.piece.blocks[2])

        sdl2.SDL_SetRenderDrawColor(self.rend.sdlrenderer, color1[0], color1[1], color1[2], 255)
        sdl2.SDL_RenderFillRect(self.rend.sdlrenderer, rect1)
        sdl2.SDL_SetRenderDrawColor(self.rend.sdlrenderer, color2[0], color2[1], color2[2], 255)
        sdl2.SDL_RenderFillRect(self.rend.sdlrenderer, rect2)
        sdl2.SDL_SetRenderDrawColor(self.rend.sdlrenderer, color3[0], color3[1], color3[2], 255)
        sdl2.SDL_RenderFillRect(self.rend.sdlrenderer, rect3)
        
    def proc(self):
          pass
    
    def move_left(self):
         
         if(self.piece.x > 0):
              self.piece.x -= 1



         pass
    def move_right(self):
         
         if(self.piece.x < 7):
              self.piece.x += 1

         pass
     
class Game:
    def __init__(self, window):
          self.renderer = sdl2.ext.Renderer(window)
          self.grid = PuzzleGrid(self.renderer, 8, 17,325, 25)
    def draw(self):
        rect = sdl2.SDL_Rect(0, 0, 1440, 1080)
        sdl2.SDL_SetRenderDrawColor(self.renderer.sdlrenderer, 0, 0, 0, 255)
        self.renderer.clear()
        self.grid.draw()
        self.renderer.present()

    def event(self, event):
          if(event.type == sdl2.SDL_KEYDOWN):
                if(event.key.keysym.sym == sdl2.SDLK_LEFT):
                    self.move_left()
                elif(event.key.keysym.sym == sdl2.SDLK_RIGHT):
                    self.move_right()
                elif(event.key.keysym.sym == sdl2.SDLK_UP):
                     self.shift()
                    
    def move_left(self):
        self.grid.move_left()
        pass
    def move_right(self):
        self.grid.move_right()
        pass
    def shift(self):
         self.grid.piece.shift_blocks()

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
