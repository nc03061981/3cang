# 🚀 Quy Trình Chuẩn Làm Việc Với Git Từ Local Đến GitHub

## 🎯 Mục tiêu
Đảm bảo bạn làm việc **an toàn**, **đồng bộ** và **chuyên nghiệp** khi phát triển code ở máy local và đẩy lên GitHub.

---

## 🧭 Tổng Quan Quy Trình
1. **Pull code mới nhất** từ GitHub về local  
2. **Tạo nhánh mới** (nếu cần thử nghiệm hoặc phát triển tính năng)  
3. **Code & commit** thay đổi ở local  
4. **Kiểm tra lại** và **merge** vào nhánh chính (nếu ổn định)  
5. **Push** code lên GitHub

---

## 🧱 Quy Trình Chi Tiết

### ✅ 1. Cập nhật code mới nhất từ GitHub
Trước khi bắt đầu code, **luôn đảm bảo local đồng bộ với GitHub**:
```bash
git checkout main
git pull origin main
```

> 💡 Nếu bạn đang ở nhánh khác, hãy merge main vào nhánh đó:
```bash
git merge main
```

---

### ✅ 2. Tạo nhánh mới (nếu cần)
Nếu bạn muốn thử nghiệm hoặc làm một tính năng mới:
```bash
git checkout -b feature-tenchucnang
```
Ví dụ:
```bash
git checkout -b feature-login
```

---

### ✅ 3. Code và lưu thay đổi
Sau khi code xong, kiểm tra file thay đổi:
```bash
git status
```

Thêm file cần commit:
```bash
git add .
```
Hoặc chọn file cụ thể:
```bash
git add file1.cs file2.cs
```

Commit với nội dung mô tả rõ ràng:
```bash
git commit -m "Thêm chức năng đăng nhập"
```

---

### ✅ 4. (Tùy chọn) Test kỹ trên nhánh thử nghiệm
Nếu ổn định, bạn có thể merge vào main:
```bash
git checkout main
git merge feature-login
```

---

### ✅ 5. Push code lên GitHub
Khi mọi thứ ổn định:
```bash
git push origin main
```

Hoặc nếu bạn đang làm việc ở nhánh khác:
```bash
git push origin feature-login
```

---

### ✅ 6. Kiểm tra trên GitHub
- Đảm bảo code đã được đẩy lên đúng nhánh.  
- Nếu bạn làm việc nhóm, có thể tạo **Pull Request** để review trước khi merge.

---

## 🧹 Quy Trình Sau Khi Hoàn Tất
- Nếu nhánh đã merge xong, xoá nhánh thử nghiệm để repo gọn gàng:
```bash
git branch -D feature-login
git push origin --delete feature-login
```

---

## ⚠️ Xử Lý Tình Huống Thường Gặp

### 🔁 Muốn bỏ hết thay đổi local, quay lại GitHub
```bash
git fetch origin
git reset --hard origin/main
git clean -fd
```

### 🧩 Muốn xem lại lịch sử commit
```bash
git log --oneline
```

### 🧪 Muốn xem khác biệt giữa 2 commit
```bash
git diff commit1 commit2
```

---

## 💡 Lời Khuyên
- Luôn **pull trước khi code**, **commit thường xuyên**, **push khi ổn định**.  
- Dùng nhánh riêng cho từng tính năng để tránh xung đột.  
- Viết nội dung commit **rõ ràng, ngắn gọn, dễ hiểu**.

---

© 2025 – Quy trình chuẩn làm việc với Git từ local đến GitHub 🚀
