import sdl2

class GameObject:
    def __init__(self, obj):
        self.obj = obj
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) < 0:
            print("Error initializing SDL:", sdl2.SDL_GetError())
            return -1

        self.window = sdl2.SDL_CreateWindow(self.obj.title, sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, self.obj.w, self.obj.h, sdl2.SDL_WINDOW_SHOWN)
        if not self.window:
            print("Error creating window:", sdl2.SDL_GetError())
            sdl2.SDL_Quit()
            return -1

        self.renderer = sdl2.SDL_CreateRenderer(self.window, -1, sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC)
        if not self.renderer:
            print("Error creating renderer:", sdl2.SDL_GetError())
            sdl2.SDL_DestroyWindow(self.window)
            sdl2.SDL_Quit()
            return -1
        self.obj.init()

    def loop(self):
        running = True
        while running:
            event = sdl2.SDL_Event()
            while sdl2.SDL_PollEvent(event):
                if event.type == sdl2.SDL_QUIT:
                    running = False
                elif event.type == sdl2.SDL_KEYDOWN and event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    running = False
                else:
                    self.obj.event(event)
        
        sdl2.SDL_SetRenderDrawColor(self.renderer, 0, 0, 0, 255)
        sdl2.SDL_RenderClear(self.renderer)
        self.obj.render(self.renderer)
        sdl2.SDL_RenderPresent(self.renderer)

    def cleanup(self):
        sdl2.SDL_DestroyRenderer(self.renderer)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()




        