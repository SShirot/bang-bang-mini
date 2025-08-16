import pygame
import math
from game_config import *
from entities.base.tank import BaseTank
from skills.base_skill import BaseSkill

class SasukeTank(BaseTank):
    """Tank Sasuke với skills: Fire Area, Speed Boost, Heal, Shield"""
    
    def __init__(self, x, y):
        # Stats riêng cho Sasuke
        sasuke_stats = BaseStats(
            hp=100,
            speed=3,
            attack_speed=60,
            damage=20,
            defense=0,
            attack=20
        )
        
        super().__init__(x, y, sasuke_stats, TANK_TYPE_SASUKE, PURPLE, PURPLE)
    
    def init_skills(self):
        """Khởi tạo skills cho Sasuke"""
        self.skills = {
            'fire_area': BaseSkill("Fire Area", FIRE_AREA_COOLDOWN, 'SPACE', FIRE_COLOR, '🔥', FIRE_AREA_RANGE, SKILL_TYPE_AREA),
            'speed_boost': BaseSkill("Speed Boost", SPEED_BOOST_COOLDOWN, 'E', YELLOW, '⚡', SPEED_BOOST_RANGE, SKILL_TYPE_BUFF),
            'heal': BaseSkill("Heal", HEAL_COOLDOWN, 'Q', PURPLE, '❤️', HEAL_RANGE, SKILL_TYPE_BUFF),
            'shield': BaseSkill("Shield", SHIELD_COOLDOWN, 'F', CYAN, '🛡️', SHIELD_RANGE, SKILL_TYPE_BUFF)
        }
    
    def execute_fire_area(self, target_pos):
        """Thực thi fire area tại vị trí mục tiêu"""
        if self.skills['fire_area'].use():
            dx = target_pos[0] - self.x
            dy = target_pos[1] - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                # Nếu vị trí target ngoài range, tự động điều chỉnh về max range
                if distance > self.skills['fire_area'].range:
                    # Tính toán vị trí mới ở max range
                    ratio = self.skills['fire_area'].range / distance
                    adjusted_x = self.x + dx * ratio
                    adjusted_y = self.y + dy * ratio
                    target_pos = (adjusted_x, adjusted_y)
                
                # Tạo FireArea object
                from game_objects import FireArea
                from game_config import FIRE_AREA_DURATION
                fire_area = FireArea(target_pos[0], target_pos[1], FIRE_AREA_DURATION)
                return fire_area
        return None
    
    def execute_speed_boost(self):
        """Thực thi speed boost"""
        if self.skills['speed_boost'].use():
            self.speed_boost_active = True
            self.speed_boost_timer = self.speed_boost_duration
            self.speed = self.original_speed * SPEED_BOOST_FACTOR
            return True
        return False
    
    def execute_heal(self):
        """Thực thi heal"""
        if self.skills['heal'].use():
            self.heal(20)
            return True
        return False
    
    def execute_shield(self):
        """Thực thi shield"""
        if self.skills['shield'].use():
            self.shield_active = True
            self.shield_timer = self.shield_duration
            return True
        return False
    
    def execute_skill(self, target_pos):
        """Thực thi skill tại vị trí mục tiêu"""
        if not self.skill_mode or not self.active_skill:
            return False
            
        skill = self.skills[self.active_skill]
        
        if not skill.ready:
            return False
            
        # Thực thi skill dựa trên loại
        if skill.skill_type == SKILL_TYPE_AREA:
            if self.active_skill == 'fire_area':
                return self.execute_fire_area(target_pos)
        elif skill.skill_type == SKILL_TYPE_DIRECTIONAL:
            return self.execute_directional_skill(target_pos)
        
        return False
    
    def execute_directional_skill(self, target_pos):
        """Thực thi directional skill (không có cho Sasuke)"""
        return False
    
    def activate_skill_mode(self, skill_name):
        """Kích hoạt skill mode để nhắm"""
        if skill_name in self.skills:
            skill = self.skills[skill_name]
            if skill.ready and skill.skill_type in [SKILL_TYPE_DIRECTIONAL, SKILL_TYPE_AREA]:
                self.skill_mode = True
                self.active_skill = skill_name
                return True
        return False
    
    def deactivate_skill_mode(self):
        """Tắt skill mode"""
        self.skill_mode = False
        self.active_skill = None
        self.skill_target_pos = None
    
    def update_skill_target(self, target_pos):
        """Cập nhật vị trí target cho skill"""
        self.skill_target_pos = target_pos
    
    def draw_skill_targeting(self, win):
        """Vẽ skill targeting khi ở skill mode"""
        if not self.skill_mode or not self.active_skill or not self.skill_target_pos:
            return
            
        skill = self.skills[self.active_skill]
        target_x, target_y = self.skill_target_pos
        
        if skill.skill_type == SKILL_TYPE_AREA:
            self.draw_area_targeting(win, skill, target_x, target_y)
    
    def draw_area_targeting(self, win, skill, target_x, target_y):
        """Vẽ targeting cho area skill"""
        # Vẽ range circle
        pygame.draw.circle(win, SKILL_RANGE_COLOR, (int(self.x), int(self.y)), skill.range, 2)
        
        # Vẽ preview của area effect
        pygame.draw.circle(win, skill.color, (int(target_x), int(target_y)), 30, 3)
        pygame.draw.circle(win, skill.color, (int(target_x), int(target_y)), 15)
        
        # Vẽ line từ tank đến target
        pygame.draw.line(win, skill.color, (int(self.x), int(self.y)), (int(target_x), int(target_y)), 3)
        
        # Vẽ target indicator
        pygame.draw.circle(win, skill.color, (int(target_x), int(target_y)), 8, 2)
        pygame.draw.circle(win, skill.color, (int(target_x), int(target_y)), 3)
        
        # Vẽ skill name
        font = pygame.font.SysFont(None, 24)
        skill_text = font.render(f"{skill.name} Mode", True, skill.color)
        win.blit(skill_text, (target_x + 15, target_y - 10))
    
    def draw_skill_bar(self, win, x, y):
        """Vẽ skill bar"""
        skill_width = 70
        skill_height = 70
        spacing = 15
        
        for i, (skill_name, skill) in enumerate(self.skills.items()):
            skill_x = x + i * (skill_width + spacing)
            skill_y = y
            
            # Highlight active skill
            if self.skill_mode and self.active_skill == skill_name:
                bg_color = LIGHT_BLUE
                pygame.draw.rect(win, bg_color, (skill_x-3, skill_y-3, skill_width+6, skill_height+6))
            
            bg_color = skill.color if skill.ready else (100, 100, 100)
            pygame.draw.rect(win, bg_color, (skill_x, skill_y, skill_width, skill_height))
            pygame.draw.rect(win, BLACK, (skill_x, skill_y, skill_width, skill_height), 2)
            
            # Icon skill
            font = pygame.font.SysFont(None, 35)
            icon_text = font.render(skill.icon_char, True, BLACK)
            icon_rect = icon_text.get_rect(center=(skill_x + skill_width//2, skill_y + skill_height//2))
            win.blit(icon_text, icon_rect)
            
            # Cooldown overlay
            if not skill.ready:
                cooldown_height = skill_height * skill.get_cooldown_ratio()
                pygame.draw.rect(win, (0, 0, 0, 128), (skill_x, skill_y + skill_height - cooldown_height, skill_width, cooldown_height))
            
            # Key binding
            key_font = pygame.font.SysFont(None, 18)
            key_text = key_font.render(skill.key, True, BLACK)
            key_rect = key_text.get_rect(center=(skill_x + skill_width//2, skill_y + skill_height + 18))
            win.blit(key_text, key_rect)
