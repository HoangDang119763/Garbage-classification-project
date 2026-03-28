# core/history.py
import json
import os
from datetime import datetime
from collections import Counter

class HistoryManager:
    def __init__(self, history_file="saves/history.json"):
        self.history_file = history_file
        self.predictions = []
        self.load()
    
    def load(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.predictions = json.load(f)
            except:
                self.predictions = []
    
    def save(self):
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.predictions, f, ensure_ascii=False, indent=2)
    
    def add(self, prediction):
        self.predictions.append(prediction)
        self.save()
    
    def get_all(self):
        return self.predictions
    
    def get_recent(self, limit=20):
        return list(reversed(self.predictions[-limit:]))
    
    def get_stats(self):
        if not self.predictions:
            return "Chưa có dữ liệu"
        
        total = len(self.predictions)
        counter = Counter([p['class'] for p in self.predictions])
        
        stats = f"📌 Tổng: {total} lần\n\n📊 Top 5:\n"
        for waste, count in counter.most_common(5):
            stats += f"  • {waste.replace('-',' ').title()}: {count} lần\n"
        
        return stats
    
    def create_prediction(self, class_name, confidence, top_3, image_path, all_predictions=None):
        return {
            'class': class_name,
            'confidence': float(confidence),
            'top_3': [(label, float(conf)) for label, conf in top_3],
            'all_predictions': [(label, float(conf)) for label, conf in all_predictions] if all_predictions else [],
            'timestamp': datetime.now().strftime("%H:%M:%S %d/%m/%Y"),
            'image_path': image_path
        }