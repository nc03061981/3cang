#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script gọi fetch.py trong vietnam-lottery-xsmb-analysis/src và cập nhật data-dacbiet.txt
"""

import sys
import os
import subprocess
import json
from datetime import date, datetime, timezone, timedelta

def run_fetch_script():
    """Chạy script fetch.py trong thư mục vietnam-lottery-xsmb-analysis/src"""
    print("🔄 Đang chạy script fetch.py trong vietnam-lottery-xsmb-analysis/src...")
    
    try:
        # Thay đổi thư mục làm việc
        original_cwd = os.getcwd()
        os.chdir('vietnam-lottery-xsmb-analysis')
        
        # Chạy script fetch.py từ thư mục gốc để đường dẫn data/ đúng
        result = subprocess.run([sys.executable, 'src/fetch.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        # Quay lại thư mục gốc
        os.chdir(original_cwd)
        
        if result.returncode == 0:
            print("✅ Script fetch.py đã chạy thành công")
            print("📊 Output:")
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    print(f"   {line}")
            return True
        else:
            print("❌ Script fetch.py chạy thất bại")
            print("📋 Lỗi:")
            for line in result.stderr.strip().split('\n'):
                if line.strip():
                    print(f"   {line}")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khi chạy script fetch.py: {str(e)}")
        # Quay lại thư mục gốc nếu có lỗi
        if 'original_cwd' in locals():
            os.chdir(original_cwd)
        return False

def read_xsmb_data():
    """Đọc dữ liệu từ file xsmb.json"""
    print("📚 Đang đọc dữ liệu từ xsmb.json...")
    
    try:
        xsmb_file = "vietnam-lottery-xsmb-analysis/data/xsmb.json"
        
        if not os.path.exists(xsmb_file):
            print(f"❌ Không tìm thấy file: {xsmb_file}")
            return None
        
        with open(xsmb_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"✅ Đã đọc {len(data)} bản ghi từ xsmb.json")
        return data
        
    except Exception as e:
        print(f"❌ Lỗi khi đọc file xsmb.json: {str(e)}")
        return None

def extract_special_numbers(xsmb_data):
    """Trích xuất 3 số cuối của giải đặc biệt từ dữ liệu xsmb"""
    print("🔍 Đang trích xuất 3 số cuối của giải đặc biệt...")
    
    try:
        special_numbers = []
        
        for record in xsmb_data:
            if 'special' in record and record['special']:
                special_number = record['special']
                last_3_digits = special_number % 1000
                special_numbers.append(last_3_digits)
        
        print(f"✅ Đã trích xuất {len(special_numbers)} số từ giải đặc biệt")
        
        # Hiển thị 5 số gần nhất
        if special_numbers:
            print(f"📊 5 số gần nhất: {special_numbers[-5:]}")
        
        return special_numbers
        
    except Exception as e:
        print(f"❌ Lỗi khi trích xuất số: {str(e)}")
        return None

def update_data_dacbiet(special_numbers):
    """Cập nhật file data-dacbiet.txt với tất cả số từ xsmb.json (xóa trắng trước)"""
    print("💾 Đang cập nhật file data-dacbiet.txt...")
    
    try:
        data_file = "data-dacbiet.txt"
        
        # Kiểm tra file hiện tại
        existing_lines = 0
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                existing_lines = len(f.readlines())
            print(f"📚 File hiện tại có {existing_lines} dòng")
        
        # Xóa trắng file trước khi cập nhật
        print(f"🧹 Đang xóa trắng file {data_file}...")
        with open(data_file, 'w', encoding='utf-8') as f:
            pass  # Tạo file trống
        
        # Ghi tất cả số mới vào file (cho phép trùng lặp)
        print(f"🆕 Đang ghi {len(special_numbers)} số mới vào file...")
        
        with open(data_file, 'w', encoding='utf-8') as f:
            for number in special_numbers:
                f.write(f"{number:03d}\n")
        
        print(f"✅ Đã ghi {len(special_numbers)} số mới vào file {data_file}")
        
        # Hiển thị thống kê
        print(f"📊 Tổng số dòng trong file: {len(special_numbers)}")
        print(f"📊 Dữ liệu cũ đã được xóa, chỉ còn dữ liệu mới")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi cập nhật file: {str(e)}")
        return False

def get_current_time_gmt7():
    """Lấy thời gian hiện tại theo GMT+7"""
    # Tạo timezone GMT+7
    gmt7 = timezone(timedelta(hours=7))
    return datetime.now(gmt7)

def is_after_18h45():
    """Kiểm tra xem thời gian hiện tại có sau 18h45 GMT+7 không"""
    current_time = get_current_time_gmt7()
    target_time = current_time.replace(hour=18, minute=45, second=0, microsecond=0)
    return current_time >= target_time

def get_today_special_number():
    """Lấy số đặc biệt của ngày hôm nay từ xsmb.json"""
    print("🔍 Đang tìm số đặc biệt của ngày hôm nay...")
    
    try:
        xsmb_file = "vietnam-lottery-xsmb-analysis/data/xsmb.json"
        
        if not os.path.exists(xsmb_file):
            print(f"❌ Không tìm thấy file: {xsmb_file}")
            return None
        
        with open(xsmb_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Lấy ngày hôm nay theo định dạng YYYY-MM-DD
        today = date.today().strftime("%Y-%m-%d")
        
        # Tìm bản ghi của ngày hôm nay (định dạng có thể là YYYY-MM-DD hoặc YYYY-MM-DDTHH:MM:SS.sss)
        for record in data:
            record_date = record.get('date', '')
            if (record_date.startswith(today) or record_date == today) and 'special' in record:
                special_number = record['special']
                last_3_digits = special_number % 1000
                print(f"✅ Tìm thấy số đặc biệt ngày {today}: {special_number} -> {last_3_digits:03d}")
                return last_3_digits
        
        print(f"⚠️  Không tìm thấy số đặc biệt cho ngày {today}")
        return None
        
    except Exception as e:
        print(f"❌ Lỗi khi tìm số đặc biệt: {str(e)}")
        return None

def get_today_prediction():
    """Lấy dự đoán của ngày hôm nay từ data-predict.json"""
    print("🔍 Đang tìm dự đoán của ngày hôm nay...")
    
    try:
        predict_file = "data-predict.json"
        
        if not os.path.exists(predict_file):
            print(f"❌ Không tìm thấy file: {predict_file}")
            return None
        
        with open(predict_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, dict) or "predictions" not in data:
            print("❌ Cấu trúc file JSON không đúng")
            return None
        
        # Lấy ngày hôm nay theo định dạng YYYY-MM-DD
        today = date.today().strftime("%Y-%m-%d")
        
        # Tìm dự đoán của ngày hôm nay
        for prediction in data["predictions"]:
            if prediction.get("date") == today:
                formatted_numbers = prediction.get("formatted_numbers", [])
                print(f"✅ Tìm thấy dự đoán ngày {today}: {len(formatted_numbers)} số")
                return formatted_numbers
        
        print(f"⚠️  Không tìm thấy dự đoán cho ngày {today}")
        return None
        
    except Exception as e:
        print(f"❌ Lỗi khi tìm dự đoán: {str(e)}")
        return None

def check_prediction_result(special_number, predictions):
    """Kiểm tra xem số đặc biệt có trong dự đoán không"""
    if special_number is None or predictions is None:
        return False
    
    # Chuyển số đặc biệt thành định dạng 3 chữ số
    special_formatted = f"{special_number:03d}"
    
    # Kiểm tra xem số có trong danh sách dự đoán không
    is_correct = special_formatted in predictions
    
    if is_correct:
        print(f"🎉 TRÚNG! Số {special_formatted} có trong dự đoán!")
    else:
        print(f"❌ TRẬT! Số {special_formatted} không có trong dự đoán")
    
    return is_correct

def save_result_to_json(special_number, is_correct):
    """Lưu kết quả vào file results.json"""
    print("💾 Đang lưu kết quả vào file results.json...")
    
    try:
        results_file = "results.json"
        today = date.today().strftime("%Y-%m-%d")
        current_time = get_current_time_gmt7().strftime("%Y-%m-%d %H:%M:%S")
        
        # Tạo dữ liệu kết quả mới
        new_result = {
            "date": today,
            "timestamp": current_time,
            "special_number": f"{special_number:03d}",
            "status": "trúng" if is_correct else "trật"
        }
        
        # Đọc dữ liệu hiện tại
        if os.path.exists(results_file):
            with open(results_file, 'r', encoding='utf-8') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = {"results": []}
        else:
            existing_data = {"results": []}
        
        # Đảm bảo có cấu trúc results
        if "results" not in existing_data:
            existing_data["results"] = []
        
        # Thêm kết quả mới
        existing_data["results"].append(new_result)
        
        # Lưu lại file
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Đã lưu kết quả vào {results_file}")
        print(f"📅 Ngày: {today}")
        print(f"🔢 Số đặc biệt: {special_number:03d}")
        print(f"📊 Trạng thái: {'trúng' if is_correct else 'trật'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi lưu kết quả: {str(e)}")
        return False

def get_today_prize6_numbers():
    """Lấy 3 số giải 6 của ngày hôm nay từ xsmb.json"""
    print("🔍 Đang tìm 3 số giải 6 của ngày hôm nay...")
    
    try:
        xsmb_file = "vietnam-lottery-xsmb-analysis/data/xsmb.json"
        
        if not os.path.exists(xsmb_file):
            print(f"❌ Không tìm thấy file: {xsmb_file}")
            return None
        
        with open(xsmb_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Lấy ngày hôm nay theo định dạng YYYY-MM-DD
        today = date.today().strftime("%Y-%m-%d")
        
        # Tìm bản ghi của ngày hôm nay
        for record in data:
            record_date = record.get('date', '')
            if (record_date.startswith(today) or record_date == today):
                prize6_numbers = []
                
                # Lấy 3 số cuối của 3 giải 6
                if 'prize6_1' in record:
                    prize6_1 = record['prize6_1'] % 1000
                    prize6_numbers.append(prize6_1)
                
                if 'prize6_2' in record:
                    prize6_2 = record['prize6_2'] % 1000
                    prize6_numbers.append(prize6_2)
                
                if 'prize6_3' in record:
                    prize6_3 = record['prize6_3'] % 1000
                    prize6_numbers.append(prize6_3)
                
                if prize6_numbers:
                    formatted_numbers = [f"{num:03d}" for num in prize6_numbers]
                    print(f"✅ Tìm thấy 3 số giải 6 ngày {today}: {formatted_numbers}")
                    return formatted_numbers
        
        print(f"⚠️  Không tìm thấy 3 số giải 6 cho ngày {today}")
        return None
        
    except Exception as e:
        print(f"❌ Lỗi khi tìm 3 số giải 6: {str(e)}")
        return None

def check_prize6_prediction_result(prize6_numbers, predictions):
    """Kiểm tra xem các số giải 6 có trong dự đoán không"""
    if prize6_numbers is None or predictions is None:
        return {"trung": 0, "trat": 0, "details": []}
    
    results = {"trung": 0, "trat": 0, "details": []}
    
    for number in prize6_numbers:
        is_correct = number in predictions
        if is_correct:
            results["trung"] += 1
            print(f"🎉 TRÚNG! Số {number} có trong dự đoán!")
        else:
            results["trat"] += 1
            print(f"❌ TRẬT! Số {number} không có trong dự đoán")
        
        results["details"].append({
            "number": number,
            "status": "trúng" if is_correct else "trật"
        })
    
    return results

def save_prize6_result_to_json(prize6_numbers, results):
    """Lưu kết quả giải 6 vào file results-giai6.json"""
    print("💾 Đang lưu kết quả giải 6 vào file results-giai6.json...")
    
    try:
        results_file = "results-giai6.json"
        today = date.today().strftime("%Y-%m-%d")
        current_time = get_current_time_gmt7().strftime("%Y-%m-%d %H:%M:%S")
        
        # Tạo dữ liệu kết quả mới
        new_result = {
            "date": today,
            "timestamp": current_time,
            "prize6_numbers": prize6_numbers,
            "trung": results["trung"],
            "trat": results["trat"],
            "details": results["details"]
        }
        
        # Đọc dữ liệu hiện tại
        if os.path.exists(results_file):
            with open(results_file, 'r', encoding='utf-8') as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = {"results": []}
        else:
            existing_data = {"results": []}
        
        # Đảm bảo có cấu trúc results
        if "results" not in existing_data:
            existing_data["results"] = []
        
        # Thêm kết quả mới
        existing_data["results"].append(new_result)
        
        # Lưu lại file
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Đã lưu kết quả giải 6 vào {results_file}")
        print(f"📅 Ngày: {today}")
        print(f"🔢 3 số giải 6: {prize6_numbers}")
        print(f"📊 Trúng: {results['trung']}, Trật: {results['trat']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi khi lưu kết quả giải 6: {str(e)}")
        return False

def check_and_save_results():
    """Kiểm tra và lưu kết quả dự đoán nếu đã sau 18h45"""
    print("🕐 Kiểm tra thời gian hiện tại...")
    
    current_time = get_current_time_gmt7()
    print(f"📅 Thời gian hiện tại (GMT+7): {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if not is_after_18h45():
        print("⏰ Chưa đến 18h45, không kiểm tra kết quả")
        return
    
    print("✅ Đã sau 18h45, bắt đầu kiểm tra kết quả dự đoán...")
    
    # Lấy số đặc biệt của ngày hôm nay
    special_number = get_today_special_number()
    if special_number is None:
        print("❌ Không thể lấy số đặc biệt của ngày hôm nay")
        return
    
    # Lấy dự đoán của ngày hôm nay
    predictions = get_today_prediction()
    if predictions is None:
        print("❌ Không thể lấy dự đoán của ngày hôm nay")
        return
    
    # Kiểm tra kết quả
    is_correct = check_prediction_result(special_number, predictions)
    
    # Lưu kết quả
    save_result_to_json(special_number, is_correct)

def check_and_save_prize6_results():
    """Kiểm tra và lưu kết quả dự đoán giải 6 nếu đã sau 18h45"""
    print("🕐 Kiểm tra thời gian hiện tại cho giải 6...")
    
    current_time = get_current_time_gmt7()
    print(f"📅 Thời gian hiện tại (GMT+7): {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if not is_after_18h45():
        print("⏰ Chưa đến 18h45, không kiểm tra kết quả giải 6")
        return
    
    print("✅ Đã sau 18h45, bắt đầu kiểm tra kết quả dự đoán giải 6...")
    
    # Lấy 3 số giải 6 của ngày hôm nay
    prize6_numbers = get_today_prize6_numbers()
    if prize6_numbers is None:
        print("❌ Không thể lấy 3 số giải 6 của ngày hôm nay")
        return
    
    # Lấy dự đoán của ngày hôm nay
    predictions = get_today_prediction()
    if predictions is None:
        print("❌ Không thể lấy dự đoán của ngày hôm nay")
        return
    
    # Kiểm tra kết quả giải 6
    results = check_prize6_prediction_result(prize6_numbers, predictions)
    
    # Lưu kết quả giải 6
    save_prize6_result_to_json(prize6_numbers, results)

def main():
    """Hàm chính"""
    print("=== GỌI FETCH.PY VÀ CẬP NHẬT DATA-DACBIET.TXT ===\n")
    
    # Bước 1: Chạy script fetch.py trong vietnam-lottery-xsmb-analysis/src
    print("🔄 BƯỚC 1: Chạy script fetch.py...")
    if not run_fetch_script():
        print("❌ Không thể chạy script fetch.py")
        return
    
    print()
    
    # Bước 2: Đọc dữ liệu từ xsmb.json
    print("🔄 BƯỚC 2: Đọc dữ liệu từ xsmb.json...")
    xsmb_data = read_xsmb_data()
    if xsmb_data is None:
        print("❌ Không thể đọc dữ liệu từ xsmb.json")
        return
    
    print()
    
    # Bước 3: Trích xuất 3 số cuối của giải đặc biệt
    print("🔄 BƯỚC 3: Trích xuất 3 số cuối của giải đặc biệt...")
    special_numbers = extract_special_numbers(xsmb_data)
    if special_numbers is None:
        print("❌ Không thể trích xuất số từ dữ liệu")
        return
    
    print()
    
    # Bước 4: Cập nhật file data-dacbiet.txt
    print("🔄 BƯỚC 4: Cập nhật file data-dacbiet.txt...")
    success = update_data_dacbiet(special_numbers)
    
    if success:
        print(f"\n{'='*60}")
        print("🎯 HOÀN THÀNH CẬP NHẬT DỮ LIỆU!")
        print(f"✅ Đã chạy script fetch.py thành công")
        print(f"✅ Đã đọc {len(xsmb_data)} bản ghi từ xsmb.json")
        print(f"✅ Đã trích xuất {len(special_numbers)} số từ giải đặc biệt")
        print(f"✅ Đã cập nhật file data-dacbiet.txt")
        print(f"{'='*60}")
        
        # Bước 5: Kiểm tra kết quả dự đoán nếu đã sau 18h45
        print(f"\n🔄 BƯỚC 5: Kiểm tra kết quả dự đoán...")
        check_and_save_results()
        
        # Bước 6: Kiểm tra kết quả dự đoán giải 6 nếu đã sau 18h45
        print(f"\n🔄 BƯỚC 6: Kiểm tra kết quả dự đoán giải 6...")
        check_and_save_prize6_results()
        
    else:
        print(f"\n⚠️  Cập nhật không thành công")

if __name__ == "__main__":
    main()
