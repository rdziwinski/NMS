from flask import render_template, request
from core.upload_file import UploadFile
from core.import_host import ImportHost
from core.import_service import ImportService
from database.host import *
from database.services import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '123456790'


@app.route('/administrator', methods=['GET', 'POST'])
def admin_hp():
    error = ""
    success = ""
    upload_file = UploadFile('data', ['xlsx', 'jpg', 'txt'])
    if upload_file.upload_file() == 1:
        error = upload_file.print_errors()
    else:
        category = upload_file.print_category()
        file_name = upload_file.print_file_name()

        if file_name == "":
            return render_template('upload_file.html', name="Administrator")

        if category == "Services":
            print("sa serwisy")
            import_services = ImportService(file_name, "Services")
            if import_services.open_file() == 1:
                error = import_services.print_errors()
                return render_template('upload_file.html', name="Administrator", error=error)
            import_services.read_file()
            if import_services.is_valid():
                error = "Wrong inside file format"
            else:
                if Services().add(import_services.print_file()) == 1:
                    error = 'Add to database failed.'
                    return render_template('upload_file.html', name="Administrator", error=error)
                success = "Import services successful"
        else:
            erase = request.form.getlist('erase')
            import_category = ImportHost(file_name, category)
            if import_category.open_file() == 1:
                error = import_category.print_errors()
                return render_template('upload_file.html', name="Administrator", error=error)
            import_category.read_file()
            if import_category.is_valid():
                error = "Wrong inside file format"
            elif import_category.is_empty() == 1:
                error = import_category.print_errors()
            else:
                if Host().add(import_category.print_file(), category, erase) == 1:
                    error = 'Add to database failed.'
                    return render_template('upload_file.html', name="Administrator", error=error)
                success = "Import host successful"
    return render_template('upload_file.html', name="Administrator", error=error, success=success)


def print_database(database_name):
    database = []
    if database_name == "Hosts":
        database = Host().show_all()
    elif database_name == "Services":
        database = Services().show_category()
    return database


@app.route('/show_all', methods=['GET', 'POST'])
def show_all():
    database = print_database("Hosts")
    print(database)
    return render_template('show_all.html', name="Administrator", database=database)


@app.route('/show_category', methods=['GET', 'POST'])
def show_category():
    database = print_database("Services")
    print(database)
    return render_template('show_category.html', name="Administrator", database=database)


@app.route('/monitoring', methods=['GET', 'POST'])
def monitoring():
    return render_template('monitoring.html', name="Administrator")


if __name__ == '__main__':
    app.run(debug=True)
