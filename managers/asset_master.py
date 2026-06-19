import pygame
from pathlib import Path


class AssetMaster:
    def __init__(self):
        self._images =  {}
        self._sounds = {}
        self._base_path = Path(__file__).parent.parent / "assets"
        
    def get_image(self, path):
        if path in self._images: return self._images[path]
        
        full_path = self._base_path / "images" / path
        
        if not full_path.exists():
            raise FileNotFoundError(f"{full_path}")
        
        img = pygame.image.load(str(full_path))
        img = img.convert_alpha()

        self._images[path] = img
        return img
    
    def get_sound(self, path: str) -> pygame.mixer.Sound:
        if path in self._sounds: return self._sounds[path]
        
        full_path = self._base_path / "sounds" / path
        
        if not full_path.exists():
            raise FileNotFoundError(f"{full_path}")
        
        sound = pygame.mixer.Sound(str(full_path))
        self._sounds[path] = sound
        return sound
    
    def get_music_path(self, path: str) -> str:
        full_path = self._base_path / "music" / path
        
        if not full_path.exists():
            raise FileNotFoundError(f"{full_path}")
        
        return str(full_path)