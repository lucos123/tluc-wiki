---
title: Quy Trình Tư Vấn Lễ Tân - Điều Phối - Tư Vấn Viên
date: 2026-07-26
tags: [quy-trinh, tu-van, le-tan, dieu-phoi, nha-khoa-3c]
source:
  - [[quytrinh_thuviec_tvv_3c]]
---

# QUY TRÌNH TƯ VẤN LỄ TÂN – ĐIỀU PHỐI – TƯ VẤN VIÊN

> **CÔNG TY TNHH TMDV Y TẾ 3C**  
> **Mã tài liệu:** TLTC/BPLT-3C | **Ngày ban hành:** 26/07/2026 | **Lần ban hành:** 01 | **Người lập:** Nguyễn Thị Vân Anh  
> **Tài liệu gốc:** [Quy Trình Đào Tạo, Đánh Giá Thử Việc TVV](./quytrinh_thuviec_tvv_3c.md) (TVV-QT-001)

---

## PHẦN I. MỤC TIÊU

Một tài liệu quy trình chi tiết và rõ ràng cho Lễ tân, Tư vấn viên và Điều phối trong phòng khám nha khoa đóng vai trò vô cùng quan trọng trong việc đảm bảo hoạt động trơn tru, chuyên nghiệp và hiệu quả của phòng khám.

Mục tiêu chính của tài liệu này bao gồm:

### 1. Đảm bảo sự thống nhất trong quy trình làm việc:
- **Tiêu chuẩn hóa các bước:** Mọi nhân viên thực hiện các công việc theo một quy trình thống nhất, tránh sự chồng chéo hoặc thiếu sót.
- **Tăng hiệu quả:** Việc làm theo quy trình giúp tiết kiệm thời gian và công sức, tăng năng suất làm việc.
- **Giảm thiểu sai sót:** Các quy trình rõ ràng giúp giảm thiểu các lỗi không đáng có trong quá trình làm việc.

### 2. Nâng cao chất lượng dịch vụ khách hàng:
- **Tạo ấn tượng tốt:** Quy trình tiếp đón, tư vấn chuyên nghiệp tạo ấn tượng tốt đẹp với khách hàng ngay từ lần đầu đến.
- **Giải quyết thắc mắc nhanh chóng:** Khách hàng được giải đáp mọi thắc mắc một cách nhanh chóng và chính xác.
- **Đảm bảo sự hài lòng:** Khách hàng cảm thấy hài lòng với dịch vụ và có xu hướng quay lại.

### 3. Quản lý hiệu quả các hoạt động:
- **Theo dõi và đánh giá:** Dựa vào quy trình, phòng khám có thể dễ dàng theo dõi và đánh giá hiệu quả công việc của từng nhân viên.
- **Cải tiến liên tục:** Nhờ việc đánh giá, phòng khám có thể đưa ra những điều chỉnh cần thiết để cải thiện quy trình.
- **Đảm bảo chất lượng dịch vụ:** Quy trình giúp đảm bảo chất lượng dịch vụ luôn được duy trì ở mức cao.

### 4. Xây dựng hình ảnh chuyên nghiệp:
- **Thống nhất hình ảnh:** Quy trình làm việc chuyên nghiệp giúp xây dựng hình ảnh thống nhất cho phòng khám.
- **Tăng cường uy tín:** Khách hàng sẽ đánh giá cao sự chuyên nghiệp và tận tâm của phòng khám.

---

## PHẦN II. NỘI DUNG QUY TRÌNH TƯ VẤN

### 1. Mô tả sơ đồ quy trình (Flowchart):

![Sơ đồ Quy trình Tư vấn](./TVV_quytrinhtuvan_v1.png)

