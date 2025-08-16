import pygame
import sys
from game_config import *
from game_manager import GameManager

class HomeScreen:
    def __init__(self):
        self.selected_tank = TANK_TYPE_NARUTO
        self.tank_options = [
            {"type": TANK_TYPE_NARUTO, "name": "Naruto", "color": DARK_GREEN, "description": "Dash + Power Shot + Heal + Shield"},
            {"type": TANK_TYPE_SASUKE, "name": "Sasuke", "color": PURPLE, "description": "Fire Area + Speed Boost + Heal + Shield"}
        ]
        
    def draw(self, win):
        """Vẽ màn hình home"""
        win.fill(WHITE)
        
        # Title
        title_font = pygame.font.SysFont(None, 72)
        title_text = title_font.render("TANK BATTLE", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH//2, 120))
        win.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_font = pygame.font.SysFont(None, 36)
        subtitle_text = subtitle_font.render("Choose Your Tank", True, BLUE)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH//2, 180))
        win.blit(subtitle_text, subtitle_rect)
        
        # Tank selection
        self.draw_tank_selection(win)
        
        # Instructions
        self.draw_instructions(win)
        
        # Buttons
        self.draw_buttons(win)
        
    def draw_tank_selection(self, win):
        """Vẽ phần chọn tank"""
        tank_y = 280
        tank_width = 350
        tank_height = 140
        spacing = 80
        
        # Tính toán vị trí để tank được chọn ở giữa
        selected_index = next(i for i, tank in enumerate(self.tank_options) if tank["type"] == self.selected_tank)
        center_offset = selected_index * (tank_width + spacing)
        
        for i, tank in enumerate(self.tank_options):
            # Tính vị trí để tank được chọn ở giữa
            tank_x = WIDTH//2 - tank_width//2 - center_offset + i * (tank_width + spacing)
            
            # Background
            bg_color = LIGHT_BLUE if tank["type"] == self.selected_tank else WHITE
            pygame.draw.rect(win, bg_color, (tank_x, tank_y, tank_width, tank_height))
            pygame.draw.rect(win, BLACK, (tank_x, tank_y, tank_width, tank_height), 3)
            
            # Tank name
            name_font = pygame.font.SysFont(None, 40)
            name_text = name_font.render(tank["name"], True, tank["color"])
            name_rect = name_text.get_rect(center=(tank_x + tank_width//2, tank_y + 35))
            win.blit(name_text, name_rect)
            
            # Tank preview (vẽ tank nhỏ)
            tank_center_x = tank_x + tank_width//2
            tank_center_y = tank_y + 80
            pygame.draw.rect(win, tank["color"], (tank_center_x - 18, tank_center_y - 18, 36, 36))
            pygame.draw.line(win, tank["color"], (tank_center_x, tank_center_y), (tank_center_x + 25, tank_center_y), 5)
            
            # Description
            desc_font = pygame.font.SysFont(None, 18)
            desc_text = desc_font.render(tank["description"], True, BLACK)
            desc_rect = desc_text.get_rect(center=(tank_x + tank_width//2, tank_y + 115))
            win.blit(desc_text, desc_rect)
            
            # Selection indicator
            if tank["type"] == self.selected_tank:
                pygame.draw.rect(win, GREEN, (tank_x - 5, tank_y - 5, tank_width + 10, tank_height + 10), 5)
        
        # Vẽ nút Previous và Next
        self.draw_navigation_buttons(win, tank_y, tank_height)
    
    def draw_navigation_buttons(self, win, tank_y, tank_height):
        """Vẽ nút điều hướng tank"""
        button_size = 50
        button_y = tank_y + tank_height//2 - button_size//2
        
        # Previous button (<)
        prev_x = 50
        prev_color = LIGHT_BLUE if len(self.tank_options) > 1 else (150, 150, 150)
        pygame.draw.rect(win, prev_color, (prev_x, button_y, button_size, button_size))
        pygame.draw.rect(win, BLACK, (prev_x, button_y, button_size, button_size), 3)
        
        # Vẽ mũi tên <
        arrow_font = pygame.font.SysFont(None, 36)
        arrow_text = arrow_font.render("<", True, BLACK)
        arrow_rect = arrow_text.get_rect(center=(prev_x + button_size//2, button_y + button_size//2))
        win.blit(arrow_text, arrow_rect)
        
        # Next button (>)
        next_x = WIDTH - 50 - button_size
        next_color = LIGHT_BLUE if len(self.tank_options) > 1 else (150, 150, 150)
        pygame.draw.rect(win, next_color, (next_x, button_y, button_size, button_size))
        pygame.draw.rect(win, BLACK, (next_x, button_y, button_size, button_size), 3)
        
        # Vẽ mũi tên >
        arrow_text = arrow_font.render(">", True, BLACK)
        arrow_rect = arrow_text.get_rect(center=(next_x + button_size//2, button_y + button_size//2))
        win.blit(arrow_text, arrow_rect)
    
    def draw_instructions(self, win):
        """Vẽ hướng dẫn điều khiển"""
        instructions_y = 500
        
        # Tank controls
        controls_font = pygame.font.SysFont(None, 26)
        controls_text = [
            "Controls:",
            "WASD - Move | Mouse - Aim | Left Click - Fire",
            "E - Skill 1 | Q - Heal | F - Shield | Space - Skill 2",
            "Use < > buttons or Arrow Keys to select tank"
        ]
        
        for i, text in enumerate(controls_text):
            color = BLUE if i == 0 else BLACK
            text_surface = controls_font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(WIDTH//2, instructions_y + i * 30))
            win.blit(text_surface, text_rect)
    
    def draw_buttons(self, win):
        """Vẽ các nút"""
        button_y = HEIGHT - 120
        button_width = 180
        button_height = 60
        spacing = 60
        
        # Start Game button
        start_x = WIDTH//2 - button_width - spacing//2
        start_color = GREEN
        pygame.draw.rect(win, start_color, (start_x, button_y, button_width, button_height))
        pygame.draw.rect(win, BLACK, (start_x, button_y, button_width, button_height), 3)
        
        start_font = pygame.font.SysFont(None, 32)
        start_text = start_font.render("START GAME", True, BLACK)
        start_rect = start_text.get_rect(center=(start_x + button_width//2, button_y + button_height//2))
        win.blit(start_text, start_rect)
        
        # Quit button
        quit_x = WIDTH//2 + spacing//2
        quit_color = RED
        pygame.draw.rect(win, quit_color, (quit_x, button_y, button_width, button_height))
        pygame.draw.rect(win, BLACK, (quit_x, button_y, button_width, button_height), 3)
        
        quit_font = pygame.font.SysFont(None, 32)
        quit_text = quit_font.render("QUIT", True, BLACK)
        quit_rect = quit_text.get_rect(center=(quit_x + button_width//2, button_y + button_height//2))
        win.blit(quit_text, quit_rect)
    
    def handle_click(self, pos):
        """Xử lý click chuột"""
        x, y = pos
        
        # Kiểm tra click vào navigation buttons
        button_size = 50
        tank_y = 280
        tank_height = 140
        button_y = tank_y + tank_height//2 - button_size//2
        
        # Previous button (<)
        prev_x = 50
        if prev_x <= x <= prev_x + button_size and button_y <= y <= button_y + button_size:
            if len(self.tank_options) > 1:
                current_index = next(i for i, tank in enumerate(self.tank_options) if tank["type"] == self.selected_tank)
                self.selected_tank = self.tank_options[(current_index - 1) % len(self.tank_options)]["type"]
            return None
        
        # Next button (>)
        next_x = WIDTH - 50 - button_size
        if next_x <= x <= next_x + button_size and button_y <= y <= button_y + button_size:
            if len(self.tank_options) > 1:
                current_index = next(i for i, tank in enumerate(self.tank_options) if tank["type"] == self.selected_tank)
                self.selected_tank = self.tank_options[(current_index + 1) % len(self.tank_options)]["type"]
            return None
        
        # Kiểm tra click vào tank selection
        tank_width = 350
        spacing = 80
        
        # Tính toán vị trí để tank được chọn ở giữa
        selected_index = next(i for i, tank in enumerate(self.tank_options) if tank["type"] == self.selected_tank)
        center_offset = selected_index * (tank_width + spacing)
        
        for i, tank in enumerate(self.tank_options):
            # Tính vị trí để tank được chọn ở giữa
            tank_x = WIDTH//2 - tank_width//2 - center_offset + i * (tank_width + spacing)
            if tank_x <= x <= tank_x + tank_width and tank_y <= y <= tank_y + tank_height:
                self.selected_tank = tank["type"]
                return None
        
        # Kiểm tra click vào buttons
        button_y = HEIGHT - 120
        button_width = 180
        button_height = 60
        spacing = 60
        
        # Start Game button
        start_x = WIDTH//2 - button_width - spacing//2
        if start_x <= x <= start_x + button_width and button_y <= y <= button_y + button_height:
            return "start_game"
        
        # Quit button
        quit_x = WIDTH//2 + spacing//2
        if quit_x <= x <= quit_x + button_width and button_y <= y <= button_y + button_height:
            return "quit"
        
        return None
    
    def handle_keydown(self, key):
        """Xử lý phím nhấn"""
        if key == pygame.K_LEFT:
            # Chọn tank trước
            current_index = next(i for i, tank in enumerate(self.tank_options) if tank["type"] == self.selected_tank)
            self.selected_tank = self.tank_options[(current_index - 1) % len(self.tank_options)]["type"]
        elif key == pygame.K_RIGHT:
            # Chọn tank sau
            current_index = next(i for i, tank in enumerate(self.tank_options) if tank["type"] == self.selected_tank)
            self.selected_tank = self.tank_options[(current_index + 1) % len(self.tank_options)]["type"]
        elif key == pygame.K_RETURN:
            # Enter để start game
            return "start_game"
        elif key == pygame.K_ESCAPE:
            # ESC để quit
            return "quit"
        
        return None

def main():
    pygame.init()
    
    # Khởi tạo màn hình
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tank Battle: Choose Your Tank")
    
    # Khởi tạo home screen và game manager
    home_screen = HomeScreen()
    game_manager = GameManager()
    
    # Game state
    current_screen = "home"  # "home" hoặc "game"
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        clock.tick(FPS)
        
        if current_screen == "home":
            # Vẽ home screen
            home_screen.draw(WIN)
            pygame.display.update()
            
            # Xử lý events cho home screen
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    action = home_screen.handle_keydown(event.key)
                    if action == "start_game":
                        # Chuyển sang game screen
                        game_manager.set_tank_type(home_screen.selected_tank)
                        game_manager.init_game()
                        current_screen = "game"
                        pygame.display.set_caption("Tank Battle: Player vs Enemy")
                    elif action == "quit":
                        running = False
                        break
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    action = home_screen.handle_click(pygame.mouse.get_pos())
                    if action == "start_game":
                        # Chuyển sang game screen
                        game_manager.set_tank_type(home_screen.selected_tank)
                        game_manager.init_game()
                        current_screen = "game"
                        pygame.display.set_caption("Tank Battle: Player vs Enemy")
                    elif action == "quit":
                        running = False
                        break
                        
        elif current_screen == "game":
            # Xử lý sự kiện game
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                    break
            
            if not running:
                break
            
            # Xử lý events cho game
            game_manager.handle_events(events)
            
            # Cập nhật game
            game_manager.update()
            
            # Vẽ game
            game_manager.draw(WIN)
            
            pygame.display.update()
            
            # Kiểm tra nếu player chết hoặc muốn về home
            if game_manager.game_over:
                # Đợi một chút rồi về home
                pygame.time.wait(2000)
                current_screen = "home"
                pygame.display.set_caption("Tank Battle: Choose Your Tank")
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
