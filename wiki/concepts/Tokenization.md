---
title: Tokenization
date: 2026-08-30
tags:
  - concept
  - token-economics
  - ai-architecture
  - llm-foundations
---

# Tokenization

**Tokenization** (tách token) là quá trình tiền xử lý và biểu diễn cơ bản nhất trong các mô hình ngôn ngữ lớn (LLM), biến đổi văn bản thô (raw text) thành các đơn vị rời rạc gọi là **token**, sau đó ánh xạ chúng thành các số nguyên (**Token IDs**) để mạng nơ-ron xử lý thông qua ma trận nhúng (embedding matrix).

---

## Vòng Đời Của Token (The Token Lifecycle)

```
┌──────────┐     Tokenizer     ┌────────┐     Vocab Lookup     ┌──────────┐     Embedding     ┌──────────────┐
│ Raw Text │ ───────────────>  │ Tokens │ ──────────────────>  │ Token ID │ ───────────────>  │ Dense Vector │
└──────────┘                   └────────┘                      └──────────┘                   └──────────────┘
```

1. **Văn bản đầu vào (Raw Text)**: Chuỗi ký tự con người nhập vào.
2. **Bộ tách Token (Tokenizer)**: Phân rã chuỗi ký tự thành các đoạn nhỏ dựa trên từ điển bộ từ vựng (Vocabulary).
3. **Mã số Token (Token ID)**: Ánh xạ mỗi token thành một số nguyên duy nhất đại diện cho vị trí của nó trong bộ từ vựng (ví dụ: `4523`, `1024`).
4. **Vector nhúng (Embeddings)**: Mô hình chuyển đổi Token ID thành vector số thực nhiều chiều để thực hiện các phép tính tự chú ý (Self-Attention).
5. **Văn bản đầu ra (Decoding)**: Chuyển đổi ngược các Token ID do mô hình sinh ra trở lại thành văn bản con người đọc được.

---

## Các Dạng Đơn Vị Token

Một token không nhất thiết phải là một từ hoàn chỉnh, mà có thể là:
- **Từ hoàn chỉnh**: Phổ biến với các từ thông dụng trong bộ từ vựng (ví dụ: `xin chào`, `hello`).
- **Từ phụ / Từ ghép nhỏ (Subwords)**: Các phần ghép của từ hiếm hoặc từ phức tạp (ví dụ: `tin` + `tưởng`, `un` + `happi` + `ness`).
- **Dấu câu & Ký tự đặc biệt**: `,`, `.`, `!`, `?`, `\n`, `\t`.
- **Chữ số**: `123`, `4.56` (thường được tách thành từng cụm chữ số hoặc từng chữ số đơn lẻ).
- **Khoảng trắng (Whitespace)**: Ký tự khoảng trắng ở đầu hoặc giữa các từ.
- **Biểu tượng cảm xúc (Emoji)**: `😊`, `🚀`, `🔥` (thường tiêu tốn từ 1 đến nhiều token tùy theo mã hóa byte UTF-8).

---

## 3 Thuật Toán Tách Token Phổ Biến

```
                                ┌───────────────────────────┐
                                │   Thuật Toán Tokenizer    │
                                └─────────────┬─────────────┘
                                              │
              ┌───────────────────────────────┼───────────────────────────────┐
              ▼                               ▼                               ▼
       ┌─────────────┐                 ┌─────────────┐                 ┌─────────────┐
       │     BPE     │                 │  WordPiece  │                 │SentencePiece│
       └─────────────┘                 └─────────────┘                 └─────────────┘
       Ghép cặp ký tự                   Ưu tiên khớp                   Xử lý text thô
       tần suất cao                     xác suất dài                   không cần space
       (GPT, Claude)                    (BERT)                         (LLaMA, T5)
```

### 1. Byte Pair Encoding (BPE)
- **Cơ chế**: Khởi tạo từ tập ký tự đơn lẻ cơ bản. Lặp đi lặp lại việc tìm và ghép cặp hai token xuất hiện cạnh nhau nhiều nhất trong tập dữ liệu huấn luyện để tạo thành token mới.
- **Cú pháp/Đặc trưng**: Ghép nối các mảnh từ trực tiếp dựa trên tần suất từ vựng.
- **Ứng dụng**: Thuật toán tiêu chuẩn trong hầu hết các LLM hiện đại ([[OpenAI]] GPT-2/3/4/5, [[Anthropic]] Claude, Meta Llama, RoBERTa).

### 2. WordPiece
- **Cơ chế**: Tương tự BPE nhưng thay vì chọn cặp có tần suất tuyệt đối cao nhất, WordPiece chọn cặp ký tự giúp tối đa hóa hàm hợp lý (likelihood) của dữ liệu huấn luyện.
- **Cú pháp/Đặc trưng**: Sử dụng tiền tố đặc biệt `##` để đánh dấu mảnh từ phụ gắn liền với phần tử đứng trước (ví dụ: từ `đang chơi` $\rightarrow$ `chơi` + `##đang`).
- **Ứng dụng**: Mô hình BERT, ALBERT, DistilBERT.

