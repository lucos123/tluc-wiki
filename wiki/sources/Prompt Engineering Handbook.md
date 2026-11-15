---
title: "Prompt Engineering Handbook"
date: 2026-11-15
tags:
  - source
  - prompt-engineering
  - visual-guide
  - context-engineering
  - llm-foundations
source: "[[raw/articles/ai-other/prompt-engineering-handbook.md]]"
source_type: visual-notes
---

# Cẩm Nang Prompt Engineering Bằng Tiếng Việt (11 Trang)

**Source Files**:
- [[raw/articles/ai-other/prompt-engineering-handbook.md]] *(Bài đăng Facebook gốc của [[Viet Nguyen AI]], 2026-11-12)*
- [[raw/screenshots/prompt-engineering-handbook/00.jpg]] *(Bìa: Tổng quan Prompt Engineering & Công thức 6 thành phần)*
- [[raw/screenshots/prompt-engineering-handbook/01.jpg]] *(1/10: Giới thiệu về Prompt Engineering)*
- [[raw/screenshots/prompt-engineering-handbook/02.jpg]] *(2/10: Cấu trúc của một Prompt tốt)*
- [[raw/screenshots/prompt-engineering-handbook/03.jpg]] *(3/10: Các loại Prompt)*
- [[raw/screenshots/prompt-engineering-handbook/04.jpg]] *(4/10: Cấu trúc Prompt & Framework)*
- [[raw/screenshots/prompt-engineering-handbook/05.jpg]] *(5/10: Few-Shot & Prompt dựa trên ví dụ)*
- [[raw/screenshots/prompt-engineering-handbook/06.jpg]] *(6/10: Chain-of-Thought & Stepwise Prompting)*
- [[raw/screenshots/prompt-engineering-handbook/07.jpg]] *(7/10: Advanced Prompting Techniques)*
- [[raw/screenshots/prompt-engineering-handbook/08.jpg]] *(8/10: Prompt cho các tác vụ khác nhau)*
- [[raw/screenshots/prompt-engineering-handbook/09.jpg]] *(9/10: Nguyên tắc viết Prompt hiệu quả)*
- [[raw/screenshots/prompt-engineering-handbook/10.jpg]] *(10/10: Danh sách kiểm tra & Điều cần nhớ)*

---

## Tổng Quan Bộ Tài Liệu

Bộ tài liệu trực quan 11 trang được [[Viet Nguyen AI]] chuyển ngữ sang tiếng Việt từ ấn phẩm tiếng Anh gốc (`instagram.com/p/Ddf156akx9W`), hệ thống hóa toàn diện nền tảng [[Prompt Engineering]] từ cấu trúc câu lệnh cơ bản đến các kỹ thuật suy luận và điều phối tác vụ nâng cao cho LLM.

Công thức tổng kết cốt lõi:
$$\text{Một prompt tốt} = \text{Chỉ dẫn rõ ràng} + \text{Ngữ cảnh phù hợp} + \text{Định dạng đúng}$$

---

## Tổng Hợp 10 Khối Kiến Thức

### 1. Bản Chất & Cấu Trúc 6 Thành Phần Của Prompt Tốt (Cover, 1/10, 2/10)
- **Nguyên lý vận hành:** LLM không có mục tiêu hay ý định tự thân; mô hình dự đoán chuỗi token tiếp theo phù hợp nhất dựa trên prompt đầu vào và dữ liệu huấn luyện ($\text{Con người} \rightarrow \text{Prompt} \rightarrow \text{LLM} \rightarrow \text{Đầu ra}$).
- **6 thành phần chuẩn của Prompt:**
  1. **Nhiệm vụ / Chỉ dẫn (Task):** Yêu cầu cụ thể cần làm gì.
  2. **Ngữ cảnh (Context):** Thông tin nền và bối cảnh tình huống.
  3. **Vai trò (Role — tùy chọn):** Gán persona chuyên môn cho mô hình.
  4. **Dữ liệu đầu vào (Input Data):** Văn bản, bảng số liệu hoặc chi tiết cần xử lý.
  5. **Ràng buộc (Constraints):** Giới hạn độ dài, giọng điệu, quy tắc nên/không nên làm.
  6. **Định dạng đầu ra (Output Format):** Gạch đầu dòng, danh sách đánh số, bảng, JSON, hoặc đoạn văn.

### 2. Phân Loại Prompt & Kỹ Thuật [[Few-Shot Prompting]] (3/10, 5/10)
- **6 dạng prompt chính:** Zero-shot (0 ví dụ, chính xác ★☆☆☆☆) $\rightarrow$ One-shot (1 ví dụ, ★★★☆☆) $\rightarrow$ Few-shot (2–10+ ví dụ, ★★★★☆) $\rightarrow$ Instruction-based (★★★★☆) $\rightarrow$ Role-based (★★★★☆) $\rightarrow$ Hybrid kết hợp Vai trò + Ví dụ + Chỉ dẫn từng bước (★★★★★).
- **Nguyên tắc chọn ví dụ:** Chất lượng quan trọng hơn số lượng; các cặp `Input → Output` phải nhất quán định dạng, sát tác vụ, bao quát biến thể và tránh nhồi nhét gây nhiễu ngữ cảnh ([[Context Rot]]).