```mermaid
graph TD
    Start(["TVV<br>- Tiếp đón KH đến cửa<br>- Xin thông tin"]) --> CheckKhachHang["LT/TVV<br>- Kiểm tra và nắm thông tin<br>xác định KH mới hay cũ"]
    CheckKhachHang --> IsNewKH{"LT/TVV<br>Xác nhận KH"}

    %% Nhánh KH mới
    IsNewKH -- KH mới --> LapHoSo["LT<br>- Lập hồ sơ KH trên Remo"]
    IsNewKH -- KH mới --> NamThongTinMoi["LT<br>- Nắm thông tin, sắp xếp bệnh và gọi điện lên<br>phòng điều trị để chuẩn bị ghế"]
    
    NamThongTinMoi --> ChupPhim{"TVV<br>Chỉ định đưa KH đi chụp phim<br>(hỏi ý kiến KH có đồng ý hay không?)"}

    ChupPhim -- Cần chụp phim để kiểm tra --> KiemTraPhim{"TVV<br>Kiểm tra phim để xem có vấn đề<br>phát sinh không?"}
    
    KiemTraPhim -- Phim có vấn đề, cần tư vấn --> DuaKHLenTuVan["TVV<br>- Đưa KH lên phòng điều trị để<br>tư vấn với bác sĩ chuyên môn"]
    DuaKHLenTuVan --> TuVanChuyenMon["BS (+TVV)<br>- Tư vấn đứng cùng với bác sĩ,<br>tiếp nhận thông tin tư vấn của bác sĩ<br>- Ghi chú lại các vấn đề phát sinh của KH"]
    TuVanChuyenMon --> TuVanLai["TVV<br>- Tư vấn lại giúp cho KH hiểu hơn các dịch vụ<br>cần thiết bác sĩ đã chỉ định<br>- Trao đổi với KH để lựa chọn được dịch vụ phù hợp"]
    TuVanLai --> QuyetDinhDieuTri{"TVV<br>KH quyết định điều trị<br>hay không?"}

    %% Quyết định không đồng ý
    QuyetDinhDieuTri -- Không đồng ý --> TuChoiDieuTri["TVV<br>- Cảm ơn KH<br>- Tiếp tục follow KH bằng Zalo công ty,<br>thuyết phục KH dùng dịch vụ<br>- Nhập những ghi chú và nội dung tư vấn<br>lên Remo để CSKH cùng nắm thông tin"]
    TuChoiDieuTri --> EndTuChoi(["LT<br>- Check 'Hoàn Thành' trên Remo"])

    %% Quyết định đồng ý -> Chuyển sang nút KH điều trị liền hay không
    QuyetDinhDieuTri -- Đồng ý làm dịch vụ --> IsDieuTriLien{"TVV<br>KH điều trị liền<br>hay không?"}
    IsDieuTriLien -- Hẹn lại --> CamOnSauDieuTri
    IsDieuTriLien -- Thực hiện liền --> DuaKHLenDieuTri

    %% Nhánh KH cũ
    IsNewKH -- KH cũ, đang điều trị --> LayHoSo["LT<br>- Lấy hồ sơ bệnh án"]
    IsNewKH -- KH cũ, đang điều trị --> NamThongTinCu["LT<br>- Nắm thông tin, sắp xếp bệnh và gọi điện lên<br>phòng điều trị để chuẩn bị ghế"]

    %% Thực hiện điều trị (từ các nguồn)
    ChupPhim -- Không cần chụp phim --> DuaKHLenDieuTri["TVV<br>- Đưa KH lên phòng điều trị<br>để thực hiện Điều Trị"]
    KiemTraPhim -- Phim không vấn đề --> DuaKHLenDieuTri
    NamThongTinCu --> DuaKHLenDieuTri

    %% Sau điều trị
    DuaKHLenDieuTri --> SauDieuTri["PT (+TVV)<br>- Sau khi điều trị xong PT sẽ đưa KH xuống quầy<br>- TVV tiếp nhận"]
    
    %% Hẹn lại hoặc Sau điều trị -> Cảm ơn & Dặn dò
    SauDieuTri --> CamOnSauDieuTri["TVV<br>- Cảm ơn KH đã sử dụng dịch vụ<br>- Hỏi thăm có đau không, dặn dò, hướng dẫn<br>cách chăm sóc sau điều trị<br>- Nhập những ghi chú hoặc những vấn đề<br>phát sinh của KH lên Remo để CSKH cùng nắm thông tin"]

    %% Xử lý sau khi cảm ơn
    CamOnSauDieuTri --> ThuTien(["LT<br>- Thu tiền gửi hóa đơn, thu tạm ứng (nếu có)<br>- Nhập lịch hẹn"])
    CamOnSauDieuTri --> DanhGiaHaiLong{"TVV<br>Hỏi thăm KH có hài lòng<br>khi vừa điều trị xong?"}

    DanhGiaHaiLong -- Hài lòng --> XinDanhGia["TVV<br>- Xin đánh giá chất lượng<br>trên các nền tảng"]
    DanhGiaHaiLong -- Không hài lòng --> XuLyKhongHaiLong["TVV<br>- Hỏi thăm, động viên, xin lỗi<br>- Xin ý kiến TBP<br>- Gửi quà tặng kèm (voucher CSRM)"]

    XinDanhGia --> EndHoanThanh(["LT<br>- Check 'Hoàn Thành' trên Remo"])
    XuLyKhongHaiLong --> EndHoanThanh
```

### 2. Chú thích sơ đồ:

#### **Biểu tượng ký hiệu**
- **Hình Oval (Bo tròn):** Biểu thị điểm Bắt đầu và Kết thúc quy trình.
- **Hình Chữ nhật:** Biểu thị một Hoạt động / Thao tác xử lý.
- **Hình Thoi:** Biểu thị Điểm ra quyết định (Điều kiện Re-route / Phân nhánh).
- **Mũi tên:** Biểu thị Hướng di chuyển của luồng quy trình.

#### **Ký hiệu viết tắt các Chủ thể & Bộ phận**
- **KH:** Khách Hàng
- **TVV:** Tư Vấn Viên
- **LT:** Lễ Tân
- **CS / CSKH:** Chăm Sóc Khách Hàng
- **ĐP:** Điều Phối
- **BS:** Bác Sĩ
- **PT:** Phụ Tá
- **TBP:** Trưởng Bộ Phận
- **Remo / Nemo:** Phần mềm quản lý nha khoa nội bộ
