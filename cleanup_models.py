#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script dọn dẹp các model cũ và scaler
"""

import os
import glob
from datetime import datetime

def cleanup_old_models(model_type=None, keep_latest=True):
    """Xóa các model cũ, chỉ giữ lại model mới nhất"""
    print("=== DỌN DẸP MODEL CŨ ===\n")
    
    try:
        if model_type:
            # Dọn dẹp model cụ thể
            model_pattern = f"lottery_model_{model_type}_*.keras"
            scaler_pattern = f"lottery_model_{model_type}_*_scaler.npy"
            print(f"🧹 Đang dọn dẹp model {model_type}...")
        else:
            # Dọn dẹp tất cả model
            model_pattern = "lottery_model_*.keras"
            scaler_pattern = "*_scaler.npy"
            print("🧹 Đang dọn dẹp tất cả model...")
        
        # Tìm tất cả file model và scaler
        model_files = glob.glob(model_pattern)
        scaler_files = glob.glob(scaler_pattern)
        
        print(f"📁 Tìm thấy {len(model_files)} file model và {len(scaler_files)} file scaler")
        
        if len(model_files) == 0:
            print("✅ Không có model nào để dọn dẹp")
            return
        
        if len(model_files) <= 1 and keep_latest:
            print("✅ Chỉ có 1 model, không cần dọn dẹp")
            return
        
        # Sắp xếp theo thời gian tạo (mới nhất trước)
        model_files.sort(key=os.path.getmtime, reverse=True)
        scaler_files.sort(key=os.path.getmtime, reverse=True)
        
        # Hiển thị danh sách file
        print(f"\n📋 Danh sách file model:")
        for i, file_path in enumerate(model_files):
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            status = "🆕 MỚI NHẤT" if i == 0 else "🗑️  SẼ XÓA"
            print(f"  {i+1}. {os.path.basename(file_path)} - {file_time.strftime('%Y-%m-%d %H:%M:%S')} {status}")
        
        print(f"\n📋 Danh sách file scaler:")
        for i, file_path in enumerate(scaler_files):
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            status = "🆕 MỚI NHẤT" if i == 0 else "🗑️  SẼ XÓA"
            print(f"  {i+1}. {os.path.basename(file_path)} - {file_time.strftime('%Y-%m-%d %H:%M:%S')} {status}")
        
        # Xác nhận xóa
        if keep_latest:
            files_to_delete = model_files[1:] + scaler_files[1:]
            print(f"\n⚠️  Sẽ xóa {len(files_to_delete)} file cũ (giữ lại file mới nhất)")
        else:
            files_to_delete = model_files + scaler_files
            print(f"\n⚠️  Sẽ xóa TẤT CẢ {len(files_to_delete)} file")
        
        if len(files_to_delete) == 0:
            print("✅ Không có file nào để xóa")
            return
        
        # Xóa các file
        deleted_count = 0
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                print(f"🗑️  Đã xóa: {os.path.basename(file_path)}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Không thể xóa {os.path.basename(file_path)}: {str(e)}")
        
        print(f"\n✅ Đã xóa {deleted_count} file cũ")
        
        # Hiển thị file còn lại
        remaining_models = glob.glob(model_pattern)
        remaining_scalers = glob.glob(scaler_pattern)
        print(f"📁 Còn lại {len(remaining_models)} model và {len(remaining_scalers)} scaler")
        
    except Exception as e:
        print(f"❌ Lỗi khi dọn dẹp model cũ: {str(e)}")

def main():
    """Hàm chính"""
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            # Xóa tất cả model
            cleanup_old_models(keep_latest=False)
        elif sys.argv[1] == "--raw_numbers":
            # Xóa model raw_numbers cũ
            cleanup_old_models("raw_numbers", keep_latest=True)
        else:
            print("❌ Tham số không hợp lệ")
            print("Sử dụng:")
            print("  python cleanup_models.py                    # Dọn dẹp tất cả model cũ (giữ mới nhất)")
            print("  python cleanup_models.py --all              # Xóa tất cả model")
            print("  python cleanup_models.py --raw_numbers      # Dọn dẹp model raw_numbers cũ")
    else:
        # Dọn dẹp tất cả model cũ (giữ mới nhất)
        cleanup_old_models(keep_latest=True)

if __name__ == "__main__":
    main()
