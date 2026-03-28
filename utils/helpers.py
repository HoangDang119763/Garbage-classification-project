# utils/helpers.py
import time
from .constants import GARBAGE_EMOJIS, GARBAGE_GRADIENTS, GARBAGE_TIPS

def format_class_name(name):
    """Chuyển 'brown-glass' thành 'Brown Glass'"""
    return name.replace('-', ' ').title()

def get_emoji(class_name):
    return GARBAGE_EMOJIS.get(class_name, '❓')

def get_gradient(class_name):
    """Lấy gradient cho loại rác"""
    return GARBAGE_GRADIENTS.get(class_name, ['#3498db', '#2980b9'])

def get_color(class_name):
    """Lấy màu chính từ gradient"""
    gradient = get_gradient(class_name)
    return gradient[0] if gradient else '#3498db'

def get_tip(class_name):
    return GARBAGE_TIPS.get(class_name, 'Chọn ảnh để xem mẹo phân loại chi tiết!')

def log_time(operation, start_time):
    """In thời gian thực hiện"""
    elapsed = time.time() - start_time
    print(f"⏱️ {operation}: {elapsed:.3f}s")
    return elapsed

def log_model_step(step_name, start_time):
    """In log giả lập như TensorFlow"""
    elapsed = time.time() - start_time
    ms = int(elapsed * 1000)
    print(f"1/1 ━━━━━━━━━━━━━━━━━━━━ {elapsed:.0f}s {ms}ms/step - {step_name}")