from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/admin')
def admin():
    return render_template('admin.html', name="Administrator")


if __name__ == '__main__':
    app.run()
