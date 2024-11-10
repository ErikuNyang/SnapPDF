import os
import signal
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file
from werkzeug.utils import secure_filename
from fpdf import FPDF  # Library for generating PDF
from PIL import Image

app = Flask(__name__)

# Set up the image upload folder
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

PREVIEW_PDF_PATH = os.path.join(UPLOAD_FOLDER, 'preview.pdf')    
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check allowed file formats
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for uploading image files
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Retrieve files from request
        files = request.files.getlist('file')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('upload_image'))
    return render_template('index.html', os=os)

# Route for deleting an uploaded image file
@app.route('/delete_image', methods=['POST'])
def delete_image():
    filename = request.form.get('filename')
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify(success=True)
    return jsonify(success=False)

# Route for creating a PDF from uploaded images
@app.route('/create_pdf', methods=['POST'])
def create_pdf():
    image_filenames = request.json.get('filenames')
    
    # Letter size: 8.5 x 11 inches (converted to mm as 215.9 x 279.4 mm)
    page_width, page_height = 215.9, 279.4
    pdf = FPDF(format = 'letter')
    pdf.set_auto_page_break(0)
    total_images = len(image_filenames)

    for index, filename in enumerate(image_filenames):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        with Image.open(file_path) as img:
            img_width, img_height = img.size
            img_width_mm = img_width * 0.264583  # Convert pixels to mm
            img_height_mm = img_height * 0.264583

            # Scale down the image to fit the page if it exceeds page dimensions
            if img_width_mm > page_width or img_height_mm > page_height:
                scale = min(page_width / img_width_mm, page_height / img_height_mm)
                img_width_mm *= scale
                img_height_mm *= scale

            pdf.add_page(format = 'letter')
            pdf.image(file_path, x=0, y=0, w=img_width_mm, h=img_height_mm)

    pdf.output(PREVIEW_PDF_PATH)
    return jsonify({"pdf_url": url_for('preview_pdf')})

# Route for previewing the PDF
@app.route('/preview_pdf')
def preview_pdf():
    return send_file(PREVIEW_PDF_PATH, as_attachment=False)

# Route for deleting the preview PDF
@app.route('/delete_preview', methods=['POST'])
def delete_preview():
    if os.path.exists(PREVIEW_PDF_PATH):
        os.remove(PREVIEW_PDF_PATH)
        return jsonify(success=True)
    return jsonify(success=False)

if __name__ == '__main__':
    app.run(debug=True)
