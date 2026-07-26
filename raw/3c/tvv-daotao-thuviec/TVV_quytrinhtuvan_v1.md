# QUY TRÌNH TƯ VẤN 

## LỄ TÂN – ĐIỀU PHỐI – TƯ VẤN VIÊN 

CÔNG TY TNHH TMDV Y TẾ 3C **TLTC/BPLT- 3C** | **Ngày ban hành: 29/09/2024** | **Lần: 1 Người lập: Nguyễn Thị Vân Anh** 

### **PHẦN I. MỤC TIÊU** 

Một tài liệu quy trình chi tiết và rõ ràng cho lễ tân, tư vấn và điều phối trong phòng khám nha khoa đóng vai trò vô cùng quan tr ọng trong việc đảm bảo hoạt động trơn tru, chuyên nghiệp và hiệu quả của phòng khám. 

Mục tiêu chính của tài liệu này bao gồm: 

### **1. Đảm bảo sự thống nhất trong quy trình làm việc:** 

- **Tiêu chuẩn hóa các bước:** Mọi nhân viên thực hiện các công việc theo một quy trình thống nhất, tránh sự chồng chéo hoặc thiếu sót. 

- **Tăng hiệu quả:** Việc làm theo quy trình giúp tiết kiệm thời gian và công sức, tăng năng suất làm việc. 

- **Giảm thiểu sai sót:** Các quy trình rõ ràng giúp giảm thiểu các lỗi không đáng có trong quá trình làm việc. 

### **2. Nâng cao chất lượng dịch vụ khách hàng:** 

- **Tạo ấn tượng tốt:** Quy trình tiếp đón, tư vấn chuyên nghiệp tạo ấn tượng tốt đẹp với khách hàng ngay từ lần đầu đến. 

- **Giải quyết thắc mắc nhanh chóng:** Khách hàng được giải đáp mọi thắc mắc một cách nhanh chóng và chính xác. 

- **Đảm bảo sự hài lòng:** Khách hàng cảm thấy hài lòng với dịch vụ và có xu hướng quay lại. 

### **3. Quản lý hiệu quả các hoạt động:** 

- **Theo dõi và đánh giá:** Dựa vào quy trình, phòng khám có thể dễ dàng theo dõi và đánh giá hiệu quả công việc của từng nhân viên. 

- **Cải tiến liên tục:** Nhờ việc đánh giá, phòng khám có thể đưa ra những điều chỉnh cần thiết để cải thiện quy trình. 

- **Đảm bảo chất lượng dịch vụ:** Quy trình giúp đảm bảo chất lượng dịch vụ luôn được duy trì ở mức cao. 

### **4. Xây dựng hình ảnh chuyên nghiệp:** 

- **Thống nhất hình ảnh:** Quy trình làm việc chuyên nghiệp giúp xây dựng hình ảnh thống nhất cho phòng khám. 

- **Tăng cường uy tín:** Khách hàng sẽ đánh giá cao sự chuyên nghiệp và tận tâm của phòng khám. 

### **PHẦN II. NỘI DUNG QUY TRÌNH TƯ VẤN** 

### **1. Mô tả quy trình:** 

