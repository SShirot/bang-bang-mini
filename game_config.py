# Game Configuration
import pygame

# Screen settings
WIDTH = 1000
HEIGHT = 700
FPS = 60

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
DARK_BLUE = (0, 0, 150)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
LIGHT_BLUE = (173, 216, 230)
SKILL_RANGE_COLOR = (135, 206, 235)  # Màu xanh nhạt cho vòng tròn range skill
FIRE_COLOR = (255, 69, 0)  # Màu cam đỏ cho fire skill

# Game settings
PLAYER_SPEED = 3
PLAYER_FIRE_RATE = 60  # 1 bullet per second
ENEMY_BASE_SPEED = 2
ENEMY_BASE_FIRE_RATE = 60
ENEMY_MAX_SPEED = 5
ENEMY_MIN_FIRE_RATE = 20

# Skill cooldowns (in frames)
DASH_COOLDOWN = 120      # 2 seconds
POWER_SHOT_COOLDOWN = 300  # 5 seconds
HEAL_COOLDOWN = 300      # 5 seconds
SHIELD_COOLDOWN = 600    # 10 seconds
FIRE_AREA_COOLDOWN = 400  # ~6.7 seconds
SPEED_BOOST_COOLDOWN = 450  # 7.5 seconds

# Skill ranges
DASH_RANGE = 100
POWER_SHOT_RANGE = None  # Vô hạn - không giới hạn khoảng cách
HEAL_RANGE = None        # Buff skill - không cần range
SHIELD_RANGE = None      # Buff skill - không cần range
FIRE_AREA_RANGE = 150    # Range cho fire area skill
SPEED_BOOST_RANGE = None # Buff skill - không cần range

# Bullet settings
BULLET_SPEED = 7
BULLET_DAMAGE = 20
POWER_SHOT_BONUS_DAMAGE = 20
POWER_SHOT_SPEED = 10

# Tank settings
TANK_SIZE = 40
TURRET_LENGTH = 35
TANK_RADIUS = 20

# Skill types
SKILL_TYPE_DIRECTIONAL = "directional"      # Skill định hướng (cần nhắm)
SKILL_TYPE_BUFF = "buff"                    # Skill buff (không cần nhắm)
SKILL_TYPE_TARGETED = "targeted"            # Skill chỉ định enemy (cần nhắm enemy)
SKILL_TYPE_AREA = "area"                    # Skill vùng (tạo hiệu ứng trong vùng)

# Tank types
TANK_TYPE_NARUTO = "naruto"     # Tank đầu tiên (cũ)
TANK_TYPE_SASUKE = "sasuke"     # Tank thứ hai (mới)

# Fire area settings
FIRE_AREA_DURATION = 180        # 3 seconds
FIRE_DAMAGE_PER_SECOND = 5      # Damage mỗi giây
FIRE_SLOW_FACTOR = 0.5          # Làm chậm 50%
SPEED_BOOST_FACTOR = 2.0        # Tăng tốc gấp đôi
SPEED_BOOST_DURATION = 180      # 3 seconds
