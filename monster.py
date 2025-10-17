import pygame
import math
import random

class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, target_player):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 50))  # Semi-transparent white for ghost
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Monster stats (will be updated based on level)
        self.max_health = 30
        self.health = self.max_health
        self.speed = 1.5
        self.damage = 15
        self.attack_cooldown = 1000  # milliseconds
        self.last_attack_time = 0
        self.level = 1  # Will be set by game
        
        # Contact damage system
        self.contact_timer = 0  # Time in contact with player
        self.contact_duration = 1000  # 1 second in milliseconds
        self.is_in_contact = False
        
        # AI
        self.target = target_player
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Monster type for variety
        self.monster_type = random.randint(0, 2)
        self.setup_monster_type()
        
        # Apply level-based scaling
        self.apply_level_scaling()
    
    def setup_monster_type(self):
        """Setup different monster types (base stats, will be scaled by level)"""
        if self.monster_type == 0:  # Fast, low health
            self.base_health = 20
            self.base_speed = 2.5
            self.base_damage = 10
            self.color = (240, 240, 240, 60)  # Light white ghost
        elif self.monster_type == 1:  # Slow, high health
            self.base_health = 50
            self.base_speed = 1.0
            self.base_damage = 20
            self.color = (220, 220, 220, 60)  # Darker white ghost
        else:  # Balanced
            self.base_health = 30
            self.base_speed = 1.5
            self.base_damage = 15
            self.color = (255, 255, 255, 60)  # Pure white ghost
    
    def set_level(self, level):
        """Set the monster level and apply scaling"""
        self.level = level
        self.apply_level_scaling()
    
    def apply_level_scaling(self):
        """Apply level-based scaling to monster stats"""
        # Health scaling: 2 hits from level 2, 3 hits from level 5, etc.
        if self.level >= 5:
            hits_required = 3 + ((self.level - 5) // 3)  # 3 hits at level 5, 4 at level 8, etc.
        elif self.level >= 2:
            hits_required = 2 + ((self.level - 2) // 3)  # 2 hits at level 2, 3 at level 5
        else:
            hits_required = 1  # 1 hit for level 1
        
        # Calculate health based on hits required (assuming 25 damage per hit)
        # Use base health as multiplier for monster type variety
        health_multiplier = self.base_health / 25  # Normalize base health
        self.max_health = int(hits_required * 25 * health_multiplier)
        self.health = self.max_health
        
        # Speed scaling: slightly faster with each level
        self.speed = self.base_speed + (self.level * 0.1)
        
        # Damage scaling: more damage with each level
        self.damage = self.base_damage + (self.level * 2)
        
        # Visual scaling: larger and more intense with level
        size_increase = min(self.level * 2, 10)  # Max 10 pixel increase
        self.image = pygame.Surface((20 + size_increase, 20 + size_increase), pygame.SRCALPHA)
        
        # Color intensity based on level
        if self.level >= 5:
            # High level ghosts are more intense
            r, g, b, a = self.color
            self.image.fill((min(255, r + 15), min(255, g + 15), min(255, b + 15), min(255, a + 20)))
        else:
            # Standard colors for lower levels
            self.image.fill(self.color)
    
    def update(self, game):
        """Update monster state"""
        self.move_towards_player()
        self.move(game)
    
    def move_towards_player(self):
        """Calculate movement towards player"""
        if self.target:
            # Calculate direction to player
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:  # Avoid division by zero
                # Normalize direction and apply speed
                self.velocity_x = (dx / distance) * self.speed
                self.velocity_y = (dy / distance) * self.speed
            else:
                self.velocity_x = 0
                self.velocity_y = 0
    
    def move(self, game):
        """Move the monster (ghosts can move everywhere)"""
        new_x = self.rect.centerx + self.velocity_x
        new_y = self.rect.centery + self.velocity_y
        
        # Keep monster on screen (updated for larger screen)
        new_x = max(12, min(1188, new_x))
        new_y = max(12, min(888, new_y))
        
        # Ghosts can move anywhere (no road restriction)
        self.rect.center = (new_x, new_y)
    
    def take_damage(self, damage):
        """Take damage"""
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def can_attack(self):
        """Check if monster can attack"""
        current_time = pygame.time.get_ticks()
        return current_time - self.last_attack_time >= self.attack_cooldown
    
    def start_contact(self):
        """Start contact with player"""
        if not self.is_in_contact:
            self.is_in_contact = True
            self.contact_timer = 0
    
    def end_contact(self):
        """End contact with player"""
        self.is_in_contact = False
        self.contact_timer = 0
    
    def update_contact(self, dt):
        """Update contact timer and check for death"""
        if self.is_in_contact:
            self.contact_timer += dt
            if self.contact_timer >= self.contact_duration:
                # Monster dies after 1 second of contact
                self.health = 0
                return True  # Monster died
        return False  # Monster still alive
    
    def get_contact_damage(self):
        """Get contact damage based on monster strength/type"""
        # Different monster types inflict different contact damage
        if self.monster_type == 0:  # Fast, low health monsters
            return 10
        elif self.monster_type == 1:  # Slow, high health monsters
            return 20
        else:  # Balanced monsters
            return 15
    
    def draw_anime_face(self, screen):
        """Draw beautiful ghost sprite"""
        # Ghost body (wavy bottom)
        ghost_body = pygame.Surface((25, 25), pygame.SRCALPHA)
        
        # Main ghost body
        pygame.draw.circle(ghost_body, (255, 255, 255, 200), (12, 8), 8)
        
        # Wavy bottom
        wavy_points = []
        for i in range(8):
            x = 4 + i * 2
            y = 16 + math.sin(i * 0.8) * 3
            wavy_points.append((x, y))
        wavy_points.append((20, 16))
        wavy_points.append((12, 8))
        pygame.draw.polygon(ghost_body, (255, 255, 255, 200), wavy_points)
        
        # Eyes (glowing and expressive)
        eye_color = (100, 150, 255)
        eye_glow = (150, 200, 255)
        
        # Left eye
        pygame.draw.circle(ghost_body, eye_glow, (8, 6), 3)
        pygame.draw.circle(ghost_body, eye_color, (8, 6), 2)
        pygame.draw.circle(ghost_body, (255, 255, 255), (8, 5), 1)
        
        # Right eye
        pygame.draw.circle(ghost_body, eye_glow, (16, 6), 3)
        pygame.draw.circle(ghost_body, eye_color, (16, 6), 2)
        pygame.draw.circle(ghost_body, (255, 255, 255), (16, 5), 1)
        
        # Mouth (ghostly expression)
        mouth_points = []
        for i in range(7):
            x = 8 + i * 1.5
            y = 10 + math.sin(i * 0.7) * 1.5
            mouth_points.append((x, y))
        pygame.draw.lines(ghost_body, (200, 200, 200, 150), False, mouth_points, 2)
        
        # Blit the ghost body
        screen.blit(ghost_body, (self.rect.centerx - 12, self.rect.centery - 12))
        
        # Ghostly aura effect
        aura = pygame.Surface((35, 35), pygame.SRCALPHA)
        pygame.draw.circle(aura, (255, 255, 255, 30), (17, 17), 17)
        pygame.draw.circle(aura, (200, 220, 255, 20), (17, 17), 12)
        screen.blit(aura, (self.rect.centerx - 17, self.rect.centery - 17))
        
        # Floating particles
        import time
        current_time = time.time()
        for i in range(3):
            particle_x = self.rect.centerx + math.sin(current_time + i) * 15
            particle_y = self.rect.centery + math.cos(current_time + i) * 15
            pygame.draw.circle(screen, (255, 255, 255, 100), 
                             (int(particle_x), int(particle_y)), 1)
        
        # Contact indicator (red glow when in contact)
        if self.is_in_contact:
            contact_glow = pygame.Surface((40, 40), pygame.SRCALPHA)
            # Intensity based on contact timer
            intensity = min(255, 100 + (self.contact_timer / self.contact_duration) * 155)
            pygame.draw.circle(contact_glow, (255, 0, 0, int(intensity)), (20, 20), 20)
            screen.blit(contact_glow, (self.rect.centerx - 20, self.rect.centery - 20))
    
    def draw_health_bar(self, screen):
        """Draw health bar above monster"""
        if self.health < self.max_health:
            bar_width = 30
            bar_height = 4
            bar_x = self.rect.centerx - bar_width // 2
            bar_y = self.rect.top - 10
            
            # Background
            pygame.draw.rect(screen, (255, 0, 0), 
                           (bar_x, bar_y, bar_width, bar_height))
            
            # Health
            health_width = (self.health / self.max_health) * bar_width
            pygame.draw.rect(screen, (0, 255, 0), 
                           (bar_x, bar_y, health_width, bar_height))
