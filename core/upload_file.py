from flask import request
from werkzeug.utils import secure_filename
import os


class UploadFile:
    def __init__(self, upload_folder, allowed_extensions):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions

    def is_allowed(self, file_name):
        return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def upload_file(self):
        self.file_name = ""
        self.category = ""
        self.error = ""
        if request.method == 'POST':
            if 'file' not in request.files:  # check if the post request has the file part
                self.error = "No file part"
                return 1
            file = request.files['file']
            if file.filename == '':
                self.error = "No selected file"
                return 1
            if not self.is_allowed(file.filename):
                self.error = "Illegal extension"
                return 1
            if file:
                app_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ''))
                self.upload_folder = os.path.join(app_root, self.upload_folder)

                filename = secure_filename(file.filename)
                file.save(os.path.join(self.upload_folder, filename))
                self.file_name = filename
                self.category = request.form['category']

    def print_errors(self):
        return self.error

    def print_file_name(self):
        return self.file_name

    def print_category(self):
        return self.category
