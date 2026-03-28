# ui/components/loading.py
import customtkinter as ctk
from utils import COLORS

class LoadingAnimation(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 
                        fg_color="transparent",  # Nền trong suốt để không che result card
                        corner_radius=0, 
                        width=500, 
                        height=140,  # Chiều cao cố định bằng với result card
                        **kwargs)
        self.pack_propagate(False)
        
        # Center container
        center = ctk.CTkFrame(self, fg_color="transparent")
        center.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Icon
        self.icon = ctk.CTkLabel(center, text="🔄", 
                                 font=("Segoe UI Emoji", 50),
                                 text_color=COLORS["accent_blue"])
        self.icon.pack(pady=(20, 10))
        
        # Text
        self.text = ctk.CTkLabel(center, text="ĐANG XỬ LÝ", 
                                 font=("Segoe UI", 18, "bold"), 
                                 text_color=COLORS["accent_orange"])
        self.text.pack(pady=5)
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(center, 
                                          width=300,
                                          height=8,
                                          corner_radius=5, 
                                          fg_color=COLORS["bg_primary"],
                                          progress_color=COLORS["accent_green"])
        self.progress.pack(pady=10)
        self.progress.set(0)
        
        # Status
        self.status = ctk.CTkLabel(center, text="Đang chuẩn bị...", 
                                   font=("Segoe UI", 11), 
                                   text_color=COLORS["text_secondary"])
        self.status.pack(pady=(0, 10))
        
        self.step = 0
        self.animating = False
        self.status_texts = [
            "📸 Đang tiền xử lý ảnh...",
            "🧠 Đang chạy model AI...",
            "📊 Đang phân tích kết quả...",
            "✨ Sắp hoàn tất..."
        ]
        self.icons = ["🔄", "⏳", "⌛", "⏰"]
    
    def start(self):
        self.animating = True
        self.animate()
    
    def animate(self):
        if self.animating:
            # Text animation
            dots = "." * (self.step % 4)
            self.text.configure(text=f"ĐANG XỬ LÝ{dots}")
            
            # Progress
            self.progress.set((self.step % 20) / 20)
            
            # Icon animation
            self.icon.configure(text=self.icons[self.step % 4])
            
            # Status update
            idx = min(self.step // 20, 3)
            self.status.configure(text=self.status_texts[idx])
            
            self.step += 1
            self.after(80, self.animate)
    
    def stop(self):
        self.animating = False
        self.destroy()