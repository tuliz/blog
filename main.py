from flask import Flask, render_template
import datetime as dt
import requests

app = Flask(__name__)


@app.route('/')
def get_home():
    response = requests.get('https://api.npoint.io/c790b4d5cab58020d391')
    response.raise_for_status()
    posts = response.json()
    year = dt.datetime.now().year
    return render_template('index.html', year=year, posts=posts)


if __name__ == '__main__':
    app.run(debug=True)