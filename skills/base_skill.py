import pygame
from game_config import *

class BaseSkill:
    """Base class cho tất cả skills"""
    
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
        """Sử dụng skill"""
        if self.ready:
            self.current_cooldown = self.cooldown
            self.ready = False
            return True
        return False
    
    def update(self):
        """Cập nhật cooldown"""
        if not self.ready:
            self.current_cooldown -= 1
            if self.current_cooldown <= 0:
                self.ready = True
    
    def get_cooldown_ratio(self):
        """Lấy tỷ lệ cooldown còn lại"""
        if self.cooldown == 0:
            return 0
        return self.current_cooldown / self.cooldown
    
    def can_use(self):
        """Kiểm tra có thể sử dụng skill không"""
        return self.ready
    
    def get_remaining_cooldown(self):
        """Lấy cooldown còn lại"""
        return max(0, self.current_cooldown)
    
    def reset_cooldown(self):
        """Reset cooldown về 0"""
        self.current_cooldown = 0
        self.ready = True
