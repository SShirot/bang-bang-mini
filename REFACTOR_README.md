# Refactor Guide - Modular Game Structure

## 🏗️ Cấu trúc mới

```
bang-bang-mini/
├── entities/
│   ├── base/
│   │   ├── entity.py          # Base class cho tất cả entities
│   │   ├── tank.py            # Base class cho tanks
│   │   └── enemy.py           # Base class cho enemies
│   ├── tanks/
│   │   ├── naruto_tank.py     # Tank Naruto cụ thể
│   │   └── sasuke_tank.py     # Tank Sasuke cụ thể (sẽ tạo)
│   └── enemies/
│       ├── basic_enemy.py     # Enemy cơ bản (sẽ tạo)
│       ├── fast_enemy.py      # Enemy nhanh (sẽ tạo)
│       └── tank_enemy.py      # Enemy máu cao (sẽ tạo)
├── skills/
│   ├── base_skill.py          # Base class cho skills
│   ├── directional_skills.py  # Skills định hướng (sẽ tạo)
│   ├── buff_skills.py         # Skills buff (sẽ tạo)
│   └── area_skills.py         # Skills vùng (sẽ tạo)
├── game_config.py              # Cấu hình và stats chung
├── game_objects.py             # Các object cũ (sẽ refactor)
├── game_manager.py             # Game manager (sẽ refactor)
└── game.py                     # Main game loop
```

## 🎯 Lợi ích của cấu trúc mới

### 1. **Modular Design:**
- **Dễ thêm mới:** Tank, Enemy, Skill mới
- **Tách biệt logic:** Mỗi class có trách nhiệm riêng
- **Dễ maintain:** Sửa lỗi và cải tiến dễ dàng
- **Reusable code:** Base classes có thể dùng lại

### 2. **Stats System:**
- **Shared stats:** Speed, HP, Damage, Defense, Attack
- **Customizable:** Mỗi entity có thể override stats
- **Balanced:** Dễ dàng cân bằng game

### 3. **Inheritance System:**
- **BaseEntity:** Chứa logic chung
- **BaseTank:** Kế thừa từ BaseEntity + logic tank
- **Specific Tanks:** Kế thừa từ BaseTank + skills riêng

## 🚀 Cách thêm Tank mới

### 1. **Tạo file mới:**
```python
# entities/tanks/new_tank.py
from entities.base.tank import BaseTank
from skills.base_skill import BaseSkill

class NewTank(BaseTank):
    def __init__(self, x, y):
        # Stats riêng
        new_stats = BaseStats(
            hp=120,          # HP cao hơn
            speed=4,         # Nhanh hơn
            attack_speed=45, # Bắn nhanh hơn
            damage=25,       # Damage cao hơn
            defense=5,       # Có defense
            attack=25
        )
        
        super().__init__(x, y, new_stats, "new_tank", BLUE, RED)
    
    def init_skills(self):
        # Skills riêng
        self.skills = {
            'skill1': BaseSkill("Skill 1", 120, 'E', YELLOW, '⚡', 100, SKILL_TYPE_DIRECTIONAL),
            'skill2': BaseSkill("Skill 2", 300, 'SPACE', ORANGE, '💥', None, SKILL_TYPE_DIRECTIONAL),
            'skill3': BaseSkill("Skill 3", 300, 'Q', PURPLE, '❤️', None, SKILL_TYPE_BUFF),
            'skill4': BaseSkill("Skill 4", 600, 'F', CYAN, '🛡️', None, SKILL_TYPE_BUFF)
        }
```

### 2. **Thêm vào game_config.py:**
```python
# Tank types
TANK_TYPE_NEW = "new_tank"
```

### 3. **Import và sử dụng:**
```python
from entities.tanks.new_tank import NewTank

# Trong GameManager
if tank_type == TANK_TYPE_NEW:
    self.player = NewTank(WIDTH//2, HEIGHT//2)
```

## 🎯 Cách thêm Enemy mới