### 3. SentencePiece
- **Cơ chế**: Xử lý trực tiếp trên chuỗi byte hoặc chuỗi ký tự thô mà không giả định khoảng trắng là ranh giới tách từ. Khoảng trắng được xem là một ký tự thông thường.
- **Cú pháp/Đặc trưng**: Sử dụng ký tự gạch dưới đặc biệt `_` để biểu thị vị trí bắt đầu của một từ mới (ví dụ: `New York thật tuyệt` $\rightarrow$ `_New` + `_York` + `_thật` + `_tuyệt`).
- **Ứng dụng**: Độc lập hoàn toàn với ngôn ngữ; tối ưu vượt trội cho các ngôn ngữ không dùng dấu cách (tiếng Trung, tiếng Nhật) và các mô hình đa ngôn ngữ lớn (T5, LLaMA 2/3, PaLM, Gemma).

---

## So Sánh Chi Tiết: Token vs. Từ vs. Ký Tự

```
                     ┌────────────────────────────────────────────────────────┐
                     │               1 Token ≠ 1 Từ ≠ 1 Ký Tự                 │
                     ├────────────────────────────────────────────────────────┤
                     │ • Từ (Word)     : Đơn vị ngôn ngữ tự nhiên (con người) │
                     │ • Token         : Mảnh văn bản đại số (mô hình dùng)   │
                     │ • Ký tự (Char)  : Chữ cái, số, ký hiệu đơn lẻ          │
                     └────────────────────────────────────────────────────────┘
```

| Khía Cạnh | Từ (Word) | Token | Ký Tự (Character) |
| :--- | :--- | :--- | :--- |
| **Định nghĩa** | Từ vựng ngôn ngữ tự nhiên | Mảnh văn bản mô hình AI sử dụng | Chữ cái, chữ số, ký hiệu riêng lẻ |
| **Kích thước** | Lớn | Thay đổi linh hoạt (nhỏ $\rightarrow$ vừa) | Nhỏ nhất |
| **Ví dụ (`trí tuệ`)** | `"trí tuệ"` (1 từ ghép) | `["trí", "tuệ"]` (2 token) | `t, r, í, t, u, ệ` (6-7 ký tự) |
| **Mô hình LLM có hiểu trực tiếp?** | ❌ Không | ✅ Có (qua Token ID) | ❌ Không |

### Bảng Quy Đổi Ước Lượng Token Trung Bình

| Loại Nội Dung | Tỷ Lệ Quy Đổi Ước Lượng | Ví Dụ Minh Họa |
| :--- | :--- | :--- |
| **Văn bản tiếng Anh** | $\sim 1 \text{ token} \approx 0.75 \text{ từ}$ (hoặc 1 từ $\approx 1.33$ token) | $10 \text{ từ} \approx 13 \text{ token}$ |
| **Tiếng Việt / Trung / Nhật** | $\sim 1 \text{ token} \approx 1 \text{ ký tự}$ | `人工智能` (4 chữ) $\approx 4 \text{ token}$ |
| **Mã nguồn (Code)** | $\sim 1 \text{ token} \approx 1.3 \text{ từ / ký hiệu}$ | `print("Hi")` $\approx 8 \text{ token}$ |
| **Chữ số** | $\sim 1 \text{ chữ số} \approx 1 \text{ token}$ | `123456` $\approx 1 - 2 \text{ token}$ |
| **Emoji** | $\sim 1 \text{ emoji} \approx 1 - 3 \text{ token}$ | `😊` $\approx 1 \text{ token}$ |

---

## Ý Nghĩa Kỹ Thuật & Tối Ưu Chi Phí

1. **Hiệu Suất Nén Đa Ngôn Ngữ (Language Parity)**:
   - Các mô hình được tối ưu bộ từ vựng đa ngôn ngữ (như Kimi K3, GPT-5.6, Claude 3.5/3.7) có tỷ lệ nén token tốt hơn nhiều cho tiếng Việt hoặc các ngôn ngữ phi Latin, giúp giảm số lượng token cần thiết để biểu diễn cùng một lượng thông tin.
2. **Ảnh Hưởng Trực Tiếp Tới Chi Phí & Ngữ Cảnh**:
   - Số lượng token quyết định chi phí API, tốc độ sinh (decode throughput) và tốc độ đầy cửa sổ ngữ cảnh ([Context Window Management](file:///c:/ttluc/Project/learn-ai/tluc-wiki/wiki/concepts/Context%20Window%20Management.md)).
   - Quản trị prompt súc tích và chính xác giúp giảm tải cả token đầu vào lẫn token đầu ra ([Cost Optimization](file:///c:/ttluc/Project/learn-ai/tluc-wiki/wiki/concepts/Cost%20Optimization.md)).

---

## Related Knowledge Nodes

- **Concepts**: [[Token Economics]], [[Cost Optimization]], [[Context Window Management]], [[Context Rot]], [[Harness Overhead vs Model Cost]].
- **Entities**: [[Anthropic]], [[OpenAI]], [[Moonshot AI]], [[Claude Code]].
- **Sources**: [[Token and API Price Guide]], [[Maximizing the Value of Your Claude Code Sessions]], [[Manage costs effectively]].
