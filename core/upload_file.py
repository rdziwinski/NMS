from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os


class UploadFile:
    def __init__(self, upload_folder, allowed_extensions):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions

    def upload_file(self):
        if request.method == 'POST':
            if 'file' not in request.files:  # check if the post request has the file part
                statement = 'No file part'
                return statement
            file = request.files['file']
            if file.filename == '':
                statement = 'No selected file'
                return statement
            if not self.allowed_file(file.filename):
                statement = "Illegal extension"
                return statement
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(self.upload_folder, filename))
