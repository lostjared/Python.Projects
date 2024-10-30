# main.py
import sdl2
import sys
import skeleton

class Game:
    def __init__(self, title, w, h):
        self.title = title
        self.w = w
        self.h = h
        self.player1_y = h // 2 - 50
        self.player2_y = h // 2 - 50
        self.ball_x, self.ball_y = w // 2, h // 2
        self.ball_vel_x, self.ball_vel_y = 5, 5
        self.paddle_speed = 8
        self.paddle_width, self.paddle_height = 10, 100
        self.ball_size = 15
        self.ai_speed = 6
    
    def init(self):
        pass

    def event(self, event):
        if event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_UP:
                self.player1_y -= self.paddle_speed
            elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                self.player1_y += self.paddle_speed

        if self.player1_y < 0:
            self.player1_y = 0
        elif self.player1_y + self.paddle_height > self.h:
            self.player1_y = self.h - self.paddle_height

    def update(self):
        keys = sdl2.SDL_GetKeyboardState(None)
        if keys[sdl2.SDL_SCANCODE_UP]:
            self.player1_y -= self.paddle_speed
        if keys[sdl2.SDL_SCANCODE_DOWN]:
            self.player1_y += self.paddle_speed

        if self.player1_y < 0:
            self.player1_y = 0
        elif self.player1_y + self.paddle_height > self.h:
            self.player1_y = self.h - self.paddle_height

        self.ball_x += self.ball_vel_x
        self.ball_y += self.ball_vel_y

        if self.ball_y <= 0 or self.ball_y + self.ball_size >= self.h:
            self.ball_vel_y = -self.ball_vel_y

        if (self.ball_x <= self.paddle_width and 
            self.player1_y < self.ball_y < self.player1_y + self.paddle_height):
            self.ball_vel_x = -self.ball_vel_x
        elif (self.ball_x + self.ball_size >= self.w - self.paddle_width and 
              self.player2_y < self.ball_y < self.player2_y + self.paddle_height):
            self.ball_vel_x = -self.ball_vel_x

        if self.ball_x < 0 or self.ball_x > self.w:
            self.ball_x, self.ball_y = self.w // 2, self.h // 2
            self.ball_vel_x = -self.ball_vel_x

        if self.player2_y + self.paddle_height // 2 < self.ball_y:
            self.player2_y += self.ai_speed
        elif self.player2_y + self.paddle_height // 2 > self.ball_y:
            self.player2_y -= self.ai_speed

        if self.player2_y < 0:
            self.player2_y = 0
        elif self.player2_y + self.paddle_height > self.h:
            self.player2_y = self.h - self.paddle_height

    def render(self, renderer):
        sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
        sdl2.SDL_RenderClear(renderer)

        sdl2.SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255)
        player1_rect = sdl2.SDL_Rect(10, self.player1_y, self.paddle_width, self.paddle_height)
        player2_rect = sdl2.SDL_Rect(self.w - 20, self.player2_y, self.paddle_width, self.paddle_height)
        ball_rect = sdl2.SDL_Rect(self.ball_x, self.ball_y, self.ball_size, self.ball_size)

        sdl2.SDL_RenderFillRect(renderer, player1_rect)
        sdl2.SDL_RenderFillRect(renderer, player2_rect)
        sdl2.SDL_RenderFillRect(renderer, ball_rect)

        sdl2.SDL_RenderPresent(renderer)

def main(args):
    obj = skeleton.GameObject(Game(b"Pong", 640, 480))
    obj.loop()
    obj.cleanup()
    return 0

sys.exit(main(sys.argv))