from flask import Flask
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'You want path: %s' % path
@app.route('/foo/<path:path>')
def foo(path):
    return 'You want foo path: %s' % path
if __name__ == '__main__':
    app.run()