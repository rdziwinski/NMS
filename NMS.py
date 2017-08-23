import os
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from flask import send_from_directory

from core.upload_file import *

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'data')


@app.route('/')
def hello_world():
    return 'Hello World!'


# Upload file start
@app.route('/admin', methods=['GET', 'POST'])
def upload_file():
    upload = UploadFile(UPLOAD_FOLDER, ['xlsx', 'jpg', 'txt'])
    result = upload.upload_file()
    return render_template('admin.html', name="Administrator", error=result)

# Upload file end


if __name__ == '__main__':
    app.run(debug=True)
