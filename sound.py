import pygame
import threading

class Sound:
    def __init__(self,audio_path:str):
        pygame.mixer.init()
        self.audio = pygame.mixer.music
        self.audio.load(audio_path)
    @staticmethod
    def play_audio_func(audio:pygame.mixer.music):audio.play()

    def play(self) -> None:
        thread = threading.Thread(target= self.play_audio_func,args= (self.audio,))
        thread.daemon = True
        thread.start()