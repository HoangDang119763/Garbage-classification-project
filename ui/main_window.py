import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import cv2
import numpy as np
import time
from tensorflow.keras.applications.resnet50 import preprocess_input as resnet_preprocess
from tensorflow.keras.applications.vgg16 import preprocess_input as vgg_preprocess

from core.model_loader import ModelLoader
from core.history import HistoryManager
from ui.components.loading import LoadingAnimation
from ui.components.preview import ImagePreview
from ui.windows.history_window import HistoryWindow
from utils import (
    format_class_name, get_emoji, get_gradient, 
    log_time, log_model_step, capture_from_camera, COLORS
)


class GarbageClassifierApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Phân Loại Rác Thải AI - Đồ Án DACN")
        self.geometry("1300x750")
        self.resizable(True, True)
        self.fullscreen = False
        
        # Khởi tạo
        self.models = ModelLoader()
        self.history = HistoryManager()
        self.img_path = None
        self.current_prediction = None
        self.loading = None
        self.result_content = None
        self.loading_frame = None
        self.notification_timer = None
        
        if not self.models.models:
            print("❌ Không tìm thấy model nào trong thư mục 'models'!")
            self.destroy()
            return
        
        # Cấu hình giao diện
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.create_ui()
    
    def create_ui(self):
        self.configure(fg_color=COLORS["bg_primary"])
        
        # Header với gradient effect
        header = ctk.CTkFrame(self, fg_color=COLORS["bg_secondary"], height=80, corner_radius=0)
        header.pack(fill="x", pady=(0, 15))
        header.pack_propagate(False)
        
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(expand=True, fill="both")
        
        title = ctk.CTkLabel(title_frame, text="♻️ PHÂN LOẠI RÁC THẢI THÔNG MINH ♻️", 
                            font=("Segoe UI", 32, "bold"), 
                            text_color=COLORS["text_primary"])
        title.pack(expand=True)
        
        subtitle = ctk.CTkLabel(title_frame, text="Sử dụng AI để nhận diện và phân loại rác thải",
                               font=("Segoe UI", 14), 
                               text_color=COLORS["text_secondary"])
        subtitle.pack()
        
        # Main container
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=10)
        main.grid_columnconfigure(0, weight=1, minsize=975)
        main.grid_columnconfigure(1, weight=0, minsize=325)
        main.grid_rowconfigure(0, weight=1)
        
        # LEFT PANEL
        self.create_left_panel(main)
        
        # RIGHT PANEL
        self.create_right_panel(main)
    
    def create_left_panel(self, parent):
        left = ctk.CTkFrame(parent, fg_color=COLORS["bg_secondary"], corner_radius=15)
        left.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(3, weight=1)
        
        # Model selection card
        model_card = ctk.CTkFrame(left, fg_color=COLORS["bg_card"], corner_radius=10)
        model_card.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        model_card.grid_columnconfigure(1, weight=1)
        
        model_icon = ctk.CTkLabel(model_card, text="🎯", font=("Segoe UI", 20))
        model_icon.grid(row=0, column=0, padx=(15, 5), pady=15)
        
        ctk.CTkLabel(model_card, text="MODEL", 
                    font=("Segoe UI", 16, "bold"), 
                    text_color=COLORS["accent_blue"]).grid(row=0, column=1, padx=5, pady=15, sticky="w")
        
        self.model_combo = ctk.CTkComboBox(model_card, 
                                          values=self.models.get_model_list(),
                                          command=self.change_model,
                                          width=300,
                                          font=("Segoe UI", 13),
                                          fg_color=COLORS["bg_primary"],
                                          button_color=COLORS["accent_blue"],
                                          button_hover_color="#2980b9",
                                          dropdown_fg_color=COLORS["bg_card"],
                                          dropdown_hover_color=COLORS["bg_hover"])
        self.model_combo.set(self.models.current_name)
        self.model_combo.grid(row=0, column=2, padx=15, pady=15, sticky="ew")
        
        # Result card với kích thước cố định
        self.result_card = ctk.CTkFrame(left, fg_color=COLORS["bg_card"], corner_radius=15, 
                                         width=550, height=200)
        self.result_card.grid(row=1, column=0, padx=15, pady=(5, 5), sticky="ew")
        self.result_card.grid_columnconfigure(0, weight=1)
        self.result_card.grid_propagate(False)
        
        # Frame chứa nội dung (emoji, result, confidence)
        self.result_content = ctk.CTkFrame(self.result_card, fg_color="transparent")
        self.result_content.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.emoji = ctk.CTkLabel(self.result_content, text="", font=("Segoe UI Emoji", 60))
        self.emoji.pack(pady=(15, 5))
        
        self.result = ctk.CTkLabel(self.result_content, text="🤔 ĐÂY LÀ CÁI GÌ?", 
                                   font=("Segoe UI", 24, "bold"), 
                                   text_color=COLORS["accent_orange"])
        self.result.pack(pady=(0, 5))
        
        self.confidence = ctk.CTkLabel(self.result_content, text="", 
                                       font=("Segoe UI", 14), 
                                       text_color=COLORS["text_secondary"])
        self.confidence.pack(pady=(0, 15))
        
        # Frame chứa loading (sẽ được show/hide)
        self.loading_frame = ctk.CTkFrame(self.result_card, fg_color="transparent")
        
        # Upload buttons
        btn_frame = ctk.CTkFrame(left, fg_color="transparent")
        btn_frame.grid(row=2, column=0, padx=15, pady=10, sticky="ew")
        btn_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.upload_btn = ctk.CTkButton(btn_frame, 
                                        text="📤 CHỌN ẢNH", 
                                        font=("Segoe UI", 15, "bold"),
                                        fg_color=COLORS["accent_blue"], 
                                        hover_color="#2980b9",
                                        height=45, 
                                        corner_radius=8,
                                        command=self.upload_image)
        self.upload_btn.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.camera_btn = ctk.CTkButton(btn_frame, 
                                        text="📸 CHỤP ẢNH", 
                                        font=("Segoe UI", 15, "bold"),
                                        fg_color=COLORS["accent_purple"], 
                                        hover_color="#8e44ad",
                                        height=45, 
                                        corner_radius=8,
                                        command=self.open_camera)
        self.camera_btn.grid(row=0, column=1, padx=5, sticky="ew")
        
        # Image preview
        preview_container = ctk.CTkFrame(left, fg_color=COLORS["bg_card"], corner_radius=10)
        preview_container.grid(row=3, column=0, padx=15, pady=10, sticky="nsew")
        preview_container.grid_columnconfigure(0, weight=1)
        preview_container.grid_rowconfigure(0, weight=1)
        
        self.preview = ImagePreview(preview_container, width=550, height=280)
        self.preview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Predict button
        self.predict_btn = ctk.CTkButton(left, 
                                         text="🔍 DỰ ĐOÁN NGAY",
                                         font=("Segoe UI", 20, "bold"),
                                         fg_color=COLORS["accent_green"], 
                                         hover_color="#27ae60",
                                         height=55, 
                                         corner_radius=10,
                                         command=self.predict)
        self.predict_btn.grid(row=4, column=0, padx=15, pady=20, sticky="ew")
    
    def create_right_panel(self, parent):
        right = ctk.CTkFrame(parent, fg_color=COLORS["bg_secondary"], corner_radius=15)
        right.grid(row=0, column=1, padx=(10, 0), sticky="nsew")
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(1, weight=1)
        
        # Fullscreen button
        self.fullscreen_btn = ctk.CTkButton(right,
                                           text="⛶ FULLSCREEN",
                                           font=("Segoe UI", 13, "bold"),
                                           fg_color=COLORS["warning"],
                                           hover_color="#d35400",
                                           height=35,
                                           corner_radius=6,
                                           command=self.toggle_fullscreen)
        self.fullscreen_btn.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="ew")

        # Predictions card (all 12 labels)
        pred_card = ctk.CTkFrame(right, fg_color=COLORS["bg_card"], corner_radius=12)
        pred_card.grid(row=1, column=0, padx=15, pady=5, sticky="nsew")
        pred_card.grid_rowconfigure(1, weight=1)
        pred_card.grid_columnconfigure(0, weight=1)

        # Predictions header
        pred_header = ctk.CTkFrame(pred_card, fg_color="transparent")
        pred_header.grid(row=0, column=0, padx=15, pady=(10, 3), sticky="ew")

        ctk.CTkLabel(pred_header, text="🎯", font=("Segoe UI", 20)).pack(side="left", padx=(0, 5))
        ctk.CTkLabel(pred_header, text="DỰ ĐOÁN:",
                    font=("Segoe UI", 14, "bold"),
                    text_color=COLORS["accent_yellow"]).pack(side="left")

        # Scrollable predictions list
        self.pred_scroll = ctk.CTkScrollableFrame(pred_card, fg_color="transparent",
                                                   corner_radius=0)
        self.pred_scroll.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.pred_scroll.grid_columnconfigure(0, weight=1)

        # Create labels for all 12 predictions
        self.all_pred_labels = []
        for i in range(12):
            frame = ctk.CTkFrame(self.pred_scroll, fg_color=COLORS["bg_primary"], corner_radius=6)
            frame.pack(fill="x", pady=2)

            label = ctk.CTkLabel(frame, text=f"{i+1}. ---",
                                font=("Segoe UI", 11),
                                anchor="w",
                                text_color=COLORS["text_secondary"])
            label.pack(padx=10, pady=5, fill="x")
            self.all_pred_labels.append(label)
        
        # Action buttons
        action_frame = ctk.CTkFrame(right, fg_color="transparent")
        action_frame.grid(row=2, column=0, padx=15, pady=10, sticky="ew")
        action_frame.grid_columnconfigure((0, 1), weight=1)

        self.save_btn = ctk.CTkButton(action_frame,
                                      text="💾 LƯU KẾT QUẢ",
                                      font=("Segoe UI", 11, "bold"),
                                      fg_color=COLORS["accent_orange"],
                                      hover_color="#e67e22",
                                      height=35,
                                      corner_radius=6,
                                      command=self.save_result)
        self.save_btn.grid(row=0, column=0, padx=3, sticky="ew")

        self.history_btn = ctk.CTkButton(action_frame,
                                         text="📜 XEM LỊCH SỬ",
                                         font=("Segoe UI", 11, "bold"),
                                         fg_color=COLORS["accent_purple"],
                                         hover_color="#8e44ad",
                                         height=35,
                                         corner_radius=6,
                                         command=self.show_history)
        self.history_btn.grid(row=0, column=1, padx=3, sticky="ew")
    
    # ==================== METHODS ====================
    
    def change_model(self, choice):
        start = time.time()
        if self.models.switch_model(choice):
            self.show_notification(f"✅ Đã chuyển sang model: {choice}")
        log_time("change_model", start)
    
    def show_notification(self, msg, color=COLORS["success"]):
        # Cancel notification cũ nếu có
        if self.notification_timer:
            self.after_cancel(self.notification_timer)
        
        original = (self.result.cget("text"), self.result.cget("text_color"))
        self.result.configure(text=msg, text_color=color)
        self.notification_timer = self.after(2000, lambda: self.result.configure(text=original[0], text_color=original[1]))
    
    def toggle_fullscreen(self):
        self.fullscreen = not getattr(self, 'fullscreen', False)
        if self.fullscreen:
            self.state('zoomed')
        else:
            self.state('normal')
        self.fullscreen_btn.configure(text="❌ RESTORE DOWN" if self.fullscreen else "⛶ FULLSCREEN")
    
    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            self.img_path = path
            self.preview.show(path)
            self.reset_result()
    
    def reset_result(self):
        self.emoji.configure(text="")
        self.result.configure(text="🤔 ĐÂY LÀ CÁI GÌ?", text_color=COLORS["accent_orange"])
        self.confidence.configure(text="")
        self.current_prediction = None
    
    def show_loading(self):
        # Ẩn content frame
        self.result_content.pack_forget()
        
        # Tạo loading animation trong loading_frame
        self.loading = LoadingAnimation(self.loading_frame)
        self.loading.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Hiển thị loading_frame
        self.loading_frame.pack(expand=True, fill="both", padx=10, pady=10)
        self.loading.start()
        self.update()
    
    def hide_loading(self):
        if self.loading:
            self.loading.stop()
            self.loading = None
        
        # Ẩn loading_frame
        self.loading_frame.pack_forget()
        
        # Hiển thị lại content frame
        self.result_content.pack(expand=True, fill="both", padx=10, pady=10)
        self.update()
    
    def predict(self):
        if not self.img_path:
            self.show_notification("❌ CHƯA CHỌN ẢNH!", COLORS["danger"])
            return
        
        self.show_loading()
        self.disable_buttons()
        self.after(100, self.run_prediction)
    
    def run_prediction(self):
        start = time.time()
        try:
            # Đọc và xử lý ảnh
            img = cv2.imread(self.img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (224, 224))
            
            # Apply preprocessing tùy theo model (MATCHING với training)
            if 'resnet' in self.models.current_name.lower():
                img_array = resnet_preprocess(img)
            elif 'vgg' in self.models.current_name.lower():
                img_array = vgg_preprocess(img)
            else:
                # Fallback nếu model name không match
                img_array = img.astype(np.float32) / 255.0
            
            img_array = np.expand_dims(img_array, axis=0)
            
            # Dự đoán
            def update_status(msg):
                if self.loading:
                    self.loading.status.configure(text=msg)
            
            result = self.models.predict(img_array, update_status)
            log_model_step("predict", start)
            
            # In ra các dự đoán với % của từng label
            import os
            img_filename = os.path.basename(self.img_path)
            print("\n" + "="*70)
            print(f"🤖 KẾT QUẢ DỰ ĐOÁN")
            print(f"📸 Ảnh: {img_filename}")
            print(f"🧠 Mô hình: {self.models.current_name}")
            print("="*70)
            for i, (label, conf) in enumerate(result['all_predictions'], 1):
                bar_length = int(conf / 5)  # Tạo thanh tiến trình
                bar = "█" * bar_length + "░" * (20 - bar_length)
                print(f"{i:2d}. {label:20s} │ {bar} │ {conf:6.2f}%")
            print("="*70 + "\n")
            
            # Lưu kết quả
            self.current_prediction = self.history.create_prediction(
                result['class'], result['confidence'], result['top_3'], self.img_path, result['all_predictions']
            )
            self.history.add(self.current_prediction)
            
            # Hiển thị
            self.hide_loading()
            self.display_result(result)
            log_time("total_prediction", start)
            
        except Exception as e:
            self.hide_loading()
            self.show_notification(f"❌ LỖI: {str(e)}", COLORS["danger"])
            import traceback
            traceback.print_exc()
        finally:
            self.enable_buttons()
    
    def display_result(self, result):
        import os
        
        # Cancel pending notification để tránh bị đè lên kết quả
        if self.notification_timer:
            self.after_cancel(self.notification_timer)
            self.notification_timer = None
        
        name = result['class']
        viet = format_class_name(name)
        emoji = get_emoji(name)
        gradient = get_gradient(name)
        
        self.emoji.configure(text=emoji)
        self.result.configure(text=f"{emoji} {viet} {emoji}", text_color=gradient[0])
        self.confidence.configure(text=f"Độ chính xác: {result['confidence']:.1f}%")
        
        # Display all 12 predictions
        for i, (label, conf) in enumerate(result['all_predictions']):
            viet_label = format_class_name(label)
            gradient = get_gradient(label)
            self.all_pred_labels[i].configure(
                text=f"{i+1}. {viet_label}: {conf:.1f}%",
                text_color=gradient[0]
            )
    
    def disable_buttons(self):
        for btn in [self.predict_btn, self.upload_btn, self.camera_btn]:
            btn.configure(state="disabled")
    
    def enable_buttons(self):
        for btn in [self.predict_btn, self.upload_btn, self.camera_btn]:
            btn.configure(state="normal")
    
    def open_camera(self):
        start = time.time()
        path = capture_from_camera()
        log_time("camera_capture", start)
        
        if path:
            self.img_path = path
            self.preview.show(path)
            self.reset_result()
        else:
            self.show_notification("❌ KHÔNG THỂ MỞ CAMERA!", COLORS["danger"])
    
    def save_result(self):
        if not self.current_prediction:
            self.show_notification("❌ CHƯA CÓ KẾT QUẢ!", COLORS["danger"])
            return
        
        start = time.time()
        from datetime import datetime
        import os
        filename = f"saves/ketqua_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*60 + "\n")
            f.write("♻️ KẾT QUẢ PHÂN LOẠI RÁC THẢI ♻️\n")
            f.write("="*60 + "\n\n")
            f.write(f"⏰ Thời gian: {self.current_prediction['timestamp']}\n")
            f.write(f"📸 Ảnh: {os.path.basename(self.img_path)}\n")
            f.write(f"📋 Model: {self.models.current_name}\n\n")
            f.write(f"🎯 KẾT QUẢ: {get_emoji(self.current_prediction['class'])} {format_class_name(self.current_prediction['class'])}\n")
            f.write(f"📊 Độ chính xác: {self.current_prediction['confidence']:.1f}%\n\n")
            f.write("📈 DỰ ĐOÁN (12 LABEL):\n")
            predictions = self.current_prediction.get('all_predictions', self.current_prediction.get('top_3', []))
            for i, (label, conf) in enumerate(predictions):
                f.write(f"   {i+1}. {format_class_name(label)}: {conf:.1f}%\n")
        
        log_time("save_result", start)
        self.show_notification(f"✅ ĐÃ LƯU: {filename}")
    
    def show_history(self):
        HistoryWindow(self, self.history)
    
    def on_closing(self):
        self.history.save()
        self.destroy()