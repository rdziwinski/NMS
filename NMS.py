from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from core.upload_file import UploadFile
from core.import_host import ImportHost
from database.host import *
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def admin():
    error = ""
    success = ""
    upload_file = UploadFile('data', ['xlsx', 'jpg', 'txt'])
    if upload_file.upload_file() == 1:
        error = upload_file.print_errors()
    else:
        category = upload_file.print_category()
        file_name = upload_file.print_file_name()
        if file_name == "":
            return render_template('admin.html', name="Administrator")
        import_category = ImportHost(file_name, category)
        if import_category.open_file() == 1:
            error = import_category.print_errors()
            return render_template('admin.html', name="Administrator", error=error)
        import_category.read_file()
        if import_category.is_valid():
            error = "Wrong inside file format"
        elif import_category.is_empty() == 1:
            error = import_category.print_errors()
        else:
            if Host().add(import_category.print_file()) == 1:
                error = 'Add to database failed.'
                return render_template('admin.html', name="Administrator", error=error)
            success = "Import host successful"
    return render_template('admin.html', name="Administrator", error=error, success=success)


if __name__ == '__main__':
    app.run(debug=True)
