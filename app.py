import get_data_from_website
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from werkzeug.exceptions import abort
from db_manager import DBManager
from get_data_from_website import add_all_urls_in_table, add_image,add_year,add_name, get_all_url_names

db_file="instance/aniworld.db"

table_names = ["anime_namen","serien_namen"]
websiten_urls = ["https://aniworld.to/animes/","https://s.to/serien/"]
webseiten_einzelneserie_url = ["https://aniworld.to/anime/","https://s.to/serie/"]

def get_db_connection():
    conn = sqlite3.connect('instance/aniworld.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.secret_key = 'dein-geheimer-schlussel'


@app.route('/')
def index():
    return render_template('base.html')

@app.route('/serien_names_sto')
def serien_names_sto() -> str:
    db = DBManager(db_file)
    all_anime_urls: tuple = db.get_all_serien_url_from_table(table_name=table_names[1])
    return render_template('serien_names_sto.html',posts=all_anime_urls)

@app.route('/serien_names_aniworld')
def serien_names_aniworld() -> str:
    db = DBManager(db_file)
    all_anime_urls: tuple = db.get_all_serien_url_from_table(table_name=table_names[0])
    return render_template('serien_names_aniworld.html',posts=all_anime_urls)

@app.route('/<string:such_url>')
def serie_name(such_url):
    db = DBManager(db_file)
    post = db.get_serie_information(such_url=such_url,table_name=table_names[0])
    db.close()
    return render_template('serie.html', post=post)

@app.route('/search-aniworld')
def search_aniworld():
    such_name = request.args.get('such_name', '').lower()
    db = DBManager(db_file)
    list_such_name = db.filter_nach_name(
        table_name=table_names[0],
        such_name=such_name
    )
    db.close()
    return render_template('_search_results.html', posts=list_such_name)

@app.route('/search-sto')
def search_sto():
    such_name = request.args.get('such_name', '').lower()
    db = DBManager(db_file)
    list_such_name = db.filter_nach_name(
        table_name=table_names[1],
        such_name=such_name
    )
    db.close()
    return render_template('_search_results.html', posts=list_such_name)

@app.route('/view_database_aniworld')
def view_database_aniworld():
    db = DBManager(db_file)
    liste_table = db.get_all_in_table(table_name=table_names[0])

    return render_template('view_db.html', daten=liste_table)

@app.route('/view_database_sto')
def view_database_sto():
    db = DBManager(db_file)
    liste_table = db.get_all_in_table(table_name=table_names[1])

    return render_template('view_db.html', daten=liste_table)

@app.route('/settings', methods=['GET', 'POST'])
def settings():    
    if request.method == 'POST':
        db = DBManager(db_file)        
        
        if 'create_ani_table' in request.form:
            try:
                result = db.create_table(table_names[0])
                flash(result, 'success')

            except Exception as e:
                flash(f'Fehler beim Erstellen: {str(e)}', 'danger')

        elif 'update_ani_urls_db' in request.form:
            try:
                flash("Start Urls Upadte", "success")
                result = add_all_urls_in_table(table_name=table_names[0],list=get_all_url_names(start_url=websiten_urls[0]))
                flash(result, "success")
            except Exception as e:
                flash(f'Fehler beim Erstellen: {str(e)}', 'danger')

        elif 'update_ani_year_db' in request.form:
            try:
                result = add_year(start_url=webseiten_einzelneserie_url[0],table_name=table_names[0])
                flash(result, "success")
            except Exception as e:
                flash(f'Fehler beim Erstellen: {str(e)}', 'danger')

        elif 'update_ani_name_db' in request.form:
            try:
                result = add_name(start_url=webseiten_einzelneserie_url[0],table_name=table_names[0])
                flash(result, "success")
            except Exception as e:
                flash(f'Fehler beim Erstellen: {str(e)}', 'danger')

        elif 'update_ani_img_db' in request.form:
            try:
                result = add_image(start_url=webseiten_einzelneserie_url[0],table_name=table_names[0])
                flash(result, "success")
            except Exception as e:
                flash(f'Fehler beim Erstellen: {str(e)}', 'danger')


        elif 'create_sto_table' in request.form:
            try:
                result = db.create_table(table_names[1])
                flash(result, 'success')

            except Exception as e:
                flash(f'Fehler beim Erstellen: {str(e)}', 'danger')
            
        elif "update_sto_urls_db" in request.form:    
            try:
                result = add_all_urls_in_table(table_name=table_names[1],list=get_all_url_names(start_url=websiten_urls[1]))
                flash(result, "success")
            except Exception as e:
                flash(f'Fehler beim Erstellen: {str(e)}', 'danger')

        elif 'update_sto_year_db' in request.form:
            try:
                result = add_year(start_url=webseiten_einzelneserie_url[1],table_name=table_names[1])
                flash(result, "success")
            except Exception as e:
                flash(f'Fehler beim Erstellen: {str(e)}', 'danger')

        elif 'update_ani_name_db' in request.form:
            try:
                result = add_name(start_url=webseiten_einzelneserie_url[1],table_name=table_names[1])
                flash(result, "success")
            except Exception as e:
                flash(f'Fehler beim Erstellen: {str(e)}', 'danger')

        elif 'update_ani_img_db' in request.form:
            try:
                result = add_image(start_url=webseiten_einzelneserie_url[1],table_name=table_names[1])
                flash(result, "success")
            except Exception as e:
                flash(f'Fehler beim Erstellen: {str(e)}', 'danger')
                

    return render_template('settings.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)