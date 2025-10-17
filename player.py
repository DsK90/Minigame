import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        self.image.fill((255, 192, 203, 100))  # Semi-transparent pink for anime character
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Player stats
        self.max_health = 100
        self.health = self.max_health
        self.speed = 3
        self.attack_damage = 25
        self.attack_range = 50
        self.attack_cooldown = 500  # milliseconds
        self.last_attack_time = 0
        
        # Movement
        self.velocity_x = 0
        self.velocity_y = 0
        self.facing_direction = 0  # 0=right, 1=down, 2=left, 3=up
        
        # Attack state
        self.is_attacking = False
        self.attack_duration = 200  # milliseconds
        self.attack_start_time = 0
        self.attack_rect = pygame.Rect(0, 0, 0, 0)
        
        # Lightning effect
        self.lightning_particles = []
        
        # Lightning upgrade system
        self.lightning_upgrades = []  # List of active upgrades
        self.base_attack_range = self.attack_range
        self.max_upgrades = 3
    
    def update(self, game):
        """Update player state"""
        self.handle_input()
        self.move(game)
        self.update_attack()
    
    def handle_input(self):
        """Handle keyboard input"""
        keys = pygame.key.get_pressed()
        
        # Reset velocity
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -self.speed
            self.facing_direction = 2
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = self.speed
            self.facing_direction = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity_y = -self.speed
            self.facing_direction = 3
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity_y = self.speed
            self.facing_direction = 1
    
    def move(self, game):
        """Move the player"""
        # Calculate new position
        new_x = self.rect.centerx + self.velocity_x
        new_y = self.rect.centery + self.velocity_y
        
        # Keep player on screen (updated for larger screen)
        new_x = max(12, min(1188, new_x))  # Adjusted for larger screen
        new_y = max(12, min(888, new_y))
        
        # Check if new position is on a road
        if game.is_on_road(new_x, new_y):
            self.rect.center = (new_x, new_y)
    
    def attack(self):
        """Start attack if cooldown is ready"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.is_attacking = True
            self.attack_start_time = current_time
            self.last_attack_time = current_time
            self.create_attack_rect()
            self.create_lightning_effect()
    
    def create_attack_rect(self):
        """Create attack hitbox based on facing direction"""
        attack_size = 40
        
        if self.facing_direction == 0:  # Right
            self.attack_rect = pygame.Rect(
                self.rect.centerx + 15, 
                self.rect.centery - attack_size//2,
                self.attack_range, 
                attack_size
            )
        elif self.facing_direction == 1:  # Down
            self.attack_rect = pygame.Rect(
                self.rect.centerx - attack_size//2,
                self.rect.centery + 15,
                attack_size,
                self.attack_range
            )
        elif self.facing_direction == 2:  # Left
            self.attack_rect = pygame.Rect(
                self.rect.centerx - 15 - self.attack_range,
                self.rect.centery - attack_size//2,
                self.attack_range,
                attack_size
            )
        elif self.facing_direction == 3:  # Up
            self.attack_rect = pygame.Rect(
                self.rect.centerx - attack_size//2,
                self.rect.centery - 15 - self.attack_range,
                attack_size,
                self.attack_range
            )
    
    def update_attack(self):
        """Update attack state"""
        if self.is_attacking:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_start_time >= self.attack_duration:
                self.is_attacking = False
                self.attack_rect = pygame.Rect(0, 0, 0, 0)
                self.lightning_particles.clear()
        
        # Update lightning particles
        self.update_lightning_particles()
        
        # Update lightning upgrades
        self.update_lightning_upgrades()
    
    def take_damage(self, damage):
        """Take damage"""
        self.health -= damage
        if self.health < 0:
            self.health = 0
    
    def draw_attack_range(self, screen):
        """Draw attack range indicator (for debugging)"""
        if self.is_attacking:
            pygame.draw.rect(screen, (255, 255, 0, 100), self.attack_rect)
    
    def draw_anime_face(self, screen):
        """Draw beautiful anime face on the character"""
        # Hair (pink anime hair)
        hair_color = (255, 182, 193)  # Light pink
        pygame.draw.circle(screen, hair_color, 
                         (self.rect.centerx, self.rect.centery - 8), 12)
        
        # Face outline
        pygame.draw.circle(screen, (255, 220, 177), 
                         (self.rect.centerx, self.rect.centery), 10)
        
        # Eyes with direction
        eye_offset = 4
        if self.facing_direction == 0:  # Right
            # Right eye
            pygame.draw.circle(screen, (255, 255, 255), 
                             (self.rect.centerx + eye_offset, self.rect.centery - 3), 3)
            pygame.draw.circle(screen, (0, 0, 0), 
                             (self.rect.centerx + eye_offset + 1, self.rect.centery - 3), 2)
            # Left eye (smaller, looking right)
            pygame.draw.circle(screen, (255, 255, 255), 
                             (self.rect.centerx - eye_offset, self.rect.centery - 3), 2)
            pygame.draw.circle(screen, (0, 0, 0), 
                             (self.rect.centerx - eye_offset + 1, self.rect.centery - 3), 1)
        elif self.facing_direction == 2:  # Left
            # Left eye
            pygame.draw.circle(screen, (255, 255, 255), 
                             (self.rect.centerx - eye_offset, self.rect.centery - 3), 3)
            pygame.draw.circle(screen, (0, 0, 0), 
                             (self.rect.centerx - eye_offset - 1, self.rect.centery - 3), 2)
            # Right eye (smaller, looking left)
            pygame.draw.circle(screen, (255, 255, 255), 
                             (self.rect.centerx + eye_offset, self.rect.centery - 3), 2)
            pygame.draw.circle(screen, (0, 0, 0), 
                             (self.rect.centerx + eye_offset - 1, self.rect.centery - 3), 1)
        else:  # Up/Down
            # Both eyes looking forward
            pygame.draw.circle(screen, (255, 255, 255), 
                             (self.rect.centerx - 3, self.rect.centery - 3), 3)
            pygame.draw.circle(screen, (0, 0, 0), 
                             (self.rect.centerx - 3, self.rect.centery - 3), 2)
            pygame.draw.circle(screen, (255, 255, 255), 
                             (self.rect.centerx + 3, self.rect.centery - 3), 3)
            pygame.draw.circle(screen, (0, 0, 0), 
                             (self.rect.centerx + 3, self.rect.centery - 3), 2)
        
        # Blush
        pygame.draw.circle(screen, (255, 182, 193), 
                         (self.rect.centerx - 6, self.rect.centery + 2), 2)
        pygame.draw.circle(screen, (255, 182, 193), 
                         (self.rect.centerx + 6, self.rect.centery + 2), 2)
        
        # Mouth (cute anime mouth)
        if self.facing_direction == 0:  # Right
            pygame.draw.arc(screen, (255, 105, 180), 
                           (self.rect.centerx + 6, self.rect.centery + 4, 6, 4),
                           0, 3.14, 2)
        elif self.facing_direction == 2:  # Left
            pygame.draw.arc(screen, (255, 105, 180), 
                           (self.rect.centerx - 12, self.rect.centery + 4, 6, 4),
                           0, 3.14, 2)
        else:  # Up/Down
            pygame.draw.arc(screen, (255, 105, 180), 
                           (self.rect.centerx - 3, self.rect.centery + 4, 6, 4),
                           0, 3.14, 2)
        
        # Hair details
        pygame.draw.arc(screen, (255, 182, 193), 
                       (self.rect.centerx - 8, self.rect.centery - 12, 16, 8),
                       0, 3.14, 2)
    
    def create_lightning_effect(self):
        """Create lightning particles for attack effect"""
        import random
        
        # Create multiple lightning bolts
        for _ in range(8):
            particle = {
                'x': self.rect.centerx,
                'y': self.rect.centery,
                'target_x': self.rect.centerx,
                'target_y': self.rect.centery,
                'life': 20,
                'max_life': 20,
                'segments': []
            }
            
            # Create lightning path based on facing direction
            if self.facing_direction == 0:  # Right
                particle['target_x'] += self.attack_range
                particle['target_y'] += random.randint(-20, 20)
            elif self.facing_direction == 1:  # Down
                particle['target_y'] += self.attack_range
                particle['target_x'] += random.randint(-20, 20)
            elif self.facing_direction == 2:  # Left
                particle['target_x'] -= self.attack_range
                particle['target_y'] += random.randint(-20, 20)
            else:  # Up
                particle['target_y'] -= self.attack_range
                particle['target_x'] += random.randint(-20, 20)
            
            # Create jagged lightning path
            self.create_lightning_path(particle)
            self.lightning_particles.append(particle)
    
    def create_lightning_path(self, particle):
        """Create a jagged lightning path"""
        import random
        
        start_x, start_y = particle['x'], particle['y']
        end_x, end_y = particle['target_x'], particle['target_y']
        
        # Create 5-8 segments for jagged effect
        num_segments = random.randint(5, 8)
        segment_length = ((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5 / num_segments
        
        current_x, current_y = start_x, start_y
        particle['segments'] = [(current_x, current_y)]
        
        for i in range(num_segments):
            # Calculate direction to target
            dx = end_x - current_x
            dy = end_y - current_y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            if distance > 0:
                # Normalize and add randomness
                dx = dx / distance * segment_length
                dy = dy / distance * segment_length
                
                # Add random offset for jagged effect
                dx += random.randint(-15, 15)
                dy += random.randint(-15, 15)
                
                current_x += dx
                current_y += dy
                particle['segments'].append((current_x, current_y))
        
        # Ensure we reach the target
        particle['segments'].append((end_x, end_y))
    
    def update_lightning_particles(self):
        """Update lightning particle effects"""
        for particle in self.lightning_particles[:]:
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.lightning_particles.remove(particle)
    
    def draw_lightning_effect(self, screen):
        """Draw lightning attack effect"""
        for particle in self.lightning_particles:
            if len(particle['segments']) > 1:
                # Calculate alpha based on life
                alpha = int(255 * (particle['life'] / particle['max_life']))
                
                # Draw lightning bolt segments
                for i in range(len(particle['segments']) - 1):
                    start_x, start_y = particle['segments'][i]
                    end_x, end_y = particle['segments'][i + 1]
                    
                    # Create surface for alpha blending
                    lightning_surface = pygame.Surface((abs(end_x - start_x) + 10, abs(end_y - start_y) + 10), pygame.SRCALPHA)
                    
                    # Draw lightning segment with glow effect
                    pygame.draw.line(lightning_surface, (100, 150, 255, alpha), 
                                   (5, 5), (end_x - start_x + 5, end_y - start_y + 5), 3)
                    pygame.draw.line(lightning_surface, (150, 200, 255, alpha), 
                                   (5, 5), (end_x - start_x + 5, end_y - start_y + 5), 1)
                    
                    screen.blit(lightning_surface, (min(start_x, end_x) - 5, min(start_y, end_y) - 5))
                
                # Draw spark effects at endpoints
                for i in [0, -1]:  # Start and end points
                    x, y = particle['segments'][i]
                    spark_alpha = int(alpha * 0.7)
                    
                    # Create spark surface
                    spark_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
                    pygame.draw.circle(spark_surface, (200, 220, 255, spark_alpha), (10, 10), 8)
                    pygame.draw.circle(spark_surface, (255, 255, 255, spark_alpha), (10, 10), 4)
                    pygame.draw.circle(spark_surface, (150, 200, 255, spark_alpha), (10, 10), 2)
                    
                    screen.blit(spark_surface, (x - 10, y - 10))
    
    def add_lightning_upgrade(self):
        """Add a lightning upgrade (max 3 stacks)"""
        if len(self.lightning_upgrades) < self.max_upgrades:
            current_time = pygame.time.get_ticks()
            upgrade = {
                'start_time': current_time,
                'duration': 4000,  # 4 seconds
                'level': len(self.lightning_upgrades) + 1
            }
            self.lightning_upgrades.append(upgrade)
            self.update_attack_range()
    
    def update_lightning_upgrades(self):
        """Update active lightning upgrades"""
        current_time = pygame.time.get_ticks()
        
        # Remove expired upgrades
        self.lightning_upgrades = [upgrade for upgrade in self.lightning_upgrades 
                                 if current_time - upgrade['start_time'] < upgrade['duration']]
        
        # Update attack range based on active upgrades
        self.update_attack_range()
    
    def update_attack_range(self):
        """Update attack range based on active upgrades"""
        upgrade_count = len(self.lightning_upgrades)
        if upgrade_count > 0:
            # Increase range by 50% per upgrade (max 150% increase)
            range_multiplier = 1.0 + (upgrade_count * 0.5)
            self.attack_range = int(self.base_attack_range * range_multiplier)
        else:
            self.attack_range = self.base_attack_range
    
    def get_upgrade_level(self):
        """Get current upgrade level"""
        return len(self.lightning_upgrades)
    
    def draw_upgrade_indicator(self, screen):
        """Draw upgrade indicator on screen"""
        if self.lightning_upgrades:
            upgrade_count = len(self.lightning_upgrades)
            
            # Draw upgrade indicator in top-right corner
            indicator_x = 1150  # Near right edge
            indicator_y = 50
            
            # Background
            pygame.draw.rect(screen, (0, 0, 0, 150), 
                           (indicator_x - 10, indicator_y - 10, 60, 30))
            
            # Upgrade text
            font = pygame.font.Font(None, 24)
            upgrade_text = font.render(f"Lightning x{upgrade_count}", True, (100, 150, 255))
            screen.blit(upgrade_text, (indicator_x, indicator_y))
            
            # Time remaining bar
            if self.lightning_upgrades:
                oldest_upgrade = min(self.lightning_upgrades, key=lambda x: x['start_time'])
                current_time = pygame.time.get_ticks()
                time_remaining = oldest_upgrade['duration'] - (current_time - oldest_upgrade['start_time'])
                time_remaining = max(0, time_remaining)
                
                bar_width = 50
                bar_height = 4
                bar_fill = (time_remaining / oldest_upgrade['duration']) * bar_width
                
                # Background bar
                pygame.draw.rect(screen, (50, 50, 50), 
                               (indicator_x, indicator_y + 15, bar_width, bar_height))
                # Fill bar
                pygame.draw.rect(screen, (100, 150, 255), 
                               (indicator_x, indicator_y + 15, bar_fill, bar_height))
