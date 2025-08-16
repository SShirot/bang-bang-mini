import pygame
import math
import random
from game_config import *
from entities.base.enemy import BaseEnemy

class BasicEnemy(BaseEnemy):
    """Enemy cơ bản với stats cân bằng"""
    
    def __init__(self, x, y):
        # Stats cơ bản
        basic_stats = BaseStats(
            hp=100,
            speed=2,
            attack_speed=60,
            damage=20,
            defense=0,
            attack=20
        )
        
        super().__init__(x, y, basic_stats, ENEMY_TYPE_BASIC, BLUE, BLUE)
    
    def update_ai(self, player_pos, bullets):
        """AI behavior cơ bản"""
        super().update_ai(player_pos, bullets)
        
        # Thêm logic riêng nếu cần
        # Ví dụ: Basic enemy có thể có behavior đặc biệt
