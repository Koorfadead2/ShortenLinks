import sqlite3 as sq
from hashids import Hashids
from flask import Flask, render_template, request, flash, redirect, url_for


connect = sq.connect('database.db', check_same_thread=False)
cursor = connect.cursor()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'wqeqwrqrqwr'

hashids = Hashids(min_length=8, salt=app.config['SECRET_KEY'])

@app.route('/', methods=('GET', 'POST'))
def index():

    if request.method == 'POST':
        url = request.form['url']
        if not url:
            flash('The URL is required!')
            return redirect(url_for('index'))
        url_data = cursor.execute('''INSERT INTO urls (original_url) VALUES (?)''',
                                (url,))
        connect.commit()
        url_id = url_data.lastrowid
        hashid = hashids.encode(url_id)
        short_url = request.host_url + hashid

        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<id>')
def url_redirect(id):

    original_id = hashids.decode(id)
    if original_id:
        original_id = original_id[0]
        original_url = cursor.execute('SELECT original_url FROM urls'
                                ' WHERE id = (?)', (original_id,)
                                ).fetchone()
        return redirect(str(original_url)[2:-3])
    else:
        flash('Invalid URL')
        return redirect(url_for('index'))



if __name__=='__main__':
    app.run()