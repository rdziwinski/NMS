from flask import render_template, request, Flask, redirect, url_for
from sqlalchemy.exc import OperationalError
from core.import_host import ImportHost
from core.run_engine import *
from core.show_host import *
from core.upload_file import UploadFile

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hosts_states():
    try:
        all_states = ShowStatus()
        database = all_states.run(0)
    except OperationalError:
        return redirect(url_for('settings'))
    except AttributeError:
        return render_template('hosts_states.html', name="Home")
    return render_template('hosts_states.html', name="Home", database=database)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    error = ""
    success = ""
    upload_file = UploadFile('data', ['xlsx', 'jpg', 'txt'])
    path = os.path.dirname(os.path.abspath(__file__)) + "/data/parameters.json"
    settings = Settings(path)
    current_settings = settings.read_file()
    if 'file' not in request.files:
        new_settings = []
        new_settings.extend(request.form.getlist('key'))
        new_settings.extend(request.form.getlist('warning'))
        new_settings.extend(request.form.getlist('critical'))
        if new_settings:
            success = settings.write_file(path, settings.set_setting(current_settings, new_settings))
        return render_template('settings.html', name="Administrator", current_settings=current_settings,
                               success=success)
    if upload_file.upload_file() == 1:
        error = upload_file.print_errors()
    else:
        category = upload_file.print_category()
        file_name = upload_file.print_file_name()
        if file_name == "":
            return render_template('settings.html', name="Administrator", current_settings=current_settings)
        erase = request.form.getlist('erase')
        import_category = ImportHost(file_name, category)
        if import_category.open_file() == 1:
            error = import_category.print_errors()
            return render_template('settings.html', name="Administrator",
                                   error=error, current_settings=current_settings)
        import_category.read_file()
        if import_category.is_valid():
            error = "Wrong inside file format"
        elif import_category.is_empty() == 1:
            error = import_category.print_errors()
        else:
            if DatabaseEngine().add_host(import_category.print_file(), category, erase) == 1:
                error = 'Add to database failed.'
                return render_template('settings.html', name="Administrator",
                                       error=error, current_settings=current_settings)
            success = "Import host successful"
    return render_template('settings.html', name="Administrator", error=error,
                           success=success, current_settings=current_settings)


@app.route('/hosts', methods=['GET'])
def hosts():
    database = DatabaseEngine().get_hosts()
    return render_template('hosts.html', name="Hosts", database=database)


@app.route('/checks', methods=['GET'])
def checks():
    database = DatabaseEngine().get_checks()
    return render_template('checks.html', name="Checks", database=database)


@app.route('/problems', methods=['GET'])
def problems():
    try:
        all_states = ShowStatus()
        database = all_states.run(1)
        if database[0] == 0:
            return redirect(url_for('settings'))
        return render_template('hosts_states.html', name="Home", database=database)
    except AttributeError:
        return render_template('hosts_states.html', name="Home")


@app.route('/host/<id>', methods=['GET', 'POST'])
def host(id):
    host = ShowHost()
    parameters = ShowStatus()
    host_data = host.get_data(id)
    if host_data[3][2] != '2':
        parameters = parameters.get_host_parameters(id, 0)
        if request.form.getlist('get_interfaces'):
            interfaces = host.get_interfaces(id)
            return render_template('host.html', name="Host", host_data=host_data, interfaces=interfaces,
                                   parameters=parameters)
        return render_template('host.html', name="Host", host_data=host_data, parameters=parameters)
    return render_template('host.html', name="Host", host_data=host_data, down=1)


if __name__ == '__main__':
    RunEngine(60)
    app.run(debug=True, port=80, host='0.0.0.0')
