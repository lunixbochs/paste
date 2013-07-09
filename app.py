from flask.ext.pymongo import PyMongo
from flask.ext.shorturl import ShortUrl
from flask import Flask, Response, abort, redirect, render_template, request

app = Flask('paste')
mongo = PyMongo(app)
surl = ShortUrl(app)


def next_id():
    return mongo.db.auto_id.find_and_modify({},
        {'$inc': {'next_id': 1}}, new=True, upsert=True)['next_id']


@app.route('/p/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def slash():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        data = request.form.get('data') or request.data
        if data:
            _id = surl.encode_url(next_id())
            mongo.db.paste.insert({'_id': _id, 'data': data})
            return redirect('/p/{0}'.format(_id))
        else:
            return abort(400)


@app.route('/p/<ObjectId:_id>.txt')
@app.route('/p/<_id>')
def get(_id):
    paste = mongo.db.paste.find_one_or_404({'_id': _id})
    return Response(paste['data'], mimetype='text/plain')

if __name__ == '__main__':
    app.run(port=5005)
