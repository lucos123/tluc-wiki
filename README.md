# tluc-wiki (2nd Brain)

Chào mừng tới **tluc-wiki** — hệ thống cơ sở trí thức cá nhân (2nd Brain) của **tluc**, tập trung nghiên cứu, tổng hợp kiến thức về **Trí tuệ Nhân tạo (AI)** và các thông tin cá nhân liên quan.

Repository này áp dụng mô hình **LLM Wiki Pattern**, được thiết kế để kết hợp giữa ghi chú dạng thẻ kết nối (Obsidian) và sự hỗ trợ trực tiếp từ các AI Agent (như Gemini, Claude Code, Codex...).

---

## 📐 Kiến trúc & Thư mục (Directory Structure)

```text
tluc-wiki/
├── GEMINI.md              # 📜 Quy tắc, Schema và Quy trình làm việc của LLM Agent
├── index.md               # 🗂️ Danh mục nội dung tổng hợp của Wiki (Catalog)
├── raw/                   # 🔒 Dữ liệu gốc bất biến (Articles, Notes, Papers, Assets)
│   ├── *.md
│   └── assets/            # Hình ảnh, tài liệu đính kèm
├── wiki/                  # 📝 Cơ sở kiến thức được LLM & cá nhân duy trì
│   ├── log.md             # Nhật ký thao tác (Ingest / Query / Lint)
│   ├── analyses/          # Phân tích tổng hợp đa nguồn, so sánh chuyên sâu
│   ├── concepts/          # Khái niệm, mô hình, phương pháp luận AI & cá nhân
│   ├── entities/          # Thượng tầng công cụ, sản phẩm, tổ chức, nhân vật
│   └── sources/           # Tóm tắt & trích xuất nội dung từ thư mục raw/
└── .agents/skills/        # 🔧 Các kỹ năng tự động hóa (Skills) cho AI Agent
    ├── wiki-ingest/       # Kỹ năng nạp tài liệu mới vào Wiki
    ├── wiki-query/        # Kỹ năng truy vấn & tổng hợp câu trả lời
    └── wiki-lint/         # Kỹ năng kiểm tra sức khỏe Wiki (liên kết hỏng, thiếu sót)
```

---

## ⚙️ Nguyên tắc Vận hành (Operating Rules)

1. **`raw/` là Bất biến (Immutable)**: Tất cả tài liệu thô, bài viết, báo cáo đưa vào `raw/` chỉ đọc, không chỉnh sửa trực tiếp.
2. **Tổng hợp theo Thực thể & Khái niệm**: Thông tin mới từ `raw/` sẽ được tổng hợp vào `wiki/sources/`, sau đó cập nhật trực tiếp vào các trang `wiki/concepts/` và `wiki/entities/` liên quan.
3. **Liên kết Standard Relative Markdown Links**: Sử dụng cú pháp Markdown chuẩn (`[Tên Trang](relative/path.md)`, percent-encoded với `%20`) để kết nối liên tục các trang khái niệm, thực thể và nguồn — bấm mở trực tiếp được trên cả **IDE Markdown Preview, GitHub lẫn Obsidian**. Trong mục `## Related Pages`, nhóm có từ 3 link trở lên được trình bày thành sub-bullet gọn gàng.
4. **Nhật ký `wiki/log.md`**: Mọi thao tác Nạp (Ingest), Truy vấn (Query) hay Kiểm tra (Lint) đều được ghi nhận theo mốc thời gian.

---

## 🚀 Các Thao tác Chính với AI Agent

- **Ingest (Nạp dữ liệu)**: *"Ingest bài viết mới trong raw/..."* -> Agent sẽ đọc file gốc, tạo tóm tắt tại `wiki/sources/`, cập nhật `wiki/concepts/` / `wiki/entities/`, và cập nhật `index.md`.
- **Query (Truy vấn)**: *"Giải thích cho tôi về khái niệm X trong wiki"* -> Agent tra cứu `index.md`, trích xuất thông tin kèm dẫn nguồn Markdown link (`[Tên Trang](relative/path.md)`).
- **Lint (Kiểm tra)**: *"Kểm tra sức khỏe wiki"* -> Agent rà soát liên kết hỏng, các trang chưa được kết nối hoặc thông tin bị trùng lặp/mâu thuẫn.

---

## 🛠️ Công cụ Sử dụng
- **IDE Markdown Preview & GitHub**: Xem, đọc và điều hướng trực tiếp giữa các file `.md` ngay trong IDE hoặc trên GitHub Web.
- **Obsidian**: Trình xem & quản lý ghi chú đồ thị (Graph view / Backlinks) — tương thích 100% với Standard Markdown Links.
- **LLM AI Agents**: Gemini Antigravity, Claude Code, CLI Tools.
