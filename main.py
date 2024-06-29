from flask import Flask, render_template
import datetime as dt
import requests
from post import Post

app = Flask(__name__)

response = requests.get('https://api.npoint.io/c790b4d5cab58020d391')
response.raise_for_status()
all_posts = response.json()

posts_list: list = []

for post in all_posts:
    new_post = Post(post['id'], post['title'], post['subtitle'], post['body'])
    posts_list.append(new_post)


@app.route('/')
def get_home():
    year = dt.datetime.now().year
    return render_template('index.html', year=year, posts=posts_list)


@app.route('/post/<int:post_id>')
def get_post(post_id):
    for post in posts_list:
        if post.id == post_id:
            return render_template('post.html', post=post)


@app.route('/about')
def get_about():
    return render_template('about.html')


@app.route('/contact')
def get_contact():
    return render_template('contact.html')


if __name__ == '__main__':
    app.run(debug=True)