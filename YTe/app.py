from flask import Flask, render_template, request
from docx import Document
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
import dash
from dash import html, dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output

'''
Dùng để khởi tạo 1 trang web flask, __name__ ở đây là tên của module hiện tại (file .py)
'''
app = Flask(__name__)


def read_data_from_word(file_path):  # Đầu vào là tên file
    try:  # Dùng try để kiểm tra xem có lỗi không, nếu có lỗi xảy ra nhả đến khối excespt để xử lý
        if not os.path.exists(file_path):
            '''
os.path.exists(file_path) là một hàm trong module os của Python, dùng để kiểm tra xem một tệp hoặc thư mục có tồn tại hay không tại đường dẫn file_path.
Nếu tệp hoặc thư mục tồn tại, nó trả về True.
Nếu không tồn tại, nó trả về False.

raise là một từ khóa trong Python dùng để tạo ra (raise) một ngoại lệ (exception).
Trong trường hợp này, raise FileNotFoundError(...) tạo ra một ngoại lệ kiểu FileNotFoundError (lỗi không tìm thấy tệp).
FileNotFoundError là một ngoại lệ đã được định nghĩa sẵn trong Python và được sử dụng khi tệp không được tìm thấy.
Thông báo lỗi được cung cấp cho ngoại lệ này thông qua f-string: f"File không tồn tại: {file_path}". F-string sẽ giúp tạo một chuỗi thông báo lỗi có chứa giá trị của file_path (đường dẫn tệp bị thiếu).

Khi ngoại lệ FileNotFoundError được ném ra, chương trình sẽ dừng lại và chuyển sang xử lý trong khối except
            '''
            raise FileNotFoundError(f"File không tồn tại: {file_path}")

        doc = Document(
            file_path)  # Document là 1 lớp trong thư viện python-docx dùng để làm việc với các tài liệu Word(.docx)
        # Ở đây, ta khởi tạo một đối tượng Document từ tệp Word có đường dẫn là file_path
        data = []  # Tạo list trống
        current_disease = {}  # Tạo từ điển trống

        for paragraph in doc.paragraphs:  # Duyệt qua từng đoạn văn trong Word
            text = paragraph.text.strip()  # Lấy thuộc tính text của paragraph (nội dung của đoạn văn), strip() để loại bỏ khoảng trắng ở đầu và cuối chuỗi (nếu có)
            if text.startswith(
                    "Tên bệnh:"):  # Dùng phương thức startswith của đối tượng chuỗi để xem nó có bắt đầu bằng "Tên bệnh:" hay không?
                if current_disease:
                    data.append(current_disease)
                '''
                if current_disease:              
                    data.append(current_disease)
                để phục vụ cho lần lặp tiếp theo, nó sẽ thêm bệnh trước vào từ điển
                '''
                '''
                bổ sung phần tử vào từ điển current_disease, key là "Disease", value là text.replace("Tên bệnh:", "")
                Giải thích value như sau: ví dụ text như sau: "Tên bệnh: Cảm cúm" thì value sẽ là "Cảm cúm"

                Những dòng mã nguồn sau trong vòng for này đều có cách giải thích gần tương tự
                '''
                current_disease = {"Disease": text.replace("Tên bệnh:", "").strip()}
            elif text.startswith("Triệu chứng:"):
                current_disease["Symptoms"] = text.replace("Triệu chứng:", "").strip()
            elif text.startswith("Nguyên nhân phỏng đoán:"):
                current_disease["Cause"] = text.replace("Nguyên nhân phỏng đoán:", "").strip()
            elif text.startswith("Phòng ngừa:"):
                current_disease["Prevention"] = text.replace("Phòng ngừa:", "").strip()
            elif text.startswith("Điều trị:"):
                current_disease["Treatment"] = text.replace("Điều trị:", "").strip()

        if current_disease:
            data.append(current_disease)
        '''
        if current_disease:
            data.append(current_disease)
        Để phục vụ thêm bệnh cuối cùng vào từ điển
        '''
        return data
        '''
        Trả về data là 1 list chứa các current_disease hay nói cách khác,
        là 1 list chứa các bệnh.
        '''
    except Exception as e:  # Ngoại lệ, đi đôi với try ở trên
        print(f"Error reading Word file: {e}")
        return []


