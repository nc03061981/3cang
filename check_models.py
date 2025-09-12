#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script kiểm tra và hiển thị thông tin về các mô hình đã huấn luyện
"""

import os
import glob
import numpy as np
import tensorflow as tf
from datetime import datetime

def get_model_info():
    """Lấy thông tin về các mô hình đã huấn luyện"""
    print("=== KIỂM TRA MÔ HÌNH ĐÃ HUẤN LUYỆN ===\n")
    
    # Tìm tất cả các file mô hình
    keras_models = glob.glob("lottery_model_*.keras")
    h5_models = glob.glob("lottery_model_*.h5")
    all_models = keras_models + h5_models
    
    if not all_models:
        print("❌ Không tìm thấy mô hình nào đã huấn luyện!")
        print("Vui lòng chạy script lottery_prediction_model.py trước")
        return
    
    print(f"✅ Tìm thấy {len(all_models)} mô hình:")
    print("-" * 80)
    
    for i, model_path in enumerate(all_models, 1):
        # Lấy thông tin file
        file_size = os.path.getsize(model_path) / (1024 * 1024)  # MB
        mod_time = datetime.fromtimestamp(os.path.getmtime(model_path))
        
        # Xác định loại mô hình
        if "raw_numbers" in model_path:
            model_type = "Raw Numbers (000-999)"
        elif "sum" in model_path:
            model_type = "Sum (0-27)"
        elif "counts" in model_path:
            model_type = "Digit Counts (0-9)"
        else:
            model_type = "Unknown"
        
        # Kiểm tra scaler
        base_path = model_path.replace('.keras', '').replace('.h5', '')
        scaler_path = f"{base_path}_scaler.npy"
        has_scaler = os.path.exists(scaler_path)
        
        print(f"{i}. {os.path.basename(model_path)}")
        print(f"   Loại: {model_type}")
        print(f"   Kích thước: {file_size:.2f} MB")
        print(f"   Ngày tạo: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Scaler: {'✅ Có' if has_scaler else '❌ Không có'}")
        
        # Kiểm tra mô hình có load được không
        try:
            model = tf.keras.models.load_model(model_path)
            model.summary()
            print(f"   Trạng thái: ✅ Load thành công")
        except Exception as e:
            print(f"   Trạng thái: ❌ Lỗi load: {str(e)}")
        
        print("-" * 80)
    
    # Thống kê
    print("\n📊 THỐNG KÊ:")
    print(f"Tổng số mô hình: {len(all_models)}")
    print(f"Mô hình .keras: {len(keras_models)}")
    print(f"Mô hình .h5: {len(h5_models)}")
    
    # Kiểm tra scaler
    scalers = glob.glob("lottery_model_*_scaler.npy")
    print(f"Scaler có sẵn: {len(scalers)}")
    
    # Mô hình mới nhất
    if all_models:
        latest_model = max(all_models, key=os.path.getmtime)
        print(f"Mô hình mới nhất: {os.path.basename(latest_model)}")

def check_data_file():
    """Kiểm tra file dữ liệu"""
    print("\n=== KIỂM TRA FILE DỮ LIỆU ===\n")
    
    data_file = "data-dacbiet.txt"
    if not os.path.exists(data_file):
        print(f"❌ Không tìm thấy file dữ liệu: {data_file}")
        return
    
    # Đọc và phân tích dữ liệu
    with open(data_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Lọc dữ liệu hợp lệ
    valid_numbers = []
    invalid_lines = []
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if line.isdigit() and len(line) == 3:
            valid_numbers.append(int(line))
        elif line:  # Bỏ qua dòng trống
            invalid_lines.append((i, line))
    
    print(f"✅ File dữ liệu: {data_file}")
    print(f"Tổng số dòng: {len(lines)}")
    print(f"Số hợp lệ: {len(valid_numbers)}")
    print(f"Số không hợp lệ: {len(invalid_lines)}")
    
    if valid_numbers:
        print(f"Phạm vi số: {min(valid_numbers):03d} - {max(valid_numbers):03d}")
        print(f"10 số gần nhất: {valid_numbers[-10:]}")
    
    if invalid_lines:
        print(f"\n⚠️  Các dòng không hợp lệ (5 dòng đầu):")
        for i, (line_num, content) in enumerate(invalid_lines[:5]):
            print(f"   Dòng {line_num}: '{content}'")

def main():
    """Hàm chính"""
    print("🔍 KIỂM TRA HỆ THỐNG DỰ ĐOÁN XỔ SỐ\n")
    
    # Kiểm tra mô hình
    get_model_info()
    
    # Kiểm tra dữ liệu
    check_data_file()
    
    print("\n" + "="*80)
    print("🎯 HƯỚNG DẪN TIẾP THEO:")
    if not glob.glob("lottery_model_*"):
        print("1. Chạy: python lottery_prediction_model.py")
        print("2. Chờ huấn luyện hoàn tất")
        print("3. Chạy: python predict_lottery.py")
    else:
        print("1. Chạy: python predict_lottery.py")
        print("2. Hoặc huấn luyện lại: python lottery_prediction_model.py")
    print("="*80)

if __name__ == "__main__":
    main()
