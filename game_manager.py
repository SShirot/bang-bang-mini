import pygame
import math
import random
from game_config import *
from game_objects import Tank, Bullet, FireArea

class GameManager:
    def __init__(self):
        self.player = None
        self.enemy = None
        self.bullets = []
        self.enemy_bullets = []
        self.fire_areas = []  # Danh sách các fire area
        self.wave = 1
        self.enemy_killed = False
        self.paused = False
        self.selected_tank_type = TANK_TYPE_NARUTO  # Tank mặc định
        
    def init_game(self):
        """Khởi tạo game từ đầu"""
        # Tạo player tank theo loại đã chọn
        if self.selected_tank_type == TANK_TYPE_NARUTO:
            self.player = Tank(WIDTH//2, HEIGHT//2, DARK_GREEN, GREEN, 
                             tank_type=TANK_TYPE_NARUTO, speed=PLAYER_SPEED, hp=100)
        else:  # TANK_TYPE_SASUKE
            self.player = Tank(WIDTH//2, HEIGHT//2, PURPLE, CYAN, 
                             tank_type=TANK_TYPE_SASUKE, speed=PLAYER_SPEED, hp=100)
            
        self.player.original_speed = PLAYER_SPEED
        self.player.player_fire_rate = PLAYER_FIRE_RATE
        self.player.player_fire_cooldown = 0
        
        self.enemy = Tank(random.randint(30, WIDTH-30), random.randint(30, HEIGHT-30), 
                         DARK_BLUE, BLUE, speed=ENEMY_BASE_SPEED, hp=100, fire_rate=ENEMY_BASE_FIRE_RATE)
        
        self.bullets = []
        self.enemy_bullets = []
        self.fire_areas = []
        self.wave = 1
        self.enemy_killed = False
        
    def set_tank_type(self, tank_type):
        """Đặt loại tank cho player"""
        self.selected_tank_type = tank_type
        
    def handle_events(self):
        """Xử lý các sự kiện game"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_click()
        return True
    
    def handle_keydown(self, key):
        """Xử lý phím nhấn"""
        if key == pygame.K_ESCAPE:
            return False
        elif key == pygame.K_p:
            self.paused = not self.paused
        elif key == pygame.K_r and not self.paused:
            self.init_game()
        elif key == pygame.K_e and self.player.alive and not self.paused:
            # E key - xử lý theo loại tank
            if self.player.tank_type == TANK_TYPE_NARUTO:
                self.handle_skill_activation('dash')
            else:  # TANK_TYPE_SASUKE
                self.player.execute_buff_skill('speed_boost')
        elif key == pygame.K_q and self.player.alive and not self.paused:
            # Heal là buff skill - sử dụng trực tiếp
            self.player.execute_buff_skill('heal')
        elif key == pygame.K_f and self.player.alive and not self.paused:
            # Shield là buff skill - sử dụng trực tiếp
            self.player.execute_buff_skill('shield')
        elif key == pygame.K_SPACE and self.player.alive and not self.paused:
            # Spacebar - xử lý theo loại tank
            if self.player.tank_type == TANK_TYPE_NARUTO:
                self.handle_skill_activation('power_shot')
            else:  # TANK_TYPE_SASUKE
                self.handle_skill_activation('fire_area')
        return True
    
    def handle_skill_activation(self, skill_name):
        """Xử lý kích hoạt skill mode (chỉ cho directional và area skills)"""
        if self.player.skill_mode and self.player.active_skill == skill_name:
            # Nếu đang ở skill mode và nhấn lại cùng skill, tắt skill mode
            self.player.deactivate_skill_mode()
        else:
            # Kích hoạt skill mode mới
            if self.player.activate_skill_mode(skill_name):
                # Nếu skill khác đang active, tắt nó trước
                if self.player.skill_mode and self.player.active_skill != skill_name:
                    self.player.deactivate_skill_mode()
                self.player.activate_skill_mode(skill_name)
    
    def handle_dash(self):
        """Xử lý skill dash (legacy - giữ lại để tương thích)"""
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]: dy -= 1
        if keys[pygame.K_s]: dy += 1
        if keys[pygame.K_a]: dx -= 1
        if keys[pygame.K_d]: dx += 1
        if dx != 0 or dy != 0:
            self.player.dash(dx, dy)
    
    def handle_power_shot(self):
        """Xử lý power shot (legacy - giữ lại để tương thích)"""
        if self.player.skills['power_shot'].ready and self.player.can_fire():
            self.player.power_shot()
            self.player.fire()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.player.x
            dy = mouse_y - self.player.y
            angle = math.degrees(math.atan2(-dy, dx))
            self.bullets.append(Bullet(self.player.x, self.player.y, angle, YELLOW, is_power_shot=True))
    
    def handle_mouse_click(self):
        """Xử lý click chuột"""
        if not self.player.alive or self.paused:
            return
            
        if self.player.skill_mode:
            # Nếu đang ở skill mode, thực thi skill
            self.execute_skill_at_target()
        else:
            # Nếu không ở skill mode, bắn đạn thường
            if self.player.can_fire():
                self.player.fire()
                self.bullets.append(Bullet(self.player.x, self.player.y, self.player.turret_angle, RED))
    
    def execute_skill_at_target(self):
        """Thực thi skill tại vị trí chuột"""
        if not self.player.skill_mode or not self.player.active_skill:
            return
            
        target_pos = pygame.mouse.get_pos()
        result = self.player.execute_skill(target_pos)
        
        if result:
            # Xử lý kết quả skill
            if self.player.active_skill == 'power_shot' and result:
                # Thêm power shot bullet vào danh sách
                self.bullets.append(result)
            elif self.player.active_skill == 'fire_area' and result[0]:
                # Thêm fire area vào danh sách
                self.fire_areas.append(result[1])
            
            # Tắt skill mode sau khi thực thi
            self.player.deactivate_skill_mode()
    
    def update_player(self):
        """Cập nhật player"""
        if not self.player.alive:
            return
            
        # Cập nhật skill targeting
        if self.player.skill_mode:
            self.player.update_skill_target(pygame.mouse.get_pos())
            
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_w]: dy -= 1
        if keys[pygame.K_s]: dy += 1
        if keys[pygame.K_a]: dx -= 1
        if keys[pygame.K_d]: dx += 1
        
        self.player.move(dx, dy)
        self.player.aim_turret(pygame.mouse.get_pos())
        self.player.update_skills()
        self.player.update_fire_cooldown()
    
    def update_enemy(self):
        """Cập nhật enemy AI"""
        if not self.enemy.alive:
            if not self.enemy_killed:
                self.enemy_killed = True
                self.wave += 1
                if self.player.alive:
                    self.player.hp = min(100, self.player.hp + 20)
                pygame.time.wait(1000)
                self.enemy.respawn(self.wave)
                self.enemy_killed = False
            return
        
        # Kiểm tra và né đạn
        dodge_dx, dodge_dy = self.enemy.dodge_bullets(self.bullets)
        
        if dodge_dx != 0 or dodge_dy != 0:
            self.enemy.move(dodge_dx, dodge_dy)
        else:
            # Di chuyển ngẫu nhiên
            if random.randint(1, 120) == 1:
                self.enemy.random_direction = random.uniform(0, 2 * math.pi)
            
            dx = math.cos(self.enemy.random_direction)
            dy = -math.sin(self.enemy.random_direction)
            
            new_x = self.enemy.x + dx * self.enemy.speed
            new_y = self.enemy.y + dy * self.enemy.speed
            
            if new_x < TANK_RADIUS or new_x > WIDTH - TANK_RADIUS or new_y < TANK_RADIUS or new_y > HEIGHT - TANK_RADIUS:
                self.enemy.random_direction = random.uniform(0, 2 * math.pi)
            else:
                self.enemy.move(dx, dy)
                
        self.enemy.aim_turret((self.player.x, self.player.y))
        
        # Bắn đạn
        if self.enemy.cooldown <= 0:
            dist = math.sqrt((self.player.x - self.enemy.x)**2 + (self.player.y - self.enemy.y)**2)
            if dist < 400:
                self.enemy_bullets.append(Bullet(self.enemy.x, self.enemy.y, self.enemy.turret_angle, BLUE))
                self.enemy.cooldown = self.enemy.fire_rate
        else:
            self.enemy.cooldown -= 1
            
        if self.enemy.dodge_timer > 0:
            self.enemy.dodge_timer -= 1
    
    def update_fire_areas(self):
        """Cập nhật các fire area"""
        for fire_area in self.fire_areas[:]:
            fire_area.update()
            
            # Kiểm tra enemy trong vùng lửa
            if self.enemy.alive:
                if fire_area.check_enemy_in_area(self.enemy):
                    fire_area.apply_fire_effect(self.enemy)
                else:
                    fire_area.remove_fire_effect(self.enemy)
            
            # Gây damage mỗi giây (60 frames = 1 giây)
            if fire_area.timer % 60 == 0:
                fire_area.damage_enemies()
            
            # Xóa fire area đã hết hạn
            if not fire_area.alive:
                # Loại bỏ hiệu ứng khỏi enemy
                if self.enemy.alive:
                    fire_area.remove_fire_effect(self.enemy)
                self.fire_areas.remove(fire_area)
    
    def update_bullets(self):
        """Cập nhật đạn"""
        for bullet in self.bullets[:]:
            bullet.move()
            if not bullet.alive:
                self.bullets.remove(bullet)
                continue
            bullet.check_collision(self.enemy)

        for bullet in self.enemy_bullets[:]:
            bullet.move()
            if not bullet.alive:
                self.enemy_bullets.remove(bullet)
                continue
            bullet.check_collision(self.player)
    
    def update(self):
        """Cập nhật game chính"""
        if self.paused:
            return True
            
        self.update_player()
        self.update_enemy()
        self.update_bullets()
        self.update_fire_areas()
        return True
    
    def draw(self, win):
        """Vẽ game"""
        win.fill(WHITE)
        
        # Vẽ đạn
        for bullet in self.bullets:
            bullet.draw(win)
        for bullet in self.enemy_bullets:
            bullet.draw(win)
        
        # Vẽ fire areas
        for fire_area in self.fire_areas:
            fire_area.draw(win)
        
        # Vẽ tanks
        self.player.draw(win)
        self.enemy.draw(win)
        
        # Vẽ skill targeting
        self.player.draw_skill_targeting(win)
        
        # Vẽ biên màn hình
        pygame.draw.rect(win, BLACK, (0, 0, WIDTH, HEIGHT), 3)
        
        # Vẽ UI
        self.draw_ui(win)
    
    def draw_ui(self, win):
        """Vẽ giao diện người dùng"""
        # Skill bar
        if self.player.alive:
            self.player.draw_skill_bar(win, 20, HEIGHT - 120)
            
            # Fire rate cooldown
            if self.player.player_fire_cooldown > 0:
                cooldown_font = pygame.font.SysFont(None, 24)
                cooldown_ratio = self.player.player_fire_cooldown / self.player.player_fire_rate
                cooldown_text = cooldown_font.render(f"Fire Cooldown: {cooldown_ratio:.1f}s", True, RED)
                win.blit(cooldown_text, (20, HEIGHT - 160))
            
            # Skill mode indicator
            if self.player.skill_mode:
                mode_font = pygame.font.SysFont(None, 28)
                skill_name = self.player.skills[self.player.active_skill].name
                skill_type = self.player.skills[self.player.active_skill].skill_type
                
                if skill_type == SKILL_TYPE_AREA:
                    mode_text = mode_font.render(f"Skill Mode: {skill_name} - Click to Place", True, CYAN)
                else:
                    mode_text = mode_font.render(f"Skill Mode: {skill_name} - Click to Execute", True, CYAN)
                win.blit(mode_text, (WIDTH//2 - 150, HEIGHT - 60))
            
            # Buff status - Right side
            status_x = WIDTH - 200
            status_y = HEIGHT - 120
            status_spacing = 25
            
            if self.player.shield_active:
                shield_font = pygame.font.SysFont(None, 24)
                shield_text = shield_font.render("Shield Active!", True, CYAN)
                win.blit(shield_text, (status_x, status_y))
                status_y += status_spacing
                
            if self.player.speed_boost_active:
                speed_font = pygame.font.SysFont(None, 24)
                speed_text = speed_font.render("Speed Boost Active!", True, YELLOW)
                win.blit(speed_text, (status_x, status_y))
                status_y += status_spacing
            
            # Tank type indicator
            tank_font = pygame.font.SysFont(None, 24)
            tank_text = tank_font.render(f"Tank: {self.player.tank_type.title()}", True, BLACK)
            win.blit(tank_text, (status_x, status_y))
        
        # Wave info - Top left
        font = pygame.font.SysFont(None, 36)
        wave_text = font.render(f"Wave: {self.wave}", True, BLACK)
        win.blit(wave_text, (20, 20))
        
        # Enemy info - Top left below wave
        if self.enemy.alive:
            enemy_info_font = pygame.font.SysFont(None, 24)
            speed_text = enemy_info_font.render(f"Enemy Speed: {self.enemy.speed:.1f}", True, BLUE)
            fire_text = enemy_info_font.render(f"Fire Rate: {self.enemy.fire_rate}", True, BLUE)
            win.blit(speed_text, (20, 60))
            win.blit(fire_text, (20, 85))
        
        # Heal notification - Center
        if self.enemy_killed and self.player.alive:
            heal_font = pygame.font.SysFont(None, 28)
            heal_text = heal_font.render("+20 HP Restored!", True, GREEN)
            win.blit(heal_text, (WIDTH//2-80, HEIGHT//2-100))
        
        # Game over messages
        self.draw_game_over_messages(win)
    
    def draw_game_over_messages(self, win):
        """Vẽ thông báo thắng thua"""
        font = pygame.font.SysFont(None, 48)
        if not self.player.alive:
            text = font.render("YOU DIED!", True, RED)
            win.blit(text, (WIDTH//2-100, HEIGHT//2))
            restart_font = pygame.font.SysFont(None, 32)
            restart_text = restart_font.render("Press R to Restart", True, BLACK)
            win.blit(restart_text, (WIDTH//2-120, HEIGHT//2+50))
        elif not self.enemy.alive:
            text = font.render(f"Wave {self.wave-1} Complete!", True, BLUE)
            win.blit(text, (WIDTH//2-150, HEIGHT//2))
            restart_font = pygame.font.SysFont(None, 32)
            restart_text = restart_font.render("Press R to Restart", True, BLACK)
            win.blit(restart_text, (WIDTH//2-120, HEIGHT//2+50))
    
    def draw_pause_screen(self, win):
        """Vẽ màn hình pause"""
        pause_font = pygame.font.SysFont(None, 72)
        pause_text = pause_font.render("PAUSED", True, BLACK)
        pause_rect = pause_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        win.blit(pause_text, pause_rect)
        
        instruction_font = pygame.font.SysFont(None, 36)
        instruction_text = instruction_font.render("Press P to Resume", True, BLACK)
        instruction_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
        win.blit(instruction_text, instruction_rect)
        
        controls_font = pygame.font.SysFont(None, 24)
        controls_text = controls_font.render("ESC: Quit | R: Restart", True, BLACK)
        controls_rect = controls_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
        win.blit(controls_text, controls_rect)