# Chuẩn bị dữ liệu huấn luyện
'''
Hàm prepare_data nhận vào 1 list chứa các bệnh
'''


def prepare_data(disease_data):
    # Chuyển triệu chứng thành vector
    vectorizer = CountVectorizer()  # Tạo đối tượng CountVectorizer của thư viện scikit-learn

    symptoms_list = [disease["Symptoms"] for disease in disease_data]
    '''
    Như đã nói ở trên disease_data là 1 danh sách gôm các bệnh (từ điển),
    symptoms_list ở đây là dùng để tạo 1 danh sách gồm các phần tử là các triệu chứng của từng bệnh
    '''
    X = vectorizer.fit_transform(symptoms_list).toarray()  # Vector hóa triệu chứng
    '''
    fit_tranform là để biến symtoms_list thành 1 ma trận tần suất, còn ma trận tần xuất là gì thì xem giải thích dưới đây:

    Ví dụ:
    Giả sử bạn có ba câu văn bản:
    documents = [
        "I love programming",
        "Python is great for programming",
        "I love Python"
    ]
    Khi bạn áp dụng CountVectorizer() vào bộ dữ liệu này:
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(documents)

    Bước 1: Tạo từ điển (vocabulary)
    CountVectorizer sẽ tạo ra một từ điển (vocabulary) gồm tất cả các từ xuất hiện trong các câu văn bản. Trong trường hợp này, từ điển có thể trông như sau:

    {
        'i': 0,
        'love': 1,
        'programming': 2,
        'python': 3,
        'is': 4,
        'great': 5,
        'for': 6
    }
    Bước 2: Biến đổi văn bản thành vector
        Sau khi xây dựng từ điển, CountVectorizer sẽ chuyển mỗi câu thành một vector, trong đó mỗi giá trị đại diện cho số lần xuất hiện của từ trong từ điển. Ví dụ:

        Câu "I love programming" sẽ trở thành:
        [1, 1, 1, 0, 0, 0, 0]
        (tức là từ "i" xuất hiện 1 lần, từ "love" xuất hiện 1 lần, từ "programming" xuất hiện 1 lần, còn các từ khác không xuất hiện)

        Câu "Python is great for programming" sẽ trở thành:
        [0, 0, 1, 1, 1, 1, 1]

        Câu "I love Python" sẽ trở thành:
        [1, 1, 0, 1, 0, 0, 0]

    Kết quả là một ma trận tần suất như sau (mỗi dòng là vector đại diện cho một câu):

    [
      [1, 1, 1, 0, 0, 0, 0],  # Câu "I love programming"
      [0, 0, 1, 1, 1, 1, 1],  # Câu "Python is great for programming"
      [1, 1, 0, 1, 0, 0, 0]   # Câu "I love Python"
    ]
    '''
    y = [disease["Disease"] for disease in disease_data]  # Nhãn là tên bệnh
    return X, y, vectorizer
    '''
    Kết quả là hàm này sẽ trả về tên bệnh + ma trận tần xuất của triệu chứng của bệnh + vectorrizer
    '''


# Hàm tính phần trăm xác suất dựa trên triệu chứng khớpc
'''
Hàm nhận vào input_symptons (list mà mỗi phần tưt là triệu chứng mà người dùng nhập vào)
và nhận vào disease_symptons (list mà mỗi phần tử là triệu chứng của từng bệnh trong cơ sở dữ liệu của nhóm)
'''


