from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)


@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory('./static', path)


@app.route('/')
@app.route('/constructor')
def hello_world():
    return send_from_directory('./templates', 'index.html')


if __name__ == '__main__':
    app.run()
