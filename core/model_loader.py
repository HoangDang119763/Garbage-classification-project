# core/model_loader.py
import os
import tensorflow as tf
from labels import CLASS_NAMES

class ModelLoader:
    def __init__(self, models_dir="models"):
        self.models_dir = models_dir
        self.models = {}
        self.current_model = None
        self.current_name = None
        self.has_warmed_up = False
        self.load_models()
    
    def load_models(self):
        """Load tất cả file .h5 trong thư mục models"""
        if not os.path.exists(self.models_dir):
            print(f"❌ Không tìm thấy thư mục {self.models_dir}")
            return False
        
        for file in os.listdir(self.models_dir):
            if file.endswith(".h5"):
                name = file.replace(".h5", "")
                path = os.path.join(self.models_dir, file)
                try:
                    model = tf.keras.models.load_model(path)
                    self.models[name] = model
                    print(f"✅ Đã load: {name}")
                except Exception as e:
                    print(f"⚠️ Lỗi load {name}: {e}")
        
        if self.models:
            self.current_name = list(self.models.keys())[0]
            self.current_model = self.models[self.current_name]
            return True
        return False
    
    def get_model_list(self):
        return list(self.models.keys())
    
    def switch_model(self, name):
        if name in self.models:
            self.current_name = name
            self.current_model = self.models[name]
            self.has_warmed_up = False
            return True
        return False
    
    def predict(self, image_array, status_callback=None):
        """Dự đoán với ảnh đã được xử lý"""
        if not self.has_warmed_up:
            if status_callback:
                status_callback("⚙️ Khởi tạo model...")
            dummy = tf.zeros((1, 224, 224, 3))
            self.current_model.predict(dummy, verbose=0)
            self.has_warmed_up = True
        
        if status_callback:
            status_callback("🧠 Đang chạy AI...")
        
        predictions = self.current_model.predict(image_array, verbose=0)[0]
        
        top_idx = tf.argsort(predictions)[-3:][::-1].numpy()
        top_conf = predictions[top_idx] * 100
        
        # Tính toán tất cả các dự đoán theo thứ tự giảm dần
        all_predictions_sorted = sorted(
            [(CLASS_NAMES[i], float(predictions[i] * 100)) for i in range(len(CLASS_NAMES))],
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            'class': all_predictions_sorted[0][0],
            'confidence': all_predictions_sorted[0][1],
            'top_3': all_predictions_sorted[:3],
            'all_predictions': all_predictions_sorted
        }