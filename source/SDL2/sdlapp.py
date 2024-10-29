import sdl2
import sys

def main(args):
    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) < 0:
        print("Error initializing SDL:", sdl2.SDL_GetError())
        return -1

    window = sdl2.SDL_CreateWindow(b"SDL2 Window", sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, 800, 600, sdl2.SDL_WINDOW_SHOWN)
    if not window:
        print("Error creating window:", sdl2.SDL_GetError())
        sdl2.SDL_Quit()
        return -1

    renderer = sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC)
    if not renderer:
        print("Error creating renderer:", sdl2.SDL_GetError())
        sdl2.SDL_DestroyWindow(window)
        sdl2.SDL_Quit()
        return -1

    running = True
    while running:
        event = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(event):
            if event.type == sdl2.SDL_QUIT:
                running = False
            elif event.type == sdl2.SDL_KEYDOWN and event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                running = False

        sdl2.SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255)
        sdl2.SDL_RenderClear(renderer)
        sdl2.SDL_RenderPresent(renderer)

    sdl2.SDL_DestroyRenderer(renderer)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()
    return 0

sys.exit(main(sys.argv))