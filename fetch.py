#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import json
from datetime import date, datetime, timezone, timedelta
import requests # type: ignore

def get_data_dacbiet(url: str) -> str | None:
    try:
        file_path = 'last-data-dacbiet.txt'

        # Kiểm tra file có tồn tại và không rỗng không
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.read().strip() # .strip() để loại bỏ khoảng trắng/xuống dòng thừa
            print(f"Đã lấy dữ liệu từ file: {data}")
        else:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.text.strip()
            print(f"Đã lấy dữ liệu từ fetch: {data}")

        # Kiểm tra hợp lệ: phải đúng 3 ký tự
        if len(data) == 3:
            return data
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi gọi API: {e}")
        return None

def save_data_dacbiet(data: str, filename: str = "data-dacbiet.txt"):
    # Chỉ ghi nếu hợp lệ (3 ký tự)
    if len(data) == 3:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(data + "\n")
        print(f"Đã ghi dữ liệu: {data}")
    else:
        print("Dữ liệu không hợp lệ, không ghi file")

def main():
    """Hàm chính"""
    print("=== GỌI FETCH.PY VÀ CẬP NHẬT DATA-DACBIET.TXT ===\n")
    
    # Lấy 3 số cuối của giải đặc biệt
    url = "https://ongvakien.com/getdb"
    special_numbers = get_data_dacbiet(url)
    success = False

    if special_numbers is not None:
        print(f"Hợp lệ, dữ liệu: {special_numbers}")
        save_data_dacbiet(special_numbers)
        print("Đã ghi dữ liệu mới vào file")
        success = True
    else:
        print("Không hợp lệ hoặc lỗi")
        print("Chưa lấy được kết quả giải đặc biệt")
        return
    
    print()
    
    if success:
        print(f"\n{'='*60}")
        print("🎯 HOÀN THÀNH CẬP NHẬT DỮ LIỆU!")
        print(f"✅ Đã trích xuất {len(special_numbers)} số từ giải đặc biệt")
        print(f"✅ Đã cập nhật file data-dacbiet.txt")
        print(f"{'='*60}")
        
    else:
        print(f"\n⚠️  Cập nhật không thành công")

if __name__ == "__main__":
    main()
