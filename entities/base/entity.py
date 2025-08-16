import pygame
import math
import random
from game_config import *

class BaseEntity:
    """Base class cho tất cả entities trong game"""
    
    def __init__(self, x, y, stats, entity_type):
        self.x = x
        self.y = y
        self.stats = stats
        self.entity_type = entity_type
        
        # Position và movement
        self.body_angle = 0
        self.turret_angle = 0
        
        # State
        self.hp = stats.hp
        self.alive = True
        
        # Combat
        self.cooldown = 0
        self.fire_rate = stats.attack_speed
        
        # Movement
        self.speed = stats.speed
        self.original_speed = stats.speed
        
        # Dodge system
        self.dodge_timer = 0
        self.dodge_direction = 0
        
        # Random movement (cho enemy)
        self.random_direction = random.uniform(0, 2 * math.pi)
        
        # Sprite system
        self.has_sprites = False
        self.body_sprite = None
        self.turret_sprite = None
        
        # Load sprites
        self.load_sprites()
    
    def load_sprites(self):
        """Load sprites - override trong subclass"""
        pass
    
    def take_damage(self, amount):
        """Nhận damage với defense calculation"""
        if hasattr(self, 'shield_active') and self.shield_active:
            amount = max(1, amount // 2)  # Shield giảm 50% damage
        
        # Áp dụng defense
        actual_damage = max(1, amount - self.stats.defense)
        self.hp -= actual_damage
        
        if self.hp <= 0:
            self.alive = False
    
    def heal(self, amount):
        """Hồi máu"""
        self.hp = min(self.stats.hp, self.hp + amount)
    
    def move(self, dx, dy):
        """Di chuyển cơ bản - override trong subclass"""
        if not self.alive: 
            return
        
        if dx != 0 or dy != 0:
            length = math.sqrt(dx*dx + dy*dy)
            dx /= length
            dy /= length
            
            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed
            
            if TANK_RADIUS <= new_x <= WIDTH - TANK_RADIUS and TANK_RADIUS <= new_y <= HEIGHT - TANK_RADIUS:
                self.x = new_x
                self.y = new_y
                self.body_angle = math.degrees(math.atan2(-dy, dx))
    
    def aim_turret(self, target_pos):
        """Nhắm turret về target"""
        tx, ty = target_pos
        dx = tx - self.x
        dy = ty - self.y
        self.turret_angle = math.degrees(math.atan2(-dy, dx))
    
    def can_fire(self):
        """Kiểm tra có thể bắn không"""
        return self.cooldown <= 0
    
    def fire(self):
        """Bắn đạn cơ bản"""
        if self.can_fire():
            self.cooldown = self.fire_rate
            return True
        return False
    
    def update_cooldown(self):
        """Cập nhật cooldown"""
        if self.cooldown > 0:
            self.cooldown -= 1
    
    def draw(self, win):
        """Vẽ entity - override trong subclass"""
        pass
    
    def update(self):
        """Cập nhật entity - override trong subclass"""
        self.update_cooldown()
    
    def respawn(self, x=None, y=None):
        """Hồi sinh entity"""
        if x is None:
            x = random.randint(30, WIDTH-30)
        if y is None:
            y = random.randint(30, HEIGHT-30)
        
        self.x = x
        self.y = y
        self.hp = self.stats.hp
        self.alive = True
        self.cooldown = 0
