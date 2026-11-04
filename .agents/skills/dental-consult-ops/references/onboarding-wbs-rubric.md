# KHUNG QUẢN TRỊ ĐÀO TẠO THỬ VIỆC TVV 8 TUẦN (MASTER WBS & RUBRIC ĐÁNH GIÁ)

> **Căn cứ tài liệu gốc:** `TVV-QT-001` (Quy trình đào tạo thử việc TVV) & `3c-quytrinhthuviec-v1.csv` (Khung WBS chuẩn HCNS).  
> **Cơ sở áp dụng:** Bộ phận Tư vấn — Hệ thống Nha Khoa 3C.  
> **Thời gian:** 02 Tháng (08 Tuần) | **Nhịp vận hành:** Họp Review Thứ 4 hằng tuần.

---

## 1. Mốc 0: Phân Luồng Năng Lực Đầu Vào (Ngày Nhận Việc)

Ngay trong ngày đầu tiên tiếp nhận nhân sự, Trưởng nhóm TVV (Lead Consultant) phỏng vấn thẩm định để phân loại nhân sự mới vào 1 trong 2 luồng:

```mermaid
graph TD
    Input["Nhân Sự Mới Nhận Việc (Ngày 1)"] --> Assess{"Thẩm Định Kinh Nghiệm"}
    
    Assess -->|Chưa có KN Nha Khoa<br>hoặc < 6 tháng Sale| Junior["Luồng 1: JUNIOR TVV<br>- Bắt buộc hoàn thành đủ 8 tuần WBS<br>- Shadowing tối thiểu 20 ca cùng BS & Lead<br>- Bài kiểm tra bắt buộc tại Ngày 7, M1, M2, M3"]
    Assess -->|1 - 2 năm KN Nha Khoa lớn<br>(Đã hiểu Implant/Sứ)| Senior["Luồng 2: SENIOR TVV<br>- Rút ngắn Tuần 1-2: Học văn hóa 3C & Thao tác Remo<br>- Bỏ qua học lý thuyết cơ bản<br>- Bắt đầu nhận KPI doanh số chính thức từ Tuần 3"]
```

---

## 2. Master Checklist Tiến Độ 8 Tuần (Chuẩn Mã WBS)

| Mã WBS | Giai Đoạn / Thời Điểm | Hạng Mục Công Việc Chi Tiết | Người Phụ Trách (PIC) | Tiêu Chí Nghiệm Thu (DoD) |
| :---: | :--- | :--- | :---: | :--- |
| **1.1** | Ngày 1 | Chào đón nhân sự mới, bố trí vị trí làm việc, cấp tài khoản phần mềm Remo & Zalo công vụ. | HCNS & Lead TVV | Bàn giao đủ tài sản & công cụ làm việc. |
| **1.2** | Ngày 1 | Giới thiệu sơ đồ nhân sự, vai trò từng thành viên: Lễ tân, Điều phối, Bác sĩ, Phụ tá, KTV X-quang. | Lead TVV | Nhân sự mới chào hỏi và nắm đầu mối liên hệ. |
| **1.3** | Ngày 1 | Bổ nhiệm Mentor/Người hướng dẫn trực tiếp theo sát trong suốt thời gian thử việc. | Lead TVV | Mentor ký cam kết đồng hành đào tạo. |
| **2.1** | Tuần 1 | Đào tạo Văn hóa doanh nghiệp, Nội quy lao động, Tác phong diện mạo chuẩn 3C, Bảo mật dữ liệu. | HCNS & Lead TVV | Ký cam kết bảo mật và nội quy phòng khám. |
| **3.1** | Tuần 1 | Làm rõ Bản mô tả công việc (JD 6 bước tư vấn) và Thẻ điểm KPI doanh số Tháng 1, Tháng 2. | Lead TVV | Thống nhất mục tiêu doanh số và tỷ lệ chuyển đổi. |
| **3.2** | Tuần 1 | Làm rõ cơ chế phối hợp 4 bên tại ghế nha và phòng tư vấn VIP. | Lead TVV | Hiểu rõ vị trí trong luồng di chuyển khách. |
| **4.1** | Tuần 1 | Phân loại 4 tệp khách hàng bên ngoài: Khách mới, Khách đang điều trị, Khách bảo hành, Khách VIP. | Lead TVV | Nhận diện đúng tâm lý từng tệp khách hàng. |
| **4.2** | Tuần 1 | Phân loại khách hàng bên trong (Lễ tân, Điều phối, Bác sĩ, Phụ tá) và đầu mối làm việc. | Lead TVV | Thuộc luồng chuyển giao thông tin bệnh nhân. |
| **5.1** | Ngày 3 (Tuần 1) | Học bảng giá cơ bản, thuộc vị trí các phòng ban cơ sở Cống Quỳnh, shadowing tiếp đón sảnh. | Lead TVV & Mentor | Vượt qua bài kiểm tra sơ đồ phòng khám. |
| **5.2** | Ngày 4-7 (Tuần 1)| Luyện tập Roleplay tiếp đón, vượt qua bài test vấn đáp 7 ngày đầu. | Lead TVV | **Đạt $\ge 80\%$ bài test Ngày 7** (Phụ lục 1). |
| **6.1** | Tuần 2 | Học và thực hành chuẩn hóa Sơ đồ luồng chạy khách (Tiếp đón $\rightarrow$ X-quang $\rightarrow$ Ghế khám $\rightarrow$ Tư vấn). | Lead TVV & Mentor | Không làm rơi khách giữa các phòng ban. |
| **6.2** | Tuần 2 - 4 | Làm chủ 5 thao tác cốt lõi trên phần mềm Remo: Tạo hồ sơ, Check-in, Lịch hẹn, Ghi chú, Hoàn thành. | Lead TVV | 100% ca tư vấn được cập nhật chuẩn xác. |
| **7.1** | Tuần 2 - 3 (Mốc 1)| **Đào tạo Khí cụ & Dịch vụ chuyên sâu:** Implant, Ghép xương, Răng sứ IPS e.max, Chỉnh nha. | Mentor & Lead TVV | **Đạt bài test Mốc 1** (Hiểu sâu vật liệu & ranh giới). |
| **7.2** | Tuần 4 - 5 (Mốc 2)| **Đào tạo Kịch bản Chốt Sales & Roleplay:** 9 phân khúc khách hàng, kỹ thuật xử lý từ chối giá. | Mentor & Lead TVV | **Đạt bài test Mốc 2** (Vượt qua 5 tình huống khó). |
| **7.3** | Tuần 6 - 8 (Mốc 3)| **Thực chiến Độc lập & Bứt phá KPI:** Làm chủ bộ 20 câu từ chối và 5 câu khủng hoảng truyền thông. | TVV Mới | **Đạt bài đánh giá Final $\ge 85/100$ điểm**. |
| **8.1** | Thứ 4 hằng tuần | Họp Review định kỳ 15 - 30 phút: Đánh giá kết quả tuần qua, tháo gỡ điểm nghẽn, giao việc tuần mới. | Lead TVV & Team TVV | Biên bản họp review và hành động cải tiến. |

