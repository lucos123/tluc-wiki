---
title: Báo Cáo Tổng Hợp Hệ Thống Tài Liệu Đào Tạo & Đánh Giá Thử Việc TVV
date: 2026-07-26
tags: [bao-cao, dao-tao, thu-viec, tvv, nha-khoa-3c, hub]
source:
  - [[quytrinh_thuviec_tvv_3c]]
  - [[TVV_quytrinhtuvan_v1]]
  - [[TVV_checklist_7_ngay_v1]]
  - [[TVV_checklist_moc_1_tuan_2_3]]
  - [[TVV_checklist_moc_2_tuan_4_5]]
  - [[TVV_checklist_moc_3_tuan_6_8]]
  - [[TVV_implant_ghepxuong_v1]]
  - [[TVV_rangsu_veneer_v1]]
  - [[TVV_thamkhao_v1]]
  - [[TVV_kichbanchuyensau_v1]]
  - [[TVV_xulytuchoi_v1]]
---

# BÁO CÁO TỔNG HỢP: HỆ THỐNG TÀI LIỆU ĐÀO TẠO & ĐÁNH GIÁ THỬ VIỆC  
# VỊ TRÍ: TƯ VẤN VIÊN NHA KHOA (TVV) — NHA KHOA 3C

**Ngày lập báo cáo:** 26/07/2026  
**Người lập:** Trưởng nhóm Tư vấn viên (Lead)  
**Đơn vị:** Bộ phận Tư vấn – Công ty TNHH TMDV Y Tế 3C  
**Địa chỉ:** A35 Cống Quỳnh, P. Cầu Ông Lãnh, Tp. Hồ Chí Minh

---

## I. MỤC TIÊU & BỐI CẢNH XÂY DỰNG TÀI LIỆU

Trước đây, việc đào tạo nhân sự mới vị trí Tư vấn viên (TVV) tại Nha khoa 3C chưa có một hệ thống tài liệu nhất quán, dẫn đến:
- **Thiếu chuẩn mực:** Mỗi Lead truyền đạt theo cách riêng, không đồng bộ.
- **Mất nhiều thời gian:** Không có lộ trình rõ ràng, TVV mới tự mò mẫm kéo dài.
- **Không theo dõi được tiến độ:** Không có biểu mẫu đánh giá định kỳ theo mốc.
- **Quyết định cuối kỳ thiếu cơ sở:** Ra quyết định ký HĐLĐ hay dừng hợp tác chủ yếu dựa vào cảm tính.

**Mục tiêu dự án:** Xây dựng bộ tài liệu đào tạo - đánh giá thử việc TVV hoàn chỉnh, chuẩn hóa theo khung WBS của Phòng HCNS, đồng thời bổ sung chiều sâu chuyên môn thực chiến đặc thù của bộ phận Tư vấn nha khoa.

---

## II. KIẾN TRÚC TỔNG THỂ CỦA HỆ THỐNG TÀI LIỆU

Hệ thống tài liệu được tổ chức theo kiến trúc **Hub & Spoke** (Trung tâm & Vệ tinh):

```
                    ┌──────────────────────────────────┐
                    │   quytrinh_thuviec_tvv_3c.md     │
                    │   🗂️  MASTER PLAN (HUB)           │
                    │   Cẩm nang & Bảng đánh giá       │
                    │   tổng hợp toàn bộ 2 tháng        │
                    └────────────┬─────────────────────┘
                                 │ Liên kết tới
          ┌──────────────────────┼──────────────────────┐
          │                      │                      │
    📐 QUY TRÌNH           📚 KIẾN THỨC            📋 BIỂU MẪU
          │                      │                ĐÁNH GIÁ THEO MỐC
  TVV_quytrinhtuvan_v1     ┌─────┴──────┐              │
  (Sơ đồ luồng chạy        │            │         ┌────┴────────────────────┐
   khách — Mermaid)   TVV_implant  TVV_rangsu      │ TVV_checklist_7_ngay   │
                      _ghepxuong  _veneer_v1        │ TVV_checklist_moc_1    │
                      _v1         (Răng sứ,         │ TVV_checklist_moc_2    │
                      (Implant,   Veneer)            │ TVV_checklist_moc_3   │
                      Ghép xương)                   └────────────────────────┘
                           │
                     ┌─────┴──────┐
                 TVV_thamkhao  TVV_kichban
                 _v1           _chuyensau_v1
                 (Roleplay &   (9 phân khúc
                 Thấu hiểu KH) khách hàng)
                                   │
                             TVV_xulytuchoi_v1
                             (20 câu từ chối +
                              5 câu khủng hoảng)
```

