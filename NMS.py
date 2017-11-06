from multiprocessing.dummy import Pool as ThreadPool

from flask import render_template, request, Flask

from core.check_engine import CheckEngine
from core.database_engine import *
from core.import_host import ImportHost
from core.upload_file import UploadFile
from core.show_status import *
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
            if Database().add_host(import_category.print_file(), category, erase) == 1:
                error = 'Add to database failed.'
                return render_template('upload_file.html', name="Administrator", error=error)
            success = "Import host successful"
    return render_template('upload_file.html', name="Administrator", error=error, success=success)


@app.route('/show_all', methods=['GET', 'POST'])
def show_all():
    database = Database().get_hosts()
    #print(database)
    return render_template('show_all.html', name="Administrator", database=database)


@app.route('/show_services', methods=['GET', 'POST'])
def show_services():
    database = Database().show_services()
    #print(database)
    return render_template('show_services.html', name="Administrator", database=database)


@app.route('/monitoring', methods=['GET', 'POST'])
def monitoring():
    engine = CheckEngine()
    hosts = Database().get_hosts()
    #print(hosts)
    pool = ThreadPool(32)
    result = pool.map(engine.run, hosts)
   # Base.metadata.drop_all(engine)
    return render_template('monitoring.html', name="Administrator", result=result)


@app.route('/show_states_all', methods=['GET', 'POST'])
def show_states_all():
    all_states = ShowStatus()
    database = all_states.get_states()
    return render_template('show_states_all.html', name="Administrator", database=database)


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
