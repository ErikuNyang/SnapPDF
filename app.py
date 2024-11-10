import os
import signal
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename
from fpdf import FPDF  # PDF 생성을 위한 라이브러리 추가

app = Flask(__name__)

# 이미지 업로드 폴더 설정
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

PREVIEW_PDF_PATH = os.path.join(UPLOAD_FOLDER, 'preview.pdf')    
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 허용된 파일 형식 확인 함수
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 사진 파일 업로드 라우트
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # 파일을 요청에서 가져옴
        files = request.files.getlist('file')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('upload_image'))
    return render_template('index.html', os=os)

# 잘못올린 사진 삭제 라우트
@app.route('/delete_image', methods=['POST'])
def delete_image():
    filename = request.form.get('filename')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify(success=True)
    return jsonify(success=False)

# PDF 생성 라우트
@app.route('/create_pdf', methods=['POST'])
def create_pdf():
    image_filenames = request.json.get('filenames')
    pdf = FPDF()
    pdf.set_auto_page_break(0)

    for filename in image_filenames:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        pdf.add_page()
        pdf.image(file_path, x=10, y=10, w=190)  # 이미지 크기와 위치 조정 가능

    pdf.output(PREVIEW_PDF_PATH)
    return jsonify({"pdf_url": url_for('preview_pdf')})

# PDF 미리보기 라우트
@app.route('/preview_pdf')
def preview_pdf():
    return send_file(PREVIEW_PDF_PATH, as_attachment=False)

# 미리보기 PDF 삭제 라우트
@app.route('/delete_preview', methods=['POST'])
def delete_preview():
    if os.path.exists(PREVIEW_PDF_PATH):
        os.remove(PREVIEW_PDF_PATH)
        return jsonify(success=True)
    return jsonify(success=False)


if __name__ == '__main__':
    app.run(debug=True)