---

## III. CHI TIẾT TỪNG TÀI LIỆU TRONG HỆ THỐNG

### 3.1. 🗂️ MASTER PLAN (HUB TRUNG TÂM)

| Tên file | Mô tả | Vai trò |
|:---|:---|:---|
| [quytrinh_thuviec_tvv_3c.md](./quytrinh_thuviec_tvv_3c.md) (`[[quytrinh_thuviec_tvv_3c]]`) | **Cẩm Nang & Bảng Đánh Giá Thử Việc TVV** | File trung tâm. Trưởng nhóm và nhân sự mới cùng sử dụng. |

**Nội dung chính của Master Plan gồm 5 Phần:**
- **Phần I:** Thông tin chung & Ma trận phân loại năng lực đầu vào (Junior vs Senior).
- **Phần II:** Bảng Master Checklist chuẩn WBS 1.1 → 7.1 (khớp 100% template Phòng HCNS).
- **Phần III:** Hướng dẫn chi tiết nội dung đào tạo theo từng WBS (6 bước làm việc hàng ngày của TVV, kỹ năng Remo, 3 Mốc đào tạo chuyên sâu).
- **Phần IV:** Hệ thống thang điểm đánh giá Final 100 điểm (4 trụ cột năng lực).
- **Phần V:** Cơ chế kết luận & đề xuất ký Hợp đồng Lao động (HĐLĐ).

---

### 3.2. 📐 TÀI LIỆU QUY TRÌNH VẬN HÀNH

| Tên file | Nội dung chính | Đặc điểm nổi bật |
|:---|:---|:---|
| [TVV_quytrinhtuvan_v1.md](./TVV_quytrinhtuvan_v1.md) (`[[TVV_quytrinhtuvan_v1]]`) | Sơ đồ luồng di chuyển khách hàng tại phòng khám, từ khi KH bước qua cửa đến khi check "Hoàn thành" trên Remo. | **Sơ đồ Mermaid** được đối chiếu và khớp 100% với bản vẽ thiết kế gốc `TVV_motaquytrinh.png`. Phân rõ vai trò 4 bên: BS, TVV, LT/ĐP, PT. Ghi đúng tên phần mềm `Remo` và voucher `CSRM`. |

**Cấu trúc sơ đồ (8 nút chính):**
1. TVV tiếp đón → 2. LT/ĐP xác nhận KH mới/cũ → 3. Chụp phim (nếu cần) → 4. BS + TVV tư vấn chuyên môn → 5. TVV tư vấn lại & báo giá → 6. KH quyết định (Đồng ý/Từ chối) → 7. Điều trị hoặc Hẹn lại → 8. Cảm ơn, đánh giá hài lòng & check Remo.

---

### 3.3. 📚 TÀI LIỆU KIẾN THỨC CHUYÊN MÔN

| Tên file | Nội dung chính | Dành cho Giai đoạn |
|:---|:---|:---|
| [TVV_implant_ghepxuong_v1.md](./TVV_implant_ghepxuong_v1.md) (`[[TVV_implant_ghepxuong_v1]]`) | Kiến thức tổng quan về Implant (cấu trúc 3 phần, các dòng trụ Hàn/Mỹ/Thụy Sĩ), kỹ thuật ghép xương (GBR, nâng xoang, Implant tức thì), quy trình tư vấn 7 bước. | **Mốc 1 — Tuần 2-3** |
| [TVV_rangsu_veneer_v1.md](./TVV_rangsu_veneer_v1.md) (`[[TVV_rangsu_veneer_v1]]`) | Phân loại răng sứ (toàn sứ Emax/Cercon/Lava vs sứ kim loại), so sánh chi tiết Bọc răng sứ vs Dán sứ Veneer, chỉ định lâm sàng từng loại. | **Mốc 1 — Tuần 2-3** |
| [TVV_thamkhao_v1.md](./TVV_thamkhao_v1.md) (`[[TVV_thamkhao_v1]]`) | Kỹ năng thấu hiểu khách hàng (5 bước tư vấn tổng quan), bảng đánh giá tiêu xương theo thời gian mất răng, 4 kịch bản hội thoại Roleplay thực chiến (ghép xương, nâng xoang, sống hàm mỏng, Implant tức thì). | **Mốc 2 — Tuần 4-5** |
| [TVV_kichbanchuyensau_v1.md](./TVV_kichbanchuyensau_v1.md) (`[[TVV_kichbanchuyensau_v1]]`) | Bộ kịch bản tư vấn chuyên sâu theo **9 phân khúc khách hàng** (Niềng răng Pitts21/Ultima, Niềng răng trẻ em tăng trưởng, Implant ghép xương, Implant tức thì, Implant toàn hàm All-on-4, Phục hình Răng sứ, Veneer nhiễm Tetra, Nhổ răng khôn). Mỗi kịch bản có 3 phiên bản: Cơ bản → Mở rộng → Cao cấp. | **Mốc 2 — Tuần 4-5** |
| [TVV_xulytuchoi_v1.md](./TVV_xulytuchoi_v1.md) (`[[TVV_xulytuchoi_v1]]`) | **5 câu xử lý khủng hoảng truyền thông** (vụ Sở Y Tế kiểm tra) + **20 câu xử lý từ chối** chia theo 4 nhóm rào cản: Giá & Tài chính, Nỗi sợ Y khoa, So sánh & Nghi ngờ, Trì hoãn & Đòi hỏi thêm thời gian. | **Mốc 3 — Tuần 6-8** |

