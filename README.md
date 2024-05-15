### Giới thiệu về Đồ án: "Sentiment Analysis of Customer Reviews on Tiki"

#### Mục tiêu của Đồ án:
Đồ án "Sentiment Analysis of Customer Reviews on Tiki" nhằm mục tiêu nghiên cứu và phân tích cảm xúc của khách hàng từ các đánh giá sản phẩm trên nền tảng thương mại điện tử Tiki.vn. Thông qua việc sử dụng các công cụ và kỹ thuật hiện đại trong xử lý ngôn ngữ tự nhiên (NLP) và học máy (Machine Learning), dự án này sẽ cung cấp cái nhìn sâu sắc về cảm xúc của người dùng, từ đó giúp doanh nghiệp hiểu rõ hơn về khách hàng của mình.

#### Phương pháp và Công cụ Sử dụng:
1. **Thu thập dữ liệu**:
   - Sử dụng API của Tiki để thu thập dữ liệu đánh giá sản phẩm.
   
2. **Tiền xử lý dữ liệu**:
   - Sử dụng các kỹ thuật xử lý văn bản để làm sạch và chuẩn hóa dữ liệu đánh giá, bao gồm loại bỏ các ký tự đặc biệt, chuẩn hóa từ viết tắt và xử lý lỗi chính tả.
   
3. **Phân tích cảm xúc**:
   - Sử dụng mô hình `PhoBERT` (một biến thể của BERT cho tiếng Việt) để phân loại cảm xúc của từng đánh giá thành các nhãn: tích cực (POS), trung lập (NEU), và tiêu cực (NEG).
   - Mô hình được triển khai thông qua thư viện `transformers` của Hugging Face.

4. **Đánh giá và Trực quan hóa kết quả**:
   - Sử dụng thư viện matplotlib để trực quan hóa kết quả phân tích cảm xúc dưới dạng biểu đồ tròn hoặc biểu đồ thanh.
   - Tổng hợp và báo cáo tỷ lệ các cảm xúc tích cực, trung lập và tiêu cực từ các đánh giá.

#### Kết quả Dự kiến:
Dự án sẽ cung cấp một bảng điều khiển (dashboard) trực quan cho phép người dùng dễ dàng nhận diện và hiểu được phân bố cảm xúc của các đánh giá sản phẩm trên Tiki. Kết quả phân tích sẽ giúp các doanh nghiệp và nhà quản lý sản phẩm trên Tiki:

- Nhận diện các sản phẩm có mức độ hài lòng cao hoặc thấp.
- Phát hiện các vấn đề cần cải thiện từ phản hồi tiêu cực của khách hàng.
- Đưa ra chiến lược kinh doanh và tiếp thị phù hợp dựa trên phân tích cảm xúc của người dùng.

#### Kết luận:
Đồ án "Sentiment Analysis of Customer Reviews on Tiki" không chỉ đóng góp vào việc ứng dụng công nghệ AI và NLP trong phân tích dữ liệu mà còn mang lại giá trị thực tiễn cao cho doanh nghiệp trong việc nâng cao trải nghiệm khách hàng. Bằng cách hiểu rõ hơn về cảm xúc và ý kiến của khách hàng, các doanh nghiệp có thể cải thiện sản phẩm và dịch vụ, từ đó tăng cường sự hài lòng và trung thành của khách hàng.
