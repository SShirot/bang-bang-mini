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

# Base Stats System
class BaseStats:
    """Base stats cho tất cả units"""
    def __init__(self, hp=100, speed=3, attack_speed=60, damage=20, defense=0, attack=20):
        self.hp = hp
        self.speed = speed
        self.attack_speed = attack_speed  # Frames giữa các lần bắn
        self.damage = damage
        self.defense = defense
        self.attack = attack

# Base Player Stats
PLAYER_BASE_STATS = BaseStats(
    hp=100,
    speed=3,
    attack_speed=60,  # 1 bullet per second
    damage=20,
    defense=0,
    attack=20
)

# Base Enemy Stats
ENEMY_BASE_STATS = BaseStats(
    hp=100,
    speed=2,
    attack_speed=60,
    damage=20,
    defense=0,
    attack=20
)

# Game settings
PLAYER_SPEED = PLAYER_BASE_STATS.speed
PLAYER_FIRE_RATE = PLAYER_BASE_STATS.attack_speed
ENEMY_BASE_SPEED = ENEMY_BASE_STATS.speed
ENEMY_BASE_FIRE_RATE = ENEMY_BASE_STATS.attack_speed
ENEMY_MAX_SPEED = 5
ENEMY_MIN_FIRE_RATE = 20

# Skill cooldowns (in frames)
DASH_COOLDOWN = 120      # 2 seconds
POWER_SHOT_COOLDOWN = 300  # 5 seconds
HEAL_COOLDOWN = 300      # 5 seconds
SHIELD_COOLDOWN = 600    # 10 seconds
FIRE_AREA_COOLDOWN = 400  # ~6.7 seconds
SPEED_BOOST_COOLDOWN = 450  # 7.5 seconds
DIVINE_ARROW_COOLDOWN = 600  # 10 seconds

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

# Debug: In ra constants
print(f"BULLET_SPEED: {BULLET_SPEED}")
print(f"WIDTH: {WIDTH}, HEIGHT: {HEIGHT}")
print(f"PLAYER_FIRE_RATE: {PLAYER_FIRE_RATE}")

# Tank settings
TANK_SIZE = 60          # Tăng từ 40 lên 60 (50% lớn hơn)
TURRET_LENGTH = 55      # Giữ nguyên
TANK_RADIUS = 30        # Tăng từ 20 lên 30 (tương ứng với TANK_SIZE)

# Skill types
SKILL_TYPE_DIRECTIONAL = "directional"      # Skill định hướng (cần nhắm)
SKILL_TYPE_BUFF = "buff"                    # Skill buff (không cần nhắm)
SKILL_TYPE_TARGETED = "targeted"            # Skill chỉ định enemy (cần nhắm enemy)
SKILL_TYPE_AREA = "area"                    # Skill vùng (tạo hiệu ứng trong vùng)

# Tank types
TANK_TYPE_NARUTO = "naruto"     # Tank đầu tiên (cũ)
TANK_TYPE_SASUKE = "sasuke"     # Tank thứ hai (mới)

# Enemy types
ENEMY_TYPE_BASIC = "basic"
ENEMY_TYPE_FAST = "fast"
ENEMY_TYPE_TANK = "tank"

# Fire area settings
FIRE_AREA_DURATION = 300  # 5 seconds
FIRE_DAMAGE_PER_SECOND = 10
FIRE_SLOW_FACTOR = 0.5

# Speed boost settings
SPEED_BOOST_FACTOR = 1.5  # Reduced from 2.0
SPEED_BOOST_DURATION = 180  # 3 seconds, reduced from 5 seconds
