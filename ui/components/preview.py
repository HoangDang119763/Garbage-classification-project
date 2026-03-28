# ui/components/preview.py
import customtkinter as ctk
from PIL import Image

class ImagePreview(ctk.CTkLabel):
    def __init__(self, parent, width=550, height=280, **kwargs):
        super().__init__(parent, 
                         text="🖼️ Kéo thả hoặc chọn ảnh từ máy",
                         font=("Segoe UI", 14), 
                         width=width, 
                         height=height,
                         corner_radius=10, 
                         fg_color="#2c3e50",
                         text_color="#95a5a6",
                         **kwargs)
        self.width = width
        self.height = height
    
    def show(self, image_path):
        try:
            img = Image.open(image_path)
            
            # Tính toán tỷ lệ để giữ nguyên aspect ratio
            img.thumbnail((self.width-30, self.height-30), Image.Resampling.LANCZOS)
            
            # Tạo background với màu nền
            bg = Image.new('RGB', (self.width, self.height), (44, 62, 80))
            
            # Căn giữa ảnh
            x = (self.width - img.size[0]) // 2
            y = (self.height - img.size[1]) // 2
            bg.paste(img, (x, y))
            
            photo = ctk.CTkImage(light_image=bg, dark_image=bg, 
                                 size=(self.width, self.height))
            self.configure(image=photo, text="")
            return True
        except Exception as e:
            self.configure(text=f"❌ Lỗi: {str(e)}")
            return False
    
    def clear(self):
        self.configure(image="", text="🖼️ Kéo thả hoặc chọn ảnh từ máy")