### 1. **Tạo file mới:**
```python
# entities/enemies/fast_enemy.py
from entities.base.enemy import BaseEnemy

class FastEnemy(BaseEnemy):
    def __init__(self, x, y):
        # Stats riêng cho enemy nhanh
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
        # AI behavior riêng
        super().update_ai(player_pos, bullets)
        # Thêm logic riêng nếu cần
```

### 2. **Thêm vào game_config.py:**
```python
# Enemy types
ENEMY_TYPE_FAST = "fast"
```

## ⚡ Cách thêm Skill mới

### 1. **Tạo skill class:**
```python
# skills/directional_skills.py
from skills.base_skill import BaseSkill

class DashSkill(BaseSkill):
    def __init__(self):
        super().__init__("Dash", DASH_COOLDOWN, 'E', YELLOW, '⚡', DASH_RANGE, SKILL_TYPE_DIRECTIONAL)
    
    def execute(self, tank, target_pos):
        # Logic thực thi skill
        return tank.execute_dash(target_pos)
```

### 2. **Sử dụng trong tank:**
```python
from skills.directional_skills import DashSkill

def init_skills(self):
    self.skills = {
        'dash': DashSkill(),
        # ... other skills
    }
```

## 🔧 Cách thêm Stats mới

### 1. **Thêm vào BaseStats:**
```python
class BaseStats:
    def __init__(self, hp=100, speed=3, attack_speed=60, damage=20, defense=0, attack=20, 
                 critical_chance=0.05, critical_damage=1.5, dodge_chance=0.1):
        self.hp = hp
        self.speed = speed
        self.attack_speed = attack_speed
        self.damage = damage
        self.defense = defense
        self.attack = attack
        self.critical_chance = critical_chance
        self.critical_damage = critical_damage
        self.dodge_chance = dodge_chance
```

### 2. **Sử dụng trong entities:**
```python
def take_damage(self, amount):
    # Dodge check
    if random.random() < self.stats.dodge_chance:
        return  # Dodge thành công
    
    # Critical hit check
    if random.random() < self.stats.critical_chance:
        amount *= self.stats.critical_damage
    
    # Defense calculation
    actual_damage = max(1, amount - self.stats.defense)
    self.hp -= actual_damage
```

## 📝 Checklist để hoàn thành refactor

### ✅ Đã hoàn thành:
- [x] Base classes (Entity, Tank, Enemy)
- [x] Stats system
- [x] Skill base class
- [x] Naruto tank class
- [x] Cấu trúc thư mục

### 🔄 Cần làm tiếp:
- [ ] Sasuke tank class
- [ ] Enemy classes (Basic, Fast, Tank)
- [ ] Skill classes (Directional, Buff, Area)
- [ ] Refactor GameManager
- [ ] Refactor game_objects.py
- [ ] Update imports và dependencies
- [ ] Test toàn bộ system

## 💡 Tips khi refactor

### 1. **Incremental Changes:**
- Thay đổi từng phần một
- Test sau mỗi thay đổi
- Không refactor tất cả cùng lúc

### 2. **Backward Compatibility:**
- Giữ nguyên interface cũ
- Thay đổi dần dần
- Fallback về code cũ nếu cần

### 3. **Testing:**
- Test từng class riêng biệt
- Test integration giữa các class
- Test performance và memory usage

## 🆘 Troubleshooting

### **Import errors:**
- Kiểm tra đường dẫn import
- Kiểm tra __init__.py files
- Kiểm tra circular imports

### **Stats không hoạt động:**
- Kiểm tra BaseStats class
- Kiểm tra inheritance chain
- Kiểm tra override methods

### **Skills không hoạt động:**
- Kiểm tra skill initialization
- Kiểm tra skill execution
- Kiểm tra cooldown system

## 🚀 Next Steps

1. **Hoàn thành Sasuke tank**
2. **Tạo enemy classes**
3. **Refactor skill system**
4. **Update GameManager**
5. **Test toàn bộ system**
6. **Documentation và examples**

Bạn có muốn tôi tiếp tục refactor phần nào tiếp theo không? 🎮
