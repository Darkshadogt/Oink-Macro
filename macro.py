import time
import threading
import pynput

class AutoClicker(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.intervalType = None
        self.positionType = None
        self.repeatType = None
        self.repeatCount = 1
        self.button = None
        self.clickType = "Single"
        self.position = None
        self.running = True
        self.started = False
        self.clicking = False

    def setButton(self, button):
        if button == "Left":
            self.button = pynput.mouse.Button.left
        elif button == "Middle":
            self.button = pynput.mouse.Button.middle
        elif button == "Right":
            self.button = pynput.mouse.Button.right

    def click(self, mouse, clicks):
        if self.positionType == "Fixed" and self.position:
            mouse.position = self.position
        mouse.click(self.button, clicks)
    
    def setSettings(self, **kwargs):
        self.setButton(kwargs.get("button", "Left"))
        self.positionType = kwargs.get("positionType", "Follow Mouse")
        self.repeatType = kwargs.get("repeatType", "Infinite")
        self.intervalType = kwargs.get("interval", 0.1)
        self.clickType = kwargs.get("clickType", "Single")
        self.repeatCount = kwargs.get("repeatCount", 1)
        self.position = kwargs.get("position", None)

    def run(self):
        mouse = pynput.mouse.Controller()
        while self.running:
            while self.clicking:
                if self.repeatType == "Finite":
                    for _ in range(self.repeatCount):
                        if not self.clicking:
                            break
                        self.click(mouse, 2 if self.clickType == "Double" else 1)
                        time.sleep(self.intervalType)
                    self.stop()
                else:
                    if not self.clicking:
                        break
                    self.click(mouse, 2 if self.clickType == "Double" else 1)
                    time.sleep(self.intervalType)
            time.sleep(0.1)


    def start(self, **kwargs):
        self.setSettings(**kwargs)
        if not self.started:
            super().start()
            self.started = True
        self.clicking = True

    def stop(self):
        self.clicking = False
    


    



