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
        
        # Divine Arrow Mode
        self.divine_arrow_active = False
        self.divine_arrow_timer = 0
        self.divine_arrow_duration = 300  # 5 seconds at 60 FPS
        self.divine_arrow_fire_timer = 0
        self.divine_arrow_fire_rate = 20  # Bắn mỗi 20 frames (3 shots/second)
        
        # Lưu stats gốc để restore
        self.original_speed = naruto_stats.speed
        self.original_fire_rate = naruto_stats.attack_speed
    
    def init_skills(self):
        """Khởi tạo skills cho Naruto"""
        self.skills = {
            'dash': BaseSkill("Dash", DASH_COOLDOWN, 'E', YELLOW, '⚡', DASH_RANGE, SKILL_TYPE_DIRECTIONAL),
            'triple_power_shot': BaseSkill("Triple Power Shot", POWER_SHOT_COOLDOWN, 'SPACE', ORANGE, '💥', POWER_SHOT_RANGE, SKILL_TYPE_DIRECTIONAL),
            'heal': BaseSkill("Heal", HEAL_COOLDOWN, 'Q', PURPLE, '❤️', HEAL_RANGE, SKILL_TYPE_BUFF),
            'divine_arrow': BaseSkill("Thần Tiễn", DIVINE_ARROW_COOLDOWN, 'F', RED, '🏹', None, SKILL_TYPE_BUFF)
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
    
    def execute_triple_power_shot(self, target_pos):
        """Thực thi triple power shot theo 3 hướng"""
        if self.skills['triple_power_shot'].use():
            dx = target_pos[0] - self.x
            dy = target_pos[1] - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                # Tính góc chính từ tank đến target
                main_angle = math.degrees(math.atan2(-dy, dx))
                
                # Tạo 3 bullets theo 3 hướng: chính, trái, phải
                angles = [main_angle, main_angle - 30, main_angle + 30]
                bullets = []
                
                from game_objects import Bullet
                for angle in angles:
                    bullet = Bullet(
                        self.x,
                        self.y,
                        angle,
                        YELLOW,
                        speed=POWER_SHOT_SPEED,
                        damage=BULLET_DAMAGE + POWER_SHOT_BONUS_DAMAGE,
                        is_power_shot=True
                    )
                    bullets.append(bullet)
                
                return bullets
        return None
    
    def execute_heal(self):
        """Thực thi heal"""
        if self.skills['heal'].use():
            self.heal(20)
            return True
        return False
    
    def execute_divine_arrow(self):
        """Thực thi Thần Tiễn Mode"""
        if self.skills['divine_arrow'].use():
            # Kích hoạt Divine Arrow Mode
            self.divine_arrow_active = True
            self.divine_arrow_timer = self.divine_arrow_duration
            self.divine_arrow_fire_timer = 0
            
            # Tăng stats: speed x1.5, fire rate x1.5
            self.speed = self.original_speed * 1.5
            self.stats.attack_speed = int(self.original_fire_rate / 1.5)
            
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
            elif self.active_skill == 'triple_power_shot':
                return self.execute_triple_power_shot(target_pos)
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
                
                # Vẽ tia vector chính
                pygame.draw.line(win, skill.color, (int(self.x), int(self.y)), (int(end_x), int(end_y)), 2)
                
                # Nếu là Triple Power Shot, vẽ thêm 2 hướng phụ
                if skill.name == "Triple Power Shot":
                    # Tính góc chính
                    main_angle = math.atan2(-dy, dx)
                    
                    # Vẽ hướng trái (lệch 30°)
                    left_angle = main_angle - math.radians(30)
                    left_dx = math.cos(left_angle)
                    left_dy = -math.sin(left_angle)
                    
                    # Tìm điểm cuối hướng trái
                    if abs(left_dx) > abs(left_dy):
                        if left_dx > 0:
                            left_end_x = WIDTH
                            left_end_y = self.y + left_dy * (WIDTH - self.x) / left_dx
                        else:
                            left_end_x = 0
                            left_end_y = self.y + left_dy * (0 - self.x) / left_dx
                    else:
                        if left_dy > 0:
                            left_end_y = HEIGHT
                            left_end_x = self.x + left_dx * (HEIGHT - self.y) / left_dy
                        else:
                            left_end_y = 0
                            left_end_x = self.x + left_dx * (0 - self.y) / left_dy
                    
                    # Vẽ tia vector hướng trái (màu nhạt hơn)
                    left_color = (skill.color[0]//2, skill.color[1]//2, skill.color[2]//2)
                    pygame.draw.line(win, left_color, (int(self.x), int(self.y)), (int(left_end_x), int(left_end_y)), 1)
                    
                    # Vẽ hướng phải (lệch 30°)
                    right_angle = main_angle + math.radians(30)
                    right_dx = math.cos(right_angle)
                    right_dy = -math.sin(right_angle)
                    
                    # Tìm điểm cuối hướng phải
                    if abs(right_dx) > abs(right_dy):
                        if right_dx > 0:
                            right_end_x = WIDTH
                            right_end_y = self.y + right_dy * (WIDTH - self.x) / right_dx
                        else:
                            right_end_x = 0
                            right_end_y = self.y + right_dy * (0 - self.x) / right_dx
                    else:
                        if right_dy > 0:
                            right_end_y = HEIGHT
                            right_end_x = self.x + right_dx * (HEIGHT - self.y) / right_dy
                        else:
                            right_end_y = 0
                            right_end_x = self.x + right_dx * (0 - self.y) / right_dy
                    
                    # Vẽ tia vector hướng phải (màu nhạt hơn)
                    pygame.draw.line(win, left_color, (int(self.x), int(self.y)), (int(right_end_x), int(right_end_y)), 1)
        
        # Vẽ line từ tank đến target
        pygame.draw.line(win, skill.color, (int(self.x), int(self.y)), (int(target_x), int(target_y)), 3)
        
        # Vẽ target indicator
        pygame.draw.circle(win, skill.color, (int(target_x), int(target_y)), 8, 2)
        pygame.draw.circle(win, skill.color, (int(target_x), int(target_y)), 3)
        
        # Vẽ skill name
        font = pygame.font.SysFont(None, 24)
        skill_text = font.render(f"{skill.name} Mode", True, skill.color)
        win.blit(skill_text, (target_x + 15, target_y - 10))
    
    def update_divine_arrow_mode(self):
        """Cập nhật Divine Arrow Mode"""
        if self.divine_arrow_active:
            # Giảm timer
            self.divine_arrow_timer -= 1
            
            # Tự động bắn power shot
            self.divine_arrow_fire_timer += 1
            if self.divine_arrow_fire_timer >= self.divine_arrow_fire_rate:
                self.divine_arrow_fire_timer = 0
                
                # Bắn power shot theo hướng turret hiện tại
                from game_objects import Bullet
                bullet = Bullet(
                    self.x,
                    self.y,
                    self.turret_angle,
                    YELLOW,
                    speed=POWER_SHOT_SPEED,
                    damage=BULLET_DAMAGE + POWER_SHOT_BONUS_DAMAGE,
                    is_power_shot=True
                )
                
                # Thêm bullet vào game (cần return để game_manager xử lý)
                # Tạm thời return None, sẽ xử lý trong game_manager
                return bullet
            
            # Hết thời gian Divine Arrow Mode
            if self.divine_arrow_timer <= 0:
                self.divine_arrow_active = False
                # Restore stats gốc
                self.speed = self.original_speed
                self.stats.attack_speed = self.original_fire_rate
        
        return None
    
    def extend_divine_arrow_duration(self, additional_frames):
        """Kéo dài thời gian Thần Tiễn mode"""
        if self.divine_arrow_active:
            self.divine_arrow_timer += additional_frames
            # Giới hạn tối đa 10 giây (600 frames)
            max_duration = 600
            if self.divine_arrow_timer > max_duration:
                self.divine_arrow_timer = max_duration
    
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
            
            # Highlight Divine Arrow Mode
            if skill_name == 'divine_arrow' and self.divine_arrow_active:
                bg_color = RED
                pygame.draw.rect(win, bg_color, (skill_x-3, skill_y-3, skill_width+6, skill_height+6))
                
                # Hiển thị thời gian còn lại
                remaining_seconds = self.divine_arrow_timer // 60
                time_font = pygame.font.SysFont(None, 16)
                time_text = time_font.render(f"+{remaining_seconds}s", True, WHITE)
                time_rect = time_text.get_rect(center=(skill_x + skill_width//2, skill_y + skill_height//2 + 15))
                win.blit(time_text, time_rect)
            
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
