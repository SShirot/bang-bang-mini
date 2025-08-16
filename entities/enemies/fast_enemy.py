import pygame
import math
import random
from game_config import *
from entities.base.enemy import BaseEnemy

class FastEnemy(BaseEnemy):
    """Enemy nhanh với HP thấp"""
    
    def __init__(self, x, y):
        # Stats cho enemy nhanh
        fast_stats = BaseStats(
            hp=80,           # HP thấp hơn
            speed=5,         # Nhanh hơn
            attack_speed=40, # Bắn nhanh hơn
            damage=15,       # Damage thấp hơn
            defense=0,
            attack=15
        )
        
        super().__init__(x, y, fast_stats, ENEMY_TYPE_FAST, RED, RED)
    
    def update_ai(self, player_pos, bullets):
        """AI behavior cho enemy nhanh"""
        super().update_ai(player_pos, bullets)
        
        # Fast enemy có thể có behavior khác
        # Ví dụ: Di chuyển nhanh hơn khi né đạn
        if self.dodge_timer > 0:
            self.speed = self.stats.speed * 1.5  # Tăng tốc khi né
        else:
            self.speed = self.stats.speed
