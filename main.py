from flask import Flask, render_template, request, redirect
import datetime as dt
import requests
import smtplib
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


EMAIL=''
PASSWORD =''
Auth = ''

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db.init_app(app)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = 'apple pie'

# Database Post Table
class Post(db.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key=True)
    title : Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    blog_image: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(String(250), nullable=False)


# WtfForms form for adding new post
class addPostForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    subtitle = StringField(validators=[DataRequired()])
    author = StringField(validators=[DataRequired()])
    blog_image = URLField(validators=[DataRequired()])
    body = StringField(validators=[DataRequired()])
    submit = SubmitField()


# route for homepage and fetching and displaying all posts
@app.route('/', methods=['GET'])
def get_home():
    year = dt.datetime.now().year
    all_posts = db.session.execute(db.select(Post)).scalars()
    return render_template('index.html', year=year, posts=all_posts)


# route for fetching a specific post by id
@app.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = db.session.execute(db.select(Post).where(Post.id == post_id)).scalar()
    return render_template('post.html', post=post)


# route for getting to the about page
@app.route('/about', methods=['GET'])
def get_about():
    return render_template('about.html')


# route for moving to add post form and add the new post to database
@app.route('/new-post', methods=['GET','POST'])
def add_post():
    form = addPostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            subtitle=form.subtitle.data,
            author=form.author.data,
            blog_image=form.blog_image.data,
            body=form.body.data
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect('/')
    return render_template('add.html', form=form)


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