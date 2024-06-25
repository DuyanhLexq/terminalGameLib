import threading
from pynput import keyboard
class Event:
    def __init__(self):
        self.KEYDOWN = "down"
        self.KEYUP = "up"
        self.key = ""
        self.thread = None
        self.type = ""

    # Function to handle key press event
    def on_press(self, key):
        try:
            self.type = self.KEYDOWN
            self.key = key.char
        except AttributeError:
            ...

    # Function to handle key release event
    def on_release(self, key):
        self.type = self.KEYUP
        self.key = ''

    # Function to start keyboard listener
    def keyBoard_listener(self) -> None:
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()

    # Function to listen for keyboard events
    def listen(self):
        self.thread = threading.Thread(target=self.keyBoard_listener)
        self.thread.start()

    # Function to stop listening for keyboard events
    def stop(self):
        self.thread.join()