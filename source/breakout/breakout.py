import sdl2;
import sdl2.ext;
import random

grid_width = 1440/32
grid_height = (1080/4)/16


class Paddle:
    def __init__(self):
        self.width = 200
        self.y = int((1080/2)+300)
        self.x = int(1440/2-(self.width/2))
    def draw(self, renderer):
        rect = sdl2.SDL_Rect(self.x, self.y, self.width, 25)
        color = (255,255,255)
        sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, color[0], color[1], color[2], 255)
        sdl2.SDL_RenderFillRect(renderer.sdlrenderer, rect)
    def move_left(self):
        if self.x > 10:
            self.x -= 10
    def move_right(self):
        if self.x+self.width < 1440-10:
            self.x += 10     

class Grid:
    def __init__(self, width, height):
        self.rows = int(height)
        self.cols = int(width)
        self.grid = [[0 for _ in range(self.rows)] for _ in range(self.cols)]
        for i in range(self.cols):
            for z in range(self.rows):
                self.grid[i][z] = random.randint(0, 5)

    def to_color(self, index):
        if index == 0:
            return (0, 0, 0)
        elif index == 1:
            return (255, 0, 0)
        elif index == 2:
            return (255,  255, 0)
        elif index == 3:
            return  (0, 255, 0)
        elif index == 4:
            return (0, 0, 255)
        else:
            return (255, 0, 255)

    def draw(self, renderer): 
        for x in range(self.cols):
            for y in range(self.rows):
                rect = sdl2.SDL_Rect(x*32, y*16, 32, 16)
                color = self.to_color(self.grid[x][y])
                sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, color[0], color[1], color[2], 255)
                sdl2.SDL_RenderFillRect(renderer.sdlrenderer, rect)
     
class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = int(1440/2)
        self.y = int(1080/2)
        self.dir = random.randint(0, 5)
        self.speed = 5

    def draw(self, renderer):
        rect = sdl2.SDL_Rect(self.x, self.y, 16, 16)
        color = (255,255,255)
        sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, color[0], color[1], color[2], 255)
        sdl2.SDL_RenderFillRect(renderer.sdlrenderer, rect)

    def proc(self, grid):
        if self.dir == 0:
            self.y += self.speed
            if self.y > 1080:
                self.reset()