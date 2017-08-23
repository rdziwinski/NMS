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
        if request.method == 'POST':  # check if the post request has the file part
            if 'file' not in request.files:
                error = 'No file part'
                # flash('No file part')
                # return redirect(request.url)
                return error
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                error = 'No selected file'
                # flash('No selected file')
                # return redirect(request.url)
                return error
            if not self.allowed_file(file.filename):
                error = "Illegal extension"
                return error
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(self.upload_folder, filename))