---

### 3.4. 📋 BỘ BIỂU MẪU CHECKLIST ĐÁNH GIÁ THEO MỐC

| Tên file | Mốc đánh giá | Nội dung đánh giá chính |
|:---|:---|:---|
| [TVV_checklist_7_ngay_v1.md](./TVV_checklist_7_ngay_v1.md) (`[[TVV_checklist_7_ngay_v1]]`) | **Tuần 1 (7 Ngày đầu)** | Lịch trình học từng ngày (Ngày 1-7), bảng chấm điểm thái độ & tố chất (thang 1-5), đề xuất: Đạt / Theo dõi thêm / Dừng. |
| [TVV_checklist_moc_1_tuan_2_3.md](./TVV_checklist_moc_1_tuan_2_3.md) (`[[TVV_checklist_moc_1_tuan_2_3]]`) | **Mốc 1 (Tuần 2-3)** | Kiến thức Implant & Ghép xương, Răng sứ & Veneer, Chỉnh nha. 5 ca Shadowing. 3 bài test cuối mốc (Lý thuyết 30 câu, Remo, Vấn đáp 1-1). |
| [TVV_checklist_moc_2_tuan_4_5.md](./TVV_checklist_moc_2_tuan_4_5.md) (`[[TVV_checklist_moc_2_tuan_4_5]]`) | **Mốc 2 (Tuần 4-5)** | Kịch bản 9 phân khúc, thực hành Roleplay 1-1, Co-counseling 5 ca thực tế. 3 bài test Roleplay cuối mốc. |
| [TVV_checklist_moc_3_tuan_6_8.md](./TVV_checklist_moc_3_tuan_6_8.md) (`[[TVV_checklist_moc_3_tuan_6_8]]`) | **Mốc 3 & Final (Tuần 6-8)** | Thực chiến độc lập 100%, 20 cuộc gọi/ngày, hoàn thành KPI Tháng 2. **Bảng chấm điểm Final 100 điểm** + Biên bản đề xuất ký HĐLĐ có 3 chữ ký (Lead, HCNS, Giám đốc). |

---

## IV. LỘ TRÌNH ĐÀO TẠO 8 TUẦN THEO DÒNG THỜI GIAN

| Tuần | Giai đoạn | Nội dung trọng tâm | Tài liệu sử dụng | Đầu ra đánh giá |
|:---:|:---|:---|:---|:---|
| **Ngày 1** | Chào đón | Onboarding, giới thiệu phòng ban, bàn giao Mentor | — | Phân loại Junior/Senior |
| **Tuần 1** | Nền tảng & Nhận diện | Văn hóa 3C, JD 6 bước, luồng KH, Remo, bảng giá cơ bản, quan sát Lễ tân, Roleplay đón tiếp | `TVV_checklist_7_ngay_v1` | **Test Ngày 7** (≥80% đạt) |
| **Tuần 2** | Quy trình & Sản phẩm 1 | Sơ đồ luồng tư vấn, 5 thao tác Remo, Implant & Ghép xương, Shadowing 5 ca | `TVV_quytrinhtuvan_v1` + `TVV_implant_ghepxuong_v1` | — |
| **Tuần 3** | Sản phẩm 2 & Bài test Mốc 1 | Răng sứ & Veneer, Chỉnh nha Pitts21/Ultima, bảng giá chi tiết, Shadowing 5 ca | `TVV_rangsu_veneer_v1` | **Test Mốc 1** (Cuối tuần 3) |
| **Tuần 4** | Kịch bản Cơ bản & Mở rộng | Kịch bản 9 phân khúc (Cơ bản + Mở rộng), kỹ năng thấu hiểu KH | `TVV_kichbanchuyensau_v1` + `TVV_thamkhao_v1` | — |
| **Tuần 5** | Roleplay & Co-counseling | Kịch bản Cao cấp, nhập vai 1-1 với Lead, đứng tư vấn song song 5 ca | `TVV_thamkhao_v1` | **Test Mốc 2** (Cuối tuần 5) |
| **Tuần 6** | Thực chiến 50% + Xử lý Từ chối | 5 câu khủng hoảng + 20 câu từ chối, đứng độc lập 50% số ca | `TVV_xulytuchoi_v1` | — |
| **Tuần 7-8** | Thực chiến 100% + KPI | Đứng độc lập 100%, 20 cuộc gọi follow/ngày, chạy KPI doanh số Tháng 2 | — | **Đánh giá Final 100 điểm** |

