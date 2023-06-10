from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SQLAlCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'your_secret_key'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


def scrap_biblus():
    url = "https://biblusi.ge/products?category=291&category_id=305&page=1"
    response = requests.get(url)
    content = response.text
    soup = BeautifulSoup(content, "html.parser")
    body = soup.find("body")
    nuxt = body.find("div", id='__nuxt')
    layout = nuxt.find("div", id='__layout')
    books = layout.find("div", {'class': "books w-100 w-md-90 mx-auto NUXT"})
    mx_auto = books.find("div", {'class': "w-90 w-md-100 mx-auto"})
    position = mx_auto.find("div", {'class': "b-overlay-wrap position-relative mt-1_875rem"})
    row = position.find("div", {'class': "row"})
    all_book = row.find_all("div", {'class': "mb-1_875rem col-sm-4 col-md-3 col-xl-2 col-6"})
    book_list = []
    for i in all_book:
        book_name = i.find("div",
                           {'class': "bg-white __product-card d-flex flex-column justify-content-between p-1rem"}).text
        book_list.append([book_name])
    headers = ['books with their prise']
    return book_list, headers


@app.route('/home')
def home():
    book_list, headers = scrap_biblus()
    return render_template('home.html', book_list=book_list, headers=headers)


@app.route("/user")
def user():
    if "username" in session:
        user = session["username"]
        return render_template('user.html', user=user)
    else:
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user1 = User(username=username, password=password)
        db.session.add(user1)
        db.session.commit(url_for('Login'))
    return render_template('registration.html')


@app.route('/register', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username

        user = User.query.filter_by(username=username).first()
        if user and user.username == username and user.pasword == password:
            flash('login saccessful :)', 'success')
            return redirect(url_for('user'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')


@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template('Logout.html')


if __name__ == '__main__':
    app.run(debug=True)