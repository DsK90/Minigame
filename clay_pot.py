import pygame
import random
import math

class ClayPot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((139, 69, 19))  # Brown color for clay pot
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Pot properties
        self.health = 1
        self.destroyed = False
        
        # Visual properties
        self.crack_level = 0  # 0 = no cracks, 1 = some cracks, 2 = many cracks
    
    def take_damage(self, damage):
        """Take damage and potentially break"""
        self.health -= damage
        if self.health <= 0:
            self.destroyed = True
            return True  # Pot was destroyed
        return False
    
    def draw_clay_pot(self, screen):
        """Draw detailed clay pot sprite"""
        # Main pot body
        pot_color = (139, 69, 19)  # Brown
        pygame.draw.ellipse(screen, pot_color, 
                           (self.rect.centerx - 12, self.rect.centery - 8, 24, 16))
        
        # Pot rim
        pygame.draw.ellipse(screen, (101, 50, 14), 
                           (self.rect.centerx - 12, self.rect.centery - 10, 24, 6))
        
        # Pot base
        pygame.draw.ellipse(screen, (101, 50, 14), 
                           (self.rect.centerx - 10, self.rect.centery + 4, 20, 4))
        
        # Cracks based on damage
        if self.crack_level > 0:
            crack_color = (80, 40, 10)
            # Vertical crack
            pygame.draw.line(screen, crack_color, 
                           (self.rect.centerx, self.rect.centery - 6),
                           (self.rect.centerx, self.rect.centery + 2), 2)
            
            if self.crack_level > 1:
                # Horizontal crack
                pygame.draw.line(screen, crack_color, 
                               (self.rect.centerx - 6, self.rect.centery - 2),
                               (self.rect.centerx + 6, self.rect.centery - 2), 2)
        
        # Pot shine/highlight
        pygame.draw.ellipse(screen, (160, 100, 50), 
                           (self.rect.centerx - 8, self.rect.centery - 6, 8, 4))
    
    def update_crack_level(self):
        """Update crack level based on health"""
        if self.health <= 0.5:
            self.crack_level = 2
        elif self.health <= 0.8:
            self.crack_level = 1
        else:
            self.crack_level = 0