---

## V. HỆ THỐNG THANG ĐIỂM ĐÁNH GIÁ FINAL (100 ĐIỂM)

| Trụ cột năng lực | Trọng số | Điểm tối đa | Cách đo lường |
|:---|:---:|:---:|:---|
| 1. Kiến thức Chuyên môn & Sản phẩm | 25% | 25đ | Bài test trắc nghiệm tổng hợp 50 câu (Implant, Sứ, Niềng, Xử lý từ chối) |
| 2. Kỹ năng Tư vấn, Chốt Sale & KPI | 35% | 35đ | Conversion Rate ≥ 30% + % hoàn thành KPI doanh số tháng 2 |
| 3. Quy trình Vận hành & Remo | 20% | 20đ | Tuân thủ 100% luồng sơ đồ, không bị phàn nàn, nhập Remo chuẩn xác |
| 4. Thái độ, Tác phong & Văn hóa 3C | 20% | 20đ | Đúng giờ, đồng phục, chủ động hỗ trợ, tinh thần đội nhóm |
| **TỔNG** | **100%** | **100đ** | |

**Cơ chế xét HĐLĐ:**
- 🏆 **≥ 85 điểm:** Ký HĐLĐ chính thức + xét thưởng KPI thử việc.
- ✅ **70-84 điểm:** Ký HĐLĐ chính thức vị trí TVV.
- ⚠️ **55-69 điểm:** Gia hạn thử việc thêm 1 tháng (Junior có thái độ tốt).
- ❌ **< 55 điểm:** Dừng hợp tác sau 2 tháng thử việc.

---

## VI. ĐIỂM NỔI BẬT & GIÁ TRỊ THỰC TIỄN CỦA BỘ TÀI LIỆU

### ✅ Tính nhất quán với Khung HCNS
- Bảng Master Checklist khớp **100% mã WBS 1.1 → 7.1** từ file CSV chuẩn của Phòng HCNS.
- Cấp trên có thể kiểm tra tiến độ trực tiếp bằng cách đối chiếu cột WBS.

### ✅ Tính chuyên sâu đặc thù của bộ phận TVV
- Không chỉ là template hành chính chung, bộ tài liệu bổ sung **chiều sâu chuyên môn y nha** thực chiến cho từng tuần.
- Bộ kịch bản 9 phân khúc khách hàng và 20 câu xử lý từ chối là **tài sản tri thức nội bộ** đặc thù của 3C.

### ✅ Tính liên kết & điều hướng thông minh
- Mọi tài liệu đều được liên kết theo **định dạng kép**: `[Tên hiển thị](./file.md)` (click được) + `[[wiki-link]]` (hiện trong Obsidian Graph).
- Trưởng nhóm chỉ cần mở Master Plan, click là đến ngay biểu mẫu đánh giá của tuần đang diễn ra.

### ✅ Cá nhân hóa lộ trình đào tạo
- **Junior TVV:** Tuân thủ 100% lộ trình 8 tuần, Shadowing tối thiểu 20 ca trước khi đứng độc lập.
- **Senior TVV:** Rút ngắn giai đoạn học sản phẩm, nhận KPI chính thức từ Tuần 3.

### ✅ Tính minh bạch trong quyết định nhân sự
- Thay vì quyết định cảm tính, toàn bộ cơ sở ký HĐLĐ được ghi nhận bằng **bảng chấm điểm 100 điểm** với 4 trụ cột đo lường rõ ràng.
- Biên bản đánh giá Final có đủ 3 chữ ký: Lead, Trưởng phòng HCNS, Giám đốc Chuyên môn.

