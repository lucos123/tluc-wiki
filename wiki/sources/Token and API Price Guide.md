---
title: "Token and API Price Guide"
date: 2026-08-30
tags:
  - source
  - token-economics
  - visual-guide
  - infosec-notes
  - tokenization
source: "[[raw/screenshots/token-and-api-price/00.png]]"
source_type: visual-notes
---

# Token & Giá API — Sổ Tay Toàn Diện (10 Phần)

**Source Files**: 
- [[raw/screenshots/token-and-api-price/00.png]] *(Bìa & Mục lục tổng quan)*
- [[raw/screenshots/token-and-api-price/01.png]] *(1/10: Token AI là gì & Quy trình hoạt động)*
- [[raw/screenshots/token-and-api-price/02.png]] *(2/10: Tách Token - Tokenization)*
- [[raw/screenshots/token-and-api-price/03.png]] *(3/10: Chi tiết các phương pháp tách token BPE, WordPiece, SentencePiece)*
- [[raw/screenshots/token-and-api-price/04.png]] *(4/10: Token vs Từ vs Ký tự)*
- [[raw/screenshots/token-and-api-price/05.png]] *(5/10: Token Đầu vào & Đầu ra)*
- [[raw/screenshots/token-and-api-price/06.png]] *(6/10: Cửa sổ ngữ cảnh - Context Window)*
- [[raw/screenshots/token-and-api-price/07.png]] *(7/10: Token & Giá API)*
- [[raw/screenshots/token-and-api-price/08.png]] *(8/10: Giới hạn Token & Thực hành tốt nhất)*
- [[raw/screenshots/token-and-api-price/09.png]] *(9/10: Kỹ thuật nén & Tối ưu hiệu quả)*
- [[raw/screenshots/token-and-api-price/10.png]] *(10/10: Điều cốt lõi & Bảng tổng hợp một trang)*

---

## Tổng Quan Bộ Tài Liệu

Bộ tài liệu trực quan 10 phần tổng hợp toàn bộ kiến thức nền tảng và thực chiến về **Token, Tokenizer, Cửa sổ ngữ cảnh (Context Window), Định giá API và Kỹ thuật tối ưu chi phí token** trong các hệ thống LLM.

Triết lý cốt lõi:
$$\text{Prompt tốt hơn} \longrightarrow \text{Token tốt hơn} \longrightarrow \text{Hiệu quả tốt hơn} \longrightarrow \text{Chi phí thấp hơn} \longrightarrow \text{Kết quả tốt hơn!}$$

---

## Chi Tiết 10 Khối Kiến Thức

### 1. Token AI & Luồng Xử Lý
- **Bản chất**: Token là đơn vị văn bản nhỏ nhất mà mô hình AI có thể đọc và sinh ra.
- **Luồng xử lý dữ liệu**:
  $$\text{Văn bản đầu vào} \longrightarrow \text{Bộ tách Token} \longrightarrow \text{Token} \longrightarrow \text{Token ID (Số)} \longrightarrow \text{LLM} \longrightarrow \text{Văn bản đầu ra}$$
- **Tính chất**: Mỗi mô hình sử dụng bộ tách token riêng; cùng một văn bản sẽ sinh ra số lượng token khác nhau giữa các mô hình.

### 2 & 3. Các Phương Pháp Tách Token (Tokenization)

| Thuật Toán | Cơ Chế Phân Tách | Cú Pháp Đánh Dấu | Thế Mạnh & Ứng Dụng |
| :--- | :--- | :--- | :--- |
| **BPE (Byte Pair Encoding)** | Khởi tạo từ ký tự đơn, ghép các cặp xuất hiện nhiều nhất theo tần suất. | Ghép mảnh từ | Hiệu quả, phổ biến nhất: GPT-2/3/4/5, LLaMA, RoBERTa. |
| **WordPiece** | Tương tự BPE nhưng dùng điểm số xác suất (likelihood) để chọn mảnh tối ưu. | Tiền tố `##` (ví dụ: `chơi`, `##đang`) | Tối ưu xử lý từ hiếm: BERT, ALBERT, DistilBERT. |
| **SentencePiece** | Xử lý trực tiếp trên chuỗi văn bản thô, coi khoảng trắng là ký tự đặc biệt `_`. | Ký tự gạch dưới `_` (ví dụ: `_New`, `_York`) | Độc lập ngôn ngữ, tối ưu cho đa ngôn ngữ (Multilingual): T5, LLaMA 2/3, PaLM, Gemma. |

### 4. Phân Biệt: Token vs. Từ (Word) vs. Ký Tự (Character)
- **Quy tắc quan trọng**: $1 \text{ token} \neq 1 \text{ từ}$ và $1 \text{ token} \neq 1 \text{ ký tự}$.
- **Ví dụ thực tế tiếng Việt**:
  - `"Xin chào, thế giới!"` (3 từ / 19 ký tự) $\longrightarrow$ `[Xin] [chào] [,] [thế giới] [!]` = **5 token**.
  - `"trí tuệ"` (1 từ ghép / 7 ký tự) $\longrightarrow$ `[trí] [tuệ]` = **2 token**.
  - `"không thể tin được"` (1 từ ghép / 18 ký tự) $\longrightarrow$ `[không] [thể] [tin được]` = **3 token**.

