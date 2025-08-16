#!/usr/bin/env python3
"""
Test file để kiểm tra hệ thống modular mới
Chạy file này để test từng component riêng biệt
"""

import sys
import os

# Thêm thư mục hiện tại vào Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test import các module mới"""
    print("🧪 Testing imports...")
    
    try:
        # Test base classes
        from entities.base.entity import BaseEntity
        from entities.base.tank import BaseTank
        from entities.base.enemy import BaseEnemy
        print("✅ Base classes imported successfully")
        
        # Test specific tanks
        from entities.tanks.naruto_tank import NarutoTank
        from entities.tanks.sasuke_tank import SasukeTank
        print("✅ Tank classes imported successfully")
        
        # Test enemies
        from entities.enemies.basic_enemy import BasicEnemy
        from entities.enemies.fast_enemy import FastEnemy
        from entities.enemies.tank_enemy import TankEnemy
        print("✅ Enemy classes imported successfully")
        
        # Test skills
        from skills.base_skill import BaseSkill
        print("✅ Skill classes imported successfully")
        
        # Test config
        from game_config import BaseStats, PLAYER_BASE_STATS, ENEMY_BASE_STATS
        print("✅ Game config imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_base_stats():
    """Test BaseStats system"""
    print("\n🧪 Testing BaseStats system...")
    
    try:
        from game_config import BaseStats, PLAYER_BASE_STATS, ENEMY_BASE_STATS
        
        # Test basic stats
        stats = BaseStats(hp=100, speed=3, attack_speed=60, damage=20)
        print(f"✅ BaseStats created: HP={stats.hp}, Speed={stats.speed}")
        
        # Test player stats
        player_stats = PLAYER_BASE_STATS
        print(f"✅ Player stats: HP={player_stats.hp}, Speed={player_stats.speed}")
        
        # Test enemy stats
        enemy_stats = ENEMY_BASE_STATS
        print(f"✅ Enemy stats: HP={enemy_stats.hp}, Speed={enemy_stats.speed}")
        
        return True
        
    except Exception as e:
        print(f"❌ BaseStats test failed: {e}")
        return False

def test_tank_creation():
    """Test tạo tanks"""
    print("\n🧪 Testing tank creation...")
    
    try:
        from entities.tanks.naruto_tank import NarutoTank
        from entities.tanks.sasuke_tank import SasukeTank
        
        # Test Naruto tank
        naruto = NarutoTank(100, 100)
        print(f"✅ Naruto tank created: Type={naruto.tank_type}, HP={naruto.hp}")
        print(f"   Skills: {list(naruto.skills.keys())}")
        
        # Test Sasuke tank
        sasuke = SasukeTank(200, 200)
        print(f"✅ Sasuke tank created: Type={sasuke.tank_type}, HP={sasuke.hp}")
        print(f"   Skills: {list(sasuke.skills.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Tank creation test failed: {e}")
        return False

def test_enemy_creation():
    """Test tạo enemies"""
    print("\n🧪 Testing enemy creation...")
    
    try:
        from entities.enemies.basic_enemy import BasicEnemy
        from entities.enemies.fast_enemy import FastEnemy
        from entities.enemies.tank_enemy import TankEnemy
        
        # Test Basic enemy
        basic = BasicEnemy(100, 100)
        print(f"✅ Basic enemy created: Type={basic.enemy_type}, HP={basic.hp}")
        
        # Test Fast enemy
        fast = FastEnemy(200, 200)
        print(f"✅ Fast enemy created: Type={fast.enemy_type}, HP={fast.hp}, Speed={fast.speed}")
        
        # Test Tank enemy
        tank = TankEnemy(300, 300)
        print(f"✅ Tank enemy created: Type={tank.enemy_type}, HP={tank.hp}, Defense={tank.stats.defense}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enemy creation test failed: {e}")
        return False

def test_skill_system():
    """Test skill system"""
    print("\n🧪 Testing skill system...")
    
    try:
        from skills.base_skill import BaseSkill
        from game_config import DASH_COOLDOWN, YELLOW, DASH_RANGE, SKILL_TYPE_DIRECTIONAL
        
        # Test skill creation
        dash_skill = BaseSkill("Dash", DASH_COOLDOWN, 'E', YELLOW, '⚡', DASH_RANGE, SKILL_TYPE_DIRECTIONAL)
        print(f"✅ Dash skill created: Name={dash_skill.name}, Cooldown={dash_skill.cooldown}")
        
        # Test skill usage
        if dash_skill.use():
            print("✅ Skill used successfully")
        else:
            print("❌ Skill usage failed")
        
        # Test cooldown
        dash_skill.update()
        print(f"✅ Skill cooldown: {dash_skill.get_remaining_cooldown()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Skill system test failed: {e}")
        return False

def test_inheritance():
    """Test inheritance system"""
    print("\n🧪 Testing inheritance system...")
    
    try:
        from entities.base.entity import BaseEntity
        from entities.base.tank import BaseTank
        from entities.tanks.naruto_tank import NarutoTank
        
        # Test inheritance chain
        naruto = NarutoTank(100, 100)
        
        # Kiểm tra inheritance
        is_base_entity = isinstance(naruto, BaseEntity)
        is_base_tank = isinstance(naruto, BaseTank)
        is_naruto = isinstance(naruto, NarutoTank)
        
        print(f"✅ Inheritance check: BaseEntity={is_base_entity}, BaseTank={is_base_tank}, Naruto={is_naruto}")
        
        # Test method inheritance
        if hasattr(naruto, 'take_damage'):
            print("✅ BaseEntity methods inherited")
        else:
            print("❌ BaseEntity methods not inherited")
        
        if hasattr(naruto, 'execute_dash'):
            print("✅ Naruto-specific methods available")
        else:
            print("❌ Naruto-specific methods not available")
        
        return True
        
    except Exception as e:
        print(f"❌ Inheritance test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting modular system tests...\n")
    
    tests = [
        test_imports,
        test_base_stats,
        test_tank_creation,
        test_enemy_creation,
        test_skill_system,
        test_inheritance
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            print(f"\n🔍 Running {test.__name__}...")
            if test():
                passed += 1
                print(f"✅ {test.__name__} passed")
            else:
                print(f"❌ {test.__name__} failed")
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
