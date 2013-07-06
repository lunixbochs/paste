from flask.ext.pymongo import PyMongo
from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for,
)

app = Flask('paste')
mongo = PyMongo(app)


@app.route('/', methods=['GET', 'POST'])
def slash():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        data = request.form.get('data') or request.data
        if data:
            _id = mongo.db.paste.insert({'data': data})
            return redirect('/p/{}.txt'.format(_id))
        else:
            return abort(419)


@app.route('/p/<ObjectId:paste_id>.txt')
def get(paste_id):
    paste = mongo.db.paste.find_one_or_404({'_id': paste_id})
    return paste['data']


if __name__ == '__main__':
    app.run(port=5005)
