import pygame
import math
import random
from game_config import *
from entities.base.enemy import BaseEnemy

class TankEnemy(BaseEnemy):
    """Enemy máu cao với tốc độ chậm"""
    
    def __init__(self, x, y):
        # Stats cho enemy máu cao
        tank_stats = BaseStats(
            hp=200,          # HP cao hơn
            speed=1,         # Chậm hơn
            attack_speed=80, # Bắn chậm hơn
            damage=30,       # Damage cao hơn
            defense=5,       # Có defense
            attack=30
        )
        
        super().__init__(x, y, tank_stats, ENEMY_TYPE_TANK, DARK_BLUE, DARK_BLUE)
    
    def update_ai(self, player_pos, bullets):
        """AI behavior cho enemy máu cao"""
        super().update_ai(player_pos, bullets)
        
        # Tank enemy có thể có behavior khác
        # Ví dụ: Ít né đạn hơn, tập trung vào việc bắn
        if self.dodge_timer > 0:
            self.dodge_timer = max(0, self.dodge_timer - 2)  # Giảm thời gian né
