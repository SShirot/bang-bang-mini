import pygame
import random
import math
from game_config import *
from entities.tanks.naruto_tank import NarutoTank
from entities.tanks.sasuke_tank import SasukeTank
from entities.enemies.basic_enemy import BasicEnemy
from entities.enemies.fast_enemy import FastEnemy
from entities.enemies.tank_enemy import TankEnemy

class GameManager:
    """Quản lý game với cấu trúc modular mới"""
    
    def __init__(self):
        self.player = None
        self.enemies = []
        self.bullets = []
        self.fire_areas = []
        self.selected_tank_type = TANK_TYPE_NARUTO
        
        # Game state
        self.wave = 1
        self.score = 0
        self.paused = False
        self.game_over = False
        
        # Initialize game
        self.init_game()
    
    def set_tank_type(self, tank_type):
        """Set loại tank được chọn"""
        self.selected_tank_type = tank_type
        
    def init_game(self):
        """Khởi tạo game"""
        # Tạo player tank
        if self.selected_tank_type == TANK_TYPE_NARUTO:
            self.player = NarutoTank(WIDTH//2, HEIGHT//2)
        elif self.selected_tank_type == TANK_TYPE_SASUKE:
            self.player = SasukeTank(WIDTH//2, HEIGHT//2)
        else:
            # Fallback về Naruto
            self.player = NarutoTank(WIDTH//2, HEIGHT//2)
        
        # Tạo enemy đầu tiên
        self.spawn_enemy()
        
        # Reset game state
        self.wave = 1
        self.score = 0
        self.game_over = False
        self.paused = False
    
    def spawn_enemy(self):
        """Spawn enemy mới"""
        # Random loại enemy
        enemy_types = [BasicEnemy, FastEnemy, TankEnemy]
        enemy_class = random.choice(enemy_types)
        
        # Random vị trí spawn
        x = random.randint(30, WIDTH-30)
        y = random.randint(30, HEIGHT-30)
        
        # Tạo enemy
        enemy = enemy_class(x, y)
        enemy.respawn(self.wave)
        self.enemies.append(enemy)
    
    def handle_events(self, events):
        """Xử lý events"""
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
        
        # Xử lý di chuyển liên tục
        self.handle_continuous_movement()
        
        # Xử lý bắn đạn
        self.handle_continuous_firing()
    
    def handle_keydown(self, event):
        """Xử lý key press"""
        if event.key == pygame.K_ESCAPE:
            return "quit"
        elif event.key == pygame.K_r:
            self.restart_game()
        elif event.key == pygame.K_p:
            self.paused = not self.paused
        
        if self.paused:
            return None
        
        # Player movement
        if event.key == pygame.K_w:
            self.player.move(0, -1)
        elif event.key == pygame.K_s:
            self.player.move(0, 1)
        elif event.key == pygame.K_a:
            self.player.move(-1, 0)
        elif event.key == pygame.K_d:
            self.player.move(1, 0)
        
        # Skill activation
        if event.key == pygame.K_e:
            if self.player.tank_type == TANK_TYPE_NARUTO:
                # Naruto: Dash
                self.player.activate_skill_mode('dash')
            elif self.player.tank_type == TANK_TYPE_SASUKE:
                # Sasuke: Speed Boost
                self.player.execute_speed_boost()
        elif event.key == pygame.K_SPACE:
            if self.player.tank_type == TANK_TYPE_NARUTO:
                # Naruto: Triple Power Shot
                self.player.activate_skill_mode('triple_power_shot')
            elif self.player.tank_type == TANK_TYPE_SASUKE:
                # Sasuke: Fire Area
                self.player.activate_skill_mode('fire_area')
        elif event.key == pygame.K_q:
            # Heal cho cả hai
            self.player.execute_heal()
        elif event.key == pygame.K_f:
            if self.player.tank_type == TANK_TYPE_NARUTO:
                # Naruto: Thần Tiễn Mode
                self.player.execute_divine_arrow()
            elif self.player.tank_type == TANK_TYPE_SASUKE:
                # Sasuke: Shield
                self.player.execute_shield()
        
        return None
    
    def handle_mouse_click(self, event):
        """Xử lý mouse click"""
        if event.button == 1:  # Left click
            if self.player.skill_mode:
                # Thực thi skill tại vị trí chuột
                self.execute_skill_at_target(event.pos)
    
    def handle_mouse_motion(self, event):
        """Xử lý mouse movement"""
        # Cập nhật turret angle
        self.player.aim_turret(event.pos)
        
        # Cập nhật skill target nếu đang ở skill mode
        if self.player.skill_mode:
            self.player.update_skill_target(event.pos)
    
    def execute_skill_at_target(self, target_pos):
        """Thực thi skill tại vị trí mục tiêu"""
        if not self.player.skill_mode:
            return
            
        # Thực thi skill
        result = self.player.execute_skill(target_pos)
        
        if result:
            # Xử lý kết quả skill
            if isinstance(result, list) and len(result) == 2:
                # Area skill trả về (success, object)
                success, obj = result
                if success and obj:
                    if hasattr(obj, '__class__') and obj.__class__.__name__ == 'FireArea':
                        self.fire_areas.append(obj)
            elif isinstance(result, list):
                # Triple power shot trả về list bullets
                for bullet in result:
                    if bullet.__class__.__name__ == 'Bullet':
                        self.bullets.append(bullet)
            elif hasattr(result, '__class__'):
                # Object trả về trực tiếp
                if result.__class__.__name__ == 'Bullet':
                    self.bullets.append(result)
                elif result.__class__.__name__ == 'FireArea':
                    self.fire_areas.append(result)
        
        # Tắt skill mode
        self.player.deactivate_skill_mode()
    
    def handle_continuous_movement(self):
        """Xử lý di chuyển liên tục"""
        keys = pygame.key.get_pressed()
        
        # Di chuyển theo WASD
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1
        
        # Normalize movement vector
        if dx != 0 or dy != 0:
            length = (dx*dx + dy*dy)**0.5
            dx /= length
            dy /= length
            self.player.move(dx, dy)
    
    def handle_continuous_firing(self):
        """Xử lý bắn đạn liên tục"""
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            if self.player.can_fire():
                # Tạo bullet từ player
                from game_objects import Bullet
                bullet = Bullet(
                    self.player.x, self.player.y,
                    self.player.turret_angle,
                    self.player.turret_color,
                    speed=BULLET_SPEED,
                    damage=self.player.stats.damage,
                    is_power_shot=False,
                    owner="player"  # Rõ ràng là bullet từ player
                )
                self.bullets.append(bullet)
                self.player.fire()
    
    def update(self):
        """Cập nhật game state"""
        if self.paused or self.game_over:
            return
        
        # Update player
        self.update_player()
        
        # Update enemies
        self.update_enemies()
        
        # Update bullets
        self.update_bullets()
        
        # Update fire areas
        self.update_fire_areas()
        
        # Check collisions
        self.check_collisions()
        
        # Check game over
        if not self.player.alive:
            self.game_over = True
    
    def update_player(self):
        """Cập nhật player"""
        if self.player and self.player.alive:
            self.player.update()
            # Cập nhật divine arrow mode cho Naruto
            if hasattr(self.player, 'update_divine_arrow_mode'):
                divine_bullet = self.player.update_divine_arrow_mode()
                if divine_bullet:
                    self.bullets.append(divine_bullet)
    
    def update_enemies(self):
        """Cập nhật enemies - tối ưu hóa performance"""
        for enemy in self.enemies:
            if enemy.alive:
                enemy.update((self.player.x, self.player.y), self.bullets)
                
                # Enemy bắn - giảm tần suất bắn để tăng performance
                if enemy.fire_at_player((self.player.x, self.player.y)) and random.random() < 0.3:
                    # Tạo bullet từ enemy
                    from game_objects import Bullet
                    bullet = Bullet(
                        enemy.x, enemy.y,
                        enemy.turret_angle,
                        enemy.turret_color,
                        speed=BULLET_SPEED,
                        damage=enemy.stats.damage,
                        is_power_shot=False,
                        owner="enemy"  # Rõ ràng là bullet từ enemy
                    )
                    self.bullets.append(bullet)
    
    def update_bullets(self):
        """Cập nhật bullets"""

            
        for bullet in self.bullets[:]:
            bullet.move()
            
            # Xóa bullet ngoài màn hình hoặc đã hit
            if (bullet.x < -10 or bullet.x > WIDTH + 10 or 
                bullet.y < -10 or bullet.y > HEIGHT + 10 or not bullet.alive):
                self.bullets.remove(bullet)
    
    def update_fire_areas(self):
        """Cập nhật fire areas - tối ưu hóa performance"""
        for fire_area in self.fire_areas[:]:
            fire_area.update()
            
            # Xóa fire area hết hạn
            if not fire_area.alive:
                self.fire_areas.remove(fire_area)
                continue
            
            # Kiểm tra enemies trong fire area - sử dụng distance squared
            for enemy in self.enemies:
                if enemy.alive:
                    dx = enemy.x - fire_area.x
                    dy = enemy.y - fire_area.y
                    distance_squared = dx*dx + dy*dy
                    radius_squared = fire_area.radius * fire_area.radius
                    
                    if distance_squared <= radius_squared:
                        # Enemy trong fire area
                        if not hasattr(enemy, 'in_fire_area'):
                            enemy.in_fire_area = True
                            enemy.original_speed = enemy.speed
                            enemy.speed *= FIRE_SLOW_FACTOR
                        
                        # Damage mỗi giây
                        if fire_area.damage_timer <= 0:
                            enemy.take_damage(FIRE_DAMAGE_PER_SECOND)
                            fire_area.damage_timer = 60  # 1 second
                    else:
                        # Enemy ra khỏi fire area
                        if hasattr(enemy, 'in_fire_area') and enemy.in_fire_area:
                            enemy.in_fire_area = False
                            enemy.speed = enemy.original_speed
            
            # Update damage timer
            if fire_area.damage_timer > 0:
                fire_area.damage_timer -= 1
    
    def check_collisions(self):
        """Kiểm tra va chạm - tối ưu hóa performance"""
        # Player bullets vs Enemies
        for bullet in self.bullets[:]:
            if not bullet.alive:
                continue
                
            # Sử dụng owner để phân biệt rõ ràng bullet từ player hay enemy
            if bullet.owner == "player":
                for enemy in self.enemies[:]:
                    if not enemy.alive:
                        continue
                    
                    # Sử dụng distance squared để tránh sqrt
                    dx = bullet.x - enemy.x
                    dy = bullet.y - enemy.y
                    distance_squared = dx*dx + dy*dy
                    
                    if distance_squared < TANK_RADIUS * TANK_RADIUS:
                        # Hit enemy
                        enemy.take_damage(bullet.damage)
                        bullet.alive = False
                        
                        if not enemy.alive:
                            # Enemy chết
                            enemy.enemy_killed = True
                            self.score += 100
                            
                            # Player hồi máu
                            self.player.heal(20)
                            
                            # Nếu đang ở Thần Tiễn mode, +1s duy trì
                            if hasattr(self.player, 'divine_arrow_active') and self.player.divine_arrow_active:
                                self.player.extend_divine_arrow_duration(60)  # +60 frames = +1 second
                            
                            # Spawn enemy mới
                            self.spawn_enemy()
                            
                            # Tăng wave
                            self.wave += 1
                        break  # Bullet đã hit, không cần check enemy khác
                        
            elif bullet.owner == "enemy":
                # Bullet từ enemy, check vs player
                dx = bullet.x - self.player.x
                dy = bullet.y - self.player.y
                distance_squared = dx*dx + dy*dy
                
                if distance_squared < TANK_RADIUS * TANK_RADIUS:
                    # Hit player
                    self.player.take_damage(bullet.damage)
                    bullet.alive = False
        
        # Xóa phần này vì đã gộp vào collision detection ở trên
    
    def restart_game(self):
        """Restart game"""
        self.init_game()
    
    def draw(self, win):
        """Vẽ game"""
        # Vẽ background - thay đổi từ BLACK sang WHITE để dễ nhìn
        win.fill(WHITE)
        
        # Vẽ player
        if self.player and self.player.alive:
            self.player.draw(win)
            self.player.draw_skill_targeting(win)
        
        # Vẽ enemies
        for enemy in self.enemies:
            if enemy.alive:
                enemy.draw(win)
        
        # Vẽ bullets
        for bullet in self.bullets:
            if bullet.alive:
                bullet.draw(win)
        
        # Vẽ fire areas
        for fire_area in self.fire_areas:
            if fire_area.active:
                fire_area.draw(win)
        
        # Vẽ UI
        self.draw_ui(win)
    
    def draw_ui(self, win):
        """Vẽ UI"""
        if not self.player:
            return
        
        # Skill bar
        self.player.draw_skill_bar(win, 20, HEIGHT - 100)
        
        # Game info
        font = pygame.font.SysFont(None, 36)
        
        # Score
        score_text = font.render(f"Score: {self.score}", True, BLACK)
        win.blit(score_text, (20, 20))
        
        # Wave
        wave_text = font.render(f"Wave: {self.wave}", True, BLACK)
        win.blit(wave_text, (20, 60))
        
        # Tank type
        tank_text = font.render(f"Tank: {self.player.tank_type.title()}", True, BLACK)
        win.blit(tank_text, (WIDTH - 200, 20))
        
        # Player HP
        hp_text = font.render(f"HP: {self.player.hp}/{self.player.stats.hp}", True, BLACK)
        win.blit(hp_text, (WIDTH - 200, 60))
        
        # Skill mode indicator
        if self.player.skill_mode:
            skill_text = font.render(f"Skill Mode: {self.player.active_skill.title()}", True, LIGHT_BLUE)
            win.blit(skill_text, (WIDTH//2 - 100, 20))
        
        # Buff indicators
        if self.player.shield_active:
            shield_text = font.render("Shield Active!", True, CYAN)
            win.blit(shield_text, (WIDTH//2 - 100, 60))
        
        if self.player.speed_boost_active:
            speed_text = font.render("Speed Boost Active!", True, YELLOW)
            win.blit(speed_text, (WIDTH//2 - 100, 100))
        
        # Pause indicator
        if self.paused:
            pause_text = font.render("PAUSED", True, RED)
            win.blit(pause_text, (WIDTH//2 - 50, HEIGHT//2))
        
        # Game over
        if self.game_over:
            game_over_text = font.render("GAME OVER", True, RED)
            restart_text = font.render("Press R to restart", True, BLACK)
            win.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2 - 50))
            win.blit(restart_text, (WIDTH//2 - 100, HEIGHT//2))
