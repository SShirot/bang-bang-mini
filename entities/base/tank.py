import pygame
import math
import random
from game_config import *
from entities.base.entity import BaseEntity

class BaseTank(BaseEntity):
    """Base class cho tất cả tanks"""
    
    def __init__(self, x, y, stats, tank_type, body_color, turret_color):
        self.tank_type = tank_type  # Set trước khi gọi super().__init__
        self.entity_type = tank_type  # Đồng bộ với BaseEntity
        self.body_color = body_color
        self.turret_color = turret_color
        
        super().__init__(x, y, stats, tank_type)
        
        # Thêm các thuộc tính cần thiết
        self.original_speed = stats.speed
        
        # Player-specific systems
        self.player_fire_cooldown = 0
        self.player_fire_rate = PLAYER_FIRE_RATE
        
        # Skill system
        self.skills = {}
        self.skill_mode = False
        self.active_skill = None
        self.skill_target_pos = None
        
        # Buff states
        self.shield_active = False
        self.shield_timer = 0
        self.shield_duration = 300  # 5 seconds
        
        self.speed_boost_active = False
        self.speed_boost_timer = 0
        self.speed_boost_duration = SPEED_BOOST_DURATION
        
        # Dash system
        self.dash_timer = 0
        self.dash_speed = 8
        self.dash_duration = 10
        self.dash_direction = None
        self.dash_target = None
        self.dash_distance = 0
        self.dash_remaining = 0
        
        # Initialize skills
        self.init_skills()
    
    def init_skills(self):
        """Khởi tạo skills - override trong subclass"""
        pass
    
    def load_sprites(self):
        """Load tank sprites"""
        try:
            # Load sprites theo tank type
            if self.tank_type == TANK_TYPE_NARUTO:
                self.body_sprite = pygame.image.load("assets/tanks/naruto/body.png")
                self.turret_sprite = pygame.image.load("assets/tanks/naruto/turret.png")
            elif self.tank_type == TANK_TYPE_SASUKE:
                # Tạm thời dùng sprites của Naruto cho Sasuke
                self.body_sprite = pygame.image.load("assets/tanks/naruto/body.png")
                self.turret_sprite = pygame.image.load("assets/tanks/naruto/turret.png")
            else:
                # Fallback
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
    
    def move(self, dx, dy):
        """Di chuyển tank với dash system"""
        if not self.alive: 
            return
        
        # Xử lý dash movement
        if self.dash_timer > 0 and hasattr(self, 'dash_direction') and hasattr(self, 'dash_remaining'):
            # Di chuyển theo hướng dash
            dash_dx, dash_dy = self.dash_direction
            
            # Tính toán khoảng cách di chuyển cho frame này
            move_distance = min(self.speed, self.dash_remaining)
            
            # Di chuyển tank
            new_x = self.x + dash_dx * move_distance
            new_y = self.y + dash_dy * move_distance
            
            # Kiểm tra biên màn hình
            if TANK_RADIUS <= new_x <= WIDTH - TANK_RADIUS and TANK_RADIUS <= new_y <= HEIGHT - TANK_RADIUS:
                self.x = new_x
                self.y = new_y
                self.dash_remaining -= move_distance
                
                # Cập nhật body angle
                self.body_angle = math.degrees(math.atan2(-dash_dy, dash_dx))
                
                # Nếu đã đến gần target hoặc hết dash
                if self.dash_remaining <= 0 or self.dash_timer <= 0:
                    # Kết thúc dash
                    self.dash_timer = 0
                    self.speed = self.original_speed
                    if hasattr(self, 'dash_direction'):
                        delattr(self, 'dash_direction')
                        delattr(self, 'dash_target')
                        delattr(self, 'dash_distance')
                        delattr(self, 'dash_remaining')
            else:
                # Nếu chạm biên, kết thúc dash
                self.dash_timer = 0
                self.speed = self.original_speed
                if hasattr(self, 'dash_direction'):
                    delattr(self, 'dash_direction')
                    delattr(self, 'dash_target')
                    delattr(self, 'dash_distance')
                    delattr(self, 'dash_remaining')
        else:
            # Di chuyển bình thường
            super().move(dx, dy)
        
        # Cập nhật dash timer
        if self.dash_timer > 0:
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                # Kết thúc dash
                self.speed = self.original_speed
                if hasattr(self, 'dash_direction'):
                    delattr(self, 'dash_direction')
                    delattr(self, 'dash_target')
                    delattr(self, 'dash_distance')
                    delattr(self, 'dash_remaining')
    
    def update_skills(self):
        """Cập nhật skills và buffs"""
        for skill in self.skills.values():
            skill.update()
        
        # Update buff timers
        if self.shield_timer > 0:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False
                
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed_boost_active = False
                self.speed = self.original_speed
    
    def update_fire_cooldown(self):
        """Cập nhật fire cooldown cho player"""
        if self.player_fire_cooldown > 0:
            self.player_fire_cooldown -= 1
    
    def can_fire(self):
        """Kiểm tra player có thể bắn không"""
        can = self.player_fire_cooldown <= 0
        return can
    
    def fire(self):
        """Player bắn đạn"""
        if self.can_fire():
            self.player_fire_cooldown = self.player_fire_rate
            return True
        return False
    
    def draw(self, win):
        """Vẽ tank"""
        if not self.alive: 
            return
        
        if self.has_sprites:
            # Vẽ tank bằng sprites
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
        
        # Hiệu ứng dash
        if self.dash_timer > 0:
            pygame.draw.circle(win, YELLOW, (int(self.x), int(self.y)), 30, 3)
        
        # Hiệu ứng shield
        if self.shield_active:
            pygame.draw.circle(win, CYAN, (int(self.x), int(self.y)), 35, 4)
            
        # Hiệu ứng speed boost
        if self.speed_boost_active:
            pygame.draw.circle(win, YELLOW, (int(self.x), int(self.y)), 40, 2)
    
    def draw_with_sprites(self, win):
        """Vẽ tank bằng sprites"""
        # Vẽ tank body (xoay theo hướng di chuyển)
        rotated_body = pygame.transform.rotate(self.body_sprite, -self.body_angle)
        body_rect = rotated_body.get_rect(center=(self.x, self.y))
        win.blit(rotated_body, body_rect)
        
        # Vẽ turret (xoay theo hướng nhắm)
        rotated_turret = pygame.transform.rotate(self.turret_sprite, -self.turret_angle)
        turret_rect = rotated_turret.get_rect(center=(self.x, self.y))
        win.blit(rotated_turret, turret_rect)
    
    def draw_manual(self, win):
        """Vẽ tank thủ công (fallback)"""
        # Thân tank
        body_rect = pygame.Rect(self.x-TANK_RADIUS, self.y-TANK_RADIUS, TANK_SIZE, TANK_SIZE)
        pygame.draw.rect(win, self.body_color, body_rect)
        
        # Nòng tank - làm to hơn, khoảng 1/3 body size
        turret_size = max(16, TANK_SIZE // 3)  # Khoảng 20px, tối thiểu 16px
        pygame.draw.circle(win, self.turret_color, (int(self.x), int(self.y)), turret_size // 2)
    
    def update(self):
        """Cập nhật tank"""
        super().update()
        self.update_skills()
        self.update_fire_cooldown()
    
    def draw_skill_targeting(self, win):
        """Vẽ skill targeting - override trong subclass"""
        pass
    
    def draw_skill_bar(self, win, x, y):
        """Vẽ skill bar - override trong subclass"""
        pass
    
    def activate_skill_mode(self, skill_name):
        """Kích hoạt skill mode - override trong subclass"""
        pass
    
    def deactivate_skill_mode(self):
        """Tắt skill mode - override trong subclass"""
        pass
    
    def execute_skill(self, target_pos):
        """Thực thi skill - override trong subclass"""
        pass
    
    def execute_heal(self):
        """Thực thi heal - override trong subclass"""
        pass
    
    def execute_shield(self):
        """Thực thi shield - override trong subclass"""
        pass
    
    def execute_speed_boost(self):
        """Thực thi speed boost - override trong subclass"""
        pass
    
    def update_skill_target(self, pos):
        """Cập nhật skill target - override trong subclass"""
        pass
