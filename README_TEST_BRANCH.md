# 🧪 Quy Trình Thử Nghiệm An Toàn Với Git Branch

## 🎯 Mục tiêu
Giúp bạn **thử nghiệm code thoải mái** mà **không ảnh hưởng đến nhánh chính (main)** hoặc GitHub.

---

## 🚀 Quy Trình Chuẩn

### ✅ 1. Cập nhật nhánh chính (main)
Trước khi bắt đầu thử nghiệm:
```bash
git checkout main
git pull origin main
```

---

### ✅ 2. Tạo nhánh thử nghiệm mới
```bash
git checkout -b test
```
> Bạn có thể đổi `test` thành tên mô tả hơn, ví dụ:  
> `feature-login`, `bugfix-api`, `experiment-new-ui`, ...

---

### ✅ 3. Thử nghiệm thoải mái
- Viết code, test logic, commit như bình thường:
```bash
git add .
git commit -m "Test logic mới"
```

---

### ✅ 4. Nếu **thành công**, muốn giữ lại thay đổi
Gộp (merge) vào nhánh chính:
```bash
git checkout main
git merge test
git push origin main
```

---

### ✅ 5. Nếu **thất bại**, muốn bỏ toàn bộ
Chỉ cần xóa nhánh thử nghiệm:
```bash
git checkout main
git branch -D test
```

> 🧹 Mọi thay đổi thử nghiệm sẽ **biến mất hoàn toàn**, main vẫn sạch.

---

### ✅ 6. Nếu đã push nhánh test lên GitHub
Xoá luôn trên GitHub:
```bash
git push origin --delete test
```

---

## 💡 Lệnh hữu ích

| Mục đích | Lệnh |
|----------|------|
| Quay về nhánh chính | `git checkout main` |
| Tạo nhánh mới từ main | `git checkout -b test` |
| Xoá nhánh local | `git branch -D test` |
| Xoá nhánh remote (trên GitHub) | `git push origin --delete test` |
| Làm nhánh test giống hệt main | `git checkout test && git reset --hard main` |

---

## 🧠 Ghi nhớ
- Luôn **pull main mới nhất** trước khi tạo nhánh test  
- Mỗi thử nghiệm = 1 nhánh riêng  
- Xoá nhánh test sau khi hoàn tất để repo gọn gàng

---

© 2025 – Quy trình Git an toàn cho thử nghiệm local 🧪
