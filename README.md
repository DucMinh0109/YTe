# Ứng Dụng Dự Đoán Bệnh Lý

Dự án này là một ứng dụng web được xây dựng bằng **Flask** và **Dash** cho phép người dùng nhập triệu chứng và dự đoán các bệnh lý có thể xảy ra dựa trên triệu chứng đó. Ứng dụng sử dụng các kỹ thuật học máy và dữ liệu được thu thập từ trang web **YouMed**.

## Cấu Trúc Dự Án
Dự án bao gồm các tệp sau:

### 1. `app.py`
Đây là tệp ứng dụng web chính sử dụng Flask. Nó cung cấp giao diện người dùng để người dùng nhập triệu chứng và nhận dự đoán về bệnh. Ứng dụng sẽ trả về các bệnh lý có thể có kèm theo xác suất của từng bệnh dựa trên triệu chứng đã nhập.

### 2. `convert_to_word.py`
Script này dùng để chuyển đổi dữ liệu bệnh (từ tệp `disease_data.docx`) thành tệp CSV (`disease_data.csv`). Tệp CSV chứa tên bệnh và các triệu chứng liên quan, được sử dụng để huấn luyện mô hình học máy.

### 3. `disease_crawled.docx`
Tệp tài liệu Word này chứa danh sách hơn 700 bệnh với các liên kết và thông tin thu thập từ trang web **YouMed**. Nó bao gồm các thông tin về tên bệnh, triệu chứng, nguyên nhân, phương pháp phòng ngừa và điều trị.

### 4. `disease_crawl.py`
Script này dùng để thu thập liên kết tới hơn 700 trang bệnh trên website **YouMed**. Nó quét trang web để lấy dữ liệu liên quan đến các bệnh và tạo ra danh sách các liên kết bệnh.

### 5. `disease_data_crawled.py`
Script này thu thập thông tin chi tiết từ các liên kết bệnh trong `disease_crawled.docx`. Nó thu thập các thông tin chi tiết về từng bệnh như triệu chứng, nguyên nhân, điều trị, phòng ngừa và lưu trữ kết quả dưới dạng cấu trúc dữ liệu.

### 6. `disease_data.csv`
Tệp CSV này chứa dữ liệu bệnh đã được xử lý và làm sạch. Mỗi dòng trong tệp đại diện cho một bệnh với các triệu chứng của bệnh. Dữ liệu này được sử dụng để huấn luyện mô hình học máy trong ứng dụng.

### 7. `disease_data.docx`
Tệp tài liệu Word này chứa dữ liệu bệnh dưới dạng dễ đọc. Nó được sử dụng làm nguồn dữ liệu cho `convert_to_word.py`.

### 8. `index.html`
Tệp HTML này là giao diện chính của ứng dụng web. Người dùng sẽ nhập triệu chứng vào trong biểu mẫu và nhận kết quả dự đoán về các bệnh có thể có. Tệp HTML này sử dụng **Bootstrap** để tạo giao diện người dùng thân thiện và dễ sử dụng. Các kết quả dự đoán sẽ được hiển thị dưới dạng bảng, bao gồm tên bệnh, xác suất, triệu chứng, nguyên nhân, phương pháp phòng ngừa và điều trị.

## Cài Đặt
Cài đặt các thư viện phụ thuộc: Bạn có thể cài đặt các thư viện cần thiết bằng pip:
pip install flask python-docx scikit-learn dash plotly requests beautifulsoup4

Chạy ứng dụng: Để chạy ứng dụng web Flask, bạn chỉ cần chạy lệnh sau:
python app.py
Ứng dụng sẽ chạy trên địa chỉ http://127.0.0.1:5000/.

Cách Sử Dụng
Dự đoán bệnh:

Mở ứng dụng web trong trình duyệt của bạn.
Nhập các triệu chứng bạn gặp phải vào biểu mẫu (các triệu chứng cách nhau bằng dấu phẩy).
Ứng dụng sẽ hiển thị danh sách các bệnh có thể có và xác suất của mỗi bệnh.
Thu thập dữ liệu bệnh:

Nếu bạn cần làm mới hoặc cập nhật dữ liệu bệnh:
Chạy disease_crawl.py để thu thập các liên kết tới các trang bệnh.
Sau đó, chạy disease_data_crawled.py để thu thập thông tin chi tiết về các bệnh.
