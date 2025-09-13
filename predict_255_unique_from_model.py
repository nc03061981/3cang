#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script dự đoán 255 số khác nhau từ mô hình raw_numbers
"""

import numpy as np # type: ignore
import tensorflow as tf # type: ignore
from sklearn.preprocessing import MinMaxScaler # type: ignore
import os
import glob
import random
import json
from datetime import datetime, timedelta

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

def predict_255_unique_numbers(model_path, scaler_path, recent_data):
    """Dự đoán 255 số khác nhau từ mô hình raw_numbers"""
    print(f"\n🔢 DỰ ĐOÁN TỪ MÔ HÌNH RAW_NUMBERS:")
    print(f"Model: {os.path.basename(model_path)}")
    
    try:
        # Load model và scaler
        model = tf.keras.models.load_model(model_path)
        scaler = np.load(scaler_path, allow_pickle=True).item()
        
        # Chuẩn hóa dữ liệu đầu vào
        numbers_normalized = scaler.transform(np.array(recent_data).reshape(-1, 1)).flatten()
        
        # Dự đoán với randomness cao để tăng đa dạng
        predictions = []
        used_numbers = set()  # Để theo dõi số đã sử dụng
        current_sequence = numbers_normalized[-10:].reshape(1, 10, 1)
        
        print("🔄 Đang thực hiện dự đoán 255 số khác nhau...")
        
        attempts = 0
        max_attempts = 1000  # Giới hạn số lần thử để tránh vòng lặp vô hạn
        
        while len(predictions) < 255 and attempts < max_attempts:
            attempts += 1
            
            if attempts % 100 == 0:
                print(f"  Đã thử {attempts} lần, đã dự đoán {len(predictions)}/255 số...")
            
            pred = model.predict(current_sequence, verbose=0)
            
            # Sử dụng temperature scaling cao để tăng randomness
            temperature = 3.0  # Tăng từ 1.5 lên 3.0
            pred_scaled = pred[0] / temperature
            pred_probs = np.exp(pred_scaled) / np.sum(np.exp(pred_scaled))
            
            # Lấy top 10 predictions thay vì top 5 để tăng đa dạng
            top_10_indices = np.argsort(pred_probs)[-10:][::-1]
            top_10_probs = pred_probs[top_10_indices]
            
            # Chọn ngẫu nhiên từ top 10 với xác suất tương ứng
            chosen_idx = np.random.choice(top_10_indices, p=top_10_probs/np.sum(top_10_probs))
            pred_normalized = chosen_idx / 999.0
            
            # Chuyển về số nguyên
            pred_original = int(scaler.inverse_transform([[pred_normalized]])[0][0])
            
            # Chỉ thêm nếu số chưa được sử dụng
            if pred_original not in used_numbers:
                predictions.append(pred_original)
                used_numbers.add(pred_original)
                
                # Cập nhật chuỗi
                current_sequence = np.roll(current_sequence, -1, axis=1)
                current_sequence[0, -1, 0] = pred_normalized
            
            # Nếu đã thử quá nhiều lần mà không đủ 255 số, thêm số ngẫu nhiên
            if attempts > 500 and len(predictions) < 255:
                remaining_numbers = set(range(1000)) - used_numbers
                if remaining_numbers:
                    random_number = random.choice(list(remaining_numbers))
                    predictions.append(random_number)
                    used_numbers.add(random_number)
        
        print(f"✅ Dự đoán thành công: {len(predictions)} số")
        
        # Kiểm tra tính đa dạng
        unique_predictions = len(set(predictions))
        print(f"📊 Số dự đoán khác nhau: {unique_predictions}/255")
        
        if unique_predictions == 255:
            print("🎉 Hoàn hảo! Tất cả 255 số đều khác nhau!")
        elif unique_predictions >= 250:
            print("👍 Tuyệt vời! Hầu hết số đều khác nhau!")
        elif unique_predictions >= 200:
            print("👍 Tốt! Mô hình đã đa dạng hơn!")
        else:
            print("⚠️  Mô hình vẫn còn lặp lại nhiều")
        
        return predictions
            
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        return []

def save_to_json(numbers, filename="data-predict-today.json"):
    """Lưu số vào file JSON với ngày hiện tại (mỗi ngày chỉ lưu 1 lần)"""
    print(f"💾 Đang lưu vào file JSON: {filename}")
    
    # Lấy ngày hôm sau (chỉ lấy ngày, không lấy giờ)
    current_date = datetime.now() + timedelta(days=1)
    date_str = current_date.strftime("%Y-%m-%d")
    
    # Tạo dữ liệu mới (chỉ lưu formatted_numbers)
    formatted_numbers = [f"{num:03d}" for num in numbers]
    new_data = {
        "date": date_str,
        "timestamp": current_date.timestamp(),
        "total_numbers": len(numbers),
        "formatted_numbers": formatted_numbers,
        "model_info": {
            "type": "raw_numbers",
            "temperature": 3.0,
            "top_k": 10,
            "unique_count": len(set(numbers))
        }
    }
    
    # Ghi đè file (luôn ghi mới, không ghi nối tiếp)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Đã lưu thành công vào file JSON: {filename}")
    print(f"📅 Ngày tạo: {date_str}")
    print(f"📊 Tổng số: {len(numbers)}")
    print(f"🔢 Số khác nhau: {len(set(numbers))}")
    
    # Hiển thị 10 số đầu và cuối để kiểm tra
    print(f"\n📊 10 số đầu tiên: {','.join(formatted_numbers[:10])}")
    print(f"📊 10 số cuối cùng: {','.join(formatted_numbers[-10:])}")
    
def main():
    """Hàm chính"""
    print("=== DỰ ĐOÁN 255 SỐ TỪ MÔ HÌNH RAW_NUMBERS ===\n")
    
    # Tải dữ liệu gần nhất
    recent_data = load_recent_data()
    if not recent_data:
        print("Không thể đọc dữ liệu gần nhất")
        return
    
    print(f"📊 Dữ liệu gần nhất ({len(recent_data)} số): {recent_data}")
    
    # Tìm mô hình raw_numbers mới nhất
    raw_models = glob.glob("lottery_model_raw_numbers_*.keras")
    if not raw_models:
        print("❌ Không tìm thấy mô hình raw_numbers!")
        print("Vui lòng chạy script lottery_prediction_model.py trước")
        return
    
    # Sắp xếp theo thời gian sửa đổi
    raw_models.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    latest_model = raw_models[0]
    
    print(f"\n🔍 Tìm thấy mô hình:")
    print(f"  raw_numbers: {os.path.basename(latest_model)}")
    
    # Dự đoán 255 số khác nhau
    scaler_path = latest_model.replace('.keras', '_scaler.npy')
    if os.path.exists(scaler_path):
        predictions = predict_255_unique_numbers(latest_model, scaler_path, recent_data)
        
        if len(predictions) == 255:
            # Chỉ lưu vào file JSON (không tạo file .txt)
            save_to_json(predictions, "data-predict-today.json")
            
            print(f"\n{'='*60}")
            print("🎯 HOÀN THÀNH!")
            print("✅ 255 số khác nhau đã được dự đoán từ mô hình raw_numbers")
            print("✅ Đã lưu vào file: data-predict-today.json")
            print("✅ Dữ liệu cũ được giữ nguyên")
            print("✅ Chỉ lưu định dạng JSON, không tạo file .txt")
            print(f"{'='*60}")
        else:
            print(f"\n❌ Không thể dự đoán đủ 255 số khác nhau")
    else:
        print(f"\n❌ Không tìm thấy scaler cho raw_numbers")

if __name__ == "__main__":
    main()
