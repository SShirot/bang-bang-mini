# Tank Battle Game - Refactored Version

## Cấu trúc dự án mới

Game đã được refactor để dễ scale và maintain hơn với cấu trúc module:

### 📁 Các file chính:

#### `game.py` - File chính
- **Chức năng**: Khởi tạo game và chạy game loop với Home Screen
- **Đơn giản**: Chỉ 40 dòng code, dễ đọc và hiểu
- **Trách nhiệm**: Khởi tạo pygame, tạo HomeScreen và GameManager, chạy game loop

#### `game_config.py` - Cấu hình
- **Chứa**: Tất cả constants, colors, settings
- **Lợi ích**: Dễ thay đổi giá trị game mà không cần sửa code logic
- **Ví dụ**: Thay đổi FPS, kích thước màn hình, cooldown skills

#### `game_objects.py` - Game objects
- **Classes**: Tank, Bullet, Skill, FireArea
- **Logic**: Tất cả logic của từng object riêng biệt
- **Tái sử dụng**: Có thể dễ dàng tạo thêm enemy types, weapon types

#### `game_manager.py` - Quản lý game
- **Game state**: Quản lý trạng thái game, player, enemy, bullets, fire areas
- **Event handling**: Xử lý input, keyboard, mouse
- **Game logic**: Update logic, collision detection, AI
- **Rendering**: Vẽ game, UI, pause screen

## 🏠 Home Screen mới

### **Màn hình chính:**
- **Title**: "TANK BATTLE"
- **Subtitle**: "Choose Your Tank"
- **Tank Selection**: Chọn giữa 2 loại tank
- **Controls**: Hướng dẫn điều khiển
- **Buttons**: START GAME và QUIT

### **Cách sử dụng:**
- **Click chuột**: Chọn tank và nhấn nút
- **Arrow keys**: Chuyển đổi giữa các tank
- **Enter**: Start game
- **ESC**: Quit

## 🎯 Hệ thống Skill mới với Phân loại

### **Phân loại Skill:**

#### 1. **Skill Định hướng (Directional Skills):**
- **E - Dash**: Range 100 pixel, di chuyển đến vị trí nhắm
- **Spacebar - Power Shot**: Range vô hạn, bắn đạn vàng theo hướng nhắm

#### 2. **Skill Buff (Buff Skills):**
- **Q - Heal**: Hồi 20 HP, sử dụng trực tiếp (không cần skill mode)
- **F - Shield**: Giảm 50% damage trong 5 giây, sử dụng trực tiếp

#### 3. **Skill Vùng (Area Skills):**
- **Spacebar - Fire Area**: Tạo vùng lửa gây damage và làm chậm enemy

#### 4. **Skill Tăng tốc (Speed Skills):**
- **E - Speed Boost**: Tăng tốc độ gấp đôi trong 3 giây

### **Chi tiết từng Tank:**

#### **🟢 Naruto Tank:**
- **Màu**: Xanh lá đậm
- **Skills**:
  - **E - Dash**: Di chuyển nhanh đến vị trí nhắm
  - **Spacebar - Power Shot**: Bắn đạn vàng mạnh
  - **Q - Heal**: Hồi 20 HP
  - **F - Shield**: Giảm 50% damage

#### **🟣 Sasuke Tank:**
- **Màu**: Tím
- **Skills**:
  - **E - Speed Boost**: Tăng tốc độ gấp đôi
  - **Spacebar - Fire Area**: Tạo vùng lửa gây damage
  - **Q - Heal**: Hồi 20 HP
  - **F - Shield**: Giảm 50% damage

### **Cách hoạt động:**

#### **Skill Định hướng:**
1. **Kích hoạt**: Nhấn phím skill (E/Spacebar)
2. **Skill Mode On**: Hiển thị targeting system
3. **Range hữu hạn**: Vẽ vòng tròn xanh nhạt + line + target indicator
4. **Range vô hạn**: Vẽ tia vector từ tank đến biên màn hình + line + target indicator
5. **Thực thi**: Click chuột để thực thi

#### **Skill Buff:**
1. **Sử dụng trực tiếp**: Nhấn phím skill (Q/F/E cho Sasuke)
2. **Không cần nhắm**: Hiệu ứng ngay lập tức
3. **Visual feedback**: Hiệu ứng đặc biệt (shield circle, speed boost circle)

#### **Skill Vùng (Fire Area):**
1. **Kích hoạt**: Nhấn Spacebar (Sasuke)
2. **Skill Mode On**: Hiển thị preview vùng lửa
3. **Thực thi**: Click để đặt vùng lửa
4. **Hiệu ứng**: Gây 5 damage/giây + làm chậm 50% enemy trong vùng

### **Chi tiết từng Skill:**

#### **⚡ Dash (E) - Naruto:**
- **Range**: 100 pixel
- **Hiệu ứng**: Tank di chuyển đến vị trí nhắm
- **Visual**: Vòng tròn xanh nhạt + targeting line

#### **💥 Power Shot (Spacebar) - Naruto:**
- **Range**: Vô hạn
- **Hiệu ứng**: Bắn đạn vàng theo hướng nhắm
- **Visual**: Tia vector đến biên màn hình + targeting line

#### **🔥 Fire Area (Spacebar) - Sasuke:**
- **Range**: 150 pixel
- **Hiệu ứng**: Tạo vùng lửa gây damage và làm chậm enemy
- **Duration**: 3 giây
- **Damage**: 5 HP/giây
- **Slow**: Giảm 50% tốc độ enemy

