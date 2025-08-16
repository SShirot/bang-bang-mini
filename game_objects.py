import pygame
import math
import random
from game_config import *

class Skill:
    def __init__(self, name, cooldown, key, color, icon_char, range_value, skill_type):
        self.name = name
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.key = key
        self.color = color
        self.icon_char = icon_char
        self.range = range_value
        self.skill_type = skill_type
        self.ready = True

    def use(self):
        if self.ready:
            self.current_cooldown = self.cooldown
            self.ready = False
            return True
        return False

    def update(self):
        if not self.ready:
            self.current_cooldown -= 1
            if self.current_cooldown <= 0:
                self.ready = True

    def get_cooldown_ratio(self):
        if self.cooldown == 0:
            return 0
        return self.current_cooldown / self.cooldown

class FireArea:
    def __init__(self, x, y, duration):
        self.x = x
        self.y = y
        self.radius = 80
        self.duration = duration
        self.timer = duration
        self.alive = True
        self.active = True  # Tương thích với game_manager
        self.affected_enemies = set()  # Lưu các enemy đang bị ảnh hưởng
        self.damage_timer = 60  # Timer cho damage mỗi giây (60 frames = 1 second)
        
    def update(self):
        if self.timer > 0:
            self.timer -= 1
        else:
            self.alive = False
            self.active = False  # Tương thích với game_manager
            
    def draw(self, win):
        if not self.alive:
            return
            
        # Vẽ vùng lửa với hiệu ứng
        alpha = int(128 + 64 * math.sin(self.timer * 0.2))  # Hiệu ứng nhấp nháy
        fire_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(fire_surface, (*FIRE_COLOR, alpha), (self.radius, self.radius), self.radius)
        win.blit(fire_surface, (self.x - self.radius, self.y - self.radius))
        
        # Vẽ viền
        pygame.draw.circle(win, FIRE_COLOR, (int(self.x), int(self.y)), self.radius, 3)
        
    def check_enemy_in_area(self, enemy):
        """Kiểm tra enemy có trong vùng lửa không"""
        dx = enemy.x - self.x
        dy = enemy.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)
        return distance < self.radius
        
    def apply_fire_effect(self, enemy):
        """Áp dụng hiệu ứng lửa lên enemy"""
        if enemy not in self.affected_enemies:
            self.affected_enemies.add(enemy)
            # Làm chậm enemy
            if not hasattr(enemy, 'original_speed'):
                enemy.original_speed = enemy.speed
            enemy.speed = enemy.original_speed * FIRE_SLOW_FACTOR
            
    def remove_fire_effect(self, enemy):
        """Loại bỏ hiệu ứng lửa khỏi enemy"""
        if enemy in self.affected_enemies:
            self.affected_enemies.remove(enemy)
            # Khôi phục tốc độ
            if hasattr(enemy, 'original_speed'):
                enemy.speed = enemy.original_speed
                
    def damage_enemies(self):
        """Gây damage cho các enemy trong vùng mỗi giây"""
        for enemy in list(self.affected_enemies):
            if enemy.alive:
                enemy.take_damage(FIRE_DAMAGE_PER_SECOND)
            else:
                self.affected_enemies.remove(enemy)

