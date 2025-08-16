import pygame
import math
from game_config import *
from entities.base.tank import BaseTank
from skills.base_skill import BaseSkill

class NarutoTank(BaseTank):
    """Tank Naruto với skills: Dash, Power Shot, Heal, Shield"""
    
    def __init__(self, x, y):
        # Stats riêng cho Naruto
        naruto_stats = BaseStats(
            hp=100,
            speed=3,
            attack_speed=60,
            damage=20,
            defense=0,
            attack=20
        )
        
        super().__init__(x, y, naruto_stats, TANK_TYPE_NARUTO, DARK_GREEN, DARK_GREEN)
    
    def init_skills(self):
        """Khởi tạo skills cho Naruto"""
        self.skills = {
            'dash': BaseSkill("Dash", DASH_COOLDOWN, 'E', YELLOW, '⚡', DASH_RANGE, SKILL_TYPE_DIRECTIONAL),
            'power_shot': BaseSkill("Power Shot", POWER_SHOT_COOLDOWN, 'SPACE', ORANGE, '💥', POWER_SHOT_RANGE, SKILL_TYPE_DIRECTIONAL),
            'heal': BaseSkill("Heal", HEAL_COOLDOWN, 'Q', PURPLE, '❤️', HEAL_RANGE, SKILL_TYPE_BUFF),
            'shield': BaseSkill("Shield", SHIELD_COOLDOWN, 'F', CYAN, '🛡️', SHIELD_RANGE, SKILL_TYPE_BUFF)
        }
    
    def execute_dash(self, target_pos):
        """Thực thi dash đến vị trí mục tiêu"""
        if self.skills['dash'].use():
            dx = target_pos[0] - self.x
            dy = target_pos[1] - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                # Nếu vị trí target ngoài range, tự động điều chỉnh về max range
                if distance > self.skills['dash'].range:
                    # Tính toán vị trí mới ở max range
                    ratio = self.skills['dash'].range / distance
                    adjusted_x = self.x + dx * ratio
                    adjusted_y = self.y + dy * ratio
                    target_pos = (adjusted_x, adjusted_y)
                    distance = self.skills['dash'].range
                
                # Normalize direction
                dx = target_pos[0] - self.x
                dy = target_pos[1] - self.y
                dx /= distance
                dy /= distance
                
                # Kích hoạt dash mode
                self.dash_timer = self.dash_duration
                self.speed = self.dash_speed
                
                # Lưu hướng dash
                self.dash_direction = (dx, dy)
                self.dash_target = target_pos
                self.dash_distance = distance
                self.dash_remaining = distance
                
                return True
        return False
    
    def execute_power_shot(self, target_pos):
        """Thực thi power shot đến vị trí mục tiêu"""
        if self.skills['power_shot'].use():
            dx = target_pos[0] - self.x
            dy = target_pos[1] - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                # Power shot có range vô hạn, không cần điều chỉnh range
                # Tính góc từ tank đến target
                angle = math.degrees(math.atan2(-dy, dx))
                
                # Tạo bullet đặc biệt
                from game_objects import Bullet
                bullet = Bullet(
                    self.x,
                    self.y,
                    angle,
                    YELLOW,
                    speed=POWER_SHOT_SPEED,
                    damage=BULLET_DAMAGE + POWER_SHOT_BONUS_DAMAGE,
                    is_power_shot=True
                )
                
                return bullet
        return None
    
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
        if skill.skill_type == SKILL_TYPE_DIRECTIONAL:
            if self.active_skill == 'dash':
                return self.execute_dash(target_pos)
            elif self.active_skill == 'power_shot':
                return self.execute_power_shot(target_pos)
        elif skill.skill_type == SKILL_TYPE_AREA:
            return self.execute_area_skill(target_pos)
        
        return False
    
    def execute_area_skill(self, target_pos):
        """Thực thi area skill (không có cho Naruto)"""
        return (False, None)
    
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
        
        if skill.skill_type == SKILL_TYPE_DIRECTIONAL:
            self.draw_directional_targeting(win, skill, target_x, target_y)
    
    def draw_directional_targeting(self, win, skill, target_x, target_y):
        """Vẽ targeting cho skill định hướng"""
        # Vẽ range circle (chỉ khi skill có range hữu hạn)
        if skill.range is not None:
            pygame.draw.circle(win, SKILL_RANGE_COLOR, (int(self.x), int(self.y)), skill.range, 2)
        else:
            # Vẽ tia vector từ tank đến end map
            dx = target_x - self.x
            dy = target_y - self.y
            if dx != 0 or dy != 0:
                # Tính điểm cuối của tia (đến biên màn hình)
                length = math.sqrt(dx*dx + dy*dy)
                dx /= length
                dy /= length
                
                # Tìm điểm cuối trên biên màn hình
                if abs(dx) > abs(dy):
                    if dx > 0:
                        end_x = WIDTH
                        end_y = self.y + dy * (WIDTH - self.x) / dx
                    else:
                        end_x = 0
                        end_y = self.y + dy * (0 - self.x) / dx
                else:
                    if dy > 0:
                        end_y = HEIGHT
                        end_x = self.x + dx * (HEIGHT - self.y) / dy
                    else:
                        end_y = 0
                        end_x = self.x + dx * (0 - self.y) / dy
                
                # Vẽ tia vector
                pygame.draw.line(win, skill.color, (int(self.x), int(self.y)), (int(end_x), int(end_y)), 2)
        
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
