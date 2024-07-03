from flask import Flask, render_template, request
import datetime as dt
import requests
import smtplib
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


EMAIL=''
PASSWORD =''
Auth = ''

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db.init_app(app)

class Post(db.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    title : Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    blog_image: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(String(250), nullable=False)


# with app.app_context():
#     new_post = Post(
#         title="days with dogs",
#         subtitle="my 90 days with dogs",
#         author="yarden tulchinsky",
#         blog_image='https://www.walla.com',
#         body='this is a post about a long 90 days with dogs'
#     )
#     db.session.add(new_post)
#     db.session.commit()


@app.route('/', methods=['GET'])
def get_home():
    year = dt.datetime.now().year
    all_posts = db.session.execute(db.select(Post)).scalars()
    return render_template('index.html', year=year, posts=all_posts)


@app.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = db.session.execute(db.select(Post).where(Post.id == post_id)).scalar()
    return render_template('post.html', post=post)


@app.route('/about', methods=['GET'])
def get_about():
    return render_template('about.html')


@app.route('/contact', methods=["POST", "GET"])
def get_contact():
    method = request.method
    if method == 'GET':
        return render_template('contact.html', message='Contact Me')
    else:
        user_email = request.form['email']
        user_name = request.form['name']
        user_phone = request.form['tel']
        user_message = request.form['tel']

        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(Auth,PASSWORD)
            connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=f'email:{user_email}\nname:{user_name}\nphone:{user_phone}\nmessage:{user_message}')
        return render_template('contact.html', message='Successfully sent message')


if __name__ == '__main__':
    app.run(debug=True)