class Tank:
    def __init__(self, x, y, body_color, turret_color, tank_type=TANK_TYPE_NARUTO, speed=PLAYER_SPEED, hp=100, fire_rate=ENEMY_BASE_FIRE_RATE):
        self.x = x
        self.y = y
        self.speed = speed
        self.body_angle = 0
        self.turret_angle = 0
        self.body_color = body_color
        self.turret_color = turret_color
        self.tank_type = tank_type
        self.cooldown = 0
        self.hp = hp
        self.alive = True
        self.fire_rate = fire_rate
        self.dodge_timer = 0
        self.dodge_direction = 0
        self.random_direction = random.uniform(0, 2 * math.pi)
        
        # Load tank sprites
        self.load_tank_sprites()
        
        # Khởi tạo skills theo loại tank
        self.init_skills()
        
        # Skill states
        self.dash_timer = 0
        self.dash_speed = 8
        self.dash_duration = 10
        
        # Dash movement attributes
        self.dash_direction = None
        self.dash_target = None
        self.dash_distance = 0
        self.dash_remaining = 0
        
        # Player fire rate system
        self.player_fire_rate = PLAYER_FIRE_RATE
        self.player_fire_cooldown = 0
        
        # Skill targeting system
        self.skill_mode = False
        self.active_skill = None
        self.skill_target_pos = None
        
        # Buff states
        self.shield_active = False
        self.shield_timer = 0
        self.shield_duration = 300  # 5 seconds
        
        # Speed boost states
        self.speed_boost_active = False
        self.speed_boost_timer = 0
        self.speed_boost_duration = SPEED_BOOST_DURATION
        
        # Lưu tốc độ gốc
        self.original_speed = speed

    def init_skills(self):
        """Khởi tạo skills theo loại tank"""
        if self.tank_type == TANK_TYPE_NARUTO:
            # Tank Naruto - skills cũ
            self.skills = {
                'dash': Skill("Dash", DASH_COOLDOWN, 'E', YELLOW, '⚡', DASH_RANGE, SKILL_TYPE_DIRECTIONAL),
                'power_shot': Skill("Power Shot", POWER_SHOT_COOLDOWN, 'SPACE', ORANGE, '💥', POWER_SHOT_RANGE, SKILL_TYPE_DIRECTIONAL),
                'heal': Skill("Heal", HEAL_COOLDOWN, 'Q', PURPLE, '❤️', HEAL_RANGE, SKILL_TYPE_BUFF),
                'shield': Skill("Shield", SHIELD_COOLDOWN, 'F', CYAN, '🛡️', SHIELD_RANGE, SKILL_TYPE_BUFF)
            }
        elif self.tank_type == TANK_TYPE_SASUKE:
            # Tank Sasuke - skills mới
            self.skills = {
                'fire_area': Skill("Fire Area", FIRE_AREA_COOLDOWN, 'SPACE', FIRE_COLOR, '🔥', FIRE_AREA_RANGE, SKILL_TYPE_AREA),
                'speed_boost': Skill("Speed Boost", SPEED_BOOST_COOLDOWN, 'E', YELLOW, '⚡', SPEED_BOOST_RANGE, SKILL_TYPE_BUFF),
                'heal': Skill("Heal", HEAL_COOLDOWN, 'Q', PURPLE, '❤️', HEAL_RANGE, SKILL_TYPE_BUFF),
                'shield': Skill("Shield", SHIELD_COOLDOWN, 'F', CYAN, '🛡️', SHIELD_RANGE, SKILL_TYPE_BUFF)
            }

    def load_tank_sprites(self):
        """Load sprites cho tank"""
        try:
            if self.tank_type == TANK_TYPE_NARUTO:
                self.body_sprite = pygame.image.load("assets/tanks/naruto/body.png")
                self.turret_sprite = pygame.image.load("assets/tanks/naruto/turret.png")
            elif self.tank_type == TANK_TYPE_SASUKE:
                # Tạm thời dùng sprites của Naruto cho Sasuke
                # Bạn có thể thay thế bằng sprites riêng sau
                self.body_sprite = pygame.image.load("assets/tanks/naruto/body.png")
                self.turret_sprite = pygame.image.load("assets/tanks/naruto/turret.png")
            else:
                # Enemy tank - tạm thời dùng sprites của Naruto
                # Bạn có thể thay thế bằng sprites riêng sau
                self.body_sprite = pygame.image.load("assets/tanks/naruto/body.png")
                self.turret_sprite = pygame.image.load("assets/tanks/naruto/turret.png")
            
            # Scale sprites về kích thước phù hợp
            # Body: giữ nguyên kích thước TANK_SIZE (60x60)
            self.body_sprite = pygame.transform.scale(self.body_sprite, (TANK_SIZE, TANK_SIZE))
            
            # Turret: làm to hơn, khoảng 1/3 kích thước body thay vì 1/5
            turret_size = max(16, TANK_SIZE // 3)  # Khoảng 20px, tối thiểu 16px
            self.turret_sprite = pygame.transform.scale(self.turret_sprite, (turret_size, turret_size))
            
            # Lưu trạng thái có sprites hay không
            self.has_sprites = True
            pass
            
        except Exception as e:
            print(f"Không thể load tank sprites cho {self.tank_type}: {e}")
            print("Sẽ sử dụng vẽ thủ công thay thế")
            # Fallback về vẽ thủ công
            self.has_sprites = False

    def use_skill(self, skill_name):
        if skill_name in self.skills:
            return self.skills[skill_name].use()
        return False

    def update_skills(self):
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
        
        # Update dash timer (đã được xử lý trong move method)
        # Không cần xử lý ở đây nữa

    def activate_skill_mode(self, skill_name):
        """Kích hoạt skill mode để nhắm (chỉ cho directional và area skills)"""
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
    
    def update_skill_target(self, mouse_pos):
        """Cập nhật vị trí nhắm skill"""
        if self.skill_mode and self.active_skill:
            self.skill_target_pos = mouse_pos

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
    
    def execute_directional_skill(self, target_pos):
        """Thực thi skill định hướng"""
        skill = self.skills[self.active_skill]
        
        # Kiểm tra khoảng cách (bỏ qua nếu range là None - vô hạn)
        if skill.range is not None:
            dx = target_pos[0] - self.x
            dy = target_pos[1] - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > skill.range:
                return False
            
        # Thực thi skill
        if self.active_skill == 'dash':
            return self.execute_dash(target_pos)
        elif self.active_skill == 'power_shot':
            return self.execute_power_shot(target_pos)
            
        return False
    
    def execute_area_skill(self, target_pos):
        """Thực thi area skill tại vị trí mục tiêu"""
        skill_name = None
        for name, skill in self.skills.items():
            if skill.skill_type == SKILL_TYPE_AREA and skill.ready:
                skill_name = name
                break
        
        if skill_name:
            # Kiểm tra range cho area skill
            dx = target_pos[0] - self.x
            dy = target_pos[1] - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance > 0:
                # Nếu vị trí target ngoài range, tự động điều chỉnh về max range
                if distance > self.skills[skill_name].range:
                    # Tính toán vị trí mới ở max range
                    ratio = self.skills[skill_name].range / distance
                    adjusted_x = self.x + dx * ratio
                    adjusted_y = self.y + dy * ratio
                    target_pos = (adjusted_x, adjusted_y)
                
                # Thực thi skill
                if skill_name == 'fire_area':
                    return self.execute_fire_area(target_pos)
        
        return (False, None)
    
    def execute_buff_skill(self, skill_name):
        """Thực thi skill buff (không cần nhắm)"""
        if skill_name not in self.skills:
            return False
            
        skill = self.skills[skill_name]
        if not skill.ready or skill.skill_type != SKILL_TYPE_BUFF:
            return False
            
        if skill_name == 'heal':
            return self.execute_heal()
        elif skill_name == 'shield':
            return self.execute_shield()
        elif skill_name == 'speed_boost':
            return self.execute_speed_boost()
            
        return False

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
    
    def execute_fire_area(self, target_pos):
        """Thực thi fire area tại vị trí mục tiêu"""
        if self.skills['fire_area'].use():
            # Tạo fire area mới
            fire_area = FireArea(target_pos[0], target_pos[1], FIRE_AREA_DURATION)
            return True, fire_area  # Return success and fire area object
        return False
    
    def execute_heal(self):
        """Thực thi heal"""
        if self.skills['heal'].use():
            self.hp = min(100, self.hp + 20)
            return True
        return False
    
    def execute_shield(self):
        """Thực thi shield"""
        if self.skills['shield'].use():
            self.shield_active = True
            self.shield_timer = self.shield_duration
            return True
        return False
    
    def execute_speed_boost(self):
        """Thực thi speed boost"""
        if self.skills['speed_boost'].use():
            self.speed_boost_active = True
            self.speed_boost_timer = self.speed_boost_duration
            self.speed = self.original_speed * SPEED_BOOST_FACTOR
            return True
        return False

    def dash(self, dx, dy):
        if self.skills['dash'].use():
            self.dash_timer = self.dash_duration
            self.speed = self.dash_speed
            return True
        return False

    def power_shot(self):
        return self.skills['power_shot'].use()

    def heal(self):
        if self.skills['heal'].use():
            self.hp = min(100, self.hp + 20)
            return True
        return False
    
    def can_fire(self):
        return self.player_fire_cooldown <= 0
    
    def fire(self):
        if self.can_fire():
            self.player_fire_cooldown = self.player_fire_rate
            return True
        return False
    
    def update_fire_cooldown(self):
        if self.player_fire_cooldown > 0:
            self.player_fire_cooldown -= 1

    def move(self, dx, dy):
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

    def dodge_bullets(self, bullets):
        if not self.alive or self.dodge_timer > 0:
            return 0, 0
            
        for bullet in bullets:
            if not bullet.alive:
                continue
                
            dx = self.x - bullet.x
            dy = self.y - bullet.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < 100:
                bullet_angle = math.atan2(-bullet.y, bullet.x)
                dodge_angle = bullet_angle + math.pi/2
                dodge_angle += random.uniform(-0.3, 0.3)
                
                dodge_dx = math.cos(dodge_angle)
                dodge_dy = -math.sin(dodge_angle)
                
                new_x = self.x + dodge_dx * self.speed * 2
                new_y = self.y + dodge_dy * self.speed * 2
                
                if TANK_RADIUS <= new_x <= WIDTH - TANK_RADIUS and TANK_RADIUS <= new_y <= HEIGHT - TANK_RADIUS:
                    self.dodge_timer = 30
                    return dodge_dx, dodge_dy
                    
        return 0, 0

    def aim_turret(self, target_pos):
        if not self.alive: 
            return
        tx, ty = target_pos
        dx = tx - self.x
        dy = ty - self.y
        self.turret_angle = math.degrees(math.atan2(-dy, dx))

    def draw(self, win):
        if not self.alive: 
            return
        
        if hasattr(self, 'has_sprites') and self.has_sprites:
            # Vẽ tank bằng sprites
            self.draw_with_sprites(win)
        else:
            # Fallback về vẽ thủ công
            self.draw_manual(win)
        
        # Thanh máu
        bar_width = TANK_SIZE
        bar_height = 6
        health_ratio = self.hp / 100
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
        
        # Vẽ hướng nhắm (tùy chọn - có thể bỏ nếu không cần)
        # end_x = self.x + math.cos(math.radians(self.turret_angle)) * (turret_size // 2 + 2)
        # end_y = self.y - math.sin(math.radians(self.turret_angle)) * (turret_size // 2 + 2)
        # pygame.draw.line(win, self.turret_color, (self.x, self.y), (end_x, end_y), 2)

    def draw_skill_targeting(self, win):
        """Vẽ skill targeting khi ở skill mode"""
        if not self.skill_mode or not self.active_skill or not self.skill_target_pos:
            return
            
        skill = self.skills[self.active_skill]
        target_x, target_y = self.skill_target_pos
        
        if skill.skill_type == SKILL_TYPE_DIRECTIONAL:
            self.draw_directional_targeting(win, skill, target_x, target_y)
        elif skill.skill_type == SKILL_TYPE_AREA:
            self.draw_area_targeting(win, skill, target_x, target_y)
    
    def draw_directional_targeting(self, win, skill, target_x, target_y):
        """Vẽ targeting cho skill định hướng"""
        # Vẽ range circle (chỉ khi skill có range hữu hạn) - sử dụng màu xanh nhạt
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
    
    def draw_area_targeting(self, win, skill, target_x, target_y):
        """Vẽ targeting cho skill vùng"""
        # Vẽ range circle
        if skill.range is not None:
            pygame.draw.circle(win, SKILL_RANGE_COLOR, (int(self.x), int(self.y)), skill.range, 2)
        
        # Vẽ preview của vùng skill
        if skill.name == "Fire Area":
            # Vẽ preview vùng lửa
            fire_surface = pygame.Surface((160, 160), pygame.SRCALPHA)
            pygame.draw.circle(fire_surface, (*FIRE_COLOR, 100), (80, 80), 80)
            win.blit(fire_surface, (target_x - 80, target_y - 80))
            pygame.draw.circle(win, FIRE_COLOR, (int(target_x), int(target_y)), 80, 3)
        
        # Vẽ skill name
        font = pygame.font.SysFont(None, 24)
        skill_text = font.render(f"{skill.name} Mode", True, skill.color)
        win.blit(skill_text, (target_x + 15, target_y - 10))

    def draw_skill_bar(self, win, x, y):
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

    def take_damage(self, amount):
        if self.shield_active:
            amount = max(1, amount // 2)  # Shield giảm 50% damage
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False

    def respawn(self, wave):
        self.x = random.randint(30, WIDTH-30)
        self.y = random.randint(30, HEIGHT-30)
        self.hp = 100
        self.alive = True
        self.fire_rate = max(ENEMY_MIN_FIRE_RATE, ENEMY_BASE_FIRE_RATE - wave * 10)
        self.speed = min(ENEMY_MAX_SPEED, ENEMY_BASE_SPEED + wave * 0.8)
        self.random_direction = random.uniform(0, 2 * math.pi)

class Bullet:
    def __init__(self, x, y, angle, color, speed=BULLET_SPEED, damage=BULLET_DAMAGE, is_power_shot=False, owner="player"):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.color = color
        self.damage = damage
        self.alive = True
        self.is_power_shot = is_power_shot
        self.owner = owner  # "player" hoặc "enemy"
        
        if is_power_shot:
            self.damage = damage + POWER_SHOT_BONUS_DAMAGE
            self.speed = POWER_SHOT_SPEED

    def move(self):
        if not self.alive: 
            return
            
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed
        
        # Chỉ set alive=False khi bullet thực sự ra ngoài màn hình
        if self.x < -10 or self.x > WIDTH + 10 or self.y < -10 or self.y > HEIGHT + 10:
            self.alive = False

    def draw(self, win):
        if self.alive:
            if self.is_power_shot:
                pygame.draw.circle(win, YELLOW, (int(self.x), int(self.y)), 10)
                pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), 6)
            else:
                pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), 5)

    def check_collision(self, tank):
        if not self.alive or not tank.alive: 
            return False
        dx = self.x - tank.x
        dy = self.y - tank.y
        distance = math.sqrt(dx*dx + dy*dy)
        if distance < 25:
            tank.take_damage(self.damage)
            self.alive = False
            return True
        return False
