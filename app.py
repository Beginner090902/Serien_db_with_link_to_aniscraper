from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from werkzeug.exceptions import abort
from db_manager import DBManager

tabel_name_anime="anime_namen"
aniworld_db="instance/aniworld.db"


def get_db_connection():
    conn = sqlite3.connect('instance/aniworld.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)

@app.route('/')
def index() -> str:
    db = DBManager(aniworld_db)
    all_anime_urls: tuple = db.get_all_serien_url_from_table(table_name=tabel_name_anime)
    print(all_anime_urls)
    return render_template('index.html',posts=all_anime_urls)

@app.route('/<string:such_url>')
def serie_name(such_url):
    db = DBManager(aniworld_db)
    post = db.get_serie_information(such_url=such_url,table_name=tabel_name_anime)
    db.close()
    return render_template('serie.html', post=post)

@app.route('/search')
def search():
    such_name = request.args.get('such_name', '').lower()

    db = DBManager(aniworld_db)
    list_such_name = db.filter_nach_name(
        table_name=tabel_name_anime,
        such_name=such_name
    )
    db.close()

    return render_template('_search_results.html', posts=list_such_name)

@app.route('/data')
def data():
    return render_template('data.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

# ------------------------
# App-Start
# ------------------------
if __name__ == '__main__':
    app.run(debug=True)