def calculate_probability(input_symptoms, disease_symptoms):
    matched_symptoms = [sym for sym in input_symptoms if sym in disease_symptoms]
    '''
    matched_symptons là list chứa các triệu chứng mà người dùng nhập vào và
    nó trùng với triệu chứng trong disease_symptoms hay triệu chứng của 1 bệnh
    '''

    matched_count = len(matched_symptoms)  # Tổng số triệu chứng trùng khớp
    total_symptoms = len(disease_symptoms)  # Tổng số triệu chứng của 1 bệnh

    # Cộng 10% cho 5 triệu chứng đầu tiên
    probability = 0
    for i in range(min(matched_count, 5)):
        probability += 10

    # Cộng phần còn lại với 80% chia đều cho các triệu chứng
    if matched_count > 5:
        remaining_probability = 80  # Đã cộng 50% cho 5 triệu chứng đầu tiên
        additional_probability_per_symptom = remaining_probability / total_symptoms
        for i in range(5, matched_count):
            probability += additional_probability_per_symptom

    # Đảm bảo tổng xác suất không vượt quá 80%
    return min(probability, 80)


# Hàm tính khoảng cách Euclidean
def calculate_knn_distance(input_symptom, disease_symptom, vectorizer, disease):
    # Chuyển triệu chứng thành vector (sử dụng CountVectorizer đã huấn luyện)
    '''
    Biến đổi triệu chứng người dùng nhập vào và triệu chứng của 1 bệnh thành vector số
    '''
    input_vector = vectorizer.transform([input_symptom]).toarray()
    disease_vector = vectorizer.transform([disease_symptom]).toarray()

    # Tính khoảng cách Euclidean giữa 2 vector triệu chứng
    distance = euclidean_distances(input_vector, disease_vector)[0][0]

    # In ra khoảng cách giữa triệu chứng người dùng và triệu chứng bệnh
    print(f"Khoảng cách giữa triệu chứng nhập vào và triệu chứng bệnh: {distance}, {disease}")
    return distance


def search_diseases_by_symptom(input_symptom):
    input_symptoms = [sym.strip().lower() for sym in input_symptom.split(",")]

    results = []

    for disease in disease_data:
        disease_symptoms = [sym.strip().lower() for sym in disease["Symptoms"].split(",")]

        # Tính xác suất của triệu chứng khớp
        probability = calculate_probability(input_symptoms, disease_symptoms)

        # Dự đoán bệnh bằng KNN (sử dụng khoảng cách Euclidean thay vì KNN trực tiếp)
        distance = calculate_knn_distance(input_symptom, disease["Symptoms"], vectorizer, disease)

        # Thêm kết quả vào danh sách nếu xác suất > 0
        if probability > 0:
            results.append({
                "Disease": disease["Disease"],
                "Probability": round(probability, 2),  # Làm tròn đến 2 chữ số thập phân
                "Matched Symptoms": ", ".join([sym for sym in input_symptoms if sym in disease_symptoms]),
                "Symptoms": disease["Symptoms"],
                "Cause": disease.get("Cause", "Không có thông tin"),
                "Prevention": disease.get("Prevention", "Không có thông tin"),
                "Treatment": disease.get("Treatment", "Không có thông tin"),
                "Distance": round(distance, 2),  # Khoảng cách ban đầu
            })

    # Trừ đi khoảng cách của từng phần tử trong results / 1000
    for result in results:
        result["Probability"] -= result["Distance"] / 100  # Trừ đi 1 phần 1000 của khoảng cách

    # Sắp xếp kết quả theo xác suất giảm dần. Nếu xác suất bằng nhau, sắp xếp theo khoảng cách tăng dần
    results.sort(key=lambda x: (-x["Probability"], x["Distance"]))

    return results[:10]


@app.route("/")
def home():
    return render_template("index.html", diseases=disease_data)
'''
Đây là một view function (hàm xử lý yêu cầu từ phía người dùng) trong Flask. 
Mỗi route trong Flask sẽ được liên kết với một hàm xử lý yêu cầu HTTP.
return render_template("index.html", diseases=disease_data)
render_template("index.html", ...) là một hàm trong Flask
 dùng để render (hiển thị) một trang HTML. Trang HTML này được lưu trữ trong thư mục templates của dự án.
"index.html": Là tên của file HTML mà Flask sẽ render. 
Đây là giao diện trang chủ của ứng dụng.
diseases=disease_data: Đây là một tham số được truyền từ hàm Python vào trong template HTML. 
Trong đó, disease_data là một biến chứa thông tin về các bệnh (danh sách các bệnh lý, triệu chứng, nguyên nhân, phương pháp phòng ngừa, điều trị, v.v.).
'''

