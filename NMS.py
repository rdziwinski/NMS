from flask import render_template, request, Flask

from core.import_host import ImportHost
from core.settings import *
from core.show_host import *
from core.upload_file import UploadFile

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def show_states_all():
    all_states = ShowStatus()
    database = all_states.run(1)
    if database[0] == 0:
        return render_template('show_services.html', name="Home")

    return render_template('show_states_all.html', name="Home", database=database)



@app.route('/settings', methods=['GET', 'POST'])
def admin_hp():
    error = ""
    success = ""
    upload_file = UploadFile('data', ['xlsx', 'jpg', 'txt'])
    path = os.path.dirname(os.path.abspath(__file__)) + "/data/services.json"
    settings = FIleJson(path)
    current_settings = settings.read_file()

    if 'file' not in request.files:
        new_settings = []
        new_settings.extend(request.form.getlist('key'))
        new_settings.extend(request.form.getlist('warning'))
        new_settings.extend(request.form.getlist('critical'))
        if new_settings:
            settings = Settings()
            data = settings.set_setting(current_settings, new_settings)
            with open(path, 'w') as f:
                json.dump(data, f)
            success = "Change settings successfully"
        return render_template('settings.html', name="Administrator", current_settings=current_settings, success=success)


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
            return render_template('settings.html', name="Administrator", error=error, current_settings=current_settings)
        import_category.read_file()
        if import_category.is_valid():
            error = "Wrong inside file format"
        elif import_category.is_empty() == 1:
            error = import_category.print_errors()
        else:
            if DatabaseEngine().add_host(import_category.print_file(), category, erase) == 1:
                error = 'Add to database failed.'
                return render_template('settings.html', name="Administrator", error=error, current_settings=current_settings)
            success = "Import host successful"

    return render_template('settings.html', name="Administrator", error=error, success=success, current_settings=current_settings)



@app.route('/show_all', methods=['GET', 'POST'])
def show_all():
    database = DatabaseEngine().get_hosts()
    #print(database)
    return render_template('show_all.html', name="Hosts", database=database)


@app.route('/show_services', methods=['GET', 'POST'])
def show_services():
    database = DatabaseEngine().get_checks()
    #print(database)
    return render_template('show_services.html', name="Checks", database=database)

@app.route('/show_states_problems', methods=['GET', 'POST'])
def show_states_problems():
    all_states = ShowStatus()
    database = all_states.run(0)
    if database[0] == 0:
        return render_template('show_services.html', name="Home")

    return render_template('show_states_all.html', name="Home", database=database)


@app.route('/host/<id>', methods=['GET', 'POST'])
def show_host(id):
    show = ShowHost()
    show2 = ShowStatus()
    host_data = show.get_data(id)
    if host_data[3][2] != '2':
        services = show2.get_host_services(id, 1)

        if request.form.getlist('get_interfaces'):
            interfaces = show.get_interfaces(id)
            return render_template('show_host.html', name="Host", host_data=host_data, interfaces=interfaces,
                                   services=services)
        return render_template('show_host.html', name="Host", host_data=host_data, services=services)
    return render_template('show_host.html', name="Host", host_data=host_data, down=1)





if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')