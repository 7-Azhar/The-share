from flask import Flask, flash, redirect, render_template, request, send_from_directory, url_for
import os
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SECRET_KEY'] = 'your_secret_key'

# Ensure the upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# Home route to render the frontend
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'myfile' not in request.files:
        flash('No file part')
        return redirect(request.url)

    files = request.files.getlist('myfile')
    file_codes = []

    for file in files:
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Generate a unique numeric code for the file
        unique_code = str(random.randint(
            10000000, 99999999))  # Generates an 8-digit numeric code
        file_name = unique_code + "_" + file.filename if file.filename else unique_code
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        file_codes.append(unique_code)

    return render_template('upload_success.html', file_codes=file_codes)


# Route to handle file downloads via form submission
@app.route('/download', methods=['POST'])
def download_file():
    code = request.form.get('code')

    if not code:
        flash('Please enter a code')
        return redirect(url_for('index'))

    # Find the file that matches the code
    for file_name in os.listdir(app.config['UPLOAD_FOLDER']):
        if file_name.startswith(code):
            return send_from_directory(app.config['UPLOAD_FOLDER'],
                                       file_name,
                                       as_attachment=True)

    flash('Invalid code or file not found')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
