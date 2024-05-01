import sys
import tkinter as tk

def main(args):
    root_window = tk.Tk()
    root_window.title("Hello, World!")
    root_window.geometry("640x480")
    root_window.mainloop()
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