```mermaid
graph TD
    Start(["TVV<br>- Tiếp đón KH đến cửa<br>- Xin thông tin"]) --> CheckKhachHang["LT/CS<br>- Kiểm tra sổ theo tên/SĐT/Mã Thẻ/ID..."]
    CheckKhachHang --> IsNewKH{"LT/CS<br>KH mới hay cũ"}

    %% Nhánh KH mới
    IsNewKH -- KH mới --> LapHoSo["LT<br>- Lập hồ sơ KH trên Nemo"]
    LapHoSo --> NamThongTinMoi["BP<br>- Nắm thông tin, sắp xếp bệnh và gọi điện lên<br>phòng điều trị để chuẩn bị ghế"]
    NamThongTinMoi --> ChupPhim{"BP<br>Chỉ định của KH đi chụp phim<br>(hỏi ý kiến KH có đồng ý chụp không?)"}

    ChupPhim -- Cần chụp phim để kiểm tra --> KiemTraPhim{"BP<br>Kiểm tra phim để xem có vấn đề gì<br>phát sinh không"}
    
    KiemTraPhim -- Phim có vấn đề, cần tư vấn --> DuaKHLenTuVan["TVV<br>- Đưa KH lên phòng điều trị để<br>tư vấn với bác sĩ chuyên môn"]
    DuaKHLenTuVan --> TuVanChuyenMon["BS+TVV<br>- Tư vấn đúng chuyên môn để tiếp nhận<br>thông tin tư vấn của bác sĩ<br>- Ghi chú lại các vấn đề phát sinh của KH"]
    TuVanChuyenMon --> TuVanLai["TVV<br>- Tư vấn lại giúp cho KH hiểu hơn các dịch vụ<br>cần thiết bác sĩ đã chỉ định<br>- Trao đổi với KH để lựa chọn được dịch vụ phù hợp"]
    TuVanLai --> QuyetDinhDieuTri{"TVV<br>KH quyết định điều trị<br>hay không?"}

    QuyetDinhDieuTri -- Không đồng ý --> TuChoiDieuTri["TVV<br>- Cảm ơn KH<br>- Tiếp tục follow KH bằng Zalo công ty,<br>thuyết phục KH dùng dịch vụ<br>- Nhập những ghi chú và nội dung tư vấn<br>lên Nemo để CSKH hằng năm thông tin"]
    TuChoiDieuTri --> EndTuChoi(["BP<br>- Check 'Hoàn Thành' trên Nemo"])

    %% Nhánh KH cũ
    IsNewKH -- KH cũ, đang điều trị --> LayHoSo["LT<br>- Lấy hồ sơ bệnh án"]
    LayHoSo --> NamThongTinCu["BP<br>- Nắm thông tin, sắp xếp bệnh và gọi điện lên<br>phòng điều trị để chuẩn bị ghế"]

    %% Hội tụ vào thực hiện điều trị
    ChupPhim -- Không đồng ý chụp phim --> DuaKHLenDieuTri["TVV<br>- Đưa KH lên phòng điều trị<br>(để thực hiện điều trị)"]
    KiemTraPhim -- Phim không có vấn đề --> DuaKHLenDieuTri
    QuyetDinhDieuTri -- Đồng ý làm dịch vụ --> DuaKHLenDieuTri
    NamThongTinCu --> DuaKHLenDieuTri

    %% Quá trình sau điều trị
    DuaKHLenDieuTri --> SauDieuTri["BS / PT / LT<br>- Sau khi điều trị xong PT sẽ đưa KH xuống quầy<br>- TVV tiếp nhận"]
    
    SauDieuTri --> HoiDieuTriTiep{"TVV<br>KH có điều trị tiếp<br>hay không"}
    HoiDieuTriTiep -- Đồng ý làm dịch vụ --> DuaKHLenDieuTri
    HoiDieuTriTiep -- Không --> CamOnSauDieuTri["TVV<br>- Cảm ơn KH đã sử dụng dịch vụ<br>- Hỏi thăm KH có đau không, dặn dò,<br>hướng dẫn cách chăm sóc sau điều trị<br>- Nhập những ghi chú hoặc những vấn đề<br>phát sinh của KH lên Nemo để CSKH cùng nắm thông tin"]

    %% Xử lý sau khi cảm ơn
    CamOnSauDieuTri --> ThuTien(["LT<br>- Thu tiền, xuất hóa đơn, thu tạm ứng (nếu có)<br>- Nhập lịch hẹn"])
    CamOnSauDieuTri --> DanhGiaHaiLong{"TVV<br>Hỏi thăm KH có hài lòng<br>sau khi điều trị xong?"}

    DanhGiaHaiLong -- Hài lòng --> XinDanhGia["TVV<br>- Xin đánh giá chất lượng<br>trên các nền tảng"]
    DanhGiaHaiLong -- Không hài lòng --> XuLyKhongHaiLong["TVV<br>- Hỏi thăm, động viên, xin lỗi<br>- Xin ý kiến TBP<br>- Gửi quà tặng kèm (voucher CSKH)"]

    XinDanhGia --> EndHoanThanh(["BP<br>- Check 'Hoàn Thành' trên Nemo"])
    XuLyKhongHaiLong --> EndHoanThanh
```

### **2. Chú thích:** 

#### • **Biểu tượng** 

- **Oval** : Biểu thị điểm bắt đầu và kết thúc. 

- **Hình chữ nhật** : Biểu thị một hoạt động. 

- **Hình thoi** : Biểu thị một quyết định. 

- **Mũi tên** : Biểu thị hướng của quy trình. 

#### • **Chủ thể** 

- **KH** : Khách Hàng 

- **TVV** : Tư Vấn Viên 

- **LT** : Lễ Tân 

- **ĐP** : Điều Phối 

- **BS** : Bác Sĩ 

- **PT** : Phụ Tá 

