from flask import render_template, request, Flask
from core.upload_file import UploadFile
from core.import_host import ImportHost
from core.database import *
from core.check_engine import CheckEngine
from multiprocessing.dummy import Pool as ThreadPool



app = Flask(__name__)

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


@app.route('/show_all', methods=['GET', 'POST'])
def show_all():
    database = Host().get_hosts()
    print(database)

    return render_template('show_all.html', name="Administrator", database=database)


@app.route('/monitoring', methods=['GET', 'POST'])
def monitoring():
    hosts = Host().get_hosts()
    engine = CheckEngine()
    pool = ThreadPool(64)
    result = pool.map(engine.run, hosts)
    return render_template('monitoring.html', name="Administrator", result=result)


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
