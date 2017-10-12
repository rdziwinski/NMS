from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from core.upload_file import UploadFile
from core.import_host import ImportHost
from database.host import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = '123456790'


# # Tymaczasowo modle Host tutaj
# class Host(db.Model):
#     name = db.Column(db.String(30), primary_key=True)  # Deklaracje pol bazy
#     description = db.Column(db.String(255))
#     address = db.Column(db.String(40))
#     snmp_version = db.Column(db.String(2))
#     community = db.Column(db.String(30))
#     security_name = db.Column(db.String(30))
#     security_level = db.Column(db.String(30))
#     auth_protocol = db.Column(db.String(30))
#     priv_key = db.Column(db.String(30))
#     priv_protocol = db.Column(db.String(30))
#     auth_key = db.Column(db.String(30))
#
#     def __init__(self, name="", description="", address="", snmp_version="", community="", security_name="",
#                  security_level="", auth_protocol="", priv_key="", priv_protocol="", auth_key=""):
#         self.name = name
#         self.description = description
#         self.address = address
#         self.snmp_version = snmp_version
#         self.community = community
#         self.security_name = security_name
#         self.security_level = security_level
#         self.auth_protocol = auth_protocol
#         self.priv_key = priv_key
#         self.priv_protocol = priv_protocol
#         self.auth_key = auth_key
#
#     def __repr__(self):
#         return self.name
#
#     def add(self, data):
#         try:
#             db.drop_all()
#             db.create_all()
#             for i in range(1, 4):
#                 host = Host(data[0][i], data[1][i], data[2][i], data[3][i], data[4][i], data[5][i], data[6][i],
#                             data[7][i], data[8][i], data[9][i], data[10][i])
#                 db.session.add(host)
#             db.session.commit()
#         except:
#             return 1


@app.route('/admin', methods=['GET', 'POST'])
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
            if Host().add(import_category.print_file(), category) == 1:
                error = 'Add to database failed.'
                return render_template('upload_file.html', name="Administrator", error=error)
            success = "Import host successful"
    return render_template('upload_file.html', name="Administrator", error=error, success=success)


@app.route('/show_all', methods=['GET', 'POST'])
def show_all():
    database = Host().show_all()
    return render_template('show_all.html', name="Administrator", database=database)

if __name__ == '__main__':
    app.run(debug=True)