### 3. Ba Framework Thiết Kế Prompt (4/10)

| Framework | Cấu Trúc Thành Phần | Trường Hợp Tối Ưu | Độ Phức Tạp |
| :--- | :--- | :--- | :---: |
| **CO-STAR** | Context – Objective – Style – Tone – Audience – Response | Viết nội dung, marketing, giao tiếp người dùng | Trung bình |
| **R-T-F** | Role – Task – Format | Phân tích dữ liệu, báo cáo, tóm tắt có cấu trúc | Thấp–TB |
| **CLEAR** | Context – Look/Role – Expectation – Action – Result | Dự án nhiều bước, giải quyết vấn đề phức tạp | Cao |

### 4. [[Chain-of-Thought Prompting]] & 7 Kỹ Thuật Nâng Cao (6/10, 7/10)
- **Chain-of-Thought (CoT):** Ép mô hình tách bước (`Hiểu vấn đề → Chia nhỏ bước → Giải từng bước → Kết luận`), khắc phục lỗi suy luận tắt trong bài toán tốc độ hay tam đoạn luận logic.
- **7 kỹ thuật trong [[Advanced Prompting Patterns]]:**
  1. **Chain-of-Thought:** Suy nghĩ từng bước.
  2. **Self-Consistency:** Tạo nhiều luồng suy luận và chọn đáp án đồng thuận cao nhất.
  3. **Role Prompting:** Gán góc nhìn chuyên gia.
  4. **ReAct-style:** Vòng lặp `Suy nghĩ → Hành động → Quan sát → Lặp lại` (nền tảng cho [[Loop Engineering]]).
  5. **Tree-of-Thought (ToT):** Khám phá nhiều nhánh hướng đi dạng cây để lập kế hoạch/tối ưu hóa.
  6. **Prompt Chaining:** Chia nhỏ tác vụ lớn thành chuỗi prompt kế tiếp (`Tóm tắt → Trích ý → Tạo tweet`).
  7. **Meta-Prompting:** Yêu cầu LLM tự nâng cấp prompt trước khi thực thi.

### 5. Mẫu Tác Vụ, 10 Nguyên Tắc & Checklist Trước Khi Gửi (8/10, 9/10, 10/10)
- **8 nhóm tác vụ phổ biến:** Tạo văn bản, Tóm tắt, Dịch thuật, Phân loại, Trích xuất dữ liệu (Table/JSON), Lập trình (Sinh/Debug/Giải thích), Viết sáng tạo, Giải quyết vấn đề / Q&A.
- **10 nguyên tắc vàng:** Rõ ràng & cụ thể; Cung cấp ngữ cảnh; Chọn định dạng; Chỉ định giọng điệu; Đặt ràng buộc; Dùng ví dụ; Chia nhỏ tác vụ; Nói rõ điều cần; Lặp lại & tinh chỉnh; Giữ sự đơn giản.
- **5 lỗi phổ biến cần tránh:** Quá mơ hồ • Quá dài gây rối • Thiếu định dạng • Thiếu ngữ cảnh • Không kiểm tra/tinh chỉnh lại phản hồi đầu tiên.

---

## Synthesis Notes

- Trên bậc thang tiến hóa [[Agent Engineering Ladder]], tài liệu này hệ thống hóa trọn vẹn tầng nền tảng **Prompt Engineering** (tầng 1), đồng thời cho thấy rõ các nguyên lý gốc như *Prompt Chaining*, *ReAct*, và *Tree-of-Thought* đã trực tiếp tiến hóa thành [[Context Engineering]], [[Loop Engineering]], và [[Graph Engineering]] trong các hệ thống agent hiện đại.
- Khi kết hợp cùng [[Token and API Price Guide]], việc áp dụng cấu trúc hóa định dạng (bảng/JSON), nén từ thừa và chọn lọc ví dụ Few-shot chất lượng cao giúp vừa tăng độ chính xác vừa giảm chi phí token và hạn chế [[Context Rot]].
- Với các mô hình suy luận thế hệ mới (native reasoning), kỹ thuật CoT thủ công trong prompt đang dần chuyển dịch sang điều khiển bằng tham số [[Reasoning Effort]].

---

## Related Knowledge Nodes

- **Entities**: [[Viet Nguyen AI]]
- **Concepts**: [[Prompt Engineering]], [[Few-Shot Prompting]], [[Chain-of-Thought Prompting]], [[Advanced Prompting Patterns]], [[Agent Engineering Ladder]], [[Context Engineering]], [[Context Rot]], [[Reasoning Effort]], [[Loop Engineering]], [[Graph Engineering]]
- **Sources**: [[Token and API Price Guide]], [[You Can Learn AI Agent Graph Engineering In 21 Min]], [[What Is Context Engineering]]
