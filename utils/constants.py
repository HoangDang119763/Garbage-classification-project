# utils/constants.py
# Emoji cho từng loại rác
GARBAGE_EMOJIS = {
    'battery': '🔋', 'biological': '🦠', 'brown-glass': '🥃',
    'cardboard': '📦', 'clothes': '👕', 'green-glass': '🍾',
    'metal': '🔧', 'paper': '📄', 'plastic': '🛍️',
    'shoes': '👟', 'trash': '🗑️', 'white-glass': '🍷'
}

# Màu sắc gradient cho từng loại rác
GARBAGE_GRADIENTS = {
    'battery': ['#FF416C', '#FF4B2B'],
    'biological': ['#00b09b', '#96c93d'],
    'brown-glass': ['#8D6E63', '#5D4037'],
    'cardboard': ['#F5DEB3', '#D2B48C'],
    'clothes': ['#FF6B6B', '#FF8E8E'],
    'green-glass': ['#2ECC71', '#27AE60'],
    'metal': ['#BDC3C7', '#95A5A6'],
    'paper': ['#ECF0F1', '#BDC3C7'],
    'plastic': ['#F1C40F', '#F39C12'],
    'shoes': ['#E67E22', '#D35400'],
    'trash': ['#7F8C8D', '#5D6D7E'],
    'white-glass': ['#FFFFFF', '#F2F4F4']
}

# Alias cho GARBAGE_GRADIENTS để tương thích với code cũ
GARBAGE_COLORS = GARBAGE_GRADIENTS

# Tips phân loại chi tiết
GARBAGE_TIPS = {
    'battery': '🔋 PIN - Cần xử lý đặc biệt! Không vứt chung với rác thải sinh hoạt. Hãy mang đến điểm thu gom pin cũ.',
    'biological': '🦠 RÁC HỮU CƠ - Có thể ủ làm phân bón cho cây. Tuyệt vời cho việc làm vườn!',
    'brown-glass': '🥃 THỦY TINH NÂU - Có thể tái chế 100% và tái chế vô hạn lần.',
    'cardboard': '📦 CARTON - Nên làm phẳng để tiết kiệm diện tích. Giữ khô ráo để tái chế tốt hơn.',
    'clothes': '👕 QUẦN ÁO - Có thể quyên góp nếu còn tốt. Vải cũ có thể tái chế thành sợi mới.',
    'green-glass': '🍾 THỦY TINH XANH - Rửa sạch, bỏ nắp trước khi tái chế.',
    'metal': '🔧 KIM LOẠI - Có thể tái chế nhiều lần. Lon nhôm tiết kiệm 95% năng lượng khi tái chế.',
    'paper': '📄 GIẤY - Chỉ giấy sạch mới tái chế được. Giấy bẩn, dính dầu mỡ không thể tái chế.',
    'plastic': '🛍️ NHỰA - Kiểm tra ký hiệu tái chế (1-7). Nhựa số 1 và 2 dễ tái chế nhất.',
    'shoes': '👟 GIÀY DÉP - Có thể sửa chữa nếu hỏng nhẹ. Giày cũ có thể tái chế thành vật liệu khác.',
    'trash': '🗑️ RÁC THẢI - Rác còn lại sẽ được xử lý tại bãi chôn lấp hoặc lò đốt.',
    'white-glass': '🍷 THỦY TINH TRẮNG - Thường dùng làm chai lọ mỹ phẩm, dược phẩm.'
}

# Màu sắc giao diện chuyên nghiệp
COLORS = {
    "bg_primary": "#1a2634",
    "bg_secondary": "#2c3e50",
    "bg_card": "#34495e",
    "bg_hover": "#3d566e",
    "accent_blue": "#3498db",
    "accent_green": "#2ecc71",
    "accent_orange": "#f39c12",
    "accent_purple": "#9b59b6",
    "accent_red": "#e74c3c",
    "accent_yellow": "#f1c40f",
    "text_primary": "#ecf0f1",
    "text_secondary": "#bdc3c7",
    "text_muted": "#95a5a6",
    "success": "#27ae60",
    "warning": "#e67e22",
    "danger": "#c0392b"
}