---

## 3. Rubric Đánh Giá Thái Độ & Tố Chất (Checklist 7 Ngày Đầu - Thang Điểm 1-5)

Lead Consultant đánh giá nhân sự mới vào ngày làm việc thứ 7 theo 5 tiêu chí nền tảng:

| STT | Tiêu Chí Đánh Giá | Mô Tả Hành Vi Đạt Chuẩn (Điểm 5) | Điểm Tối Đa | Điểm Thực Tế |
| :---: | :--- | :--- | :---: | :---: |
| 1 | **Kỷ luật & Tác phong** | Đúng giờ tuyệt đối, đồng phục phẳng phiu, đeo bảng tên, trang điểm tươi tắn, không dùng điện thoại riêng khi làm việc. | 5đ | [ ] / 5 |
| 2 | **Khả năng tiếp thu** | Chủ động ghi chép cẩn thận vào sổ tay, nắm nhanh kiến thức y khoa và thuật ngữ chuyên môn, không để nhắc lại 2 lần. | 5đ | [ ] / 5 |
| 3 | **Tinh thần phụng sự** | Nhiệt tình, niềm nở, chủ động chào hỏi khách hàng trong vòng 5 giây, không ngại hỗ trợ đồng đội khi sảnh đông khách. | 5đ | [ ] / 5 |
| 4 | **Kỹ năng giao tiếp & Thấu cảm** | Giọng nói truyền cảm, rõ ràng, biết lắng nghe chân thành, không ngắt lời khách hàng, biểu cảm tự tin. | 5đ | [ ] / 5 |
| 5 | **Tinh thần đồng đội & Phối hợp** | Tôn trọng Bác sĩ và đồng nghiệp, phối hợp nhịp nhàng với Lễ tân và Phụ tá, tiếp thu tích cực góp ý từ Lead. | 5đ | [ ] / 5 |
| **TỔNG**| **Tổng Điểm Đánh Giá Thái Độ (Yêu cầu đạt $\ge 20/25$ điểm)** | | **25đ** | **[ ] / 25** |

### Quyết định sau 7 ngày đầu:
- **ĐẠT ($\ge 20$ điểm thái độ + $\ge 80\%$ test kiến thức):** Ký hợp đồng thử việc chính thức 2 tháng.
- **KHÔNG ĐẠT:** Dừng hợp tác ngay tại Ngày thứ 7 để tránh lãng phí chi phí đào tạo.

---

## 4. Bảng Tổng Hợp Đánh Giá Final Sau 8 Tuần (Thang Điểm 100)

| STT | Cấu Phần Đánh Giá | Tỷ Trọng | Yêu Cầu Tối Thiểu | Điểm Đạt |
| :---: | :--- | :---: | :---: | :---: |
| 1 | **Kiểm tra Lý thuyết Chuyên môn (Implant, Sứ, Niềng răng)** | 20% | $\ge 18/20$ điểm | [ ] / 20 |
| 2 | **Kỹ năng Thao tác Hệ thống & Phần mềm Remo** | 15% | $\ge 14/15$ điểm | [ ] / 15 |
| 3 | **Thi Thử Roleplay Xử lý Từ chối & Khủng hoảng (Trực tiếp với Lead)** | 25% | $\ge 22/25$ điểm | [ ] / 25 |
| 4 | **Hiệu Suất Thực Tế (Tỷ lệ Chuyển đổi ca tư vấn $\ge 40\%$)** | 25% | $\ge 20/25$ điểm | [ ] / 25 |
| 5 | **Kỷ Luật, Tác Phong & Văn Hóa Phối Hợp Nội Bộ** | 15% | $\ge 14/15$ điểm | [ ] / 15 |
| **TỔNG**| **ĐIỂM TỔNG HỢP SAU 08 TUẦN THỬ VIỆC** | **100%** | **$\ge 85/100$ điểm** | **[ ] / 100** |

> **Quyết định tiếp nhận:** Nhân sự đạt $\ge 85 \text{ điểm}$ và không có lỗi vi phạm nghiêm trọng (Fatal Flaws) sẽ được ký Hợp đồng Lao động chính thức vị trí Tư Vấn Viên Nha Khoa 3C.