---

## VII. DANH MỤC FILE HOÀN CHỈNH

| STT | Tên file | Loại | Kích thước | Mô tả |
|:---:|:---|:---:|:---:|:---|
| 1 | [quytrinh_thuviec_tvv_3c.md](./quytrinh_thuviec_tvv_3c.md) | Hub | 16.7 KB | Master Plan — Cẩm nang & Bảng đánh giá tổng hợp |
| 2 | [TVV_quytrinhtuvan_v1.md](./TVV_quytrinhtuvan_v1.md) | Quy trình | 7.5 KB | Sơ đồ luồng chạy khách (Mermaid, khớp PNG gốc) |
| 3 | [TVV_motaquytrinh.png](./TVV_motaquytrinh.png) | Hình ảnh | 83.3 KB | Bản vẽ sơ đồ quy trình gốc (nguồn chuẩn tham chiếu) |
| 4 | [TVV_implant_ghepxuong_v1.md](./TVV_implant_ghepxuong_v1.md) | Kiến thức | 13.5 KB | Tài liệu chuyên môn Implant & Ghép xương |
| 5 | [TVV_rangsu_veneer_v1.md](./TVV_rangsu_veneer_v1.md) | Kiến thức | 10.2 KB | Tài liệu chuyên môn Răng sứ & Veneer |
| 6 | [TVV_thamkhao_v1.md](./TVV_thamkhao_v1.md) | Kỹ năng | 8.6 KB | Roleplay & Kỹ năng thấu hiểu khách hàng |
| 7 | [TVV_kichbanchuyensau_v1.md](./TVV_kichbanchuyensau_v1.md) | Kịch bản | 22.8 KB | Bộ kịch bản tư vấn chuyên sâu 9 phân khúc |
| 8 | [TVV_xulytuchoi_v1.md](./TVV_xulytuchoi_v1.md) | Kịch bản | 20.7 KB | Bộ 20 câu xử lý từ chối + 5 câu khủng hoảng |
| 9 | [TVV_checklist_7_ngay_v1.md](./TVV_checklist_7_ngay_v1.md) | Biểu mẫu | 6.6 KB | Checklist đánh giá 7 ngày đầu (Tuần 1) |
| 10 | [TVV_checklist_moc_1_tuan_2_3.md](./TVV_checklist_moc_1_tuan_2_3.md) | Biểu mẫu | 6.9 KB | Checklist đánh giá Mốc 1 (Tuần 2-3) |
| 11 | [TVV_checklist_moc_2_tuan_4_5.md](./TVV_checklist_moc_2_tuan_4_5.md) | Biểu mẫu | 7.2 KB | Checklist đánh giá Mốc 2 (Tuần 4-5) |
| 12 | [TVV_checklist_moc_3_tuan_6_8.md](./TVV_checklist_moc_3_tuan_6_8.md) | Biểu mẫu | 8.1 KB | Checklist đánh giá Mốc 3 & Final (Tuần 6-8) |
| 13 | [3c_quytrinhthuviec_v1.csv](./3c_quytrinhthuviec_v1.csv) | Nguồn gốc | 3.2 KB | Template WBS gốc từ Phòng HCNS (nguồn tham chiếu) |
| | **TỔNG CỘNG** | **13 files** | **~226 KB** | **Bộ tài liệu đào tạo TVV hoàn chỉnh** |

---

## VIII. ĐỀ XUẤT BỔ SUNG & PHÁT TRIỂN (v2)

1. **Bộ câu hỏi thi kiến thức (Question Bank):** Xây dựng ngân hàng 50-100 câu trắc nghiệm để chạy bài test chính thức cuối Mốc 1 & Final.
2. **Bảng theo dõi KPI hàng tuần:** File Excel/Sheet theo dõi doanh số thực tế từng TVV trong Tuần 6-8.
3. **Video Roleplay mẫu:** Quay lại 2-3 ca tư vấn thực tế đạt chuẩn để TVV mới xem và học theo.
4. **Chuyển thư mục chính thức:** Sau khi Lead xác nhận toàn bộ nội dung, di chuyển bộ tài liệu từ `raw/3c/tvv-daotao-thuviec/` về `wiki/concepts/` để quản lý phiên bản chính thức.

---

*Báo cáo được lập bởi Trưởng nhóm Tư vấn viên — Nha khoa 3C*  
*Tất cả tài liệu lưu tại: `raw/3c/tvv-daotao-thuviec/`*
