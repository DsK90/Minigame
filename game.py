import pygame
import sys
import os
import random
import math

# Add current directory to Python path so we can import local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from player import Player
from monster import Monster
from clay_pot import ClayPot

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1200  # Increased from 800
SCREEN_HEIGHT = 900  # Increased from 600
FPS = 60
TILE_SIZE = 40  # Larger tiles for better visibility
ROAD_WIDTH = 1  # Roads are 1 tile wide for more challenge

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Anime Monster Fighter")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize audio
        self.init_audio()

        # Game state
        self.score = 0
        self.game_over = False
        self.current_map = 1
        self.font = pygame.font.Font(None, 36)

        # Audio state
        self.background_music_playing = False
        
        # Create player at center (will be adjusted to road position)
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.clay_pots = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        
        # Monster spawning
        self.monster_spawn_timer = 0
        self.monster_spawn_delay = 120  # frames (2 seconds at 60 FPS)
        
        # Clay pot spawning
        self.clay_pot_spawn_timer = 0
        self.clay_pot_spawn_delay = 300  # frames (5 seconds at 60 FPS)
        
        # Road system
        self.road_tiles = set()  # Set of (x, y) tuples for road positions
        self.map_exits = []  # List of exit positions
        self.create_dungeon_map()
        
        # Position player on a road tile
        self.position_player_on_road()
    
    def create_dungeon_map(self):
        """Create a dungeon-like road system"""
        self.road_tiles.clear()
        self.map_exits.clear()
        
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Random map selection for each level
        import random
        map_types = [1, 2, 3]  # Available map types
        selected_map = random.choice(map_types)
        
        if selected_map == 1:
            self.create_map_1(center_x, center_y)
        elif selected_map == 2:
            self.create_map_2(center_x, center_y)
        elif selected_map == 3:
            self.create_map_3(center_x, center_y)
        else:
            self.create_random_map(center_x, center_y)
    
    def create_map_1(self, center_x, center_y):
        """Create first dungeon map - fully connected maze"""
        # Create a fully connected maze with all paths reachable
        grid_size = 25  # Increased for larger screen
        start_x = center_x - (grid_size//2) * TILE_SIZE
        start_y = center_y - (grid_size//2) * TILE_SIZE
        
        # Create main horizontal corridors (all connected)
        for i in range(2, grid_size-2, 3):
            self.add_road_line(start_x + 2*TILE_SIZE, start_y + i*TILE_SIZE, 1, 0, grid_size-5)
        
        # Create main vertical corridors (all connected)
        for i in range(2, grid_size-2, 3):
            self.add_road_line(start_x + i*TILE_SIZE, start_y + 2*TILE_SIZE, 0, 1, grid_size-5)
        
        # Add connecting paths to ensure all areas are reachable
        for i in range(5, grid_size-2, 3):
            for j in range(5, grid_size-2, 3):
                self.add_road_line(start_x + i*TILE_SIZE, start_y + j*TILE_SIZE, 1, 0, 1)  # Short horizontal connectors
                self.add_road_line(start_x + i*TILE_SIZE, start_y + j*TILE_SIZE, 0, 1, 1)  # Short vertical connectors
        
        # Add single exit on a road tile
        exit_x = start_x + (grid_size-3)*TILE_SIZE
        exit_y = start_y + (grid_size-3)*TILE_SIZE
        self.map_exits = [(exit_x, exit_y)]
        
        # Ensure exit is on a road tile
        self.ensure_exits_on_roads()
    
    def create_map_2(self, center_x, center_y):
        """Create second dungeon map - connected spiral maze"""
        # Create a fully connected spiral maze
        grid_size = 21  # Increased for larger screen
        start_x = center_x - (grid_size//2) * TILE_SIZE
        start_y = center_y - (grid_size//2) * TILE_SIZE
        
        # Create outer ring (fully connected)
        self.add_road_line(start_x + 1*TILE_SIZE, start_y + 1*TILE_SIZE, 1, 0, 6)  # Top horizontal
        self.add_road_line(start_x + 6*TILE_SIZE, start_y + 1*TILE_SIZE, 0, 1, 6)  # Right vertical
        self.add_road_line(start_x + 6*TILE_SIZE, start_y + 6*TILE_SIZE, -1, 0, 6)  # Bottom horizontal
        self.add_road_line(start_x + 1*TILE_SIZE, start_y + 6*TILE_SIZE, 0, -1, 6)  # Left vertical
        
        # Create inner ring (fully connected)
        self.add_road_line(start_x + 3*TILE_SIZE, start_y + 3*TILE_SIZE, 1, 0, 2)  # Inner top
        self.add_road_line(start_x + 4*TILE_SIZE, start_y + 3*TILE_SIZE, 0, 1, 2)  # Inner right
        self.add_road_line(start_x + 4*TILE_SIZE, start_y + 4*TILE_SIZE, -1, 0, 2)  # Inner bottom
        self.add_road_line(start_x + 3*TILE_SIZE, start_y + 4*TILE_SIZE, 0, -1, 2)  # Inner left
        
        # Add multiple connecting paths to ensure full connectivity
        self.add_road_line(start_x + 2*TILE_SIZE, start_y + 3*TILE_SIZE, 0, 1, 1)  # Connect outer to inner
        self.add_road_line(start_x + 5*TILE_SIZE, start_y + 3*TILE_SIZE, 0, 1, 1)  # Connect outer to inner
        self.add_road_line(start_x + 3*TILE_SIZE, start_y + 2*TILE_SIZE, 1, 0, 1)  # Connect outer to inner
        self.add_road_line(start_x + 3*TILE_SIZE, start_y + 5*TILE_SIZE, 1, 0, 1)  # Connect outer to inner
        
        # Add single exit on a road tile
        exit_x = start_x + 6*TILE_SIZE
        exit_y = start_y + 6*TILE_SIZE
        self.map_exits = [(exit_x, exit_y)]
        
        # Ensure exit is on a road tile
        self.ensure_exits_on_roads()
    
    def create_map_3(self, center_x, center_y):
        """Create third dungeon map - fully connected corridor maze"""
        # Create a fully connected corridor maze
        grid_size = 19  # Increased for larger screen
        start_x = center_x - (grid_size//2) * TILE_SIZE
        start_y = center_y - (grid_size//2) * TILE_SIZE
        
        # Create horizontal corridors (all connected)
        for i in range(1, grid_size-1, 2):
            self.add_road_line(start_x + 1*TILE_SIZE, start_y + i*TILE_SIZE, 1, 0, grid_size-3)
        
        # Create vertical corridors (all connected)
        for i in range(1, grid_size-1, 2):
            self.add_road_line(start_x + i*TILE_SIZE, start_y + 1*TILE_SIZE, 0, 1, grid_size-3)
        
        # Add connecting paths to ensure full connectivity
        for i in range(3, grid_size-2, 2):
            for j in range(3, grid_size-2, 2):
                self.add_road_line(start_x + i*TILE_SIZE, start_y + j*TILE_SIZE, 1, 0, 1)  # Short horizontal connectors
                self.add_road_line(start_x + i*TILE_SIZE, start_y + j*TILE_SIZE, 0, 1, 1)  # Short vertical connectors
        
        # Add single exit on a road tile
        exit_x = start_x + (grid_size-2)*TILE_SIZE
        exit_y = start_y + (grid_size-2)*TILE_SIZE
        self.map_exits = [(exit_x, exit_y)]
        
        # Ensure exit is on a road tile
        self.ensure_exits_on_roads()
    
    def create_random_map(self, center_x, center_y):
        """Create random dungeon map for higher levels"""
        import random
        
        # Start with center
        self.road_tiles.add((center_x, center_y))
        
        # Create random paths
        for _ in range(20):
            start_x = center_x + random.randint(-6, 6) * TILE_SIZE
            start_y = center_y + random.randint(-6, 6) * TILE_SIZE
            dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            length = random.randint(3, 8)
            self.add_road_line(start_x, start_y, dx, dy, length)
        
        # Add single random exit on a road tile
        if self.road_tiles:
            exit_position = random.choice(list(self.road_tiles))
            self.map_exits = [exit_position]
        else:
            # Fallback if no roads (shouldn't happen)
            self.map_exits = [(center_x, center_y)]
    
    def add_road_line(self, start_x, start_y, dx, dy, length):
        """Add a line of road tiles"""
        for i in range(length + 1):  # +1 to include the end point
            x = start_x + (dx * i * TILE_SIZE)
            y = start_y + (dy * i * TILE_SIZE)
            
            # Add road tiles with width
            for w in range(ROAD_WIDTH):
                for h in range(ROAD_WIDTH):
                    road_x = x + (w - ROAD_WIDTH//2) * TILE_SIZE
                    road_y = y + (h - ROAD_WIDTH//2) * TILE_SIZE
                    if 0 <= road_x < SCREEN_WIDTH and 0 <= road_y < SCREEN_HEIGHT:
                        self.road_tiles.add((road_x, road_y))
    
    def position_player_on_road(self):
        """Position the player on a road tile near the center"""
        center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        
        # Find the closest road tile to the center
        closest_road = None
        min_distance = float('inf')
        
        for road_x, road_y in self.road_tiles:
            distance = ((road_x - center_x) ** 2 + (road_y - center_y) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                closest_road = (road_x, road_y)
        
        # Position player on the closest road tile
        if closest_road:
            self.player.rect.center = closest_road
    
    def ensure_exits_on_roads(self):
        """Ensure all exits are placed on road tiles"""
        for i, (exit_x, exit_y) in enumerate(self.map_exits):
            # Check if exit is on a road tile
            if not self.is_on_road(exit_x, exit_y):
                # Find the closest road tile to the exit
                closest_road = None
                min_distance = float('inf')
                
                for road_x, road_y in self.road_tiles:
                    distance = ((road_x - exit_x) ** 2 + (road_y - exit_y) ** 2) ** 0.5
                    if distance < min_distance:
                        min_distance = distance
                        closest_road = (road_x, road_y)
                
                # Move exit to the closest road tile
                if closest_road:
                    self.map_exits[i] = closest_road
    
    def draw_roads(self):
        """Draw pixel art roads"""
        for x, y in self.road_tiles:
            pygame.draw.rect(self.screen, DARK_GRAY, 
                           (x - TILE_SIZE//2, y - TILE_SIZE//2, TILE_SIZE, TILE_SIZE))
            # Add road border
            pygame.draw.rect(self.screen, GRAY, 
                           (x - TILE_SIZE//2, y - TILE_SIZE//2, TILE_SIZE, TILE_SIZE), 1)
            # Add center dot to show road tile center
            pygame.draw.circle(self.screen, (100, 100, 100), (x, y), 2)
        
        # Draw exits
        for exit_x, exit_y in self.map_exits:
            pygame.draw.rect(self.screen, YELLOW, 
                           (exit_x - TILE_SIZE//2, exit_y - TILE_SIZE//2, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(self.screen, (255, 255, 0), 
                           (exit_x - TILE_SIZE//2, exit_y - TILE_SIZE//2, TILE_SIZE, TILE_SIZE), 3)
    
    def spawn_monster(self):
        """Spawn a monster anywhere on screen (ghosts can move everywhere)"""
        # Calculate max monsters based on level (more monsters per level)
        max_monsters = 5 + (self.current_map * 2)  # 5 at level 1, 7 at level 2, 9 at level 3, etc.
        max_monsters = min(max_monsters, 15)  # Cap at 15 monsters
        
        if len(self.monsters) < max_monsters:
            # Spawn monsters anywhere on screen since they're ghosts
            spawn_x = random.randint(50, SCREEN_WIDTH - 50)
            spawn_y = random.randint(50, SCREEN_HEIGHT - 50)
            monster = Monster(spawn_x, spawn_y, self.player)
            monster.set_level(self.current_map)  # Set monster level
            self.monsters.add(monster)
            self.all_sprites.add(monster)
    
    def spawn_clay_pot(self):
        """Spawn a clay pot on a road tile"""
        if len(self.clay_pots) < 3:  # Limit max clay pots
            if self.road_tiles:  # Make sure we have road tiles
                spawn_point = random.choice(list(self.road_tiles))
                clay_pot = ClayPot(spawn_point[0], spawn_point[1])
                self.clay_pots.add(clay_pot)
                self.all_sprites.add(clay_pot)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.attack()
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
    
    def update(self):
        """Update game logic"""
        if not self.game_over:
            # Update player
            self.player.update(self)
            
            # Spawn monsters (faster spawning at higher levels)
            self.monster_spawn_timer += 1
            # Faster spawning at higher levels (minimum 60 frames = 1 second)
            current_spawn_delay = max(60, self.monster_spawn_delay - (self.current_map * 10))
            if self.monster_spawn_timer >= current_spawn_delay:
                self.spawn_monster()
                self.monster_spawn_timer = 0
            
            # Spawn clay pots
            self.clay_pot_spawn_timer += 1
            if self.clay_pot_spawn_timer >= self.clay_pot_spawn_delay:
                self.spawn_clay_pot()
                self.clay_pot_spawn_timer = 0
            
            # Update monsters
            for monster in self.monsters:
                monster.update(self)
                if monster.health <= 0:
                    # Score based on monster level (higher level = more points)
                    score_bonus = 10 + (monster.level * 5)  # 10 for level 1, 15 for level 2, etc.
                    self.score += score_bonus
                    monster.kill()
            
            # Check player attacks vs monsters
            attack_played = False
            for monster in self.monsters:
                if self.player.is_attacking and self.player.attack_rect.colliderect(monster.rect):
                    if not attack_played:
                        self.play_attack_sound()
                        attack_played = True
                    monster.take_damage(self.player.attack_damage)
            
            # Check player attacks vs clay pots
            for clay_pot in self.clay_pots:
                if self.player.is_attacking and self.player.attack_rect.colliderect(clay_pot.rect):
                    if clay_pot.take_damage(self.player.attack_damage):
                        # Clay pot was destroyed, give upgrade
                        self.player.add_lightning_upgrade()
                        clay_pot.kill()
                        self.score += 5  # Small score bonus for destroying pots
            
            # Check monster contact damage vs player
            dt = 16  # Approximate frame time in milliseconds (60 FPS)
            contact_sound_played = False
            for monster in self.monsters:
                if monster.rect.colliderect(self.player.rect):
                    # Start or continue contact
                    monster.start_contact()

                    # Deal contact damage based on monster's remaining health
                    contact_damage = monster.get_contact_damage()
                    if contact_damage > 0 and not contact_sound_played:
                        self.play_contact_sound()
                        contact_sound_played = True
                    self.player.take_damage(contact_damage)
                    
                    # Update contact timer and check for monster death
                    if monster.update_contact(dt):
                        # Monster died from contact, give score
                        score_bonus = 10 + (monster.level * 5)
                        self.score += score_bonus
                        monster.kill()
                else:
                    # End contact if not touching
                    monster.end_contact()
            
            # Check map exits
            self.check_map_exits()
            
        # Check game over
        if self.player.health <= 0:
            self.game_over = True
            if self.audio_available and self.background_music:
                self.background_music.stop()  # Stop music when game ends
    
    def draw(self):
        """Draw everything"""
        self.screen.fill(BLACK)
        
        # Draw roads
        self.draw_roads()
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw anime faces on characters
        self.player.draw_anime_face(self.screen)
        for monster in self.monsters:
            monster.draw_anime_face(self.screen)
            monster.draw_health_bar(self.screen)
        
        # Draw clay pots
        for clay_pot in self.clay_pots:
            clay_pot.draw_clay_pot(self.screen)
        
        # Draw lightning attack effect
        self.player.draw_lightning_effect(self.screen)
        
        # Draw upgrade indicator
        self.player.draw_upgrade_indicator(self.screen)
        
        # Attack range debug box removed for cleaner visuals
        
        # Debug: Show road tile count and monster health
        debug_text = f"Road tiles: {len(self.road_tiles)}"
        if self.monsters:
            first_monster = list(self.monsters)[0]
            debug_text += f" | Monster health: {first_monster.health}/{first_monster.max_health}"
            if first_monster.is_in_contact:
                debug_text += f" | Contact: {first_monster.contact_timer:.0f}ms"
        debug_text += f" | Player on road: {self.is_on_road(self.player.rect.centerx, self.player.rect.centery)}"
        debug_display = self.font.render(debug_text, True, WHITE)
        self.screen.blit(debug_display, (10, 210))
        
        # Draw UI
        self.draw_ui()
        
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_ui(self):
        """Draw user interface"""
        # Health bar
        health_text = self.font.render(f"Health: {self.player.health}", True, WHITE)
        self.screen.blit(health_text, (10, 10))
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 50))
        
        # Monster count (moved to combined display below)
        
        # Current map
        map_text = self.font.render(f"Map: {self.current_map}", True, WHITE)
        self.screen.blit(map_text, (10, 130))
        
        # Monster count and level info
        monster_info = f"Monsters: {len(self.monsters)}"
        if self.monsters:
            # Show average monster level
            avg_level = sum(monster.level for monster in self.monsters) / len(self.monsters)
            monster_info += f" (Avg Level: {avg_level:.1f})"
        monster_text = self.font.render(monster_info, True, WHITE)
        self.screen.blit(monster_text, (10, 170))
    
    def draw_game_over(self):
        """Draw game over screen"""
        game_over_text = self.font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.font.render("Press R to restart", True, WHITE)
        
        # Center the text
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def check_map_exits(self):
        """Check if player reached a map exit"""
        player_center = (self.player.rect.centerx, self.player.rect.centery)
        
        for exit_x, exit_y in self.map_exits:
            distance = ((player_center[0] - exit_x) ** 2 + (player_center[1] - exit_y) ** 2) ** 0.5
            if distance < TILE_SIZE:
                self.next_map()
                break
    
    def next_map(self):
        """Progress to next map"""
        self.current_map += 1
        self.score += 100  # Bonus for completing map
        
        # Clear all monsters and clay pots
        self.monsters.empty()
        self.clay_pots.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        
        # Create new map
        self.create_dungeon_map()
        
        # Position player on a road tile in the new map
        self.position_player_on_road()
        
        # Reset spawn timer
        self.monster_spawn_timer = 0
    
    def is_on_road(self, x, y):
        """Check if position is on a road"""
        # Check if the position is within any road tile with precise collision
        for road_x, road_y in self.road_tiles:
            # Check if the point is within the road tile bounds
            if (road_x - TILE_SIZE//2 <= x <= road_x + TILE_SIZE//2 and 
                road_y - TILE_SIZE//2 <= y <= road_y + TILE_SIZE//2):
                return True
        return False
    
    def restart_game(self):
        """Restart the game"""
        self.score = 0
        self.game_over = False
        self.current_map = 1
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.monsters.empty()
        self.clay_pots.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.monster_spawn_timer = 0
        self.clay_pot_spawn_timer = 0
        self.create_dungeon_map()
        self.position_player_on_road()

        # Restart background music
        if self.audio_available and self.background_music:
            self.background_music.play(-1)  # Restart music

    def init_audio(self):
        """Initialize audio system and load sounds"""
        # Check if pygame.mixer is properly initialized
        if not pygame.mixer.get_init():
            print("Warning: pygame.mixer not properly initialized")
            self.audio_available = False
            return

        try:
            # Use pygame's built-in sound generation for reliability
            self.background_music = self.create_simple_music()
            self.attack_sound = self.create_simple_attack_sound()
            self.contact_sound = self.create_simple_contact_sound()
            self.audio_available = True
        except Exception as e:
            print(f"Audio initialization failed: {e}")
            self.audio_available = False

        # Start background music
        if self.audio_available and self.background_music:
            try:
                self.background_music.play(-1)  # Loop indefinitely
                self.background_music.set_volume(0.3)  # Slightly higher volume
                print("✅ Background music started successfully")
            except Exception as e:
                print(f"❌ Failed to start background music: {e}")
                self.audio_available = False
        elif self.audio_available:
            print("⚠️ Audio available but no background music object")
        else:
            print("❌ Audio system not available - running without sound")

    def generate_background_music(self):
        """Legacy method - kept for compatibility"""
        return self.create_simple_music()

    def generate_attack_sound(self):
        """Legacy method - kept for compatibility"""
        return self.create_simple_attack_sound()

    def generate_contact_sound(self):
        """Legacy method - kept for compatibility"""
        return self.create_simple_contact_sound()

    def create_simple_music(self):
        """Create simple, reliable background music using pygame.mixer"""
        # Create a simple melody using individual note sounds
        # We'll create 8 different note sounds and play them in sequence

        # Note frequencies for C major scale
        note_freqs = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]

        # Create a sequence of note sounds
        note_sounds = []
        for freq in note_freqs:
            # Generate a simple sine wave for each note
            samples = []
            sample_rate = 44100
            duration = 0.3  # 300ms per note

            for i in range(int(sample_rate * duration)):
                t = i / sample_rate
                # Simple envelope for smooth attack/decay
                envelope = min(t * 10, (duration - t) * 10, 1.0)
                sample = 0.2 * envelope * math.sin(2 * math.pi * freq * t)
                samples.append(sample)

            # Create pygame Sound object
            sound = pygame.mixer.Sound(pygame.sndarray.make_sound(samples))
            note_sounds.append(sound)

        # Create a simple melody sequence: C-D-E-F-G-F-E-D
        melody_sequence = [0, 1, 2, 3, 4, 3, 2, 1]  # Indices into note_freqs

        # Create the full melody by concatenating note sounds
        full_melody = []
        for note_idx in melody_sequence:
            note_sound = note_sounds[note_idx]
            # Get the sound samples and add them to our melody
            samples = pygame.sndarray.samples(note_sound)
            full_melody.extend(samples)

        # Create final sound object
        return pygame.mixer.Sound(pygame.sndarray.make_sound(full_melody))

    def create_simple_attack_sound(self):
        """Create a simple, reliable attack sound"""
        sample_rate = 44100
        duration = 0.2
        frequency = 800

        samples = []
        for i in range(int(sample_rate * duration)):
            t = i / sample_rate
            # Quick attack, fast decay
            envelope = math.exp(-t * 15) * (1 - math.exp(-t * 50))
            sample = 0.3 * envelope * math.sin(2 * math.pi * frequency * t)
            samples.append(sample)

        return pygame.mixer.Sound(pygame.sndarray.make_sound(samples))

    def create_simple_contact_sound(self):
        """Create a simple, reliable contact sound"""
        sample_rate = 44100
        duration = 0.15
        frequency = 150

        samples = []
        for i in range(int(sample_rate * duration)):
            t = i / sample_rate
            # Slow attack, medium decay
            envelope = math.exp(-t * 8) * (1 - math.exp(-t * 20))
            sample = 0.25 * envelope * math.sin(2 * math.pi * frequency * t)
            samples.append(sample)

        return pygame.mixer.Sound(pygame.sndarray.make_sound(samples))

    def create_attack_tone(self):
        """Legacy method - kept for compatibility"""
        return self.create_simple_attack_sound()

    def create_contact_tone(self):
        """Legacy method - kept for compatibility"""
        return self.create_simple_contact_sound()


    def play_attack_sound(self):
        """Play attack sound effect"""
        if self.audio_available and self.attack_sound:
            self.attack_sound.play()

    def play_contact_sound(self):
        """Play contact damage sound effect"""
        if self.audio_available and self.contact_sound:
            self.contact_sound.play()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