#### **⚡ Speed Boost (E) - Sasuke:**
- **Range**: Không cần
- **Hiệu ứng**: Tăng tốc độ gấp đôi trong 3 giây
- **Cách dùng**: Nhấn E trực tiếp
- **Visual**: Vòng tròn vàng xung quanh tank

#### **❤️ Heal (Q) - Cả hai:**
- **Range**: Không cần
- **Hiệu ứng**: Hồi 20 HP
- **Cách dùng**: Nhấn Q trực tiếp

#### **🛡️ Shield (F) - Cả hai:**
- **Range**: Không cần
- **Hiệu ứng**: Giảm 50% damage trong 5 giây
- **Cách dùng**: Nhấn F trực tiếp
- **Visual**: Vòng tròn xanh dương xung quanh tank

### **Visual Feedback:**

#### **Directional Skills:**
- **Range hữu hạn**: Vòng tròn xanh nhạt + line + target indicator
- **Range vô hạn**: Tia vector đến biên màn hình + line + target indicator

#### **Area Skills:**
- **Fire Area**: Preview vùng lửa + range circle + targeting line

#### **Buff Skills:**
- **Heal**: Không có visual đặc biệt
- **Shield**: Vòng tròn xanh dương xung quanh tank
- **Speed Boost**: Vòng tròn vàng xung quanh tank

## 🚀 Lợi ích của cấu trúc mới:

#### 1. **Dễ thêm tính năng mới:**
- Thêm tank mới → Chỉ cần thêm vào `tank_options` trong HomeScreen
- Thêm enemy mới → Chỉ cần tạo class Enemy mới trong `game_objects.py`
- Thêm weapon mới → Tạo class Weapon trong `game_objects.py`
- Thêm map mới → Tạo class Map trong `game_objects.py`

#### 2. **Dễ sửa đổi:**
- Thay đổi balance → Chỉ cần sửa `game_config.py`
- Sửa AI logic → Chỉ cần sửa method trong `game_manager.py`
- Thay đổi UI → Chỉ cần sửa method draw trong `game_manager.py`

#### 3. **Code sạch hơn:**
- Mỗi file có trách nhiệm rõ ràng
- Dễ debug và test từng phần
- Dễ đọc và hiểu code

#### 4. **Tái sử dụng:**
- Có thể import Tank, Bullet để tạo game khác
- Có thể tái sử dụng GameManager cho game khác
- Dễ dàng tạo mods và extensions

## 🔧 Cách thêm tính năng mới:

#### Thêm tank type mới:
```python
# Trong game_objects.py
def init_skills(self):
    if self.tank_type == "new_tank":
        self.skills = {
            'new_skill': Skill("New Skill", 300, 'G', RED, '⭐', 100, SKILL_TYPE_DIRECTIONAL),
            # ... các skill khác
        }

# Trong game.py
self.tank_options = [
    # ... tanks hiện tại
    {"type": "new_tank", "name": "New Tank", "color": RED, "description": "New skills..."}
]
```

#### Thêm skill mới:
```python
# Trong game_config.py
NEW_SKILL_COOLDOWN = 400
NEW_SKILL_RANGE = 120

# Trong game_objects.py
'new_skill': Skill("New Skill", NEW_SKILL_COOLDOWN, 'G', RED, '⭐', NEW_SKILL_RANGE, SKILL_TYPE_DIRECTIONAL)
```

## 📊 So sánh trước và sau:

| Trước | Sau |
|-------|-----|
| 1 file 400+ dòng | 4 files, mỗi file <150 dòng |
| Không có home screen | Home screen với chọn tank |
| 1 loại tank | 2 loại tank với skills khác nhau |
| Khó thêm tính năng | Dễ thêm tính năng |
| Khó debug | Dễ debug từng phần |
| Code lộn xộn | Code có tổ chức |
| Khó maintain | Dễ maintain |

## 🎮 Cách chạy game:

```bash
python game.py
```

## 🎯 Điều khiển mới:

### **Home Screen:**
- **Click chuột**: Chọn tank và nhấn nút
- **Arrow keys**: Chuyển đổi giữa các tank
- **Enter**: Start game
- **ESC**: Quit

### **Game:**
- **WASD**: Di chuyển tank
- **Mouse**: Nhắm nòng tank
- **Click chuột trái**: Bắn đạn thường (khi không ở skill mode)

### **Skills theo Tank:**

#### **Naruto:**
- **E**: Kích hoạt Dash Mode → Click để dash
- **Q**: Heal trực tiếp
- **F**: Shield trực tiếp
- **Spacebar**: Kích hoạt Power Shot Mode → Click để bắn

#### **Sasuke:**
- **E**: Speed Boost trực tiếp
- **Q**: Heal trực tiếp
- **F**: Shield trực tiếp
- **Spacebar**: Kích hoạt Fire Area Mode → Click để đặt vùng lửa

### **Game Control:**
- **P**: Pause/Resume
- **R**: Restart
- **ESC**: Quit

## 🌟 Tính năng mới:

- **Home Screen**: Menu chọn tank trước khi vào game
- **Tank Selection**: Chọn giữa Naruto và Sasuke
- **Fire Area Skill**: Tạo vùng lửa gây damage và làm chậm enemy
- **Speed Boost Skill**: Tăng tốc độ tạm thời
- **Different Skill Sets**: Mỗi tank có bộ skill riêng biệt
- **Visual Tank Preview**: Xem trước tank trong menu
- **Auto Return to Home**: Tự động về home khi chết
