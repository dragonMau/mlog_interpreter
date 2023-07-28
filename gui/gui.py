import structure
import editor

class Application:
    def __init__(self) -> None:
        self.window = structure.Window()
        self.editor = editor.Editor(self.window.container1_1)

    def mainloop(self):
        self.window.mainloop()
        
app = Application()
app.mainloop()