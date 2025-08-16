import pygame
import math
import random
from game_config import *
from entities.base.entity import BaseEntity

class BaseEnemy(BaseEntity):
    """Base class cho tất cả enemies"""
    
    def __init__(self, x, y, stats, enemy_type, body_color, turret_color):
        self.enemy_type = enemy_type  # Set trước khi gọi super().__init__
        self.entity_type = enemy_type  # Đồng bộ với BaseEntity
        self.body_color = body_color
        self.turret_color = turret_color
        
        super().__init__(x, y, stats, enemy_type)
        
        # Thêm các thuộc tính cần thiết
        self.original_speed = stats.speed
        
        # Enemy-specific stats
        self.wave = 1
        self.enemy_killed = False
        
        # AI behavior
        self.dodge_timer = 0
        self.dodge_cooldown = 120  # 2 seconds
        
        # Thêm thuộc tính cần thiết
        self.speed_boost_active = False
        self.in_fire_area = False
        
        # Load sprites
        self.load_sprites()
    
    def load_sprites(self):
        """Load enemy sprites"""
        try:
            # Tạm thời dùng sprites của Naruto cho tất cả enemies
            self.body_sprite = pygame.image.load("assets/tanks/naruto/body.png")
            self.turret_sprite = pygame.image.load("assets/tanks/naruto/turret.png")
            
            # Scale sprites
            self.body_sprite = pygame.transform.scale(self.body_sprite, (TANK_SIZE, TANK_SIZE))
            turret_size = max(16, TANK_SIZE // 3)
            self.turret_sprite = pygame.transform.scale(self.turret_sprite, (turret_size, turret_size))
            
            self.has_sprites = True
            # Bỏ print để tăng performance
            
        except Exception as e:
            # Bỏ print để tăng performance
            self.has_sprites = False
    
    def respawn(self, wave):
        """Hồi sinh enemy với stats tăng theo wave"""
        self.wave = wave
        self.x = random.randint(30, WIDTH-30)
        self.y = random.randint(30, HEIGHT-30)
        self.hp = self.stats.hp
        
        # Tăng stats theo wave
        self.fire_rate = max(ENEMY_MIN_FIRE_RATE, self.stats.attack_speed - wave * 10)
        self.speed = min(ENEMY_MAX_SPEED, self.stats.speed + wave * 0.8)
        self.original_speed = self.speed
        
        self.alive = True
        self.cooldown = 0
        self.random_direction = random.uniform(0, 2 * math.pi)
        self.enemy_killed = False
    
    def dodge_bullets(self, bullets):
        """Né đạn từ player - tối ưu hóa performance"""
        if self.dodge_timer > 0:
            self.dodge_timer -= 1
            return 0, 0
        
        # Giảm số bullet check để tăng performance
        bullets_to_check = bullets[:min(5, len(bullets))]  # Chỉ check 5 bullet gần nhất
        
        for bullet in bullets_to_check:
            if not bullet.alive:
                continue
                
            # Sử dụng distance squared để tránh sqrt
            dx = bullet.x - self.x
            dy = bullet.y - self.y
            distance_squared = dx*dx + dy*dy
            
            # Nếu bullet quá gần, né
            if distance_squared < 2500:  # 50^2
                # Tính hướng né (vuông góc với hướng bullet)
                bullet_angle = math.atan2(-dy, dx)
                dodge_angle = bullet_angle + math.pi/2  # Né vuông góc
                
                # Random né trái hoặc phải
                if random.random() < 0.5:
                    dodge_angle += math.pi
                
                dodge_dx = math.cos(dodge_angle)
                dodge_dy = -math.sin(dodge_angle)
                
                # Kích hoạt dodge
                self.dodge_timer = self.dodge_cooldown
                return dodge_dx, dodge_dy
        
        return 0, 0
    
    def update_ai(self, player_pos, bullets):
        """Cập nhật AI behavior - tối ưu hóa performance"""
        if not self.alive:
            return
        
        # Giảm tần suất update AI để tăng performance
        if random.random() < 0.5:  # Chỉ update 50% frames
            # Kiểm tra và né đạn
            dodge_dx, dodge_dy = self.dodge_bullets(bullets)
            
            if dodge_dx != 0 or dodge_dy != 0:
                # Né đạn
                self.move(dodge_dx, dodge_dy)
            else:
                # Di chuyển ngẫu nhiên - giảm tần suất
                if random.randint(1, 240) == 1:  # Tăng từ 120 lên 240
                    self.random_direction = random.uniform(0, 2 * math.pi)
                
                dx = math.cos(self.random_direction)
                dy = -math.sin(self.random_direction)
                
                new_x = self.x + dx * self.speed
                new_y = self.y + dy * self.speed
                
                if new_x < TANK_RADIUS or new_x > WIDTH - TANK_RADIUS or new_y < TANK_RADIUS or new_y > HEIGHT - TANK_RADIUS:
                    self.random_direction = random.uniform(0, 2 * math.pi)
                else:
                    self.move(dx, dy)
        
        # Nhắm vào player - luôn update
        self.aim_turret(player_pos)
    
    def should_fire(self, player_pos):
        """Kiểm tra có nên bắn không"""
        if not self.can_fire():
            return False
        
        # Tính khoảng cách đến player
        dx = player_pos[0] - self.x
        dy = player_pos[1] - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        # Chỉ bắn khi player trong tầm
        return distance < 400
    
    def fire_at_player(self, player_pos):
        """Bắn đạn về phía player"""
        if self.should_fire(player_pos):
            self.fire()
            return True
        return False
    
    def draw(self, win):
        """Vẽ enemy"""
        if not self.alive: 
            return
        
        if self.has_sprites:
            # Vẽ enemy bằng sprites
            self.draw_with_sprites(win)
        else:
            # Fallback về vẽ thủ công
            self.draw_manual(win)
        
        # Thanh máu
        bar_width = TANK_SIZE
        bar_height = 6
        health_ratio = self.hp / self.stats.hp
        pygame.draw.rect(win, RED, (self.x-TANK_RADIUS, self.y+TANK_RADIUS+5, bar_width, bar_height))
        pygame.draw.rect(win, GREEN, (self.x-TANK_RADIUS, self.y+TANK_RADIUS+5, bar_width*health_ratio, bar_height))
    
    def draw_with_sprites(self, win):
        """Vẽ enemy bằng sprites"""
        # Vẽ enemy body (không xoay theo hướng di chuyển)
        rotated_body = pygame.transform.rotate(self.body_sprite, -self.body_angle)
        body_rect = rotated_body.get_rect(center=(self.x, self.y))
        win.blit(rotated_body, body_rect)
        
        # Vẽ turret (xoay theo hướng nhắm)
        rotated_turret = pygame.transform.rotate(self.turret_sprite, -self.turret_angle)
        turret_rect = rotated_turret.get_rect(center=(self.x, self.y))
        win.blit(rotated_turret, turret_rect)
    
    def draw_manual(self, win):
        """Vẽ enemy thủ công (fallback)"""
        # Thân enemy
        body_rect = pygame.Rect(self.x-TANK_RADIUS, self.y-TANK_RADIUS, TANK_SIZE, TANK_SIZE)
        pygame.draw.rect(win, self.body_color, body_rect)
        
        # Nòng enemy
        turret_size = max(16, TANK_SIZE // 3)
        pygame.draw.circle(win, self.turret_color, (int(self.x), int(self.y)), turret_size // 2)
    
    def update(self, player_pos, bullets):
        """Cập nhật enemy"""
        super().update()
        self.update_ai(player_pos, bullets)
