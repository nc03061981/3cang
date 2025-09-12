#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script dự đoán xổ số sử dụng mô hình LSTM đã huấn luyện
"""

import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
import os
import glob

class LotteryPredictor:
    """Lớp dự đoán xổ số sử dụng mô hình đã huấn luyện"""
    
    def __init__(self, model_path, scaler_path=None):
        self.model = tf.keras.models.load_model(model_path)
        self.scaler = None
        
        # Tự động tìm scaler tương ứng
        if scaler_path is None:
            base_path = model_path.replace('.keras', '').replace('.h5', '')
            scaler_path = f"{base_path}_scaler.npy"
        
        if os.path.exists(scaler_path):
            self.scaler = np.load(scaler_path, allow_pickle=True).item()
            print(f"Đã tải scaler từ: {scaler_path}")
        else:
            print("Không tìm thấy scaler, sẽ tạo mới khi cần")
        
        # Xác định loại mô hình từ tên file
        if "raw_numbers" in model_path:
            self.model_type = "raw_numbers"
        elif "sum" in model_path:
            self.model_type = "sum"
        elif "counts" in model_path:
            self.model_type = "counts"
        else:
            self.model_type = "raw_numbers"  # Mặc định
        
        print(f"Đã tải mô hình: {self.model_type}")
    
    def predict_next_numbers(self, recent_numbers, num_predictions=255):
        """Dự đoán số tiếp theo"""
        if self.model_type == "raw_numbers":
            return self._predict_raw_numbers(recent_numbers, num_predictions)
        else:
            raise ValueError("Chỉ hỗ trợ dự đoán raw_numbers")
    
    def _predict_raw_numbers(self, recent_numbers, num_predictions):
        """Dự đoán số nguyên với randomness"""
        if self.scaler is None:
            # Tạo scaler mới nếu không có
            self.scaler = MinMaxScaler()
            self.scaler.fit(np.array(recent_numbers).reshape(-1, 1))
        
        # Chuẩn hóa dữ liệu đầu vào
        numbers_normalized = self.scaler.transform(np.array(recent_numbers).reshape(-1, 1)).flatten()
        
        # Dự đoán với randomness
        predictions = []
        current_sequence = numbers_normalized[-10:].reshape(1, 10, 1)
        
        for _ in range(num_predictions):
            pred = self.model.predict(current_sequence, verbose=0)
            
            # Sử dụng temperature scaling để tăng randomness
            temperature = 1.5
            pred_scaled = pred[0] / temperature
            pred_probs = np.exp(pred_scaled) / np.sum(np.exp(pred_scaled))
            
            # Lấy top 5 predictions và chọn ngẫu nhiên
            top_5_indices = np.argsort(pred_probs)[-5:][::-1]
            top_5_probs = pred_probs[top_5_indices]
            
            # Chọn ngẫu nhiên từ top 5 với xác suất tương ứng
            chosen_idx = np.random.choice(top_5_indices, p=top_5_probs/np.sum(top_5_probs))
            pred_normalized = chosen_idx / 999.0
            
            # Chuyển về số nguyên
            pred_original = int(self.scaler.inverse_transform([[pred_normalized]])[0][0])
            predictions.append(pred_original)
            
            # Cập nhật chuỗi
            current_sequence = np.roll(current_sequence, -1, axis=1)
            current_sequence[0, -1, 0] = pred_normalized
        
        return predictions
    
    def _predict_sum(self, recent_numbers, num_predictions):
        """Dự đoán tổng các chữ số với randomness"""
        if self.scaler is None:
            # Tạo scaler mới nếu không có
            self.scaler = MinMaxScaler()
            sums = [sum(int(digit) for digit in str(num).zfill(3)) for num in recent_numbers]
            self.scaler.fit(np.array(sums).reshape(-1, 1))
        
        # Tính tổng các chữ số
        sums = []
        for num in recent_numbers:
            digit_sum = sum(int(digit) for digit in str(num).zfill(3))
            sums.append(digit_sum)
        
        # Chuẩn hóa dữ liệu
        sums_normalized = self.scaler.transform(np.array(sums).reshape(-1, 1)).flatten()
        
        # Dự đoán với randomness
        predictions = []
        current_sequence = sums_normalized[-10:].reshape(1, 10, 1)
        
        for _ in range(num_predictions):
            pred = self.model.predict(current_sequence, verbose=0)
            
            # Sử dụng temperature scaling để tăng randomness
            temperature = 1.5
            pred_scaled = pred[0] / temperature
            pred_probs = np.exp(pred_scaled) / np.sum(np.exp(pred_scaled))
            
            # Lấy top 5 predictions và chọn ngẫu nhiên
            top_5_indices = np.argsort(pred_probs)[-5:][::-1]
            top_5_probs = pred_probs[top_5_indices]
            
            # Chọn ngẫu nhiên từ top 5 với xác suất tương ứng
            chosen_idx = np.random.choice(top_5_indices, p=top_5_probs/np.sum(top_5_probs))
            pred_normalized = chosen_idx / 27.0
            
            # Chuyển về tổng gốc
            pred_original = int(self.scaler.inverse_transform([[pred_normalized]])[0][0])
            predictions.append(pred_original)
            
            # Cập nhật chuỗi
            current_sequence = np.roll(current_sequence, -1, axis=1)
            current_sequence[0, -1, 0] = pred_normalized
        
        return predictions
    
    def _predict_counts(self, recent_numbers, num_predictions):
        """Dự đoán chữ số xuất hiện nhiều nhất tiếp theo"""
        if self.scaler is None:
            # Tạo scaler mới nếu không có
            self.scaler = MinMaxScaler()
            digit_counts = []
            for num in recent_numbers:
                digits = [int(d) for d in str(num).zfill(3)]
                counts = [digits.count(i) for i in range(10)]
                digit_counts.append(counts)
            self.scaler.fit(digit_counts)
        
        # Đếm số lần xuất hiện của từng chữ số
        digit_counts = []
        for num in recent_numbers:
            digits = [int(d) for d in str(num).zfill(3)]
            counts = [digits.count(i) for i in range(10)]
            digit_counts.append(counts)
        
        # Chuẩn hóa dữ liệu
        digit_counts_normalized = self.scaler.transform(digit_counts)
        
        # Dự đoán với randomness
        predictions = []
        current_sequence = digit_counts_normalized[-10:].reshape(1, 10, 10)
        
        for i in range(num_predictions):
            pred = self.model.predict(current_sequence, verbose=0)
            
            # Sử dụng temperature scaling để tăng randomness
            temperature = 2.0
            pred_scaled = pred[0] / temperature
            pred_probs = np.exp(pred_scaled) / np.sum(np.exp(pred_scaled))
            
            # Lấy top 3 predictions và chọn ngẫu nhiên
            top_3_indices = np.argsort(pred_probs)[-3:][::-1]
            top_3_probs = pred_probs[top_3_indices]
            
            # Chọn ngẫu nhiên từ top 3 với xác suất tương ứng
            chosen_idx = np.random.choice(top_3_indices, p=top_3_probs/np.sum(top_3_probs))
            predictions.append(chosen_idx)
            
            # Cập nhật chuỗi (sử dụng one-hot encoding)
            one_hot = np.zeros(10)
            one_hot[chosen_idx] = 1
            current_sequence = np.roll(current_sequence, -1, axis=1)
            current_sequence[0, -1, :] = one_hot
        
        return predictions

def load_recent_data(data_file="data-dacbiet.txt", num_recent=10):
    """Đọc dữ liệu gần nhất từ file"""
    if not os.path.exists(data_file):
        print(f"Không tìm thấy file dữ liệu: {data_file}")
        return []
    
    with open(data_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Lọc và chuyển đổi dữ liệu
    numbers = []
    for line in lines:
        line = line.strip()
        if line.isdigit() and len(line) == 3:
            numbers.append(int(line))
    
    # Trả về số gần nhất
    return numbers[-num_recent:]

def find_latest_model():
    """Tìm mô hình mới nhất"""
    # Tìm cả file .keras và .h5 để tương thích ngược
    model_files = glob.glob("lottery_model_*.keras") + glob.glob("lottery_model_*.h5")
    if not model_files:
        return None
    
    # Sắp xếp theo thời gian sửa đổi
    model_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return model_files[0]

def main():
    """Hàm chính"""
    print("=== DỰ ĐOÁN XỔ SỐ SỬ DỤNG MÔ HÌNH LSTM ===\n")
    
    # Tìm mô hình mới nhất
    model_path = find_latest_model()
    if not model_path:
        print("Không tìm thấy mô hình đã huấn luyện!")
        print("Vui lòng chạy script lottery_prediction_model.py trước")
        return
    
    print(f"Sử dụng mô hình: {model_path}")
    
    # Tải dữ liệu gần nhất
    recent_data = load_recent_data()
    if not recent_data:
        print("Không thể đọc dữ liệu gần nhất")
        return
    
    print(f"Dữ liệu gần nhất ({len(recent_data)} số): {recent_data}")
    
    # Tạo predictor
    try:
        predictor = LotteryPredictor(model_path)
        
        # Dự đoán
        print(f"\nDự đoán sử dụng mô hình {predictor.model_type}:")
        
        if predictor.model_type == "raw_numbers":
            predictions = predictor.predict_next_numbers(recent_data, 255)
            print(f"255 số dự đoán tiếp theo:")
            
            # Hiển thị chi tiết (20 số đầu và 20 số cuối)
            print("\n20 số đầu tiên:")
            for i, pred in enumerate(predictions[:20], 1):
                print(f"  {i:3d}: {pred:03d}")
            
            print("\n20 số cuối cùng:")
            for i, pred in enumerate(predictions[-20:], 236):
                print(f"  {i:3d}: {pred:03d}")
            
            print(f"\nTổng cộng: {len(predictions)} số dự đoán")
        else:
            print("Chỉ hỗ trợ dự đoán raw_numbers")
        
        print(f"\nLưu ý: Đây chỉ là dự đoán dựa trên mô hình AI, không đảm bảo kết quả chính xác!")
        
    except Exception as e:
        print(f"Lỗi khi dự đoán: {str(e)}")

if __name__ == "__main__":
    main()