### 5. Token Đầu Vào (Input) vs. Token Đầu Ra (Output)
- **Token Đầu Vào (Prompt)**: Hướng dẫn hệ thống (System Prompt), Lịch sử chat, Dữ liệu tài liệu RAG, Câu hỏi hiện tại, Ví dụ few-shot.
- **Token Đầu Ra (Completion)**: Câu trả lời mô hình tạo ra, code sinh ra, định dạng bảng/danh sách, và reasoning thinking tokens.
- **Ước lượng tỷ lệ chuyển đổi trung bình**:
  - Tiếng Anh: $1 \text{ token} \approx 0.75 \text{ từ}$ (hoặc 10 từ $\approx$ 13 token).
  - Tiếng Việt / Trung / Nhật: $1 \text{ token} \approx 1 \text{ ký tự}$.
  - Mã nguồn (Code): $1 \text{ token} \approx 1.3 \text{ từ}$.
  - Con số: $1 \text{ chữ số} \approx 1 \text{ token}$.
  - Emoji: $1 \text{ emoji} \approx 1 \text{ đến nhiều token}$.

### 6. Cửa Sổ Ngữ Cảnh (Context Window)
- **Định nghĩa**: Không gian bộ nhớ làm việc (RAM) tối đa mà LLM có thể xử lý cùng lúc trong một lượt tương tác:
  $$\text{Tổng Token} = \text{System Prompt} + \text{Lịch sử hội thoại} + \text{Tài liệu RAG} + \text{Prompt hiện tại} + \text{Dự phòng Output}$$
- **Rủi ro khi đầy context**: Token cũ bị đẩy ra ngoài (trục xuất ngữ cảnh), mất chỉ dẫn quan trọng, model trả lời lạc đề, suy giảm suy luận ([Context Rot](file:///c:/ttluc/Project/learn-ai/tluc-wiki/wiki/concepts/Context%20Rot.md)).
- **Quy mô context tiêu biểu**: GPT-3.5 (16K), GPT-4o (128K), Claude 3.5/3.7 (200K), Gemini 1.5/2.0 (1M–2M).

### 7. Định Giá API & Mô Hình Chi Phí
- Nhà cung cấp tính phí riêng biệt giữa Token Đầu Vào (Input) và Token Đầu Ra (Output, thường đắt gấp **3x – 5x** do chi phí giải mã GPU tuần tự):
  $$\text{Tổng Chi Phí} = \left(\frac{\text{Tokens Input}}{1.000.000} \times \text{Đơn giá Input}\right) + \left(\frac{\text{Tokens Output}}{1.000.000} \times \text{Đơn giá Output}\right)$$
- **Ví dụ**: 10.000 input tokens ($2.00/1M) + 20.000 output tokens ($8.00/1M) = $\$0.02 + \$0.16 = \$0.18$.

### 8 & 9. Kỹ Thuật Nén & Thực Hành Tốt Nhất (Best Practices)

| Kỹ Thuật Nén | Mô Tả & Hành Động | Mức Tiết Kiệm Thực Tế |
| :--- | :--- | :---: |
| **Loại bỏ từ thừa / từ đệm** | Cắt bỏ lời chào, từ hoa mỹ, cụm lặp lại (`rất, rất quan trọng` $\rightarrow$ `quan trọng`). | 15% – 25% |
| **Tóm tắt & Trích từ khóa** | Giữ ý chính, chuyển đoạn văn dài thành gạch đầu dòng ngắn. | 50% – 65% |
| **Định dạng cấu trúc** | Sử dụng Markdown bảng, danh sách bullet thay vì đoạn văn xuôi dài dòng. | 30% – 40% |
| **Cắt tỉa lịch sử & RAG Chunking** | Chỉ gửi các đoạn tài liệu có độ liên quan cao nhất thay vì ném cả file. | 60% – 76% |

**Ví dụ nén thực tế**:
- *Đoạn văn gốc*: 90 token.
- *Bản nén ý chính*: 35 token (tiết kiệm **61%**).
- *Bản trích từ khóa*: 22 token (tiết kiệm **75%**).

### 10. Bảng Tổng Hợp 5 Nguyên Tắc Vàng
1. **Rõ ràng và ngắn gọn**: Viết prompt trực diện, bỏ từ rườm rà.
2. **Chỉ cung cấp ngữ cảnh cần thiết**: Dùng RAG lọc chính xác, không đưa dữ liệu thừa.
3. **Cấu trúc hóa thông tin**: Sử dụng bảng, gạch đầu dòng, danh sách.
4. **Tóm tắt nội dung dài**: Tóm tắt tài liệu trước khi nạp vào phiên làm việc chính.
5. **Kiểm tra và đo lường định kỳ**: Dùng `tiktoken`, OpenAI Tokenizer, IDE token counter để giám sát.

---

## Related Knowledge Nodes

- **Concepts**: [[Tokenization]], [[Token Economics]], [[Cost Optimization]], [[Context Window Management]], [[Context Rot]], [[Harness Overhead vs Model Cost]].
- **Entities**: [[Anthropic]], [[OpenAI]], [[Claude Code]], [[Moonshot AI]].
- **Sources**: [[Maximizing the Value of Your Claude Code Sessions]], [[Manage costs effectively]], [[Track cost and usage]].
