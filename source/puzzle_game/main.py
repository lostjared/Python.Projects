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
         if i < 0:
              return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
         elif i == 0:
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
    score = 0
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
        sdl2.SDL_RenderFillRect(self.rend.sdlrenderer, rect)
        for x1 in range(0, self.w):
           for y1 in range(0, self.h):
                rect = sdl2.SDL_Rect(self.off_x+(x1*(32*3))+1, self.off_y+(y1*(16*3))+1, 32*3-2, 14*3-2)
                colorval = self.piece.intToColor(self.puzzle_grid[x1][y1])
                sdl2.SDL_SetRenderDrawColor(self.rend.sdlrenderer, colorval[0], colorval[1], colorval[2], 255)
                sdl2.SDL_RenderFillRect(self.rend.sdlrenderer, rect)           
        self.draw_piece()
        
    def draw_piece(self):
        self.chk_blocks()
        rect1 = sdl2.SDL_Rect(self.off_x+(self.piece.x*(32*3)), self.off_y+(self.piece.y*(16*3)), 32*3, 16*3)
        rect2 = sdl2.SDL_Rect(self.off_x+(self.piece.x*(32*3)), self.off_y+((self.piece.y+1)*(16*3)), 32*3, 16*3)
        rect3 = sdl2.SDL_Rect(self.off_x+(self.piece.x*(32*3)), self.off_y+((self.piece.y+2)*(16*3)), 32*3, 16*3)
        color1 = self.piece.intToColor(self.piece.blocks[0])
        color2 = self.piece.intToColor(self.piece.blocks[1])
        color3 = self.piece.intToColor(self.piece.blocks[2])

        sdl2.SDL_SetRenderDrawColor(self.rend.sdlrenderer, color1[0], color1[1], color1[2], 255)
        sdl2.SDL_RenderFillRect(self.rend.sdlrenderer, rect1)
        sdl2.SDL_SetRenderDrawColor(self.rend.sdlrenderer, color2[0], color2[1], color2[2], 255)
        sdl2.SDL_RenderFillRect(self.rend.sdlrenderer, rect2)
        sdl2.SDL_SetRenderDrawColor(self.rend.sdlrenderer, color3[0], color3[1], color3[2], 255)
        sdl2.SDL_RenderFillRect(self.rend.sdlrenderer, rect3)
        

    def test_piece(self, x, y):
         if(x < self.w and y < self.h and self.puzzle_grid[x][y] == 0 and self.puzzle_grid[x][y+1] == 0 and self.puzzle_grid[x][y+2] == 0):
              return True
         return False

    def test_block(self, x, y, color):
         if (x >= 0 and y >= 0 and x < 8 and y < 17 and self.puzzle_grid[x][y] >= 1 and self.puzzle_grid[x][y] == color):
              return True
         return False

    def chk_blocks(self):
        for x in range(0, self.w):
              for y in range(0, self.h):
                   if self.puzzle_grid[x][y] < 0:
                        self.puzzle_grid[x][y] -= 1
                        if self.puzzle_grid[x][y] < -200:
                             self.puzzle_grid[x][y] = 0
         

        for x in range(0, self.w):
              for y in range(0, self.h):
                color = self.puzzle_grid[x][y]
                if color >= 1:
                    if self.test_block(x, y+1, color)  and self.test_block(x, y+2, color):
                         self.puzzle_grid[x][y] = -1
                         self.puzzle_grid[x][y+1] = -1
                         self.puzzle_grid[x][y+2] = -1
                         self.score += 1
                         if self.test_block(x, y+3, color):
                              self.puzzle_grid[x][y+3] = -1
                    if self.test_block(x+1, y, color) and self.test_block(x+2, y, color):
                             self.puzzle_grid[x][y] = -1
                             self.puzzle_grid[x+1][y] = -1
                             self.puzzle_grid[x+2][y] = -1
                             self.score += 1
                             if self.test_block(x+3, y, color):
                                  self.puzle_grid[x][y+3] = -1



              
                    
    def proc(self):
           self.move_down()
    
    def move_left(self):    
         if(self.piece.x > 0 and self.test_piece(self.piece.x-1, self.piece.y)):
              self.piece.x -= 1
    def move_right(self):
         if(self.piece.x < 7 and self.test_piece(self.piece.x+1, self.piece.y)):
              self.piece.x += 1
    def move_down(self):
        if(self.piece.y < 14 and self.test_piece(self.piece.x, self.piece.y+1)):
              self.piece.y += 1
        else:
              self.set()

    def set(self):
         self.puzzle_grid[self.piece.x][self.piece.y] = self.piece.blocks[0]
         self.puzzle_grid[self.piece.x][self.piece.y+1] = self.piece.blocks[1]
         self.puzzle_grid[self.piece.x][self.piece.y+2] = self.piece.blocks[2]
         self.piece.reset_piece()


class Game:
    def __init__(self, window):
          self.renderer = sdl2.ext.Renderer(window)
          self.grid = PuzzleGrid(self.renderer, 8, 17,325, 25)
          self.speed = 1000

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
                elif(event.key.keysym.sym == sdl2.SDLK_DOWN):
                     self.down()
                    
    def move_left(self):
        self.grid.move_left()
    def move_right(self):
        self.grid.move_right()
    def shift(self):
         self.grid.piece.shift_blocks()
    def down(self):
         self.grid.move_down()
    def proc(self):
         self.grid.proc()


def main():
    sdl2.ext.init()
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

        gameobj.draw()
        nticks = sdl2.SDL_GetTicks()
        time_t += nticks-ticks
        ticks = nticks
        if(time_t > gameobj.speed):
             gameobj.proc()
             time_t = 0

        window.refresh()
    return 0

if __name__ == "__main__":
        sys.exit(main())
