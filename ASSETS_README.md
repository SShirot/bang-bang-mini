# Tank Assets Guide

## 📁 Cấu trúc thư mục assets

```
assets/tanks/
├── naruto/
│   ├── body.png      # Tank body (40x40px)
│   └── turret.png    # Turret (35x35px)
├── sasuke/
│   ├── body.png      # Tank body (40x40px)
│   └── turret.png    # Turret (35x35px)
└── enemy/
    ├── body.png      # Tank body (40x40px)
    └── turret.png    # Turret (35x35px)
```

## 🎨 Yêu cầu cho sprites

### Body Sprite:
- **Kích thước:** 60x60 pixels (TANK_SIZE) - đã tăng từ 40x40
- **Pivot point:** Ở giữa (center)
- **Background:** Transparent (PNG)
- **Hướng mặc định:** Hướng lên (North)
- **Màu sắc:** 
  - Naruto: Xanh lá (DARK_GREEN)
  - Sasuke: Tím (PURPLE)
  - Enemy: Xanh dương (BLUE)

### Turret Sprite:
- **Kích thước:** 20x20 pixels (khoảng 1/3 body size - đã tăng từ 12x12)
- **Pivot point:** Ở giữa (center)
- **Background:** Transparent (PNG)
- **Hướng mặc định:** Hướng lên (North)
- **Màu sắc:** Tương ứng với body
- **Vai trò:** Điểm nhỏ ở giữa tank để hiển thị hướng nhắm (đã to hơn để dễ nhìn)

## 🔄 Cách hoạt động

### 1. Body Rotation:
- **Xoay theo:** `body_angle` (hướng di chuyển WASD)
- **Pivot:** Center của sprite
- **Logic:** `pygame.transform.rotate(body_sprite, -body_angle)`

### 2. Turret Rotation:
- **Xoay theo:** `turret_angle` (hướng chuột)
- **Pivot:** Center của sprite
- **Logic:** `pygame.transform.rotate(turret_sprite, -turret_angle)`

### 3. Fallback System:
- **Nếu có sprites:** Sử dụng `draw_with_sprites()`
- **Nếu không có sprites:** Sử dụng `draw_manual()` (vẽ thủ công)

## 📝 Hướng dẫn tạo assets

### 1. Sử dụng Photoshop/GIMP:
- Tạo canvas 40x40px cho body, 35x35px cho turret
- Vẽ tank với background transparent
- Export dưới dạng PNG

### 2. Sử dụng online tools:
- Piskel (https://www.piskelapp.com/)
- Aseprite
- GraphicsGale

### 3. Tìm assets miễn phí:
- OpenGameArt.org
- Itch.io (free assets)
- Game-icons.net

## 🚀 Cách test

1. **Chuẩn bị assets** theo cấu trúc trên
2. **Chạy game:** `python game.py`
3. **Kiểm tra console** để xem có load được sprites không
4. **Nếu có lỗi:** Game sẽ tự động fallback về vẽ thủ công

## 🔧 Tùy chỉnh

### Thay đổi kích thước:
```python
# Trong game_config.py
TANK_SIZE = 60        # Kích thước body (đã tăng từ 40)
TURRET_LENGTH = 35    # Kích thước turret (giữ nguyên)
TANK_RADIUS = 30      # Bán kính tank (tương ứng với TANK_SIZE)
```

### Thêm tank mới:
```python
# Trong game_objects.py
elif self.tank_type == "new_tank":
    self.body_sprite = pygame.image.load("assets/tanks/new_tank/body.png")
    self.turret_sprite = pygame.image.load("assets/tanks/new_tank/turret.png")
```

## 💡 Tips

1. **Sprite size:** 
   - Body: Nên làm sprite lớn hơn (120x120px) rồi scale down về 60x60px
   - Turret: Làm sprite nhỏ (40x40px hoặc 50x50px) rồi scale down về 20x20px
2. **Turret design:** Turret đã to hơn để dễ nhìn, nhưng vẫn nhỏ hơn body nhiều lần
3. **Anti-aliasing:** Bật anti-aliasing để sprite mượt hơn
4. **Test rotation:** Kiểm tra sprite có xoay đẹp không
5. **Performance:** Sprites sẽ nhanh hơn vẽ thủ công
6. **Memory:** Mỗi sprite sẽ chiếm bộ nhớ, cân nhắc kích thước
7. **Proportions:** Body vẫn to hơn turret nhiều lần để trông tự nhiên
8. **Visibility:** Tank to hơn sẽ dễ nhìn và điều khiển hơn
9. **Turret visibility:** Turret to hơn sẽ dễ nhìn hướng nhắm

## 🆘 Troubleshooting

### Lỗi "Không thể load tank sprites":
- Kiểm tra đường dẫn file
- Kiểm tra tên file có đúng không
- Kiểm tra file có bị corrupt không
- Game sẽ tự động fallback về vẽ thủ công

### Sprite bị lệch vị trí:
- Kiểm tra pivot point có ở center không
- Kiểm tra kích thước sprite có đúng không
- Điều chỉnh offset trong code nếu cần
