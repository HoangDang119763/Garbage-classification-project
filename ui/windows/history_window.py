# ui/windows/history_window.py
import customtkinter as ctk
from utils import format_class_name, get_emoji, get_gradient, COLORS

class HistoryWindow:
    def __init__(self, parent, history):
        self.window = ctk.CTkToplevel(parent)
        self.window.title("📜 LỊCH SỬ DỰ ĐOÁN")
        self.window.geometry("650x550")
        self.window.transient(parent)
        self.window.grab_set()
        self.window.configure(fg_color=COLORS["bg_primary"])
        
        self.history = history
        self.create()
    
    def create(self):
        # Header
        header = ctk.CTkFrame(self.window, fg_color=COLORS["bg_secondary"], height=70, corner_radius=0)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(expand=True)
        
        ctk.CTkLabel(header_content, text="📜", font=("Segoe UI", 28)).pack(side="left", padx=5)
        ctk.CTkLabel(header_content, 
                    text=f"LỊCH SỬ DỰ ĐOÁN ({len(self.history.get_all())} kết quả)",
                    font=("Segoe UI", 18, "bold"), 
                    text_color=COLORS["text_primary"]).pack(side="left")
        
        if not self.history.get_all():
            self.show_empty()
        else:
            self.show_history()
    
    def show_empty(self):
        frame = ctk.CTkFrame(self.window, fg_color="transparent")
        frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        content = ctk.CTkFrame(frame, fg_color=COLORS["bg_card"], corner_radius=15)
        content.pack(expand=True, fill="both", padx=20, pady=20)
        
        ctk.CTkLabel(content, text="📭", font=("Segoe UI Emoji", 80)).pack(pady=30)
        ctk.CTkLabel(content, text="CHƯA CÓ LỊCH SỬ", 
                    font=("Segoe UI", 22, "bold"), 
                    text_color=COLORS["accent_orange"]).pack(pady=10)
        ctk.CTkLabel(content, text="Hãy dự đoán một số ảnh để xem lịch sử!", 
                    font=("Segoe UI", 13), 
                    text_color=COLORS["text_secondary"]).pack(pady=10)
        
        ctk.CTkButton(content, text="ĐÓNG", 
                     fg_color=COLORS["accent_red"], 
                     hover_color="#c0392b",
                     font=("Segoe UI", 13, "bold"),
                     command=self.window.destroy, 
                     width=180, 
                     height=40).pack(pady=20)
    
    def show_history(self):
        # Scrollable content
        scroll = ctk.CTkScrollableFrame(self.window, fg_color="transparent", corner_radius=0)
        scroll.pack(fill="both", expand=True, padx=15, pady=15)
        
        for pred in self.history.get_recent(30):  # Hiển thị 30 kết quả gần nhất
            self.create_card(scroll, pred)
        
        # Close button
        footer = ctk.CTkFrame(self.window, fg_color=COLORS["bg_secondary"], height=70, corner_radius=0)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        
        ctk.CTkButton(footer, text="ĐÓNG", 
                     fg_color=COLORS["accent_red"], 
                     hover_color="#c0392b",
                     font=("Segoe UI", 14, "bold"),
                     command=self.window.destroy, 
                     width=200, 
                     height=40).pack(expand=True)
    
    def create_card(self, parent, pred):
        card = ctk.CTkFrame(parent, fg_color=COLORS["bg_card"], corner_radius=10)
        card.pack(fill="x", pady=5)
        
        # Header
        header = ctk.CTkFrame(card, fg_color="transparent")
        header.pack(fill="x", padx=15, pady=(12, 5))
        
        emoji = get_emoji(pred['class'])
        name = format_class_name(pred['class'])
        gradient = get_gradient(pred['class'])
        
        ctk.CTkLabel(header, text=f"{emoji} {name}", 
                    font=("Segoe UI", 16, "bold"),
                    text_color=gradient[0]).pack(side="left")
        
        # Confidence badge
        conf_frame = ctk.CTkFrame(header, fg_color=COLORS["bg_primary"], corner_radius=12)
        conf_frame.pack(side="right")
        
        ctk.CTkLabel(conf_frame, text=f"{pred['confidence']:.1f}%", 
                    font=("Segoe UI", 12, "bold"),
                    text_color=COLORS["accent_green"]).pack(padx=10, pady=2)
        
        # Time and Image name
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=(0, 5))
        
        ctk.CTkLabel(info_frame, text=f"⏰ {pred['timestamp']}", 
                    font=("Segoe UI", 11),
                    text_color=COLORS["text_muted"]).pack(side="left")
        
        # Image name
        import os
        img_name = os.path.basename(pred.get('image_path', ''))
        if img_name:
            ctk.CTkLabel(info_frame, text=f"📸 {img_name}", 
                        font=("Segoe UI", 11),
                        text_color=COLORS["text_muted"]).pack(side="right")
        
        # Top 3
        top3_frame = ctk.CTkFrame(card, fg_color=COLORS["bg_primary"], corner_radius=8)
        top3_frame.pack(fill="x", padx=15, pady=(0, 12))
        
        for j, (label, conf) in enumerate(pred['top_3']):
            viet_label = format_class_name(label)
            gradient = get_gradient(label)
            
            item_frame = ctk.CTkFrame(top3_frame, fg_color="transparent")
            item_frame.pack(fill="x", padx=10, pady=2)
            
            ctk.CTkLabel(item_frame, text=f"{j+1}. {viet_label}", 
                        font=("Segoe UI", 12),
                        text_color=gradient[0]).pack(side="left")
            
            ctk.CTkLabel(item_frame, text=f"{conf:.1f}%", 
                        font=("Segoe UI", 12, "bold"),
                        text_color=COLORS["text_secondary"]).pack(side="right")