# utils/camera.py
import cv2
import time

def capture_from_camera(save_path="saves/temp_capture.jpg"):
    """Chụp ảnh từ camera"""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None
    
    cv2.namedWindow("Camera - SPACE: chụp, ESC: thoát")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Hiển thị hướng dẫn
        cv2.putText(frame, "SPACE: Chup anh | ESC: Thoat", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow("Camera - SPACE: chụp, ESC: thoát", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # ESC
            break
        elif key == 32:  # SPACE
            cv2.imwrite(save_path, frame)
            cap.release()
            cv2.destroyAllWindows()
            return save_path
    
    cap.release()
    cv2.destroyAllWindows()
    return None