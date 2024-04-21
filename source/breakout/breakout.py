# in progress

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
        self.reset()
    def reset(self):
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
    def is_empty(self):  
        for row in self.grid:
            if any(cell != 0 for cell in row):
                return False
        return True

class Ball:
    def __init__(self):
        self.lives = 4
        self.reset()
        self.score = 0
        self.lives = 4

    def reset(self):
        self.x = 1440 // 2
        self.y = 1080 // 2 - 50  
        self.vx = random.choice([-5, 5])  
        self.vy = -5
        self.lives -= 1


    def draw(self, renderer):
        rect = sdl2.SDL_Rect(int(self.x), int(self.y), 16, 16)
        color = (255, 255, 255)
        sdl2.SDL_SetRenderDrawColor(renderer.sdlrenderer, color[0], color[1], color[2], 255)
        sdl2.SDL_RenderFillRect(renderer.sdlrenderer, rect)

    def update(self, paddle, grid):
        self.x += self.vx
        self.y += self.vy

        if self.x <= 0 or self.x >= 1440 - 16:
            self.vx = -self.vx

        if self.y <= 0:
            self.vy = -self.vy

        if self.y > paddle.y + 25:
            if self.y > 1080:
                self.reset()
            return  

        if (self.x + 16 >= paddle.x and self.x <= paddle.x + paddle.width) and (self.y + 16 >= paddle.y):
            self.vy = -self.vy  

        for x in range(grid.cols):
            for y in range(grid.rows):
                brick = grid.grid[x][y]
                if brick > 0:
                    brick_x = x * 32
                    brick_y = y * 16
                    if (self.x + 16 > brick_x and self.x < brick_x + 32) and (self.y + 16 > brick_y and self.y < brick_y + 16):
                        self.vy = -self.vy  
                        grid.grid[x][y] = 0  
                        self.score += 100

        if self.y > 1080:
            self.reset()