# Route dự đoán
@app.route("/predict", methods=["POST"])
#Đây là hàm xử lý yêu cầu POST khi người dùng gửi dữ liệu triệu chứng. Flask sẽ gọi hàm này khi người dùng truy cập vào URL /predict với yêu cầu POST.
def predict():
    global latest_results
    try:
        symptoms = request.form.get("symptoms", "").lower().strip()
        '''
        Đây là cách flask lấy dữ liệu từ form gửi lên. Phương thức request.form cho phép truy cập vào dữ liệu
        từ các trường trong form html
        '''
        if not symptoms: #Nếu chuỗi rỗng, trả về thông báo lỗi cho người dùng yêu cầu họ nhập triệu chứng
            return render_template("index.html", message="Vui lòng nhập triệu chứng.")

        results = search_diseases_by_symptom(symptoms)
        latest_results = results

        '''
        Sau khi tìm được kết quả, hàm này sẽ render lại trang index.html và truyền các tham số sau vào
        '''
        return render_template("index.html", diseases=disease_data, results=results, input_symptoms=symptoms)


    except Exception as e:
        print(f"Error during prediction: {e}")
        return render_template("index.html", message="Đã xảy ra lỗi, vui lòng thử lại.")
    '''
    Nếu trong quá trình dự đoán có lỗi xảy ra (ví dụ: dữ liệu không hợp lệ, lỗi tính toán, hoặc bất kỳ lỗi nào khác), phần except sẽ được thực thi.
    '''


# Khởi tạo Dash app
dash_app = dash.Dash(
    __name__,
    server=app,
    url_base_pathname='/dash/',
    external_stylesheets=['https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css']
)

# Layout cho Dash app
dash_app.layout = html.Div([
    html.H1("Biểu đồ trực quan", style={'textAlign': 'center', 'color': '#58a6ff'}),
    dcc.Graph(id='probability-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # Cập nhật mỗi giây
        n_intervals=0
    )
], style={'backgroundColor': '#0d1117', 'padding': '20px'})

# Biến toàn cục để lưu kết quả dự đoán mới nhất
latest_results = []

# Callback để cập nhật biểu đồ
@dash_app.callback(
    Output('probability-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    global latest_results
    if not latest_results:
        return {
            'data': [],
            'layout': go.Layout(
                title='Phần Trăm Xác Suất Các Bệnh',
                xaxis={'title': ''},
                yaxis={'title': 'Xác Suất (%)'},
                plot_bgcolor='#0d1117',
                paper_bgcolor='#0d1117',
                font={'color': '#c9d1d9'}
            )
        }

    diseases = [result["Disease"] for result in latest_results]
    probabilities = [result["Probability"] for result in latest_results]

    figure = {
        'data': [
            go.Bar(
                x=diseases,
                y=probabilities,
                marker=dict(color='rgb(88, 166, 255)')
            )
        ],
        'layout': go.Layout(
            title='Phần Trăm Xác Suất Các Bệnh',
            xaxis={'title': ' '},
            yaxis={'title': 'Xác Suất (%)'},
            plot_bgcolor='#0d1117',
            paper_bgcolor='#0d1117',
            font={'color': '#c9d1d9'},
            hovermode='closest'
        )
    }

    return figure

# Chạy ứng dụng Flask
if __name__ == "__main__":
    # Load dữ liệu bệnh
    disease_data = read_data_from_word("disease_data.docx")
    # Chuẩn bị dữ liệu huấn luyện
    X_train, y_train, vectorizer = prepare_data(disease_data)

    # Khởi tạo kết quả mới nhất
    latest_results = []

    app.run(debug=True)
